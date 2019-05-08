import json
import websocket


class RealtimeAPI(object):
    def __init__(self, url, channel, on_message, on_error, on_close):
        self.url = url
        self.channel = channel

        self.ws = websocket.WebSocketApp(self.url, header=None, on_open=self.on_open, on_message=on_message, on_error=on_error, on_close=on_close)
        websocket.enableTrace(False)

    def connect(self):
        self.ws.run_forever(
            ping_interval=10,
            ping_timeout=5
        )

    def on_open(self):
        output_json = json.dumps(
            {'method': 'subscribe',
             'params': {'channel' : self.channel}
             }
        )
        self.ws.send(output_json)
