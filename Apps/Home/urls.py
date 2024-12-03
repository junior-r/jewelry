from django.urls import path

from Apps.Home.views import HomeView

app_name = 'Home'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
]
