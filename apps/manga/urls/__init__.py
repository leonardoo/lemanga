from django.conf.urls import include, url

from .manga import MANGA
from .chapter import CHAPTER

urlpatterns = [
    url(r'^', include(MANGA)),
    url(r'^', include(CHAPTER)),
]
