from decimal import *


class StreamDataResponse(object):
    def __init__(self):
        pass


class LightningExecutions(StreamDataResponse):
    def __init__(self, args):
        super().__init__()
        self.id: int = args["id"]
        self.side: str = args["side"]
        self.price: int = args["price"]
        self.size: float = args["size"]
        self.exec_date: str = args["exec_date"]
        self.buy_child_order_acceptance_id: str = args["buy_child_order_acceptance_id"]
        self.sell_child_order_acceptance_id: str = args["sell_child_order_acceptance_id"]


class PositionDataResponse(object):
    def __init__(self, args):
        self.product_code = args.get("product_code")
        self.side = args.get("side")
        self.price = args.get("price")
        self.size: Decimal = Decimal(args.get("size"))
        self.commission = args.get("commission")
        self.swap_point_accumulate = args.get("swap_point_accumulate")
        self.require_collateral = args.get("require_collateral")
        self.open_date = args.get("open_date")
        self.leverage = args.get("leverage")
        self.pnl = args.get("pnl")
        self.sfd = args.get("sfd")


class OrderDataRequest(object):
    def __init__(self, args):
        self.product_code = args.get("product_code") or "FX_BTC_JPY"
        self.child_order_type = args.get("child_order_type")
        self.side = args.get("side")
        self.price = args.get("price")
        self.size: Decimal = Decimal(args.get("size"))
        self.minute_to_expire = args.get("minute_to_expire") or 43200
        self.time_in_force = args.get("time_in_force") or "GTC"


class OrderDataResponse(object):
    def __init__(self, args):
        self.child_order_acceptance_id = args["child_order_acceptance_id"]


