# encoding:utf-8

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
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
