import time


def order_time_handler(order, courier):
    for dh in order.delivery_hours:
        order_starts = time.strptime(dh[:5], '%H:%M')
        order_ends = time.strptime(dh[6:], '%H:%M')
        for wh in courier.working_hours:
            courier_starts = time.strptime(wh[:5], '%H:%M')
            courier_ends = time.strptime(wh[6:], '%H:%M')
            if courier_starts <= order_starts and order_ends <= courier_ends:
                return True
    return False


def order_update(orders, courier):
    if len(orders) == 0:
        return
    if courier.courier_type == 'foot':
        weight = 10
    elif courier.courier_type == 'bike':
        weight = 15
    else:
        weight = 50
    for o in orders:
        if not o.complete:
            if weight - o.weight >= 0:
                if o.region in courier.regions:
                    time_is_right = order_time_handler(o, courier)
                    if time_is_right:
                        continue
        o.assigned = None
        o.save()



