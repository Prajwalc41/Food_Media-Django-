from django.contrib import admin
from .models import Post, Like, Comment, StarRating, FoodiePoint


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('dish_name', 'restaurant', 'created_at', 'like_count', 'comment_count')
    list_filter = ('created_at',)
    search_fields = ('dish_name', 'restaurant__username', 'restaurant__full_name')
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    search_fields = ('text', 'author__username')


@admin.register(StarRating)
class StarRatingAdmin(admin.ModelAdmin):
    list_display = ('enthusiast', 'restaurant', 'score', 'updated_at')


@admin.register(FoodiePoint)
class FoodiePointAdmin(admin.ModelAdmin):
    list_display = ('giver', 'recipient', 'created_at')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('enthusiast', 'post')
