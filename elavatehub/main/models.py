

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    # """
    # Profile model to store additional user details
    # """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    business_idea = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Post(models.Model):
    """
    Post model for user ideas or business concepts
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    content = models.TextField()
    funding_pledged = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.CharField(max_length=100, choices=[
        ('Technology', 'Technology'),
        ('Education', 'Education'),
        ('Health', 'Health'),
        ('Environment', 'Environment'),
        ('Business', 'Business'),
        ('Other', 'Other'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Order posts by creation date, newest first
