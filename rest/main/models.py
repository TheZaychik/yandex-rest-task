from django.db import models


class Courier(models.Model):
    courier_id = models.IntegerField(verbose_name='Courier ID', unique=True)
    courier_type = models.CharField(verbose_name='Courier type', max_length=8)
    regions = models.JSONField(verbose_name='Regions')
    working_hours = models.JSONField(verbose_name='Working hours')
    rating = models.FloatField(verbose_name='Rating', default=0, null=True)
    earnings = models.IntegerField(verbose_name='Earnings', default=0, null=True)


class Order(models.Model):
    order_id = models.IntegerField(verbose_name='Order ID', unique=True)
    assigned = models.ForeignKey(to=Courier, verbose_name='Order assigner', on_delete=models.CASCADE, blank=True,
                                 null=True)
    weight = models.FloatField(verbose_name='Weight')
    region = models.IntegerField(verbose_name='Region')
    delivery_hours = models.JSONField(verbose_name='Delivery hours')
