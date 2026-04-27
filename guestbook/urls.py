from django.urls import path

from guestbook.views import (
    EntryCreateAPIView,
    EntryListAPIView,
    UserStatsAPIView,
)

urlpatterns = [
    path("entries/create/", EntryCreateAPIView.as_view(), name="entry-create"),
    path("entries/", EntryListAPIView.as_view(), name="entry-list"),
    path("users/", UserStatsAPIView.as_view(), name="user-stats"),
]
