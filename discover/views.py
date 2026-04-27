from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import FoodHistory
from accounts.models import CustomUser


@login_required
def discover(request):
    query = request.GET.get('q', '').strip()
    restaurants = []

    if query:
        restaurants = CustomUser.objects.filter(
            role='RESTAURANT',
            is_active=True
        ).filter(
            Q(full_name__icontains=query) |
            Q(restaurant_address__icontains=query)
        )

    articles = FoodHistory.objects.all()

    return render(request, 'discover/discover.html', {
        'query': query,
        'restaurants': restaurants,
        'articles': articles,
    })


@login_required
def food_history_detail(request, pk):
    article = get_object_or_404(FoodHistory, pk=pk)
    return render(request, 'discover/food_history_detail.html', {'article': article})
