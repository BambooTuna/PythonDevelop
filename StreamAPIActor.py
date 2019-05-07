import pykka
import time


class StreamAPIActor(pykka.ThreadingActor):
    def __init__(self, parent_actor_proxy):
        super().__init__()
        self._parent_actor_proxy = parent_actor_proxy

    def run(self):
        self.__connect()

    def __connect(self):
        time.sleep(2)
        self._parent_actor_proxy.position_result("stream api result = ???")
