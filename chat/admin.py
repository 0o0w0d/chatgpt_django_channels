from django.contrib import admin
from .models import RolePlayingRoom
from .forms import RolePlayingRoomForm

# Register your models here.


@admin.register(RolePlayingRoom)
class RolePlayingRoomAdmin(admin.ModelAdmin):
    form = RolePlayingRoomForm

    def save_model(self, request, obj, form, change):
        # 신규 생성 시에만 request.user를 할당
        if change is False and form.is_valid():
            obj.user = request.user

        super().save_model(request, obj, form, change)
