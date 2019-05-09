import ActorSupport
import WebSocket


class StreamActor(ActorSupport.ActorSupport):
    use_daemon_thread = True

    def __init__(self, parent_actor, channel="lightning_executions_FX_BTC_JPY"):
        super().__init__()
        self._parent_actor_proxy = parent_actor.proxy()
        self.realtime_api = WebSocket.RealtimeAPI(
            url="wss://ws.lightstream.bitflyer.com/json-rpc",
            channel=channel,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

    def run(self):
        self.realtime_api.connect()

    def on_message(self, message):
        self._parent_actor_proxy.received_data(message)

    def on_error(self, error):
        self._parent_actor_proxy.restart(error)

    def on_close(self):
        self._parent_actor_proxy.restart()
