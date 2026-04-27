from django.db import models
from .base import BaseModel


class GuestUser(BaseModel):
    name = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
    )

    class Meta:
        db_table = "guestbook_user"
        ordering = ["name"]

    def __str__(self):
        return self.name