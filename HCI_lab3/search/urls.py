from django.conf.urls import url
from . import views

app_name='search'

urlpatterns=[
	url(r'^$',views.index,name='index'),
	url(r'^result/$',views.search_result,name='search_result'),
	url(r'^upload/$',views.upload,name='upload'),
]