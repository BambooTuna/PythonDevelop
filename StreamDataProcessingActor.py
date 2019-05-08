import pykka
import time
import StreamActor


class StreamDataProcessingActor(pykka.ThreadingActor):
    use_daemon_thread = True

    def __init__(self, parent_actor):
        super().__init__()
        self._parent_actor_proxy = parent_actor.proxy()
        self._executions_actor_proxy = None
        self.actor_ref.proxy().create_children_actor()

    def create_children_actor(self):
        self._executions_actor_proxy = StreamActor.StreamActor.start(self.actor_ref, "lightning_executions_FX_BTC_JPY").proxy()

    def run(self):
        self._executions_actor_proxy.run()

    def received_data(self, message):
        self._parent_actor_proxy.stream_api_result(message)

    def restart(self, error):
        print("restart", self.__class__.__name__)
        time.sleep(5)
        self._executions_actor_proxy.actor_ref.stop()
        self.actor_ref.proxy().create_children_actor()
        self.actor_ref.proxy().run()
