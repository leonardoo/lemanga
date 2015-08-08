
from django.shortcuts import render, redirect

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
