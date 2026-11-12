from datetime import date

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import models

from .forms import EditProfileForm
from .models import Turf, Booking, Review


# HOME PAGE
def home(request):
    turfs = Turf.objects.filter(is_available=True)

    return render(request, 'booking/home.html', {
        'turfs': turfs
    })


# TURF DETAILS PAGE
def turf_details(request, turf_id):
    turf = get_object_or_404(Turf, id=turf_id)

    return render(request, 'booking/turf_details.html', {
        'turf': turf
    })


# BOOK TURF PAGE
@login_required
def book_turf(request, turf_id):
    turf = get_object_or_404(Turf, id=turf_id)

    selected_date = request.GET.get('date', '')
    booked_slots = []

    if selected_date:
        booked_slots = list(
            Booking.objects.filter(
                turf=turf,
                booking_date=selected_date,
                status='Confirmed'
            ).values_list('time_slot', flat=True)
        )

    return render(request, 'booking/book_turf.html', {
        'turf': turf,
        'selected_date': selected_date,
        'booked_slots': booked_slots,
        'today': date.today().isoformat(),
    })


# CONFIRM BOOKING PAGE
@login_required
def confirm_booking(request, turf_id):
    turf = get_object_or_404(Turf, id=turf_id)

    selected_date = request.GET.get('date', '')
    selected_time = request.GET.get('time', '')
    error = ''

    if request.method == 'POST':
        selected_date = request.POST.get('date', '')
        selected_time = request.POST.get('time', '')

        if not selected_date or not selected_time:
            error = 'Please select a date and time.'

        else:
            try:
                booking_date = date.fromisoformat(selected_date)
            except ValueError:
                booking_date = None
                error = 'Please select a valid date.'

            if booking_date and booking_date < date.today():
                error = 'Past dates cannot be booked.'

            if not error:
                already_booked = Booking.objects.filter(
                    turf=turf,
                    booking_date=booking_date,
                    time_slot=selected_time,
                    status='Confirmed'
                ).exists()

                if already_booked:
                    error = 'This time slot is already booked.'

                else:
                    booking = Booking.objects.create(
                        user=request.user,
                        turf=turf,
                        booking_date=booking_date,
                        time_slot=selected_time
                    )

                    return render(
                        request,
                        'booking/booking_success.html',
                        {'booking': booking}
                    )

    return render(request, 'booking/confirm_booking.html', {
        'turf': turf,
        'selected_date': selected_date,
        'selected_time': selected_time,
        'error': error,
    })


# BOOKING SUCCESS PAGE
def booking_success(request):
    return render(request, 'booking/booking_success.html')


# MY BOOKINGS PAGE
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user
    ).select_related('turf').order_by('-created_at')

    return render(request, 'booking/my_bookings.html', {
        'bookings': bookings,
    })


# CANCEL BOOKING
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if request.method == 'POST' and booking.status == 'Confirmed':
        booking.status = 'Cancelled'
        booking.save(update_fields=['status'])

    return redirect('my_bookings')


# REGISTER PAGE
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'booking/register.html', {
        'form': form
    })


# EDIT PROFILE PAGE
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'booking/edit_profile.html', {
        'form': form
    })


# TURF REVIEWS AND RATINGS PAGE
def turf_reviews(request, turf_id):
    turf = get_object_or_404(Turf, id=turf_id)
    error = ''

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()

        if not rating or not comment:
            error = 'Please select a rating and write a review.'

        elif rating not in ['1', '2', '3', '4', '5']:
            error = 'Please select a valid rating.'

        else:
            already_reviewed = Review.objects.filter(
                user=request.user,
                turf=turf
            ).exists()

            if already_reviewed:
                error = 'You have already reviewed this turf.'

            else:
                has_booking = Booking.objects.filter(
                    user=request.user,
                    turf=turf,
                    status='Confirmed'
                ).exists()

                if not has_booking:
                    error = 'Please book this turf before submitting a review.'

                else:
                    Review.objects.create(
                        user=request.user,
                        turf=turf,
                        rating=int(rating),
                        comment=comment
                    )

                    return redirect('turf_reviews', turf_id=turf.id)

    reviews = Review.objects.filter(
        turf=turf
    ).select_related('user').order_by('-created_at')

    average_rating = reviews.aggregate(
        average=models.Avg('rating')
    )['average']

    return render(request, 'booking/turf_reviews.html', {
        'turf': turf,
        'reviews': reviews,
        'average_rating': average_rating,
        'error': error,
    })