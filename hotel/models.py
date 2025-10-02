from django.db import models
from django.utils import timezone
from decimal import Decimal

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
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="rooms/", blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Imagen de {self.room.name}"

    def src(self):

        if self.image:
            return self.image.url
        return self.image_url or ""



class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    holder_name = models.CharField(max_length=120)
    holder_email = models.EmailField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=0)
    created_at = models.DateTimeField(default=timezone.now)
    PAYMENT_STATUS = [
        ("pending", "Pendiente"),
        ("paid", "Pagado"),
        ("cancelled", "Cancelada"),
    ]
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS, default="pending"
    )

    def __str__(self):
        return f"Reserva {self.room.name} {self.check_in}→{self.check_out}"

    @property
    def nights(self):
        return max((self.check_out - self.check_in).days, 0)

    @property
    def deposit_30(self):

        return (Decimal('0.30') * self.total_amount).quantize(Decimal('1'))