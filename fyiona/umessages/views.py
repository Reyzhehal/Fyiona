from uuid import UUID
from typing import Optional
from django.http.request import HttpRequest, QueryDict
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from rest_framework.authentication import (
    BaseAuthentication,
    BasicAuthentication,
    SessionAuthentication,
)

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_403_FORBIDDEN,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from .models import Message, MessageSession
from .serializers import MessageSerializer, MessageSessionSerializer
from users.middlewares import JWTAuthentication
from django.shortcuts import get_object_or_404


class MessageViewSet(ViewSet):
    """
    Example viewset demonstrating the standard
    actions that will be handled by a router class.
    """

    serializer_class = MessageSerializer
    authentication_classes = (BasicAuthentication,)

    def create(self, request: HttpRequest):
        if (
            request.FILES
            and request.FILES.get("attachments")
            or request.data.get("text")
        ):

            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                data={
                    "success": True,
                    "result": "Message has been created successfully!",
                },
                status=HTTP_201_CREATED,
            )
        return Response(
            data={
                "success": False,
                "result": "text or attachements has not been provided!",
            },
            status=HTTP_406_NOT_ACCEPTABLE,
        )

    def destroy(self, request: HttpRequest, pk=None):
        message = get_object_or_404(Message, pk=pk)

        if message.sender == request.user:
            message.delete()

            return Response(
                data={
                    "success": True,
                    "result": "Message successfully deleted!",
                },
                status=HTTP_200_OK,
            )
        return Response(
            data={
                "success": False,
                "result": "Access denied!",
            },
            status=HTTP_403_FORBIDDEN,
        )

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class MessageSessionViewSet(ViewSet):
    """
    Example viewset demonstrating the standard
    actions that will be handled by a router class.
    """

    serializer_class = MessageSessionSerializer
    authentication_classes = (
        BasicAuthentication,
        JWTAuthentication,
    )

    def list(self, request: HttpRequest):
        requester = request.user
        message_session = MessageSession.objects.filter(participants__in=[requester])

        serializer = self.serializer_class(message_session, many=True)

        serializer.is_valid(raise_exception=True)

        return Response(
            data={
                "success": True,
                "result": serializer.data,
            },
            status=HTTP_200_OK,
        )

    def destroy(self, request: HttpRequest, pk=None):
        message_session = get_object_or_404(MessageSession, session=pk)

        if request.user in message_session.participants.all():
            message_session.delete()

            return Response(
                data={
                    "success": True,
                    "result": "Session has been successfully deleted!",
                },
                status=HTTP_200_OK,
            )
        return Response(
            data={
                "success": False,
                "result": "Access denied!",
            },
            status=HTTP_403_FORBIDDEN,
        )

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "list":
            permission_classes = (IsAuthenticated,)
        elif self.action == "destroy":
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
