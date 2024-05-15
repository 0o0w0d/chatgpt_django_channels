from django.urls import path
from . import views

urlpatterns = [
    path("", views.RolePlayingRoomListView.as_view(), name="role_playing_room_list"),
    path(
        "create/",
        views.RolePlayingRoomCreateView.as_view(),
        name="role_playing_room_create",
    ),
    path(
        "<int:pk>/update/",
        views.RolePlayingRoomUpdateView.as_view(),
        name="role_playing_room_update",
    ),
    path(
        "<int:pk>/",
        views.RolePlayingRoomDetailView.as_view(),
        name="role_playing_room_detail",
    ),
    path(
        "<int:pk>/delete/",
        views.RolePlayingRoomDeleteView.as_view(),
        name="role_playing_room_delete",
    ),
]
