import logging

from django.db import transaction
from django.db.utils import IntegrityError

from guestbook.models import GuestUser, Entry


logger = logging.getLogger("guestbook")


def create_entry(name: str, subject: str, message: str) -> Entry:
    """
    Creates a guestbook entry and ensures the user exists.
    Wrapped in a transaction to prevent race conditions.
    """
    try:
        with transaction.atomic():
            user, _ = GuestUser.objects.get_or_create(name=name)

            entry = Entry.objects.create(
                user=user,
                subject=subject,
                message=message,
            )

            logger.info(
                "Entry created user=%s entry_id=%s",
                user.name,
                entry.id,
            )

            return entry

    except IntegrityError:
        # rare race condition fallback
        user = GuestUser.objects.get(name=name)

        entry = Entry.objects.create(
            user=user,
            subject=subject,
            message=message,
        )

        logger.warning(
            "Race condition handled during user creation",
            extra={"user": user.name},
        )

        return entry
