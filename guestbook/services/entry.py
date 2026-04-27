import logging

from django.db import transaction
from django.db.utils import IntegrityError

from guestbook.models import GuestUser, Entry


logger = logging.getLogger("guestbook")


def create_entry(name: str, subject: str, message: str) -> Entry:
    try:
        with transaction.atomic():
            user, _ = GuestUser.objects.get_or_create(name=name)

            entry = Entry.objects.create(
                user=user,
                subject=subject,
                message=message,
            )

            logger.info(
                "Entry created",
                extra={
                    "user": user.name,
                    "entry_id": entry.id,
                },
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