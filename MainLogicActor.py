import pykka
import schedule

import OrderActor
import PositionActor
import StreamAPIActor


class MainLogicActor(pykka.ThreadingActor):
    def __init__(self, parent_actor_proxy):
        super().__init__()
        self._parent_actor_proxy = parent_actor_proxy
        self._my_actor_proxy = self.actor_ref.proxy()

        self._order_actor_proxy = OrderActor.OrderActor.start(self._my_actor_proxy).proxy()
        self._position_actor_proxy = PositionActor.PositionActor.start(self._my_actor_proxy).proxy()
        self._stream_api_actor_proxy = StreamAPIActor.StreamAPIActor.start(self._my_actor_proxy).proxy()

    def run(self):
        print("run main logic")
        self._stream_api_actor_proxy.run()
        self._position_actor_proxy.run()
        self._order_actor_proxy.send_order(5, block=False)
        self._order_actor_proxy.send_order(10, block=False)


    def order_result(self, data):
        print(data)

    def position_result(self, data):
        print(data)

    def stream_api_result(self, data):
        print(data)
