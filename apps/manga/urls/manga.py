from django.conf.urls import include, url

from .. import views

MANGA = [
    url(r'^listado/$', views.MangaListView.as_view(), name="list-mangas"),
    url(r'^(?P<name>\w+)/$', views.MangaDetailView.as_view(),
        name="detail-manga"),
]
