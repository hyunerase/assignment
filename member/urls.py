from django.urls import path, include
from .views import *

app_name = 'member'

urlpatterns = [
    path('signup/', include('dj_rest_auth.registration.urls')),
    path('', include('dj_rest_auth.urls')),
    path('info/', get_info),
    path('post/', get_list),
]