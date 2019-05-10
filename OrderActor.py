import ActorSupport
import Protocol
import pybitflyer
from decimal import *


class OrderActor(ActorSupport.ActorSupport):
    use_daemon_thread = True

    def __init__(self, parent_actor, api: pybitflyer.API):
        super().__init__()
        self._parent_actor_proxy = parent_actor.proxy()
        self.api = api

    def send_order(self, order_data: Protocol.OrderDataRequest):
        setcontext(Context(prec=8, rounding=ROUND_HALF_DOWN))
        self.logger.info("Order: %s %s %s %s %s" % (order_data.product_code, order_data.child_order_type, order_data.side, order_data.price, order_data.size))
        result = None
        try:
            result = self.api.sendchildorder(
                product_code=order_data.product_code,
                child_order_type=order_data.child_order_type,
                side=order_data.side,
                price=order_data.price,
                size=float(order_data.size),
                minute_to_expire=order_data.minute_to_expire,
                time_in_force=order_data.time_in_force
            )
        except Exception as e:
            self.logger.error(e)

        if result is not None:
            try:
                self._parent_actor_proxy.order_result(Protocol.OrderDataResponse(result))
            except Exception as e:
                self.logger.error(e)
