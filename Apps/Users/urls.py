from django.urls import path, include

from Apps.Users.views import UserProfileTemplateView, UserProfileView

app_name = 'Users'

urlpatterns = [
    path('<str:username>/', UserProfileView.as_view(), name='profile'),
    # path('api/', include('Apps.Users.API.urls', namespace='API')),
]
