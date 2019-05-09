import ActorSupport
import MainLogicActor
import pybitflyer
import setting


class MainActor(ActorSupport.ActorSupport):
    def __init__(self):
        super().__init__()
        api = pybitflyer.API(
            api_key=setting.API_KEY,
            api_secret=setting.API_SECRET
        )
        self.actor_proxy = MainLogicActor.MainLogicActor.start(self.actor_ref, api).proxy()

    def run(self):
        self.actor_proxy.run()


if __name__ == '__main__':
    MainActor.start().proxy().run()
