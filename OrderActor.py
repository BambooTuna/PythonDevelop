import pykka
import time


class OrderActor(pykka.ThreadingActor):
    def __init__(self, parent_actor_proxy):
        super().__init__()
        self._parent_actor_proxy = parent_actor_proxy

    def send_order(self, order_data):
        time.sleep(order_data)
        self._parent_actor_proxy.order_result("send order result = ???")
