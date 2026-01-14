"""
Models for the AI Blog Generator application
"""
from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    """Model to store blog posts generated from YouTube videos"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    category = models.CharField(max_length=50, default='Technology')
    
    # YouTube video information
    youtube_url = models.URLField()
    youtube_title = models.CharField(max_length=200, blank=True)
    youtube_channel = models.CharField(max_length=100, blank=True)
    youtube_duration = models.CharField(max_length=20, blank=True)
    
    # User and timestamps
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        return self.title
