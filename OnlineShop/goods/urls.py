from django.conf.urls import url

from goods.views import good_detail_view, catalog, add_comment

urlpatterns = [
    url(r'^(?P<pk>\d+)$', good_detail_view, name="good"),
    url(r'^catalog$', catalog, name="catalog"),
    url(r'^comment$', add_comment, name="add_comment"),
]
