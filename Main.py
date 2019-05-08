import pykka
import MainLogicActor
import logging
from logging import getLogger, StreamHandler, Formatter


class MainActor(pykka.ThreadingActor):
    def __init__(self):
        super().__init__()
        logger = getLogger("MainActor")
        logger.setLevel(logging.DEBUG)
        stream_handler = StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(handler_format)
        logger.addHandler(stream_handler)

        self.actor_proxy = MainLogicActor.MainLogicActor.start(self.actor_ref, logger).proxy()

    def run(self):
        self.actor_proxy.run()


if __name__ == '__main__':
    MainActor.start().proxy().run()
