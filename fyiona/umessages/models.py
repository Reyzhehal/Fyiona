from uuid import uuid4
from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _

from fyiona.fields import ContentTypeRestrictedFileField


class TrackableDateModel(models.Model):
    """
    This model automatically adds two fields in model that inhereted TrackableDateModel.
    These fields are responsible for tracking the updated and creation date.
    """

    updated_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Date Updated"),
    )
    created_at = models.DateTimeField(
        editable=False,
        default=timezone.now,
        verbose_name=_("Date Created"),
    )


class MessageSession(TrackableDateModel):
    """
    MessageSession is responsible for grouping all messages in one place.
    Every time a User wants to send a messages this message has to have a MessageSesion, in order be identified later.
    MessageSession either created or updated automatically each time a new message is created.
    There cannot be more than 2 participants in a one session.
    """

    session = models.UUIDField(
        default=uuid4,
        editable=False,
        primary_key=True,
        verbose_name=_("Session ID"),
    )

    participants = models.ManyToManyField(
        to=CustomUser,
        related_name="message_sessions",
        verbose_name=_("Participants of Chat")
    )

    def __str__(self) -> str:
        return "Session ID: %s" % self.session


class Message(TrackableDateModel):
    """
    Message object has two required fields: receiver and text|attachment.
    Message can be created without a text but attachments only.
    """

    REACTIONS = (
        (0, "Like"),
        (1, "Smile"),
        (2, "LOL"),
        (3, "Angry"),
    )
    message_session = models.ForeignKey(
        editable=False,
        to=MessageSession,
        on_delete=models.CASCADE,
        related_name="session_messages",
        verbose_name=_("Message Session"),
    )
    sender = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name=_("Message Creator"),
    )
    receiver = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="received_messages",
        verbose_name=_("Message Receiver"),
    )

    text = models.TextField(
        blank=True,
        verbose_name=_("Message Text"),
    )
    reaction = models.CharField(
        null=True,
        blank=True,
        choices=REACTIONS,
        max_length=10,
        verbose_name=_("Reaction to message"),
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name=_("Has been read"),
    )

    def __str__(self) -> str:
        return "From %s to %s at %s" % (self.sender, self.receiver, self.created_at)


class MessageFile(TrackableDateModel):
    """
    MessageFile object is an attachment to a message that sent from one user to another.
    MessageFile's size might be 25 MB maximum.
    """

    msg = models.OneToOneField(
        Message,
        on_delete=models.CASCADE,
        related_name="attachments",
    )
    attachment = ContentTypeRestrictedFileField(
        upload_to="messages/attachments/",
        verbose_name=_("Message File"),
        content_types=[
            "image/jpeg",
            "image/png",
            "image/jpg",
        ],
        max_upload_size=settings.MESSAGE_MAX_FILE_SIZE,
    )

    def __str__(self) -> str:
        return "Message ID: %s  Path: %s" % (self.msg.id, self.attachment)
