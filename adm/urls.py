from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:turf_id>/', views.book_turf, name='book_turf'),
    path('confirm/<int:turf_id>/', views.confirm_booking, name='confirm_booking'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path(
    'cancel-booking/<int:booking_id>/',
    views.cancel_booking,
    name='cancel_booking'
),
path(
    'login/',
    auth_views.LoginView.as_view(
        template_name='booking/login.html'
    ),
    name='login'
),

# path(
#     'logout/',
#     auth_views.LogoutView.as_view(),
#     name='logout'
# ),
path('register/', views.register, name='register'),
path(
    'logout/',
    auth_views.LogoutView.as_view(next_page='home'),
    name='logout'
),
path('turf/<int:turf_id>/', views.turf_details, name='turf_details'),
path('edit-profile/', views.edit_profile, name='edit_profile'),
path(
    'turf/<int:turf_id>/reviews/',
    views.turf_reviews,
    name='turf_reviews'
),
]