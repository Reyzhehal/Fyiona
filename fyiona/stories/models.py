from django.db import models
from django.conf import settings
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.db.models.fields.related import ManyToManyField


from fyiona.fields import ContentTypeRestrictedFileField

ALLOWED_TO_REPLY = (
    (
        "Everyone",
        "Everyone",
    ),
    (
        "People You Follow",
        "People You Follow",
    ),
    (
        "Off",
        "Off",
    ),
)


class Story(models.Model):
    author = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="post_comments",
        verbose_name=_("Author of a story"),
    )

    viewers = models.ManyToManyField(
        blank=True,
        default=[],
        to=CustomUser,
        related_name="viewers",
        verbose_name=_("People viewed a story"),
    )

    caption = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_("On screen text"),
    )

    # interactions = models.IntegerField(
    #     default=0,
    #     verbose_name=_("Actions people take when they engage with a story"),
    # )

    reaction = models.CharField(
        max_length=5,
        verbose_name=_("Reaction"),
        blank=True,
    )

    # replies = models.IntegerField(
    #     default=0,
    #     verbose_name=_("Messages have been sent as a reaction to a story"),
    # )

    # accounts_reached = models.IntegerField(
    #     default=0,
    #     verbose_name=_("Accounts taken from a story"),
    # )

    # impressions = models.IntegerField(
    #     default=0,
    #     verbose_name=_("People impressed by a story"),
    # )

    # follows = models.IntegerField(
    #     default=0,
    #     verbose_name=_("People started to follow after viewing"),
    # )

    # back = models.IntegerField(
    #     default=0,
    #     verbose_name=_("Tap back"),
    # )

    # forward = models.IntegerField(
    #     default=0,
    #     verbose_name=_("Tap forward"),
    # )

    # next_story = models.IntegerField(
    #     default=0,
    #     verbose_name=_("Saw next story"),
    # )

    # exited = models.IntegerField(
    #     default=0,
    #     verbose_name=_("Exited"),
    # )

    hidden_story_from = ManyToManyField(
        to=CustomUser,
        related_name="hidden_from",
        verbose_name=_("Hide a story from"),
        blank=True,
        default=[],
    )

    allow_message_replies = models.CharField(
        max_length=25,
        choices=ALLOWED_TO_REPLY,
        verbose_name=_("Who allowed to reply"),
        default=ALLOWED_TO_REPLY[0][0],
    )

    save_story_to_gallery = models.BooleanField(
        default=False,
        verbose_name=_("Save story to gallery"),
    )

    save_story_to_archive = models.BooleanField(
        default=True,
        verbose_name=_("Save story to archive"),
    )

    allow_to_share = models.BooleanField(
        default=True,
        verbose_name=_("Allow to share"),
    )

    allow_sharing_messages = models.BooleanField(
        default=False,
        verbose_name=_("Allow sharing messages"),
    )

    def __str__(self) -> str:
        return self.author.first_name

    class Meta:
        ordering = ["-id"]


class StoryFile(models.Model):
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name="attachments"
    )
    attachment = ContentTypeRestrictedFileField(
        upload_to="accounts/stories/",
        verbose_name=_("Story File"),
        content_types=[
            "image/jpeg",
            "image/png",
            "image/jpg",
            "video/mp4",
            "video/ogg",
        ],
        max_upload_size=settings.STORY_MAX_FILE_SIZE,
    )

    def __str__(self) -> str:
        return "Story ID: %s  Path: %s" % (self.story.id, self.content_file)
