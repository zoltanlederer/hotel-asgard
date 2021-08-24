from django.contrib import admin
from .models import Rooms, Media, Reservations


class RoomsAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'adult_price', 'child_price')


class ReservationsAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'check_in', 'check_out', 'reserved_room', 'reservation_date', 'payed')


# Register your models here.
admin.site.register(Rooms, RoomsAdmin)
admin.site.register(Media)
admin.site.register(Reservations, ReservationsAdmin)