from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tweet_search/$', views.search, name='search'),
    url(r'^tweet_search/results/', views.results, name='results'),
    url(r'populate', views.populate, name='populate'),
]
