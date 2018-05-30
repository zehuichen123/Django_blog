from django.conf.urls import url
from . import views

app_name='search'

urlpatterns=[
	url(r'^$',views.index,name='index'),
	url(r'^result/$',views.search_result,name='search_result'),
	url(r'^upload/$',views.upload,name='upload'),
	url(r'^add_to_favorite/(?P<image_address>[0-9a-zA-Z\_]+)/$'\
		,views.add_to_favorite,name='add_to_favorite'),
	url(r'^show_favorite/$',views.show_favorite,name='show_favorite'),
]