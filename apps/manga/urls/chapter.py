from django.conf.urls import include, url

from .. import views

CHAPTER = [
    url(r'^d/(?P<name>(\w|-)+)/create/$', views.manga_create_chapter,
        name="create-chapter"),
]