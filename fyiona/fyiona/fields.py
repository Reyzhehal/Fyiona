from django.forms import forms
from django.db.models import FileField
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import filesizeformat

from django.conf import settings

"""
Same as FileField, but you can specify:
    * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
    * max_upload_size - a number indicating the maximum file size allowed for upload.
        2.5MB - 2621440
        5MB   - 5242880
        10MB  - 10485760
        20MB  - 20971520
        50MB  - 5242880
        100MB - 104857600
        250MB - 214958080
        500MB - 429916160
        750MB - 644874240
"""


class ContentTypeRestrictedFileField(FileField):
    """
        ContentType Restricted FileField a custom class to control file type entity
        This class works in 2 ways:
        1. Validator - validates the size and type of attached file
        2. ModelField - keeps the information about a file in the database
    """
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", [])
        self.max_upload_size = kwargs.pop(
            "max_upload_size", settings.POST_MAX_FILE_SIZE
        )

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        """
            .clean() method is responsible for validation by FILESIZE and FILE TYPE
            In the result, methods returns itself but with specific modifications inside
        """
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(
                        _("Please keep filesize under %s. Current filesize %s")
                        % (
                            filesizeformat(self.max_upload_size),
                            filesizeformat(file._size),
                        )
                    )
            else:
                raise forms.ValidationError(_("Filetype not supported."))
        except AttributeError:
            pass

        return data
