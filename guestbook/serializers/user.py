from rest_framework import serializers


class UserStatsSerializer(serializers.Serializer):
    username = serializers.CharField(source="name")
    total_messages = serializers.IntegerField()
    last_entry = serializers.CharField()
