from uuid import UUID, uuid4
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework.fields import CharField, UUIDField

from rest_framework.serializers import (
    ModelSerializer,
)

from users.models import CustomUser

from .models import Message, MessageFile, MessageSession

#########################################################
###################### Message ##########################
#########################################################


class MessageFileSerializer(ModelSerializer):
    class Meta:
        model = MessageFile
        fields = (
            "id",
            "attachment",
        )


class MessageSerializer(ModelSerializer):
    """
    Serializer for create Message.
    """

    def validate(self, attrs):
        user = self.context.get("request").user.id
        session = MessageSession.objects.filter(
            session=attrs.get("message_session")
        ).first()
        if session:
            if (
                CustomUser.objects.get(pk=user) not in session.participants.all()
                and len(session.participants.all()) >= 2
            ):
                raise ValidationError("You are not a member of this session.")
        return super().validate(attrs)

    def create(self, validated_data) -> Message:
        """Creates a new Message, however, adds an author's id who made a request before to save a Message"""

        user_id = self.context.get("request").user.id
        validated_data.update({"sender_id": user_id})
        mss = validated_data.pop("message_session", uuid4())
        session = MessageSession.objects.filter(session=mss).first()
        if session:
            message_session = session
        else:
            message_session = MessageSession(session=mss)
            message_session.save()

        user = CustomUser.objects.get(pk=user_id)

        if user not in message_session.participants.all():
            message_session.participants.add(user)

        message = Message(**validated_data)
        message.message_session = message_session
        message.save()

        attachments = self.context.get("request").FILES.getlist("attachments")

        for attachment in attachments:
            sf = MessageFile(msg=message, attachment=attachment)
            sf.save()

        return message

    attachments = MessageFileSerializer(read_only=True, required=False)
    message_session = UUIDField(required=False)

    class Meta:
        model = Message
        fields = "__all__"

        read_only_fields = (
            "id",
            "sender",
            "created_at",
        )


class MessageSessionSerializer(ModelSerializer):
    session_messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = MessageSession
        fields = (
            "session",
            "participants",
            "session_messages",
        )
