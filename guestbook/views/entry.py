from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from guestbook.models import Entry
from guestbook.pagination import GuestBookPagination
from guestbook.serializers import EntryCreateSerializer, EntryListSerializer
from guestbook.services import create_entry

from drf_spectacular.utils import extend_schema


class EntryCreateAPIView(APIView):
    serializer_class = EntryCreateSerializer

    @extend_schema(
        request=EntryCreateSerializer,
        responses={201: EntryListSerializer},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        entry = create_entry(**serializer.validated_data)

        return Response(
            EntryListSerializer(entry).data,
            status=status.HTTP_201_CREATED,
        )


class EntryListAPIView(ListAPIView):
    serializer_class = EntryListSerializer
    pagination_class = GuestBookPagination

    def get_queryset(self):
        return (
            Entry.objects
            .select_related("user")
            .order_by("-created_date")
        )
