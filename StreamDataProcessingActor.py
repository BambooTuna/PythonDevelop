import ActorSupport
import StreamActor
import Protocol
import json
import time


class StreamDataProcessingActor(ActorSupport.ActorSupport):
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

    def received_data(self, message: str):
        try:
            result = map(lambda x: Protocol.LightningExecutions(x), json.loads(message)["params"]["message"])
            self._parent_actor_proxy.stream_api_result(list(result))
        except Exception as e:
            self.logger.error(e)

    def restart(self, error):
        self.logger.error("Restart ErrorReason: " % error)
        time.sleep(5)
        self._executions_actor_proxy.actor_ref.stop()
        self.actor_ref.proxy().create_children_actor()
        self.actor_ref.proxy().run()
