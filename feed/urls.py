from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.feed, name='feed'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:pk>/comment/<int:cid>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('upload/', views.create_post, name='create_post'),
    path('my-uploads/', views.my_uploads, name='my_uploads'),
    path('restaurant/<str:username>/rate/', views.rate_restaurant, name='rate_restaurant'),
    path('profile/<str:username>/give-point/', views.give_foodie_point, name='give_foodie_point'),
]
