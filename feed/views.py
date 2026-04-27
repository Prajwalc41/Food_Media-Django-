from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import Post, Like, Comment, StarRating, FoodiePoint
from .forms import PostForm, CommentForm
from accounts.models import CustomUser


@login_required
def feed(request):
    mode = request.GET.get('mode', 'recent')
    thirty_days_ago = timezone.now() - timedelta(days=30)

    if mode == 'popular':
        posts_qs = Post.objects.filter(
            created_at__gte=thirty_days_ago
        ).annotate(
            num_likes=Count('likes')
        ).order_by('-num_likes', '-created_at')
    else:
        mode = 'recent'
        posts_qs = Post.objects.all().order_by('-created_at')

    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get liked posts for current user
    liked_post_ids = set()
    if request.user.is_enthusiast():
        liked_post_ids = set(
            Like.objects.filter(enthusiast=request.user).values_list('post_id', flat=True)
        )

    return render(request, 'feed/feed.html', {
        'page_obj': page_obj,
        'mode': mode,
        'liked_post_ids': liked_post_ids,
    })


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.select_related('author').all()
    comment_form = CommentForm()

    liked = False
    if request.user.is_enthusiast():
        liked = Like.objects.filter(post=post, enthusiast=request.user).exists()

    can_comment = (
        request.user.is_enthusiast() or
        (request.user.is_restaurant() and request.user == post.restaurant)
    )

    return render(request, 'feed/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'liked': liked,
        'can_comment': can_comment,
    })


@login_required
def create_post(request):
    if not request.user.is_restaurant():
        messages.error(request, 'Only restaurant accounts can upload posts.')
        return redirect('feed')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.restaurant = request.user
            post.save()
            messages.success(request, "Your dish has been served! 🍽️")
            return redirect('my_uploads')
    else:
        form = PostForm()

    return render(request, 'feed/create_post.html', {'form': form})


@login_required
def my_uploads(request):
    if not request.user.is_restaurant():
        messages.error(request, 'This page is for restaurant accounts only.')
        return redirect('feed')
    posts = request.user.posts.all()
    return render(request, 'feed/my_uploads.html', {'posts': posts})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        if request.user == post.restaurant or request.user.is_staff:
            post.delete()
            messages.success(request, 'Post deleted. 🗑️')
            if request.user.is_staff:
                return redirect('feed')
            return redirect('my_uploads')
        else:
            messages.error(request, 'You do not have permission to delete this post.')
            return redirect('post_detail', pk=pk)

    return redirect('post_detail', pk=pk)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    can_comment = (
        request.user.is_enthusiast() or
        (request.user.is_restaurant() and request.user == post.restaurant)
    )

    if not can_comment:
        messages.error(request, 'You cannot comment on this post.')
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')

    return redirect('post_detail', pk=pk)


@login_required
def delete_comment(request, pk, cid):
    post = get_object_or_404(Post, pk=pk)
    comment = get_object_or_404(Comment, pk=cid, post=post)

    if request.method == 'POST':
        can_delete = (
            request.user == comment.author or
            request.user == post.restaurant or
            request.user.is_staff
        )
        if can_delete:
            comment.delete()
            messages.success(request, 'Comment deleted.')
        else:
            messages.error(request, 'You cannot delete this comment.')

    return redirect('post_detail', pk=pk)


@login_required
def toggle_like(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    if not request.user.is_enthusiast():
        return JsonResponse({'error': 'Only enthusiasts can like posts'}, status=403)

    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, enthusiast=request.user)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.like_count})


@login_required
def rate_restaurant(request, username):
    if not request.user.is_enthusiast():
        messages.error(request, 'Only enthusiasts can rate restaurants.')
        return redirect('restaurant_profile', username=username)

    restaurant = get_object_or_404(CustomUser, username=username, role='RESTAURANT')

    if request.user == restaurant:
        messages.error(request, 'You cannot rate yourself.')
        return redirect('restaurant_profile', username=username)

    if request.method == 'POST':
        score = request.POST.get('score')
        try:
            score = int(score)
            if score < 1 or score > 5:
                raise ValueError
        except (TypeError, ValueError):
            messages.error(request, 'Invalid rating score.')
            return redirect('restaurant_profile', username=username)

        rating, created = StarRating.objects.update_or_create(
            restaurant=restaurant,
            enthusiast=request.user,
            defaults={'score': score}
        )
        if created:
            messages.success(request, 'Your rating has been saved! ⭐')
        else:
            messages.success(request, 'Your rating has been updated! ⭐')

    return redirect('restaurant_profile', username=username)


@login_required
def give_foodie_point(request, username):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    if not request.user.is_enthusiast():
        return JsonResponse({'success': False, 'error': 'Only enthusiasts can give Foodie Points'}, status=403)

    recipient = get_object_or_404(CustomUser, username=username, role='ENTHUSIAST')

    if request.user == recipient:
        return JsonResponse({'success': False, 'error': "You can't give yourself a Foodie Point! 😄"})

    point, created = FoodiePoint.objects.get_or_create(
        giver=request.user,
        recipient=recipient
    )

    if not created:
        return JsonResponse({'success': False, 'error': 'Already given'})

    return JsonResponse({'success': True, 'new_count': recipient.foodie_points_count})
