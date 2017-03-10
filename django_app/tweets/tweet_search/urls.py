from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.search, name='index'),
	url(r'results', views.results, name='results'),
	url(r'populate', views.populate, name='populate'),
	url(r'about', views.about, name='about'),
	]
