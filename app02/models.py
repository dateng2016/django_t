from django.db import models

# Create your models here.


class Admin(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.username


class Department(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self) -> str:
        return self.title


class UserInfo(models.Model):
    name = models.CharField(max_length=16)
    password = models.CharField(max_length=64)
    age = models.IntegerField()
    account = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField()

    # Note: Django will automatically generate the "_id" at the end of the foreign key
    depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    # depart = models.ForeignKey(
    #     to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL
    # )

    gender_choices = (
        (1, "Male"),
        (2, "Female"),
    )  # Restriction within Django can only be 1 or 2
    gender = models.SmallIntegerField(choices=gender_choices)


class PrettyNum(models.Model):
    mobile = models.CharField(max_length=11)
    price = models.IntegerField(default=0, null=True, blank=True)

    level_choices = (
        (1, "level 1"),
        (2, "level 2"),
        (3, "level 3"),
        (4, "level 4"),
    )

    level = models.SmallIntegerField(choices=level_choices, default=1)

    status_choices = ((1, "Occupied"), (2, "Not Occupied"))

    status = models.SmallIntegerField(choices=status_choices, default=2)


class Task(models.Model):
    level_choices = ((1, "Emergency"), (2, "Important"), (3, "Temporary"))
    level = models.SmallIntegerField(choices=level_choices)
    title = models.CharField(max_length=64)
    detail = models.TextField()

    user = models.ForeignKey(to="admin", on_delete=models.CASCADE)


class Order(models.Model):
    oid = models.CharField(max_length=64)
    title = models.CharField(max_length=32)
    price = models.IntegerField()

    status_choices = ((1, "Not Paid"), (2, "Paid"))
    status = models.SmallIntegerField(choices=status_choices, default=1)

    admin = models.ForeignKey(to="Admin", on_delete=models.CASCADE)


class Boss(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    img = models.CharField(max_length=123)
