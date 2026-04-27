from rest_framework import serializers

from guestbook.models import Entry


class EntryCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField(max_length=2000)

    def validate_name(self, value: str) -> str:
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Name cannot be empty.")

        return value

    def validate_subject(self, value: str) -> str:
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Subject cannot be empty.")

        return value

    def validate_message(self, value: str) -> str:
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Message cannot be empty.")

        return value


class EntryListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.name")

    class Meta:
        model = Entry
        fields = ["user", "subject", "message"]
