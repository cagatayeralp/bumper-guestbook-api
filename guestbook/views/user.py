from rest_framework.response import Response
from rest_framework.views import APIView

from guestbook.serializers import UserStatsSerializer
from guestbook.services import get_user_stats

from drf_spectacular.utils import extend_schema


class UserStatsAPIView(APIView):
    serializer_class = UserStatsSerializer

    @extend_schema(responses=UserStatsSerializer(many=True))
    def get(self, request):
        users = get_user_stats()
        serializer = self.serializer_class(users, many=True)

        return Response({"users": serializer.data})
