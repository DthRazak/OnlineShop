from django.conf.urls import url

from profiles.views import signup, login, logout

urlpatterns = [
    url(r'^signup$', signup, name="signup"),
    url(r'^login$', login, name="login"),
    url(r'^logout$', logout, name="logout"),
]
