from django.db import models

from django.db import models

class Shop(models.Model):
    BIG = 'big'
    MEDIUM = 'medium'
    SMALL = 'small'

    SHOP_SIZE = (
        (BIG, 'big'),
        (MEDIUM, 'medium'),
        (SMALL, 'small')
    )

    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    opened_date = models.DateField()
    charter_capital = models.DecimalField(max_digits=8, decimal_places=2) # I'd prefer to use decimal data type in financial data
    shop_size = models.CharField(max_length=255, choices=SHOP_SIZE, null=True)