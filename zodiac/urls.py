from django.urls import path

from . import views

app_name = "zodiac"

urlpatterns = [
    path("", views.home, name="home"),
    path("compatibilidade/", views.compatibilidade, name="compatibilidade"),
    path("<str:username>/", views.resultado, name="resultado"),
]
