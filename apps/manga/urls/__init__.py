from django.conf.urls import include, url

from .manga import MANGA

urlpatterns = [
    url(r'^', include(MANGA)),
]
