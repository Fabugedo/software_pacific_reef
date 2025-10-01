from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Room, Reservation, RoomImage
from .forms import SearchForm, ReservationForm, CheckoutForm, PaymentForm


# ------------------------------
# Helpers
# ------------------------------

def _parse_dates(request):
    """
    Lee check_in, check_out y guests desde request.GET (formato YYYY-MM-DD).
    Retorna (check_in, check_out, guests) con defaults seguros.
    """
    ci = request.GET.get("check_in")
    co = request.GET.get("check_out")
    guests = request.GET.get("guests") or "1"
    try:
        check_in = datetime.strptime(ci, "%Y-%m-%d").date() if ci else None
        check_out = datetime.strptime(co, "%Y-%m-%d").date() if co else None
        guests = int(guests)
    except Exception:
        return None, None, 1
    return check_in, check_out, guests


# ------------------------------
# Público
# ------------------------------

def home(request):
    """Hero + buscador. Si vienen los 3 parámetros, redirige al catálogo."""
    if {"check_in", "check_out", "guests"} <= set(request.GET.keys()):
        return redirect(
            f"{reverse('catalog')}?check_in={request.GET['check_in']}"
            f"&check_out={request.GET['check_out']}"
            f"&guests={request.GET['guests']}"
        )
    return render(request, "hotel/home.html")


def catalog(request):
    """Lista de habitaciones disponibles para el rango/huéspedes."""
    check_in, check_out, guests = _parse_dates(request)
    error = None
    rooms = []

    if not (check_in and check_out and check_in < check_out):
        error = "Ingresa un rango de fechas válido."
    else:
        base_qs = Room.objects.filter(
            is_active=True, capacity__gte=guests
        ).order_by("price_per_night")
        rooms = [r for r in base_qs if r.is_available(check_in, check_out)]

    ctx = dict(
        rooms=rooms,
        check_in=check_in,
        check_out=check_out,
        guests=guests,
        error=error,
    )
    return render(request, "hotel/catalog.html", ctx)


def room_detail(request, room_id):
    """Detalle de una habitación + card con resumen y CTA."""
    room = get_object_or_404(Room, pk=room_id, is_active=True)
    check_in, check_out, guests = _parse_dates(request)
    if not (check_in and check_out and check_in < check_out):
        return HttpResponseBadRequest("Parámetros de fecha inválidos.")

    nights = (check_out - check_in).days
    total = nights * room.price_per_night
    images = RoomImage.objects.filter(room=room)

    ctx = dict(
        room=room,
        images=images,
        check_in=check_in,
        check_out=check_out,
        guests=guests,
        nights=nights,
        total=total,
        form=ReservationForm(),   # si mantienes un mini-form
    )
    return render(request, "hotel/detail.html", ctx)


def reserve(request, room_id):
    """
    (Opcional si usas 'checkout' como único flujo).
    Crea la reserva desde un form simple del detalle.
    """
    room = get_object_or_404(Room, pk=room_id, is_active=True)
    check_in, check_out, guests = _parse_dates(request)

    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido.")

    form = ReservationForm(request.POST)
    if not (check_in and check_out and check_in < check_out) or not form.is_valid():
        return HttpResponseBadRequest("Datos inválidos.")

    # double check de disponibilidad
    if not room.is_available(check_in, check_out):
        return HttpResponseBadRequest("La habitación ya no está disponible en esas fechas.")

    nights = (check_out - check_in).days
    total = nights * room.price_per_night

    res = Reservation.objects.create(
        room=room,
        check_in=check_in,
        check_out=check_out,
        guests=guests,
        holder_name=form.cleaned_data["holder_name"],
        holder_email=form.cleaned_data["holder_email"],
        total_amount=total,                # <- nombre consistente
        # payment_status por default = 'pending'
    )
    return redirect("confirmation", res_id=res.id)


def confirmation(request, res_id):
    """Pantalla de confirmación (estado). Muestra CTA a pago si está pending."""
    res = get_object_or_404(Reservation, pk=res_id)
    return render(request, "hotel/confirm.html", {"res": res})


def checkout(request, room_id):
    """Página con formulario de datos del titular + validaciones + create."""
    room = get_object_or_404(Room, pk=room_id, is_active=True)

    ci, co, guests = _parse_dates(request)
    initial = {}
    if ci:
        initial["check_in"] = ci
    if co:
        initial["check_out"] = co
    if guests:
        initial["guests"] = guests

    error = None

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            ci = form.cleaned_data["check_in"]
            co = form.cleaned_data["check_out"]
            guests = form.cleaned_data["guests"]

            if ci >= co:
                error = "Las fechas no son válidas."
            elif guests > room.capacity:
                error = "La habitación no soporta esa cantidad de huéspedes."
            elif not room.is_available(ci, co):
                error = "La habitación no está disponible en esas fechas."
            else:
                nights = (co - ci).days
                total = nights * room.price_per_night
                res = Reservation.objects.create(
                    room=room,
                    check_in=ci,
                    check_out=co,
                    guests=guests,
                    holder_name=form.cleaned_data["holder_name"],
                    holder_email=form.cleaned_data["holder_email"],
                    total_amount=total,   # <- consistente
                    # payment_status default 'pending'
                )
                return redirect("confirmation", res_id=res.id)
        else:
            error = "Revisa los campos del formulario."
    else:
        form = CheckoutForm(initial=initial)

    # Resumen lateral
    nights = (co - ci).days if (ci and co and ci < co) else 0
    total = nights * room.price_per_night if nights else 0
    images = RoomImage.objects.filter(room=room)

    ctx = dict(
        room=room,
        images=images,
        form=form,
        error=error,
        check_in=ci,
        check_out=co,
        guests=guests or 1,
        nights=nights,
        total=total,
    )
    return render(request, "hotel/checkout.html", ctx)


def payment(request, res_id):
    """Simulación de pago. Si es válido, marca como 'paid' y redirige a confirmación."""
    res = get_object_or_404(Reservation, pk=res_id)
    nights = (res.check_out - res.check_in).days
    total = res.total_amount

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Demo: marcamos como pagado
            res.payment_status = "paid"
            res.save()
            return redirect("confirmation", res_id=res.id)
    else:
        form = PaymentForm(initial={"method": "card"})

    return render(
        request,
        "hotel/payment.html",
        {"res": res, "nights": nights, "total": total, "form": form},
    )


# ------------------------------
# Staff (Panel)
# ------------------------------

def is_staff_user(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff_user)
def staff_dashboard(request):
    """
    Panel liviano para staff: últimas reservas.
    Asegúrate de que el template use {{ r.total_amount }} si así se llama en el modelo.
    """
    reservas = (
        Reservation.objects.select_related("room")
        .order_by("-created_at")[:50]
    )
    return render(request, "hotel/staff_dashboard.html", {"reservas": reservas})
