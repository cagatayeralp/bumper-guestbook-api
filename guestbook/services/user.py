from django.db.models import CharField, Count, OuterRef, Subquery, Value
from django.db.models.functions import Concat

from guestbook.models import Entry, GuestUser


def get_user_stats():
    latest_entry = (
        Entry.objects
        .filter(user=OuterRef("pk"))
        .order_by("-created_date")
    )

    return (
        GuestUser.objects
        .annotate(
            total_messages=Count("entries"),
            last_entry=Subquery(
                latest_entry
                .annotate(
                    combined=Concat(
                        "subject",
                        Value(" | "),
                        "message",
                        output_field=CharField(),
                    )
                )
                .values("combined")[:1]
            ),
        )
        .filter(total_messages__gt=0)
        .order_by("name")
    )