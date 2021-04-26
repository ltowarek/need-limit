from django.contrib import admin
from feeds.models import Feed, FeedEntry

admin.site.register((Feed, FeedEntry))
