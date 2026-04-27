from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('ENTHUSIAST', 'Food Enthusiast'),
        ('RESTAURANT', 'Restaurant'),
    ]

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True
    )
    bio = models.TextField(max_length=500, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # Restaurant-only fields
    restaurant_address = models.CharField(max_length=300, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return f'{self.username} ({self.role or "admin"})'

    def is_enthusiast(self):
        return self.role == 'ENTHUSIAST'

    def is_restaurant(self):
        return self.role == 'RESTAURANT'

    @property
    def average_star_rating(self):
        ratings = self.star_ratings_received.all()
        if not ratings.exists():
            return 0.0
        total = sum(r.score for r in ratings)
        return round(total / ratings.count(), 1)

    @property
    def star_rating_count(self):
        return self.star_ratings_received.count()

    @property
    def foodie_points_count(self):
        return self.points_received.count()
