from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseBadRequest
from .models import Room, Reservation, RoomImage
from .forms import SearchForm, ReservationForm

def _parse_dates(request):
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

def home(request):
    # Si viene el form con GET, redirige a catálogo con los parámetros
    if {"check_in", "check_out", "guests"} <= set(request.GET.keys()):
        return redirect(f"{reverse('catalog')}?check_in={request.GET['check_in']}&check_out={request.GET['check_out']}&guests={request.GET['guests']}")
    return render(request, "hotel/home.html")

def catalog(request):
    check_in, check_out, guests = _parse_dates(request)
    error = None
    rooms = []

    if not (check_in and check_out and check_in < check_out):
        error = "Ingresa un rango de fechas válido."
    else:
        # filtra por capacidad y disponibilidad
        base_qs = Room.objects.filter(is_active=True, capacity__gte=guests).order_by("price_per_night")
        rooms = [r for r in base_qs if r.is_available(check_in, check_out)]

    ctx = dict(rooms=rooms, check_in=check_in, check_out=check_out, guests=guests, error=error)
    return render(request, "hotel/catalog.html", ctx)

def room_detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id, is_active=True)
    check_in, check_out, guests = _parse_dates(request)
    if not (check_in and check_out and check_in < check_out):
        return HttpResponseBadRequest("Parámetros de fecha inválidos.")
    nights = (check_out - check_in).days
    total = nights * room.price_per_night
    images = RoomImage.objects.filter(room=room)
    form = ReservationForm()
    ctx = dict(room=room, images=images, check_in=check_in, check_out=check_out,
               guests=guests, nights=nights, total=total, form=form)
    return render(request, "hotel/detail.html", ctx)

def reserve(request, room_id):
    room = get_object_or_404(Room, pk=room_id, is_active=True)
    check_in, check_out, guests = _parse_dates(request)
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido.")
    form = ReservationForm(request.POST)
    if not (check_in and check_out and check_in < check_out) or not form.is_valid():
        return HttpResponseBadRequest("Datos inválidos.")

    # Verifica disponibilidad justo antes de crear
    if not room.is_available(check_in, check_out):
        return HttpResponseBadRequest("La habitación ya no está disponible en esas fechas.")

    nights = (check_out - check_in).days
    total = nights * room.price_per_night
    res = Reservation.objects.create(
        room=room, check_in=check_in, check_out=check_out, guests=guests,
        holder_name=form.cleaned_data["holder_name"],
        holder_email=form.cleaned_data["holder_email"],
        total_amount=total,
    )
    return redirect("confirmation", res_id=res.id)

def confirmation(request, res_id):
    res = get_object_or_404(Reservation, pk=res_id)
    return render(request, "hotel/confirm.html", {"res": res})
