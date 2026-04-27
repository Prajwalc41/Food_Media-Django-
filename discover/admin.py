from django.contrib import admin
from .models import FoodHistory


@admin.register(FoodHistory)
class FoodHistoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)
