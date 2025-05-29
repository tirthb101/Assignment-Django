from django.db import models
from django.core.validators import MinLengthValidator


class Students(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField()
    enrollment_number = models.CharField( 
            max_length=10,
            validators=[MinLengthValidator(10, "The enrollment_number must contain 10 characters")]
        )
    password = models.CharField(
            max_length=150,
            validators=[MinLengthValidator(10, "The password must contain at least 10 characters")]
        )


