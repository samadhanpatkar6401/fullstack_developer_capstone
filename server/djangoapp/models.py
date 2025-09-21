# Uncomment the following imports before adding the Model code
from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime  # To dynamically set the current year if needed

# Create your models here.

# Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Optional fields (example)
    country = models.CharField(max_length=100, blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name  # Display car make name


# Car Model model
class CarModel(models.Model):
    # Many-To-One relationship (One CarMake → Many CarModels)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    # Limited choices for car type
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('TRUCK', 'Truck'),
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')

    # Year between 2015 and 2023 (or current year)
    current_year = datetime.datetime.now().year
    year = models.IntegerField(
        validators=[MinValueValidator(2015), MaxValueValidator(2023)],
        default=current_year
    )

    # Optional: Dealer ID to link to external dealer database
    dealer_id = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.car_make.name} - {self.name}"  # Show make and model