from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.PlayGraphView.as_view(), name='index'),
    url(r'^plays/(?P<bgg_id>[^/]+)$', views.PlayGraphDataView.as_view(), name='play_data'),
]