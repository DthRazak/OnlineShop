from django.conf.urls import url

from cart.views import checkout, remove, remove_all, add, buy


urlpatterns = [
    url(r'^$', checkout, name="checkout"),
    url(r'^remove$', remove, name="remove"),
    url(r'^remove_all$', remove_all, name="remove_all"),
    url(r'^add$', add, name="add"),
    url(r'^buy$', buy, name="buy"),
]
