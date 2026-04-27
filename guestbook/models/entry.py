from django.db import models
from .base import BaseModel


class Entry(BaseModel):
    user = models.ForeignKey(
        "guestbook.GuestUser",
        related_name="entries",
        on_delete=models.CASCADE,
    )
    subject = models.CharField(max_length=255)
    message = models.TextField()

    class Meta:
        db_table = "guestbook_entry"
        ordering = ["-created_date"]
        indexes = [
            models.Index(fields=["-created_date"]),
            models.Index(fields=["user", "-created_date"]),
        ]

    def __str__(self):
        return f"{self.subject} - {self.user.name}"