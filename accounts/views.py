from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from .models import CustomUser
from .forms import (
    EnthusiastRegistrationForm,
    RestaurantRegistrationForm,
    EnthusiastProfileEditForm,
    RestaurantProfileEditForm,
)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')

    ent_form = EnthusiastRegistrationForm()
    res_form = RestaurantRegistrationForm()
    active_tab = 'enthusiast'

    if request.method == 'POST':
        role = request.POST.get('role', 'enthusiast')
        active_tab = role

        if role == 'enthusiast':
            ent_form = EnthusiastRegistrationForm(request.POST, request.FILES)
            if ent_form.is_valid():
                user = ent_form.save(commit=False)
                user.set_password(ent_form.cleaned_data['password'])
                user.role = 'ENTHUSIAST'
                user.is_active = True
                if not ent_form.cleaned_data.get('profile_picture'):
                    user.profile_picture = None
                user.save()
                login(request, user)
                messages.success(request, f'Welcome to Food Media, {user.full_name}! 🎉')
                return redirect('feed')
        else:
            res_form = RestaurantRegistrationForm(request.POST, request.FILES)
            if res_form.is_valid():
                user = res_form.save(commit=False)
                user.set_password(res_form.cleaned_data['password'])
                user.role = 'RESTAURANT'
                user.is_active = True
                if not res_form.cleaned_data.get('profile_picture'):
                    user.profile_picture = None
                user.save()
                login(request, user)
                messages.success(request, f'Welcome to Food Media, {user.full_name}! 🍽️')
                return redirect('feed')

    return render(request, 'accounts/register.html', {
        'ent_form': ent_form,
        'res_form': res_form,
        'active_tab': active_tab,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(60 * 60 * 24 * 14)  # 2 weeks
            next_url = request.GET.get('next', 'feed')
            return redirect(next_url)
        else:
            error = 'Invalid username or password.'

    return render(request, 'accounts/login.html', {'error': error})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def own_profile_redirect(request):
    user = request.user
    if user.is_restaurant():
        return redirect('restaurant_profile', username=user.username)
    return redirect('enthusiast_profile', username=user.username)


@login_required
def enthusiast_profile(request, username):
    profile_user = get_object_or_404(CustomUser, username=username, role='ENTHUSIAST')
    already_given = False
    if request.user.is_enthusiast():
        from feed.models import FoodiePoint
        already_given = FoodiePoint.objects.filter(
            giver=request.user, recipient=profile_user
        ).exists()

    context = {
        'profile_user': profile_user,
        'already_given': already_given,
        'is_own_profile': request.user == profile_user,
    }
    return render(request, 'accounts/enthusiast_profile.html', context)


@login_required
def restaurant_profile(request, username):
    restaurant = get_object_or_404(CustomUser, username=username, role='RESTAURANT')
    posts = restaurant.posts.all()

    user_rating = None
    if request.user.is_enthusiast():
        from feed.models import StarRating
        try:
            user_rating = StarRating.objects.get(restaurant=restaurant, enthusiast=request.user)
        except StarRating.DoesNotExist:
            pass

    context = {
        'restaurant': restaurant,
        'posts': posts,
        'user_rating': user_rating,
        'is_own_profile': request.user == restaurant,
        'star_range': range(1, 6),
    }
    return render(request, 'accounts/restaurant_profile.html', context)


@login_required
def edit_profile(request):
    user = request.user

    if user.is_enthusiast():
        FormClass = EnthusiastProfileEditForm
    elif user.is_restaurant():
        FormClass = RestaurantProfileEditForm
    else:
        return redirect('feed')

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=user)
        if form.is_valid():
            instance = form.save(commit=False)
            if 'profile_picture' in request.FILES:
                instance.profile_picture = request.FILES['profile_picture']
            instance.save()
            messages.success(request, 'Profile updated successfully! ✅')
            return redirect('own_profile')
    else:
        form = FormClass(instance=user)

    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully! 🔐')
            return redirect('own_profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def delete_account(request):
    user = request.user

    if request.method == 'POST':
        step = request.POST.get('step')
        if step == '2':
            confirm_text = request.POST.get('confirm_text', '')
            if confirm_text == 'DELETE':
                logout(request)
                user.delete()
                messages.info(request, 'Your account has been permanently deleted.')
                return redirect('login')
            else:
                messages.error(request, 'You must type DELETE exactly to confirm.')

    context = {
        'user': user,
        'posts_count': user.posts.count() if user.is_restaurant() else 0,
        'foodie_points': user.foodie_points_count if user.is_enthusiast() else 0,
        'star_rating': user.average_star_rating if user.is_restaurant() else 0,
    }
    return render(request, 'accounts/delete_account.html', context)
