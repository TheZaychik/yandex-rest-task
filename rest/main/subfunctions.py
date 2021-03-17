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
