import pykka
import configparser
import pybitflyer
import OrderActor
import PositionActor
import StreamDataProcessingActor


class MainLogicActor(pykka.ThreadingActor):
    use_daemon_thread = True

    def __init__(self, parent_actor, logger):
        super().__init__()
        self._parent_actor_proxy = parent_actor.proxy()
        self.logger = logger

        config = configparser.ConfigParser()
        config.read("setting.txt")
        section1 = "ApiKey"
        key = config.get(section1, 'key')
        secret = config.get(section1, 'secret')
        api = pybitflyer.API(api_key=key, api_secret=secret)

        self._order_actor_proxy = OrderActor.OrderActor.start(self.actor_ref, api).proxy()
        # 5秒ごとにポジションを取得
        self._position_actor_proxy = PositionActor.PositionActor.start(self.actor_ref, api, 5).proxy()
        self._stream_api_actor_proxy = StreamDataProcessingActor.StreamDataProcessingActor.start(self.actor_ref).proxy()

    def run(self):
        self.logger.info("==========MainLogicActor Start==========")
        self._stream_api_actor_proxy.run()
        self._position_actor_proxy.run()

    def order_result(self, data):
        self.logger.info("order: %s" % data)

    def position_result(self, data):
        self.logger.info("position: %s" % data)

    def stream_api_result(self, data):
        self.logger.info("executions: %s" % data)
        # 例: 約定履歴で大きい約定が流れてきたとき注文を出す。Jsonパース、条件設定は各自で（時間あったらかく）
        if True:
            self._order_actor_proxy.send_order(5)

