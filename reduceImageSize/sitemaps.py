# sitemaps.py in your app directory

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from .models import Blog, CustomPage


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Blog.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated


class CustomPageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return CustomPage.objects.all()

    def lastmod(self, obj):
        return timezone.now()
