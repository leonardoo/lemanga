from django.shortcuts import render, redirect
from django.views import generic

import extra_views

from . import mixin
from .. import forms
from .. import models



class ChapterPictureInline(extra_views.InlineFormSet):
    model = models.ChapterPicture
    form_class = forms.ChapterForm
    can_delete = False
    extra = 1


class CreateChapterView(mixin.DynamicTemplateMixin,
                        extra_views.NamedFormsetsMixin,
                        extra_views.CreateWithInlinesView):

    model = models.Chapter
    form_class = forms.ChapterForm
    context_object_name = "form"
    inlines = [ChapterPictureInline]
    inlines_names = ['pictures']
    template_name_suffix = "create"
    template_name = "manga/chapter/create.html"

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        manga = models.Manga.objects.get(slug=self.kwargs.get("name"))
        instance = models.Chapter(upload_by=self.request.user, manga=manga)
        kwargs = super(CreateChapterView, self).get_form_kwargs()
        kwargs.update({'instance': instance})
        return kwargs


class ChapterDetailView(mixin.DynamicTemplateMixin,
                        mixin.MultipleSlugsMixin,
                        generic.DetailView):
    model = models.ChapterPicture
    slug_url_kwargs = ["name", "chapter", "user", "number"]
    slug_fields = ["chapter__manga__slug", "chapter__number",
                   "chapter__upload_by_id", "number"]
    template_name_suffix = 'detail'
