from django.http import QueryDict
from django.http.request import HttpRequest

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_403_FORBIDDEN,
)
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from .models import Story
from users.models import CustomUser
from .serializers import StorySerializer
from users.middlewares import JWTAuthentication
from django.shortcuts import get_object_or_404


class StoryViewSet(ViewSet):
    """
    Example viewset demonstrating the standard
    actions that will be handled by a router class.
    """

    serializer_class = StorySerializer
    authentication_classes = (JWTAuthentication,)

    def create(self, request: HttpRequest):
        if request.FILES and request.FILES.get("attachments"):
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data={
                    "success": True,
                    "result": "Story has been created successfully!",
                },
                status=HTTP_201_CREATED,
            )
        return Response(
            data={
                "success": False,
                "result": "attachments field was not provided!",
            },
            status=HTTP_406_NOT_ACCEPTABLE,
        )

    def retrieve(self, request: HttpRequest, pk=None):
        user = get_object_or_404(CustomUser, pk=pk)
        stories = Story.objects.filter(author=user)
        serializer = self.serializer_class(stories, many=True)
        return Response(
            data={
                "success": True,
                "result": serializer.data,
            },
            status=HTTP_200_OK,
        )

    def destroy(self, request: HttpRequest, pk=None):
        story = get_object_or_404(Story, pk=pk)

        if story.author.id == request.user.id:
            story.delete()
            return Response(
                data={
                    "success": True,
                    "result": "Story successfully deleted!",
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
        elif self.action == "retrieve":
            permission_classes = [IsAuthenticated]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
