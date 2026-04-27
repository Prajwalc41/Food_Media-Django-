from django.db import models
from django.conf import settings


class FoodHistory(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='food_history/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Food History Article'
        verbose_name_plural = 'Food History Articles'

    def __str__(self):
        return self.title

    def content_snippet(self):
        return self.content[:150]
