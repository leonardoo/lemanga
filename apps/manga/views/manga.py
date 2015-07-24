from django.views import generic

from .. import models

from .mixin import DynamicTemplateMixin


class MangaListView(DynamicTemplateMixin, generic.ListView):
    model = models.Manga
    paginate_by = 25
    template_name_suffix = 'list'


class MangaDetailView(DynamicTemplateMixin, generic.DetailView):
    model = models.Manga
    template_name_suffix = 'detail'
