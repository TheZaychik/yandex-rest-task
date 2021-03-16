from rest_framework import serializers
from main import models
import re


class CourierSerializer(serializers.Serializer):
    courier_id = serializers.IntegerField()
    courier_type = serializers.CharField(max_length=8)
    regions = serializers.JSONField()
    working_hours = serializers.JSONField()
    rating = serializers.FloatField(default=0, allow_null=True)
    earnings = serializers.IntegerField(default=0, allow_null=True)

    def create(self, validated_data):
        return models.Courier.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return models.Courier.objects.filter(courier_id=instance.courier_id).update(**validated_data)

    def validate(self, data):
        couriers = models.Courier.objects.all()
        #  check courier_id
        if not self.partial:
            for c in couriers:
                if data['courier_id'] == c.courier_id:
                    raise serializers.ValidationError({'courier_id': "Courier ID is not unique"})
        #  check courier_type
        if not (data['courier_type'] == 'foot' or data['courier_type'] == 'car' or data['courier_type'] == 'bike'):
            raise serializers.ValidationError({'courier_type': "Courier type is not valid"})
        #  check regions
        if len(data['regions']) == 0:
            raise serializers.ValidationError({'regions': "Regions is empty"})
        else:
            for r in data['regions']:
                if type(r) is str:
                    raise serializers.ValidationError({'regions': "Regions is not valid"})
        #  check working_hours
        if len(data['working_hours']) == 0:
            raise serializers.ValidationError({'working_hours': "Working hours is empty"})
        else:
            regex = re.compile(r'\d\d:\d\d-\d\d:\d\d')
            for w in data['working_hours']:
                if not regex.match(w) or len(w) != 11:
                    raise serializers.ValidationError({'working_hours': "Working hours format is not valid"})
                times = w.split('-')
                for t in times:
                    if not (0 <= int(t[0:2]) <= 24 and 0 <= int(t[3:5]) <= 59):
                        raise serializers.ValidationError({'working_hours': f"Working hours {t} is not valid"})
        return data


class OrderSerializer(serializers.Serializer):
    order_id = serializers.FloatField()
    assigned = serializers.PrimaryKeyRelatedField(source='Courier', queryset=models.Courier.objects.all(), required=False)
    weight = serializers.FloatField()
    region = serializers.IntegerField()
    delivery_hours = serializers.JSONField()

    def create(self, validated_data):
        return models.Order.objects.create(**validated_data)

    def validate(self, data):
        orders = models.Order.objects.all()
        #  check order_id
        if not self.partial:
            for o in orders:
                if data['order_id'] == o.order_id:
                    raise serializers.ValidationError({'order_id': "Order ID is not unique"})
        #  check weight
        if ((data['weight'] < 0.01) or (data['weight'] > 50)) or ((type(data['weight']) is not float) and (
                type(data['weight']) is not int)):
            print(type(data['weight']))
            raise serializers.ValidationError({'weight': "Weight is not valid"})
        else:
            data['weight'] = round(data['weight'], 2)
        #  check region
        if type(data['region']) is not int:
            raise serializers.ValidationError({'region': "Region is not valid"})
        #  check working_hours
        if len(data['delivery_hours']) == 0:
            raise serializers.ValidationError({'delivery_hours': "Delivery hours is empty"})
        else:
            regex = re.compile(r'\d\d:\d\d-\d\d:\d\d')
            for w in data['delivery_hours']:
                if not regex.match(w) or len(w) != 11:
                    raise serializers.ValidationError({'delivery_hours': "Delivery hours format is not valid"})
                times = w.split('-')
                for t in times:
                    if not (0 <= int(t[0:2]) <= 24 and 0 <= int(t[3:5]) <= 59):
                        raise serializers.ValidationError({'delivery_hours': f"Delivery hours {t} is not valid"})
        return data
