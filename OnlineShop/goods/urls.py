from django.conf.urls import url

from goods.views import GoodDetailView, catalog

urlpatterns = [
    url(r'^(?P<pk>\d+)$', GoodDetailView.as_view(), name="good"),
    url(r'^catalog$', catalog, name="catalog"),
]
