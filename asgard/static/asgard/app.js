const inputCheckIn = document.querySelector('#input-checkin');
const inputCheckOut = document.querySelector('#input-checkout');
const inputAdult = document.querySelector('#input-adult');
const inputChildren = document.querySelector('#input-children');
const checkAvailabilityBtn = document.querySelector('#checkAvailability');
const preReserveForm = document.querySelector('.pre-reservation-form');
const preReserveBtn = document.querySelector('#pre-reserve-btn');
const reservation = document.querySelector('#reservation');
const nonavailableBtn = document.querySelector('#nonavailable');
const confirmation = document.querySelector('#confirmation');


// If the session storage is not empty load the form values from the session storage
if (checkAvailabilityBtn || preReserveForm) {         
    // Set Session
    if (sessionStorage.length != 0) {
        inputCheckIn.value = sessionStorage.checkIn;
        inputCheckOut.value = sessionStorage.checkOut;
        inputAdult.value = sessionStorage.adult;
        sessionStorage.children == '' ? inputChildren.value = 0 : inputChildren.value = sessionStorage.children;
    }
}


// Set defaults for inputs
function setDefaults() {
    // Set default date if checkin/checkout input value empty
    const todaysDate = new Date();
    const tomorrowsDateStamp = new Date();
    const tomorrowsDate = new Date(tomorrowsDateStamp.setDate(tomorrowsDateStamp.getDate()+1));
    const yeartoday = todaysDate.getFullYear().toString();
    const monthtodayInt = todaysDate.getMonth()+1;
    let monthtoday = monthtodayInt.toString();
    let daytoday = todaysDate.getDate().toString();
    const yeartomorrow = tomorrowsDate.getFullYear().toString();
    const monthtomorrowInt = tomorrowsDate.getMonth()+1;
    let monthtomorrow = monthtomorrowInt.toString();
    let daytomorrow = tomorrowsDate.getDate().toString();

    // Add 0 if necessary front of month and day
    monthtoday.length == 1 ? monthtoday = `0${monthtoday}` : monthtoday;
    daytoday.length == 1 ? daytoday = `0${daytoday}` : daytoday;
    monthtomorrow.length == 1 ? monthtomorrow = `0${monthtomorrow}` : monthtomorrow;
    daytomorrow.length == 1 ? daytomorrow = `0${daytomorrow}` : daytomorrow;

    if (inputCheckIn.value == '') {
        inputCheckIn.value = `${yeartoday}-${monthtoday}-${daytoday}`;
    }

    if (inputCheckOut.value == '') {
        inputCheckOut.value = `${yeartomorrow}-${monthtomorrow}-${daytomorrow}`;
    }

    // Set default value to Adults and Children input if empty
    if (inputAdult.value == '') {
        inputAdult.value = 1;
    }

    if (inputChildren.value == '') {
        inputChildren.value = 0;
    }
}


// Check Availability - Form check before submit
function addSession(e) {
    // Give an error message if the form is not filled out
    if (inputCheckIn.value === '' || inputCheckOut.value === '' || inputAdult.value == 0) {
        e.preventDefault();
        alert('There is an empty field');
    } else {
        // Add to session storage the form values if the browser supports session storage
        if (typeof(Storage) !== "undefined") {
            sessionStorage.checkIn = inputCheckIn.value;
            sessionStorage.checkOut = inputCheckOut.value;
            sessionStorage.adult = inputAdult.value;
            sessionStorage.children = inputChildren.value;
        } else {
            console.log('Local storage not supported');
        }
    }
}


// From the index page when checking the availability
if (checkAvailabilityBtn) {
    sessionStorage.removeItem('roomId');
    // Set input defaults
    setDefaults();
    checkAvailabilityBtn.addEventListener('click', addSession);
}


// Pre-reserve form (room.html)
if (preReserveForm) {
    // Set input defaults
    setDefaults();
    // Update room id in session
    sessionStorage.roomId = preReserveForm.dataset.roomid;
}


// From the room page when starting the reservation, update the session info and check if the room is available
if (preReserveBtn) {       
    preReserveBtn.addEventListener('click', addSession)
    
    // Check if the room is available
    preReserveBtn.addEventListener('click', event => {
        event.preventDefault();

        // Fetch from database the room availability 
        const sessionCheckIn = new Date(sessionStorage.checkIn).getTime()/1000
        const sessionCheckOut = new Date(sessionStorage.checkOut).getTime()/1000
        
        fetch(`/reservatoindata/${sessionStorage.roomId}`)
        .then(response => response.json())
        .then(reservation => {

            if (reservation.length === 0) {
                preReserveForm.submit()
            } else {
                let reserved = true;
                reservation.forEach( e => {
                    // Dates convert to unix time
                    const reservedCheckIns = new Date(e.check_in).getTime()/1000
                    const reservedCheckOuts = new Date(e.check_out).getTime()/1000

                    // If room not available
                        // Within the range
                    if ( ( (sessionCheckIn >= reservedCheckIns && sessionCheckIn <= reservedCheckOuts) ||
                        (sessionCheckOut >= reservedCheckIns && sessionCheckOut <= reservedCheckOuts) ) ||
                        // Outside the range
                        (sessionCheckIn <= reservedCheckIns) && (sessionCheckOut >= reservedCheckOuts) ){
                        reserved = true;
                    // If available
                    } else {
                        reserved = false;
                    }
                })

                if (reserved) {
                    nonavailableBtn.click();
                } else {
                    preReserveForm.submit()
                }
            }                   
        })
    })
}


// Reservation
if (reservation) {
    const checkin = document.querySelector('#checkin');
    const checkout = document.querySelector('#checkout');
    const adult = document.querySelector('#adult');
    const children = document.querySelector('#children');
    const subtotalInput = document.querySelector('#subtotal');
    const discountInput = document.querySelector('#discount');
    const totalInput = document.querySelector('#total');
    const vatInput = document.querySelector('#vat');
    const grandtotalInput = document.querySelector('#grandtotal');
    // Your details form
    const inputFirstName = document.querySelector('#inputFirstName');
    const inputLastName = document.querySelector('#inputLastName');
    const inputEmail = document.querySelector('#inputEmail');
    const inputPhone = document.querySelector('#inputPhone');
    const inputAddress = document.querySelector('#inputAddress');
    const inputAddress2 = document.querySelector('#inputAddress2');
    const inputCity = document.querySelector('#inputCity');
    const inputCountry = document.querySelector('#inputCountry');
    const inputZip = document.querySelector('#inputZip');

    const checkInDate = new Date(sessionStorage.checkIn);
    const checkOutDate = new Date(sessionStorage.checkOut);

    // Convert date to British English day-month-year order
    const checkInDateFormat = Intl.DateTimeFormat('en-GB').format(checkInDate);
    const checkOutDateFormat = Intl.DateTimeFormat('en-GB').format(checkOutDate);

    // Calculate the number of days between two dates
    const differenceInTime = checkOutDate.getTime() - checkInDate.getTime();
    const days = differenceInTime / (1000 * 3600 * 24);

    // Variables for the price breakdown
    let subtotal = 0;
    let discount = 0;
    let total = 0;
    let vat = 0;
    let grandtotal = 0;

    // From session storage add the values to DOM
    checkin.innerHTML = checkInDateFormat;
    checkout.innerHTML = checkOutDateFormat;
    adult.innerHTML = sessionStorage.adult;
    children.innerHTML = sessionStorage.children;

    // Fetch from database the prices and make calculations
    fetch(`/roomdata/${sessionStorage.roomId}`)
    .then(response => response.json())
    .then(room => {
            subtotal = ((room.adult_price * sessionStorage.adult) + (room.child_price * sessionStorage.children)) * days;
            if (days >= 7) {
                discount = subtotal * 0.15;
            }
            total = subtotal - discount;
            vat = total * 0.08;
            grandtotal = total + vat;
            
            // Add values to DOM
            subtotalInput.innerHTML = subtotal.toFixed(2);
            discountInput.innerHTML = discount.toFixed(2);
            totalInput.innerHTML = total.toFixed(2);
            vatInput.innerHTML = vat.toFixed(2);
            grandtotalInput.innerHTML = grandtotal.toFixed(2);
    })

    // Form validation check to make sure all inputs are filled out
    reservation.addEventListener('submit', function (event) {
        if (!reservation.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
            reservation.classList.add('was-validated')
        }
    })

    // Stripe card payment
    const payNowBtn = document.querySelector('#pay-now');

    payNowBtn.addEventListener('click', event => {
        // Form validation check to make sure all inputs are filled out
        if (!reservation.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
            reservation.classList.add('was-validated')
        } else {
            // Add to session storage the contact details form values if the browser supports session storage
            if (typeof(Storage) !== "undefined") {
                sessionStorage.firstName = inputFirstName.value;
                sessionStorage.lastName = inputLastName.value;
                sessionStorage.email = inputEmail.value;
                sessionStorage.phone = inputPhone.value;
                sessionStorage.address = inputAddress.value;
                sessionStorage.address2 = inputAddress2.value;
                sessionStorage.city = inputCity.value;
                sessionStorage.country = inputCountry.value;
                sessionStorage.zip = inputZip.value;
            } else {
                console.log('Local storage not supported');
            }

            fetch(`/checkout/${sessionStorage.roomId}`)
            .then((result) => { return result.json() })
            .then((data) => {
            const stripe = Stripe(data.stripe_public_key);

            stripe.redirectToCheckout({
                sessionId: data.session_id
            }).then(function (result) {
                console.log(result.error.message);
            });
            })
        }
    })
}

    
// Confirmation
// If the payment was succesfull, after the page loaded it will request a Fetch POST, and add the booking to the database
if (confirmation) {
    document.addEventListener('DOMContentLoaded', () => {
        const payed = document.querySelector('#payed');
        if (payed) {
            fetch(`/reservation_submit/${sessionStorage.roomId}/payed`, {
                method: 'POST',
                body: JSON.stringify({
                    firstName: sessionStorage.firstName,
                    lastName: sessionStorage.lastName,
                    email: sessionStorage.email,
                    phone: sessionStorage.phone,
                    address: sessionStorage.address,
                    address2: sessionStorage.address2,
                    city: sessionStorage.city,
                    country: sessionStorage.country,
                    zip: sessionStorage.zip,
                }) 
            })
        }
    })
}
