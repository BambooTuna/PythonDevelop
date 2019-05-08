import pykka
import time


class OrderActor(pykka.ThreadingActor):
    use_daemon_thread = True

    def __init__(self, parent_actor, api):
        super().__init__()
        self._parent_actor_proxy = parent_actor.proxy()
        self.api = api

    def send_order(self, order_data):
        print(order_data)
        time.sleep(1)
        self._parent_actor_proxy.order_result("send order result = ???")
