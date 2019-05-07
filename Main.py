import MainLogicActor


def main():
    actor_proxy = MainLogicActor.MainLogicActor.start(1).proxy()
    actor_proxy.run()


if __name__ == '__main__':
    main()
