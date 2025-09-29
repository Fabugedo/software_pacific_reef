from django.contrib import admin
from .models import Room, RoomImage, Reservation

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "capacity", "price_per_night", "is_active")
    list_filter = ("category", "is_active")
    inlines = [RoomImageInline]

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("room", "check_in", "check_out", "guests", "total_amount")
    list_filter = ("room", "check_in")
from django.contrib import admin

# Register your models here.
