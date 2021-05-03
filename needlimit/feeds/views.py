from typing import Any

from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from feeds.forms import FeedRefreshForm
from feeds.models import Feed, FeedEntry
from feeds.services import crawl_feed


class FeedListView(ListView):
    def get_queryset(self) -> QuerySet:
        return Feed.objects.all().order_by("title", "pk")


class FeedDetailView(DetailView):
    model = Feed


class FeedCreateView(CreateView):
    model = Feed
    fields = ["xml_link"]
    success_url = reverse_lazy("feeds:feed_list")

    def form_valid(self, form: ModelForm) -> HttpResponseRedirect:
        output = super().form_valid(form)
        crawl_feed(self.object)
        return output


class FeedUpdateView(UpdateView):
    model = Feed
    fields = ["xml_link"]
    success_url = reverse_lazy("feeds:feed_list")


class FeedDeleteView(DeleteView):
    model = Feed
    success_url = reverse_lazy("feeds:feed_list")


class FeedRefreshView(SingleObjectMixin, FormView):
    model = Feed
    template_name = "feeds/feed_refresh.html"
    form_class = FeedRefreshForm
    success_url = reverse_lazy("feeds:feed_list")

    def get(
        self, request: HttpRequest, *args: str, **kwargs: Any
    ) -> HttpResponseRedirect:
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(
        self, request: HttpRequest, *args: str, **kwargs: Any
    ) -> HttpResponseRedirect:
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form: FeedRefreshForm) -> HttpResponseRedirect:
        feed = self.get_object()
        crawl_feed(feed)
        return super().form_valid(form)


class FeedEntryListView(ListView):
    template_name = "feeds/feed_entry_list.html"

    def get_queryset(self) -> QuerySet:
        return FeedEntry.objects.filter(feed=self.kwargs["feed_pk"]).order_by(
            "published", "pk"
        )


class FeedEntryDetailView(DetailView):
    model = FeedEntry
    template_name = "feeds/feed_entry_detail.html"
