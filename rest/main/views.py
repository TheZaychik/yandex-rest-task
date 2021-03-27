from rest_framework.response import Response
from rest_framework.decorators import api_view
from main import models
from main import serializers
from main import subfunctions
from datetime import datetime


@api_view(['POST'])
def couriers_post(request):  # получение данных о курьерах
    couriers = request.data.get('data')
    if couriers is None:
        return Response(status=400)
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


@api_view(['PATCH', 'GET'])  # изменение курьеров, либо получение информации о курьере
def couriers_patch_get(request, courier_id):
    try:
        courier = models.Courier.objects.get(courier_id=courier_id)
    except:
        return Response(status=404)
    if request.method == 'PATCH':
        courier_to_patch = serializers.CourierSerializer(courier).data
        field = request.data
        keys = list(field.keys())
        for k in keys:
            if k == 'courier_type':
                courier_to_patch[k] = field[k]
            elif k == 'regions':
                courier_to_patch[k] = field[k]
            elif k == 'working_hours':
                courier_to_patch[k] = field[k]
            else:
                return Response(status=400)
        courier_serializer = serializers.CourierSerializer(courier, data=courier_to_patch,
                                                           partial=True)
        if courier_serializer.is_valid():
            courier_serializer.update(courier, courier_to_patch)
            subfunctions.order_update(
                models.Order.objects.all().filter(assigned_id=courier.id, complete_time__isnull=True),
                models.Courier.objects.get(courier_id=courier_id))
            return Response(courier_to_patch, status=200)
        else:
            return Response(status=400)
    else:
        if len(courier.delivery) == 0:
            return Response(serializers.CourierSerializer(courier).data, status=200)
        orders = models.Order.objects.all().filter(assigned_id=courier.id, complete_time__isnull=False).order_by(
            'region')
        regions_time = {}
        avg_time = []
        for o in orders:
            timedelta = o.complete_time - o.assign_time
            if o.region not in regions_time.keys():
                regions_time[o.region] = []
            regions_time[o.region].append(timedelta.seconds)
        keys = list(regions_time.keys())
        for k in keys:
            avg_time.append(sum(regions_time[k]) / len(regions_time[k]))
        courier.rating = round((60 * 60 - min(min(avg_time), 60 * 60)) / (60 * 60) * 5, 2)
        for delivery in courier.delivery:
            if not delivery['paid']:
                if delivery['delivery_type'] == 'foot':
                    c = 2
                elif delivery['delivery_type'] == 'bike':
                    c = 5
                else:
                    c = 9
                courier.earnings += 500 * c
                delivery['paid'] = True
        courier.save()
        return Response(serializers.CourierSerializer(courier).data, status=200)


@api_view(['POST'])
def orders_post(request):  # получение заказов
    orders = request.data.get('data')
    if orders is None:
        return Response(status=400)
    not_valid = {
        "validation_error": {
            "orders": [],
            "errors": []
        }
    }
    valid = {
        "orders": []
    }
    for o in orders:
        order_serializer = serializers.OrderSerializer(data=o)
        if order_serializer.is_valid():
            valid['orders'].append({'id': o['order_id']})
        else:
            not_valid['validation_error']['orders'].append({'id': o['order_id']})
            not_valid['validation_error']['errors'].append({o['order_id']: order_serializer.errors})
    if len(not_valid['validation_error']['orders']) != 0:
        return Response(not_valid, status=400)
    else:
        for o in orders:
            order_serializer = serializers.OrderSerializer(data=o)
            order_serializer.create(o)
        return Response(valid, status=201)


@api_view(['POST'])
def orders_assign(request):
    courier_id = request.data.get('courier_id')
    try:
        courier = models.Courier.objects.get(courier_id=courier_id)
    except:
        return Response(status=400)
    orders = models.Order.objects.all()
    orders_response = {
        "orders": [],
        "assign_time": ""
    }
    # проверка на незавершенные заказы
    time_assigned = False
    for o in orders:
        if o.assigned_id == courier.id and o.complete_time is None:
            orders_response['orders'].append({'id': o.order_id})
            if not time_assigned:
                orders_response['assign_time'] = o.assign_time
                time_assigned = True
    # если есть незавершенные заказы
    if len(orders_response['orders']) != 0:
        return Response(orders_response, status=200)
    # foot 10 bike 15 car 50
    if courier.courier_type == 'foot':
        weight = 10
    elif courier.courier_type == 'bike':
        weight = 15
    else:
        weight = 50
    assign_time = datetime.now().isoformat()
    orders_response['assign_time'] = assign_time
    for o in orders:
        if o.assigned is None and o.assign_time is None and o.complete_time is None:
            if weight - o.weight >= 0:
                if o.region in courier.regions:
                    time_is_right = subfunctions.order_time_handler(o, courier)
                    if time_is_right:
                        o.assigned = courier
                        o.assign_time = assign_time
                        weight -= o.weight
                        orders_response['orders'].append({'id': o.order_id})
                        o.save()
    # если не нашлось подходящих заказов
    if len(orders_response['orders']) == 0:
        return Response({"orders": []}, status=200)
    courier.delivery.append({'delivery_type': courier.courier_type, 'completed': False, 'paid': False})
    courier.save()
    return Response(orders_response, status=200)


@api_view(['POST'])
def orders_complete(request):  # уведомление о завершении развоза
    courier_id = request.data.get('courier_id')
    order_id = request.data.get('order_id')
    try:
        order = models.Order.objects.get(order_id=order_id)
        courier = models.Courier.objects.get(courier_id=courier_id)
        complete_time = datetime.fromisoformat(request.data.get('complete_time'))
    except:
        return Response(status=400)
    if order.assigned_id == courier.id:
        if order.complete_time is None:
            order.complete_time = complete_time.isoformat()
            order.save()
            orders = models.Order.objects.all().filter(assigned_id=courier.id)
            completed_orders = True
            # проверка на завершение развоза
            for o in orders:
                if o.complete_time is None:
                    completed_orders = False
            if completed_orders:
                courier.delivery[len(courier.delivery) - 1]['completed'] = True
                courier.save()
        return Response({'order_id': order.order_id}, status=200)
    else:
        return Response(status=400)
