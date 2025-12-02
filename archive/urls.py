from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('api/videos/', views.get_videos, name='get_videos'),
    path('api/playlists/', views.get_playlists, name='get_playlists'),
    path('api/playlists/create/', views.create_playlist, name='create_playlist'),
    path('api/playlists/add/', views.add_to_playlist, name='add_to_playlist'),
    path('api/playlists/remove/', views.remove_from_playlist, name='remove_from_playlist'),
    path('api/playlists/delete/', views.delete_playlist, name='delete_playlist'),
    path('video/<path:filename>/', views.serve_video, name='serve_video'),
    path('thumbnail/<path:filename>/', views.serve_thumbnail, name='serve_thumbnail'),
]
