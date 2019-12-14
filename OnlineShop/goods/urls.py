from django.conf.urls import url

from goods.views import GoodDetailView

urlpatterns = [
    url(r'^(?P<pk>\d+)$', GoodDetailView.as_view(), name="good"),
]