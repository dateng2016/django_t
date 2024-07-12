from django.db import models


class UserInfo(models.Model):
    """
    CREATE TABLE app01_userinfo(
        id bigint auto_increment primary key,
        name varchar(32),
        password varchar(64),
        page int
    )
    """

    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    age = models.IntegerField(default=2)

    # size = models.IntegerField()
    # data = models.IntegerField(null=True, blank=True)


class Department(models.Model):
    title = models.CharField(max_length=16)
