from django import forms
from django.forms.models import BaseModelFormSet

from .. import models


class ChapterForm(forms.ModelForm):
    class Meta:
        model = models.Chapter
        fields = ["number"]


class ChapterPrictureForm(forms.ModelForm):
    class Meta:
        model = models.ChapterPicture
        fields = ["number", "picture"]


ChapterPrictureFormSet = modelformset_factory(models.ChapterPricture,
                                              form=ChapterPrictureForm)
