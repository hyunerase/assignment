from django.urls import path
from .views import *

app_name = 'board'

urlpatterns = [
    path('', post_list),
    path('<int:pk>/', post_detail),
    path('<int:post_id>/comment/', comments_list),
    path('<int:post_id>/comment/<int:comment_id>/', comment_delete),
]