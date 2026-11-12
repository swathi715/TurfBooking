from django.db import models
from django.contrib.auth.models import User


class Turf(models.Model):
    SPORT_CHOICES = [
        ('Cricket', 'Cricket'),
        ('Football', 'Football'),
        ('Badminton', 'Badminton'),
    ]

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    sport_type = models.CharField(
        max_length=20,
        choices=SPORT_CHOICES
    )
    price_per_hour = models.PositiveIntegerField()
    image = models.ImageField(upload_to='turf_images/',blank=True,null=True)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    turf = models.ForeignKey(
        Turf,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    booking_date = models.DateField()
    time_slot = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        default='Confirmed'
    )

    def __str__(self):
        return f"{self.turf.name} - {self.booking_date} - {self.time_slot}"


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    turf = models.ForeignKey(
        Turf,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveIntegerField(
        choices=RATING_CHOICES
    )

    comment = models.TextField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.turf.name}"