from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from datetime import datetime
from .models import Rooms, Reservations
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

import stripe
import json


stripe.api_key = settings.STRIPE_PRIVATE_KEY


# index page
def index(request):
    return render(request, "asgard/index.html")


# contact page
def contact(request):
    return render(request, "asgard/contact-page.html")


# about page
def about(request):
    return render(request, "asgard/about-us.html")


# Page for all rooms
def rooms(request):
    rooms = Rooms.objects.all()
    return render(request, "asgard/rooms.html", { 'rooms': rooms })


# Page for an individual room
def room(request, id, name):
    room = Rooms.objects.get(id=id)
    return render(request, "asgard/room.html", { 'room': room})


# Check available rooms at the index page
def available(request):
    if request.method == 'POST':
        checkin = request.POST['checkin']
        checkout = request.POST['checkout']
        adults = request.POST['adults']
        children = request.POST['children']
        totalPerson = int(adults) + int(children)

        # Add to sessions
        if "checkin" in request.session:
            del request.session["checkin"]
            request.session["checkin"] = request.POST['checkin']
        else:
            request.session["checkin"] = request.POST['checkin']

        if "checkout" in request.session:
            del request.session["checkout"]
            request.session["checkout"] = request.POST['checkout']
        else:
            request.session["checkout"] = request.POST['checkout']

        if "adults" in request.session:
            del request.session["adults"]
            request.session["adults"] = request.POST['adults']
        else:
            request.session["adults"] = request.POST['adults']

        if "children" in request.session:
            del request.session["children"]
            request.session["children"] = request.POST['children']
        else:
            request.session["children"] = request.POST['children']
            

        # Convert to datetime.date type
        checkin_date = datetime.strptime(checkin, "%Y-%m-%d").date()
        checkout_date = datetime.strptime(checkout, "%Y-%m-%d").date()

        # Check if the room is already reserved
        reservations = Reservations.objects.all()

        # Create excludes set list (Using set() to prevent duplications)
        excludes = set()
        # For loop for each reserved room
        for rooms in reservations:
            # Searching for the date range between the check-in and check-out dates which come through the form
            reserved = Reservations.objects.filter(Q(check_in__range=(checkin_date, checkout_date)) | Q(check_out__range=(checkin_date, checkout_date)))

            # If there is any reserved room
            if reserved.exists():
                # Loop through the reserved rooms
                for room in reserved:
                    # Append the reserved room-id to the excludes set list
                    excludes.add(room.reserved_room_id)
                    # With the exclude method, returned a new QuerySet with the available rooms (__in iterate the excludes set list)
                    available_rooms = Rooms.objects.exclude(id__in=excludes).filter(max_people__gte=totalPerson)

            else:
                available_rooms = Rooms.objects.all().filter(max_people__gte=totalPerson)
                return render(request, "asgard/rooms.html", {'rooms': available_rooms})

    return render(request, "asgard/rooms.html", {'rooms': available_rooms})


# Save the pre-reservation form's input values into session at the room page
def reservation(request, id, name):
    room = Rooms.objects.get(id=id)

    if request.method == 'POST':
        # Add to sessions
        if "checkin" in request.session:
            del request.session["checkin"]
            request.session["checkin"] = request.POST['checkin']
        else:
            request.session["checkin"] = request.POST['checkin']

        if "checkout" in request.session:
            del request.session["checkout"]
            request.session["checkout"] = request.POST['checkout']
        else:
            request.session["checkout"] = request.POST['checkout']

        if "adults" in request.session:
            del request.session["adults"]
            request.session["adults"] = request.POST['adults']
        else:
            request.session["adults"] = request.POST['adults']

        if "children" in request.session:
            del request.session["children"]
            request.session["children"] = request.POST['children']
        else:
            request.session["children"] = request.POST['children']

    return render(request, "asgard/reservation.html", { 'room': room })


# For JS to fetch the prices and make calculations
def reservatoindata(request, id):
    reservations = Reservations.objects.filter(reserved_room_id=id)
    return JsonResponse([reservation.reservation_api() for reservation in reservations], safe=False)


# For JS to fetch the prices and make calculations
def roomdata(request, id):
    room = Rooms.objects.get(id=id)
    return JsonResponse(room.room_api())


# Submit the reservation, and add to the database either paid or unpayed
@csrf_exempt
def reservation_submit(request, id, status):
    room = Rooms.objects.get(id=id)
    adults = request.session["adults"]
    children = request.session["children"]
    checkin = datetime.strptime(request.session["checkin"], '%Y-%m-%d').date()
    checkout = datetime.strptime(request.session["checkout"], '%Y-%m-%d').date()
    adult_price = room.adult_price
    child_price = room.child_price
    discount = 0

    differenceInTime = checkout - checkin
    days = differenceInTime.days

    subtotal = ((float(adult_price) * float(adults)) + (float(child_price) * float(children))) * float(days)
    if days >= 7:
        discount = subtotal * 0.15
    total = subtotal - discount
    vat = total * 0.08
    # Float with 2 decimals
    grandtotal = format(total + vat, '.2f')

    # Check if the room is already reserved
    reservations = Reservations.objects.all()

    # For loop for each reserved room
    for rooms in reservations:
        # Searching for the date range between the check-in and check-out dates which come through the form
        reserved = Reservations.objects.filter(reserved_room_id=id).filter(check_in__range=(checkin, checkout)) | Reservations.objects.filter(reserved_room_id=id).filter(check_out__range=(checkin, checkout))

    if reserved.exists():
        return render(request, "asgard/confirmation.html", { 'message': 'Error' })
    else:
        if request.method == 'POST':
            if status == 'unpayed':
                reservation = Reservations()
                reservation.reserved_room_id = id
                reservation.first_name = request.POST["first-name"]
                reservation.last_name = request.POST["last-name"]
                reservation.email = request.POST["email"]
                reservation.phone = request.POST["phone"]
                reservation.address = request.POST["address"]
                reservation.address_2 = request.POST["address2"]
                reservation.city = request.POST["city"]
                reservation.country = request.POST["country"]
                reservation.zipcode = request.POST["zipcode"]
                reservation.price = subtotal
                reservation.discount = discount
                reservation.total = total
                reservation.vat = vat
                reservation.grand_total = grandtotal
                reservation.adult = adults
                reservation.child = children
                reservation.check_in = checkin
                reservation.check_out = checkout
                reservation.payed = False
                reservation.save()           

                return render(request, "asgard/confirmation.html", { 'message': 'Success' })

            # After successfull card payment JS fetch post request at the comfirmation page
            if status == 'payed':
                data = json.loads(request.body)
                reservation = Reservations()
                reservation.reserved_room_id = id
                reservation.first_name = data.get('firstName', '')
                reservation.last_name = data.get('lastName', '')
                reservation.email = data.get('email', '')
                reservation.phone = data.get('phone', '')
                reservation.address = data.get('address', '')
                reservation.address_2 = data.get('address2', '')
                reservation.city = data.get('city', '')
                reservation.country = data.get('country', '')
                reservation.zipcode = data.get('zip', '')
                reservation.price = subtotal
                reservation.discount = discount
                reservation.total = total
                reservation.vat = vat
                reservation.grand_total = grandtotal
                reservation.adult = adults
                reservation.child = children
                reservation.check_in = checkin
                reservation.check_out = checkout
                reservation.payed = True
                reservation.save()  

        else:
            return render(request, "asgard/confirmation.html", { 'message': 'SuccesPayment' })
 
    return render(request, "asgard/confirmation.html", { 'message': 'Error' })


# Stripe card payment
def checkout(request, id):
    room = Rooms.objects.get(id=id)
    adults = request.session["adults"]
    children = request.session["children"]
    checkin = datetime.strptime(request.session["checkin"], '%Y-%m-%d').date()
    checkout = datetime.strptime(request.session["checkout"], '%Y-%m-%d').date()
    adult_price = room.adult_price
    child_price = room.child_price
    discount = 0

    differenceInTime = checkout - checkin
    days = differenceInTime.days

    subtotal = ((float(adult_price) * float(adults)) + (float(child_price) * float(children))) * float(days)
    if days >= 7:
        discount = subtotal * 0.15
    total = subtotal - discount
    vat = total * 0.08
    # Float with 2 decimals
    grandtotal = format(total + vat, '.2f')

    # Convert Grand Total for Stripe card payment
    grandtotalstr = str(grandtotal).replace('.', '')
    grandtotalint = int(grandtotalstr)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                'name': 'Reservation',
                'images': ['https://zoltanlederer.com/asgard-hotel-logo.png'],
                },
                'unit_amount': grandtotalint,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('reservation_submit', args=[id, 'payed'])) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('confirmation', args=['Error'])) + '?session_id={CHECKOUT_SESSION_ID}',
    )

    return JsonResponse({
        'session_id' : session.id,
        'stripe_public_key' : settings.STRIPE_PUBLIC_KEY
    })


# Confirmation of the reservation
def confirmation(request, status):
    message = status
    return render(request, 'asgard/confirmation.html', {'message': message})