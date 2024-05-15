from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .models import RolePlayingRoom
from .forms import RolePlayingRoomForm
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required


# staff member만 접근 가능하도록
@method_decorator(staff_member_required, name="dispatch")
class RolePlayingRoomCreateView(CreateView):
    model = RolePlayingRoom
    form_class = RolePlayingRoomForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        role_playing_room = form.save(commit=False)
        role_playing_room.user = self.request.user
        return super().form_valid(form)


@method_decorator(staff_member_required, name="dispatch")
class RolePlayingRoomUpdateView(UpdateView):
    model = RolePlayingRoom
    form_class = RolePlayingRoomForm

    # 본인이 생성한 채팅방만 조회 가능하도록
    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


@method_decorator(staff_member_required, name="dispatch")
class RolePlayingRoomListView(ListView):
    model = RolePlayingRoom

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


@method_decorator(staff_member_required, name="dispatch")
class RolePlayingRoomDetailView(DetailView):
    model = RolePlayingRoom

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs
