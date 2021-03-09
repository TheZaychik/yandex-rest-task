from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main import models
from main import serializers
import json


@api_view(['POST'])
def couriers_post(request):
    couriers = request.data.get('data')
    not_valid = {
        "validation_error": {
            "couriers": [],
            "errors": []
        }
    }
    valid = {
        "couriers": []
    }
    for c in couriers:
        courier_serializer = serializers.CourierSerializer(data=c)
        if courier_serializer.is_valid():
            valid['couriers'].append({'id': c['courier_id']})
        else:
            not_valid['validation_error']['couriers'].append({'id': c['courier_id']})
            not_valid['validation_error']['errors'].append(courier_serializer.errors)
    if len(not_valid['validation_error']['couriers']) != 0:
        return Response(not_valid, status=400)
    else:
        for c in couriers:
            courier_serializer = serializers.CourierSerializer(data=c)
            courier_serializer.create(c)
        return Response(valid, status=201)
