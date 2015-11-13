# encoding:utf-8

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator


class LoginMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginMixin, self).dispatch(*args, **kwargs)


class DynamicTemplateMixin(object):

    template_generate = "{0}/{1}/{2}.html"

    def get_template_names(self):
        if self.template_name:
            return super(DynamicTemplateMixin, self).get_template_names()

        if hasattr(self, 'model'):
            opts = self.model._meta
            template = self.template_generate.format(opts.app_label,
                                                     opts.model_name,
                                                     self.template_name_suffix)
            return [template]
        else:
            raise ImproperlyConfigured("")
        return names


class MultipleSlugsMixin(object):

    def get_object(self, queryset=None):
        """
        this mixin try to get multilples a object from multiples slugs
        and a pk in for return a object in the URLconf.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        # Next, try looking up by primary key.
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        # Next, try looking up the slugs.
        if slug:
            queryset = queryset.filter(**self.get_slug_fields())
        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    @property
    def slug_url_kwarg(self):
        if type(self.slug_url_kwargs) != list:
            raise AttributeError("slug_url_kwargs in view %s must be a list"
                                 % self.__class__.__name__)
        if len(self.slug_url_kwargs) > 0:
            return self.slug_url_kwargs[0]
        else:
            raise AttributeError("slug_url_kwargs in view %s must have least"
                                 "a element"
                                 % self.__class__.__name__)

    def get_slug_fields(self):
        fields = enumerate(self.slug_fields)
        filters = {}
        for index, field in fields:
            data = self.kwargs.get(self.slug_url_kwargs[index], None)
            filters.update({field: data})
        return filters
