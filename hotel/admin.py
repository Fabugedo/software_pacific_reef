from django.contrib import admin
from django.utils.html import format_html
from .models import Room, RoomImage, Reservation

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1
    fields = ("image", "image_url", "preview")
    readonly_fields = ("preview",)

    def preview(self, obj):
        url = obj.src() if obj.pk else ""
        return format_html('<img src="{}" style="height:60px;border-radius:6px"/>', url) if url else "—"

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "capacity", "price_per_night", "is_active")
    list_filter = ("category", "is_active")
    inlines = [RoomImageInline]

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("room", "check_in", "check_out", "guests", "total_amount")
    list_filter = ("room", "check_in")
