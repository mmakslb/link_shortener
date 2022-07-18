from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from .views import main_view, redirect_url_view, registration_view, login_view, links_view

appname = "url_cutter"

urlpatterns = [
    path("", main_view, name="main"),
    path('<str:shortened_part>', redirect_url_view, name='redirect'),
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('main')), name='logout'),
    path('links/', links_view, name='links'),
]
