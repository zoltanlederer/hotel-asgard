from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact-page", views.contact, name="contact"),
    path("about-us", views.about, name="about"),
    path("rooms", views.rooms, name="rooms"),
    path("room/<int:id>/<str:name>", views.room, name="room"),
    path("available", views.available, name="available"),
    path("reservation/<int:id>/<str:name>", views.reservation, name="reservation"),
    path("reservation_submit/<int:id>/<str:status>", views.reservation_submit, name="reservation_submit"),
    path('checkout/<int:id>', views.checkout, name='checkout'),
    path('confirmation/<str:status>', views.confirmation, name='confirmation'),
    # API/AJAX
    path("reservatoindata/<int:id>", views.reservatoindata, name="reservatoindata"),
    path("roomdata/<int:id>", views.roomdata, name="roomdata"),
]
