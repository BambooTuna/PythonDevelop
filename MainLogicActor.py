import ActorSupport
import OrderActor
import PositionActor
import StreamDataProcessingActor
import Protocol
from typing import List
from decimal import *


class MainLogicActor(ActorSupport.ActorSupport):
    use_daemon_thread = True

    def __init__(self, parent_actor, api):
        super().__init__()
        self._parent_actor_proxy = parent_actor.proxy()
        self._order_actor_proxy: OrderActor.OrderActor = OrderActor.OrderActor.start(self.actor_ref, api).proxy()
        # 5秒ごとにポジションを取得
        self._position_actor_proxy: PositionActor.PositionActor = PositionActor.PositionActor.start(self.actor_ref, api, 5).proxy()
        self._stream_api_actor_proxy: StreamDataProcessingActor.StreamDataProcessingActor = StreamDataProcessingActor.StreamDataProcessingActor.start(self.actor_ref).proxy()

    def run(self):
        self.logger.info("==========MainLogicActor Start==========")
        self._stream_api_actor_proxy.run()

    def order_result(self, data: Protocol.OrderDataResponse):
        self.logger.info("order: %s" % data.child_order_acceptance_id)

    def position_result(self, data: List[Protocol.PositionDataResponse]):
        setcontext(Context(prec=8, rounding=ROUND_HALF_DOWN))
        total_position_size = Decimal(0)
        for i in data:
            total_position_size += i.size * Decimal(1 if i.side == "BUY" else -1)
        self.logger.info("position: %s" % total_position_size)

    def stream_api_result(self, data: List[Protocol.LightningExecutions]):
        max_size = 0
        for i in data:
            max_size += i.size * (1 if i.side == "BUY" else -1)

        # 例: 約定履歴で大きい約定が流れてきたとき注文を出す。Jsonパース、条件設定は各自で（時間あったらかく）
        if abs(max_size) >= 10:
            self._order_actor_proxy.send_order(Protocol.OrderDataRequest({
                "child_order_type": "MARKET",
                "side": ("BUY" if max_size > 0 else "SELL"),
                "price": 0,
                "size": 0.01
            }))

