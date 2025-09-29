from django.db import models
from django.utils import timezone

class Room(models.Model):
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=80, blank=True)
    capacity = models.PositiveIntegerField(default=2)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=0)  # CLP
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (cap {self.capacity})"

    def is_available(self, check_in, check_out):
        """Disponible si NO hay reservas traslapadas en el rango dado."""
        overlap = self.reservation_set.filter(
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exists()
        return not overlap


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return f"Imagen de {self.room.name}"


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    holder_name = models.CharField(max_length=120)
    holder_email = models.EmailField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reserva {self.room.name} {self.check_in}→{self.check_out}"
