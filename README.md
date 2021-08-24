# Capstone Project
### CS50’s Web Programming with Python and JavaScript


CS50 Lesson for - [Final Project - Capstone](https://cs50.harvard.edu/web/2020/projects/final/capstone)


## Description:
Hotel Asgard is a fully functional website, where people can search for the hotel’s available rooms and get information for each of the room specifications. The website is also able to make reservations and store them in the database. There is an option to only book the selected room without payment, or prepay the reservation with card payment.
All the room information, facilities, and media such as their image files are stored in the database and easily can modify or update in the Django administration panel. Moreover, within the administration panel simply can add or remove existing rooms and the website dynamically adds/removes them.

## Distinctiveness and Complexity: 
This web application includes Stripe API, which is an online payment processing platform for businesses. The website at the backend creates the calculation of the payment which will be sent securely to the Stripe API and platform to do a card transaction. After the successful payment, the web application adds to SQLite database the reservation and mark it as paid. In case of unsuccessful payment, the user receives an error message and will not appear the reservation in the database.

## Project files and directories:
**Within _hotel_ folder:**
- hotel/settings.py  – At the end of the settings.py file was added Stripe API’s Public and Private Key
- hotel/urls.py – Created a path to the “asgard” app (Which was given after the hotel’s name)

**Within _asgard_ folder:**
- asgard/admin.py – Models registered here
- asgard/models.py – It includes three models
    - Rooms (model): Stores the information of the room, and provide limited API access to the Rooms in the database
    - Media (model): Connected with a ForeignKey to the Rooms model. This models only purpose to store the media URLs (images) for their room
    - Reservation (model): Stores all the incoming reservations, and it’s connected to the Rooms model with a ForeignKey, and provide limited API access to the Reservations in the database
- asgard/urls.py – Routes created to the application
- asgard/views.py – The view.py contains the following functions:
    - index: index page
    - contact: contact page
    - about: about page
    - rooms: Page for all rooms
    - room: Page for an individual room
    - available: Check available rooms at the index page
    - reservation: Save the pre-reservation form's input values into session at the room page
    - reservatoindata: For JS to fetch the prices and make calculations
    - roomdata: For JS to fetch the prices and make calculations
    - reservation_submit: Submit the reservation, and add to the database either paid or unpaid
    - checkout: Stripe card payment
    - confirmation: Confirmation of the reservation

**Within _asgard/static/asgard_ folder:** 
- aboutus.css: style file for the about us page
- contact.css: style file for the contact page
- header.css: style file for the application’s header
- home.css: style file for the index page
- reservation.css: style file for the reservation page
- room.css: style file for the selected room page
- rooms.css: style file for the available rooms / room selection page
- favicon.ico: favicon for the website
- app.js: The app.js JavaScript file contains all the necessary functions for the application. Including GET and POST fetch to check room availability, storing sessions in the local storage, function for Stripe API payment and confirmation.

**Within _asgard/static/asgard/img_ folder:** This folder contains all the media (image) files.

**Within _asgard/templates/asgard_ folder:** This folder contains all the html template files.
- about-us.html: About Us page
- confirmation.html: Confirmation page
- contact-page.html: Contact page
- index.html: The website’s main page
- layout.html: The layout html, which contains the website’s header with the navigation and the footer part of the page. 
- reservation.html: The reservation page, where customer can finalize their booking, including their contact information and begin the card payment.
- room.html: This is file contains the template for the individual room
- rooms.html: This is file contains the template for the available rooms and room selection.

## Installation:
Install project dependencies by running ```pip install -r requirements.txt```. It includes ```stripe==2.60.0```, which is necessary for the card payment.