import os
import sys
import random
from math import log

import matplotlib.pyplot as plt


#sys.path.append('')

from sim import Color, semaphore
from sim import Sim as simulation

# simulation_time = 360
simulation_time = 3600

change_state_time = 0

simul = simulation(simulation_time)

class queue():
    def __init__(self):
        self.size = 0
        self.time = []
        self.vals = []

    def add(self, time):
        self.size += 1
        self.vals.append(self.size)
        self.time.append(time)

    def sub(self, time):
        if self.size > 0:
            self.size -= 1
            self.vals.append(self.size)
            self.time.append(time)

    def free(self, time):
        self.size = 0
        self.vals.append(self.size)
        self.time.append(time)

car_queue = queue()
man_queue = queue()

def exp_generator(mean):
    return -log(1 - random.random()) * mean


class semaphore_w_button():
    def __init__(self):
        self.button_active = False

        self.car_sem = semaphore(start_color= Color.RED)
        self.people_sem = semaphore(start_color=Color.RED)
        self.press_button_event = None
        self.change_state_time = 0

        self.car_pass_generator = None

    def press_button(self):
        print("press_button")
        if self.button_active == False:
            raise BaseException
        simul.new_event(self.allow_people_pass, 10)
        # create event через 10 с движение автомобилей запрещается
        pass

    def allow_people_pass(self):
        print("allow_people_pass")
        self.button_active = False

        # print("", self.car_sem.value)
        if self.car_sem.value == Color.GREEN:
            self.car_sem.turn_ligth()
        self.people_sem.turn_ligth()

        global man_queue
        man_queue.free(simul.time)

        simul.new_event(self.deprecate_people_pass, 7)
        simul.new_event(self.allow_car_pass, 10)

        # create event after 10s to deprecate

    def deprecate_people_pass(self):
        print("deprecate_people_pass")
        # self.people_sem.value == Color.RED
        self.people_sem.turn_ligth()
        if self.people_sem.value == Color.GREEN:
            raise BaseException

    def allow_car_pass(self):
        print("allow_car_pass")

        if self.people_sem.value == Color.GREEN:
            raise BaseException

        self.car_sem.value = Color.GREEN

        global change_state_time
        change_state_time = simul.time

        # need to activate car pass generator here
        print("self.car_pass_generator", self.car_pass_generator)
        self.car_pass_generator()

sem = semaphore_w_button()

def car_generator():
    simul.new_event(car_generator, exp_generator(60. / 25.))
    # print("car_generator")
    global car_queue
    car_queue.add(simul.time)
    # print("car_queue_size", car_queue.size)


def car_generator_pass():
    if sem.car_sem.value != Color.GREEN:
        print("sem disabled!!!!")
        return

    print("car_generator_pass")
    if simul.time - change_state_time > 10:
        mean = 60. / 50.
    else:
        mean = 60. / 10.

    global car_queue
    car_queue.sub(simul.time)
    # print("car_queue_size", car_queue.size)

    simul.new_event(car_generator_pass, exp_generator(mean))


sem.car_pass_generator = car_generator_pass


def people_generator():
    print("people_generator")
    simul.new_event(people_generator, exp_generator(60. / 2.))

    if sem.button_active == False:
        sem.button_active = True
        sem.press_button()

    global man_queue
    man_queue.add(simul.time)
    # print("people_queue_size", man_queue.size)


def main():
    # simul.new_event(sem.allow_people_pass, 0)
    car_generator()
    people_generator()

    sem.allow_car_pass()
    # car_generator_pass()

    while simul.pop_event() != None:
        if simul.time > simul.sim_time:
            # print("done")
            break

        print("time:", simul.time)
        simul.event.action()

    fig, axes = plt.subplots(2, 1, figsize=(12, 9), sharex=True)
    fig.set_dpi(100)
    axes[0].plot(car_queue.time, car_queue.vals, linewidth=2.0, linestyle="-")
    axes[0].set_xlabel("time", fontsize=16)
    axes[0].set_ylabel("car queue size", fontsize=16)
    axes[0].grid()

    axes[1].plot(man_queue.time, man_queue.vals, linewidth=2.0, linestyle="-")
    axes[1].set_xlabel("time", fontsize=16)
    axes[1].set_ylabel("man queue", fontsize=16)
    axes[1].grid()

    # plt.plot(car_queue.time, car_queue.vals, linewidth=2.0, linestyle="-")
    # plt.plot(man_queue.time, man_queue.vals, linewidth=2.0, linestyle="-")
    # plt.xlabel('time')
    # plt.ylabel('queue size')
    # plt.grid(True)
    # plt.title('voltage (mV) vs. time (sec)')
    # plt.savefig("plot-voltage-vs.-time.png")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
