from django.db import models


class Rooms(models.Model):
    class Meta:
        verbose_name_plural = 'Rooms'

    room_name = models.CharField(max_length=64)
    bed_type = models.CharField(max_length=64)
    max_people = models.IntegerField()
    accommodates = models.IntegerField()
    bathrooms = models.IntegerField()
    bedroom = models.IntegerField()
    beds = models.IntegerField()
    view = models.CharField(max_length=32)
    adult_price = models.DecimalField(max_digits=7, decimal_places=2)
    child_price = models.DecimalField(max_digits=7, decimal_places=2)
    weekly_discount = models.IntegerField()
    url_slug = models.CharField(max_length=64)

    def __str__(self):
        return self.room_name

    def room_api(self):
        return {
            'room_id': self.id,
            'adult_price': self.adult_price,
            'child_price': self.child_price,
            'weekly_discount': self.weekly_discount,
        }


class Media(models.Model):
    class Meta:
        verbose_name_plural = 'Media'

    room_name = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    image_main = models.CharField(max_length=256, default='-')
    image_1 = models.CharField(max_length=256, default='-')
    image_2 = models.CharField(max_length=256, default='-')
    image_3 = models.CharField(max_length=256, default='-')
    image_4 = models.CharField(max_length=256, default='-')
    image_5 = models.CharField(max_length=256, default='-')

    def __str__(self):
        return self.room_name.room_name



class Reservations(models.Model):
    class Meta:
        verbose_name_plural = 'Reservations'

    reserved_room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    address_2 = models.CharField(max_length=64, default='-')
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    zipcode = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    discount = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    vat = models.DecimalField(max_digits=7, decimal_places=2, default=8.0)
    grand_total = models.DecimalField(max_digits=7, decimal_places=2)
    adult = models.IntegerField(default=1)
    child = models.IntegerField(default=0)
    check_in = models.DateField(null=True)
    check_out = models.DateField(null=True)
    reservation_date = models.DateTimeField(auto_now=True)
    payed = models.BooleanField(default=False)

    def reservation_api(self):
        return {
            'room_id': self.reserved_room_id,
            'check_in': self.check_in,
            'check_out': self.check_out,
        }

    def __str__(self):
        return f"{self.last_name}, {self.first_name}, {self.check_in}, {self.check_out}, {self.reserved_room.room_name}, {self.reservation_date}"