from django.views import generic

from .. import models
from .. import forms

from .mixin import DynamicTemplateMixin


class MangaListView(DynamicTemplateMixin, generic.ListView):
    model = models.Manga
    paginate_by = 25
    template_name_suffix = 'list'
    context_object_name = "list"


class MangaDetailView(DynamicTemplateMixin, generic.DetailView):
    model = models.Manga
    template_name_suffix = 'detail'
    slug_url_kwarg = "name"
    slug_field = 'slug'


class MangaCreateView(DynamicTemplateMixin, generic.CreateView):
    model = models.Manga
    template_name_suffix = 'create'
    form_class = forms.MangaForm
