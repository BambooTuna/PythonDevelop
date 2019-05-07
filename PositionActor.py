import pykka
import time
import schedule


class PositionActor(pykka.ThreadingActor):
    def __init__(self, parent_actor_proxy):
        super().__init__()
        self._parent_actor_proxy = parent_actor_proxy

    def run(self):
        schedule.every(1/20).minutes.do(self.__get_my_position)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def __get_my_position(self):
        time.sleep(1)
        self._parent_actor_proxy.position_result("get my position result = ???")
