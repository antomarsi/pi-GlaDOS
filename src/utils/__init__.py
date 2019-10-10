import asyncio
import logging
import abc
import concurrent


class BaseComponent(metaclass=abc.ABCMeta):
    def __init__(self, sockets, tick=5):
        self.sockets = sockets
        self.timer_tick = 1 / tick
        self.on_updates = []
        pass

    def add_update(self, on_update):
        self.on_updates.append(on_update)
        logging.info("Added {} to the {} Component".format(
            on_update.__name__, type(self).__name__))

    def start(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._process())
        loop.run_forever()

    async def broadcast(self, sockets, message):
        for socket in sockets:
            await socket.send(message)

    def handle_message(self, sockets, message):
        logging.error(
            "[{}] - Override this process event".format(type(self).__name__))

    def process(self):
        logging.error(
            "[{}] - Override this process event".format(type(self).__name__))

    async def _process(self):
        try:
            while True:
                self.process()
                for on_update in self.on_updates:
                    logging.info("Processing {} in {}".format(
                        on_update.__name__, type(self).__name__))
                    await on_update(self)
                await asyncio.sleep(self.timer_tick)
        except Exception as e:
            logging.error("{} has a error".format(type(self).__name__))
            print(e)

    async def message_handler(self, message):
        logging.error(
            "[{}] - Override this process event".format(type(self).__name__))


executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)


async def start_component(component, update_list=[]):
    for updates in update_list:
        component.add_update(updates)
    loop = asyncio.get_event_loop()
    loop.run_in_executor(executor, component.start)
    return component
