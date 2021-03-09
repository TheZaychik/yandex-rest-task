from rest_framework.response import Response
from rest_framework.decorators import api_view
from main import models
from main import serializers


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


@api_view(['PATCH', 'GET'])
def couriers_patch(request, courier_id):
    courier = models.Courier.objects.get(courier_id=courier_id)
    if request.method == 'PATCH':
        field = request.data
        key = list(field.keys())[0]
        if key == 'courier_type':
            courier.courier_type = field[key]
        elif key == 'regions':
            courier.regions = field[key]
        elif key == 'working_hours':
            courier.working_hours = field[key]
        else:
            return Response(status=400)
        courier_serializer = serializers.CourierSerializer(courier, data=serializers.CourierSerializer(courier).data,
                                                           partial=True)
        if courier_serializer.is_valid():
            courier.save()
            return Response(courier_serializer.data, status=200)
        else:
            print(courier_serializer.errors)
            return Response(status=400)
    else:
        return Response('GET', status=200)
