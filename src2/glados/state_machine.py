import enum
from transitions import Machine
import logging
from time import sleep

class StateEnum(enum.Enum):
    IDLE = 0
    SEARCH_FACE = 1
    MOVE_TO_FACE = 2

class Glados(object):
    def __init__(self, name="Glados"):
        self.name = name
        self.machine = Machine(model=self, states=StateEnum, initial=StateEnum.IDLE)
        self.running = True
        self.machine.add_transition(trigger='do_something', source=StateEnum.IDLE, dest=StateEnum.SEARCH_FACE)
        self.machine.add_transition(trigger='found_face', source=StateEnum.SEARCH_FACE, dest=StateEnum.MOVE_TO_FACE)
        self.machine.add_transition(trigger='rest', source="*", dest=StateEnum.IDLE)

    def run(self):
        while self.running:
            if self.state == StateEnum.IDLE:
                self.do_something();
            sleep(3)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('transitions').setLevel(logging.INFO)
    glados = Glados()
    glados.run()