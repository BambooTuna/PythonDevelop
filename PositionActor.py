import ActorSupport
import time
import Protocol


class PositionActor(ActorSupport.ActorSupport):
    use_daemon_thread = True

    def __init__(self, parent_actor, api, interval=5):
        super().__init__()
        self._parent_actor_proxy = parent_actor.proxy()
        self.api = api
        self.interval = interval
        self.actor_ref.proxy().get_my_position()

    def get_my_position(self):
        result = None
        try:
            result = self.api.getpositions(product_code="FX_BTC_JPY")
        except Exception as e:
            self.logger.error(e)

        if type(result) == list:
            try:
                self._parent_actor_proxy.position_result(list(map(lambda x: Protocol.PositionDataResponse(x), result)))
            except Exception as e:
                self.logger.error(e)
        else:
            self.logger.error(result)

        time.sleep(self.interval)
        self.actor_ref.proxy().get_my_position()
