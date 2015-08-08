from django import forms
from django.forms import models as formsets

from .. import models


class ChapterForm(forms.ModelForm):
    class Meta:
        model = models.Chapter
        fields = ["number"]


class ChapterPrictureForm(forms.ModelForm):
    class Meta:
        model = models.ChapterPicture
        fields = ["number", "picture"]


class _ChapterPrictureFormSetBase(formsets.BaseInlineFormSet):
    pass


ChapterPrictureFormSet = formsets.inlineformset_factory(models.Chapter,
                                                        models.ChapterPicture,
                                                        form=ChapterPrictureForm,
                                                        extra=2)
