from django.shortcuts import render, redirect
from django.views import generic

from . import mixin
from .. import forms
from .. import models


def manga_create_chapter(request, **kwargs):
    Form = forms.ChapterForm
    FormSet = forms.ChapterPrictureFormSet
    manga = models.Manga.objects.get(slug=kwargs.get("name"))
    instance = models.Chapter(upload_by=request.user, manga=manga)
    form = Form(request.POST or None,
                instance=instance)
    formset = FormSet(request.POST or None, request.FILES or None,
                      instance=instance)
    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect(manga.get_absolute_url())
    return render(request, 'manga/chapter/create.html',
                  {'form': form, 'formset': formset})


class ChapterDetailView(mixin.DynamicTemplateMixin,
                        mixin.MultipleSlugsMixin,
                        generic.DetailView):
    model = models.ChapterPicture
    slug_url_kwargs = ["name", "chapter", "user", "number"]
    slug_fields = ["chapter__manga__slug", "chapter__number",
                   "chapter__upload_by_id", "number"]
    template_name_suffix = 'detail'
