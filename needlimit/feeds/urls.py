from django.urls import include, path
from feeds import views

feed_entry_patterns = [
    path("", views.FeedEntryListView.as_view(), name="feed_entry_list"),
    path("<int:pk>", views.FeedEntryDetailView.as_view(), name="feed_entry_detail"),
]


feed_patterns = (
    [
        path("", views.FeedListView.as_view(), name="feed_list"),
        path("create/", views.FeedCreateView.as_view(), name="feed_create"),
        path("<int:pk>", views.FeedDetailView.as_view(), name="feed_detail"),
        path("<int:pk>/update", views.FeedUpdateView.as_view(), name="feed_update"),
        path("<int:pk>/delete", views.FeedDeleteView.as_view(), name="feed_delete"),
        path("<int:pk>/refresh", views.FeedRefreshView.as_view(), name="feed_refresh"),
        path("<int:feed_pk>/entries/", include(feed_entry_patterns)),
    ],
    "feeds",
)

urlpatterns = [
    path("", include(feed_patterns)),
]
