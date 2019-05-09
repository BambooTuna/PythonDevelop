import pykka
import LogSupport


class ActorSupport(pykka.ThreadingActor):
    def __init__(self):
        super().__init__()
        self.logger = LogSupport.LogSupport(self.__class__.__name__).logger
