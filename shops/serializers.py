from rest_framework import serializers
from decimal import Decimal

from .models import Shop

class ShopSerializer(serializers.ModelSerializer):
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive value.")
        return value
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['chapter_capital'] = '$' + str(instance.charter_capital)
        return data

    def create(self, validated_data):
        charter_c = validated_data['charter_capital']
        size = 'small'
        
        if charter_c > 10000.00 and charter_c < 50000.00:
            size = 'medium'
        elif charter_c >= 50000.00:
            size = 'big'
        
        validated_data['shop_size'] = size

        validated_data['charter_capital'] *= Decimal(0.9)  # lets say 10% for reserve deposited, so we give up 10% to the bank

        return super().create(validated_data)

    class Meta:
        model = Shop
        fields = '__all__'

# For test in python shell

#from shops.serializers import ShopSerializer
#from datetime import date
#a_d = date(2000, 1, 1)
#data = {'name': 'Coca cola', 'owner': 'Umidjon', 'opened_date': a_d, 'charter_capital':1000}
#shop_ser = ShopSerializer(data=data)
#shop_ser.is_valid()
#shop_ser.save()
#shop_ser.data