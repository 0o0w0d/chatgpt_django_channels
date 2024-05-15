from django.urls import path
from . import views

urlpatterns = [
    path(
        "room-create/",
        views.RolePlayingRoomCreateView.as_view(),
        name="role_playing_room_create",
    ),
    path(
        "<int:pk>/room-update/",
        views.RolePlayingRoomUpdateView.as_view(),
        name="role_playing_room_update",
    ),
]
