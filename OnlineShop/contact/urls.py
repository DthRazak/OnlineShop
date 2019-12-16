from django.conf.urls import url

from contact.views import email_view, success_view

urlpatterns = [
    url(r'^$', email_view, name="email"),
    url(r'^success$', success_view, name="success"),
]
