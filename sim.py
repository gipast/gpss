import os
import sys
import math
import numpy as np

from enum import IntEnum, auto
from itertools import cycle
from operator import attrgetter

class Color(IntEnum):
    _order_ = 'GREEN RED'
    GREEN = 1
    RED = 2


class semaphore():

    colors = ['GREEN', 'RED']

    def __init__(self, start_color=Color.RED):
        self.sem = cycle(enumerate(semaphore.colors, start=start_color))
        self.value = next(self.sem)

    def turn_ligth(self):
        self.value = next(self.sem)
        pass


# class sim_obj():
#     queue_income = []
#     queue_outcome = []

#     def __init__(self, name="NoName"):
#         self.name = name
#         pass

#     def process(self):
#         print(self.name)


class sim_event():
    time = 0.
    action = None

    def __init__(self, action, sys_time, time):
        self.time = sys_time + time
        self.action = action


class Sim(sim_event):
    next_evets_queue = []
    time = 0

    def finished(self):
        print("sim done")

    def new_event(self, action, time):
        event = sim_event(action, self.time, time)
        self.next_evets_queue.append(event)

    def __init__(self, sim_time):
        self.sim_time = sim_time
        self.event = sim_event(None, 0, 0)
        self.new_event(self.finished, sim_time)

    def pop_event(self):
        '''
        pops event with min time from queue self.event
        '''
        if len(self.next_evets_queue) == 0:
            return None
        min_val = min(self.next_evets_queue, key=attrgetter('time'))
        minpos = self.next_evets_queue.index(min_val)
        self.event = self.next_evets_queue[minpos]
        self.time = min_val.time
        # print("time = ", self.time)

        self.next_evets_queue.remove(self.event)
        return 0


# static unsigned int seed = 12345
# double u01()
# {
#     seed = seed * 69069 + 1
#     return seed / 4294967296.0
# }

# double exponential(double mean)
# {
#     return -log(u01()) * mean
# }



# static PyObject *
# di_di(PyObject * self, PyObject * args)
# {
#     PyObject * obj
#     if (!PyArg_ParseTuple(args, "l:di", & obj))
#     return NULL

#     Py_INCREF(obj)
#     return obj
# }


def main():

    # sem1 = semaphore()
    # for i in range(20):
    #     print(sem1.value)
    #     sem1.turn_ligth()

    # sim = Sim(1000)

    # so1 = sim_obj()
    # se1 = sim_event(so1, 10)
    # se2 = sim_event(None, 12)

    # sim.new_event(se1)
    # sim.new_event(se2)

    # while sim.pop_event() != None:
    #     # print(sim.event)

    #     sim_obj.process(sim.event.obj)
    #     # sim.event.object_id.process()



    return None

if __name__ == "__main__":
    main()
