from typing import Optional
from django.utils.translation import ugettext_lazy as _
from rest_framework.relations import (
    StringRelatedField,
)
from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    ValidationError,
)

from users.serializers import CustomUserDetailSerializer
from .models import Story, StoryFile

#########################################################
######################## Story ##########################
#########################################################


class StoryFileSerializer(ModelSerializer):
    class Meta:
        model = StoryFile
        fields = "__all__"


class StorySerializer(ModelSerializer):
    """
    Serializer for create Story.
    """

    def create(self, validated_data) -> Story:
        """Creates a new Story, however, adds an author's id who made a request before to save a Story"""
        viewers = []
        hidden_story_from = validated_data.pop("hidden_story_from", [])

        user_id = self.context.get("request").user.id
        validated_data.update({"author_id": user_id})
        story = Story(**validated_data)
        story.save()

        story.viewers.set(viewers)
        story.hidden_story_from.set(hidden_story_from)

        attachments = self.context.get("request").FILES.getlist("attachments")

        for attachment in attachments:
            sf = StoryFile(story=story, attachment=attachment)
            sf.save()

        return story

    viewers = CustomUserDetailSerializer(many=True, required=False)
    attachments = StoryFileSerializer(many=True, read_only=True)

    class Meta:
        model = Story
        fields = "__all__"

        read_only_fields = (
            "id",
            "created_at",
            "author",
            "story_files",
        )
