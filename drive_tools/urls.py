from django.urls import path
from aSync import views

urlpatterns = [
    path('authorize_drive/', views.authorize_drive, name='drive_authorize'),
    path('oauth2callback_drive/', views.oauth2callback_drive, name='drive_callback'),
    path('files/', views.list_files, name='drive_files'),
]
