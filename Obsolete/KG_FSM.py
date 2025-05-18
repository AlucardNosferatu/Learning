import time

from state_machine import *
import numpy as np
import random


def fake_results():
    ids = []
    rel_ids = []
    for i in range(5):
        a = np.random.randint(0, 9)
        while a in rel_ids:
            a = np.random.randint(0, 9)
        rel_ids.append(a)
    for i in range(10):
        a = np.random.randint(0, 200)
        while a in ids:
            a = np.random.randint(0, 200)
        ids.append(a)
    relationships = []
    for i in range(30):
        a = 0
        b = 0
        c = 0
        while [a, b, c] in relationships or a == c:
            a = random.choice(ids)
            b = random.choice(rel_ids)
            c = random.choice(ids)
        relationships.append([a, b, c])
    return relationships, ids, rel_ids


@acts_as_state_machine
class Person:
    name = 'Billy'

    sleeping = State(initial=True)
    running = State()
    cleaning = State()

    run = Event(from_states=sleeping, to_state=running)
    cleanup = Event(from_states=running, to_state=cleaning)
    sleep = Event(from_states=(running, cleaning), to_state=sleeping)

    @before('sleep')
    def do_one_thing(self):
        print("{} is sleepy".format(self.name))

    @before('sleep')
    def do_another_thing(self):
        print("{} is REALLY sleepy".format(self.name))

    @after('sleep')
    def snore(self):
        print("Zzzzzzzzzzzz")

    @after('sleep')
    def big_snore(self):
        print("Zzzzzzzzzzzzzzzzzzzzzz")


def test_billy():
    person = Person()
    print(person.current_state == Person.sleeping)  # True
    print(person.is_sleeping)  # True
    print(person.is_running)  # False
    person.run()
    print(person.is_running)  # True
    person.sleep()

    # Billy is sleepy
    # Billy is REALLY sleepy
    # Zzzzzzzzzzzz
    # Zzzzzzzzzzzzzzzzzzzzzz

    print(person.is_sleeping)  # True


def parse_rel_ids(rels, mode):
    if 'on_dst' in mode:
        rel_ids = []
        for rel in rels:
            a, b, c = rel
            if 'on_rel' in mode:
                # rel和dst都相同的才合并
                temp = [b, c]
            else:
                # 只根据dst相同的合并不同rel
                temp = [c]
            if temp not in rel_ids:
                rel_ids.append(temp)
        return rel_ids
    else:
        # 完全不合并
        return rels


class GBody:
    states = []
    events = []
    initial_state = State(initial=True)
    name = ''
    ids = []
    rels = []
    rel_ids = []

    def __init__(self, name, rels, ids, mode=None):
        self.ids = ids
        self.rels = rels

        if mode is None:
            mode = ['on_dst']
        self.name = name
        for id in ids:
            state = State()
            self.states.append(state)
        rel_ids = parse_rel_ids(rels, mode)
        self.rel_ids = rel_ids
        for rel_id in rel_ids:
            t_state = self.states[ids.index(rel_id[-1])]
            f_states = [self.initial_state]
            for rel in rels:
                start_i = len(rel) - len(rel_id)
                if rel[start_i:] == rel_id:
                    f_states.append(self.states[ids.index(rel[0])])
            event = Event(from_states=tuple(f_states), to_state=t_state)
            self.events.append(event)


def build_class_str(GBInstance):
    class_head = """
@acts_as_state_machine
class {}:
    name = '{}'
        """.format(
        'GBInterface',
        GBInstance.name
    )

    class_initial_state = """
    {} = {}.initial_state
        """.format(
        's0',
        'GWilliam'
    )

    class_states = class_initial_state
    for i in range(len(GBInstance.states)):
        class_state = """
    {} = {}.states[{}]
            """.format(
            's{}'.format(i + 1),
            'GWilliam',
            i
        )
        class_states += class_state

    class_events = ''
    for i in range(len(GBInstance.events)):
        class_event = """
    {} = {}.events[{}]
            """.format(
            'e{}'.format(i),
            'GWilliam',
            i
        )
        class_events += class_event

    event_annotations = ''
    for i in range(len(GBInstance.events)):
        event_annotation = """
    @before('{}')
    def before_{}(self):
        print("before_{}")

    @after('{}')
    def after_{}(self):
        print("after_{}")
            """.format(
            'e{}'.format(i),
            'e{}'.format(i),
            'e{}'.format(i),
            'e{}'.format(i),
            'e{}'.format(i),
            'e{}'.format(i)
        )
        event_annotations += event_annotation
    class_str = class_head + class_states + class_events + event_annotations
    return class_str, 'GBInterface'


def build_class_imp(GBInstance):
    class_str, imp_name = build_class_str(GBInstance=GBInstance)
    exec(class_str)
    class_new = eval(imp_name)
    return class_new


def test_invalid_transition(GBInstance, GIInstance):
    obj_name = 'GIInstance'
    local_vars = locals().copy()
    for k, v in local_vars.items():
        if v is GIInstance:
            obj_name = k
            break
    event_index = 0
    while True:
        try:
            event_index = random.randint(0, len(GBInstance.events) - 1)
            exec('{}.e{}()'.format(obj_name, event_index))
        except InvalidStateTransition:
            print('This event does not alter current state.')
            print('Event Index:', event_index, 'Event ID:', GBInstance.rel_ids[event_index])
            state_str = eval('{}.current_state'.format(obj_name))
            print('State Index:', state_str, 'State ID:', GBInstance.ids[int(state_str.replace('s', '')) - 1])
            time.sleep(1)


if __name__ == "__main__":
    rels, ids, rel_ids = fake_results()
    GWilliam = GBody('William', rels, ids)
    class_new = build_class_imp(GWilliam)
    GMonster = class_new()
    test_invalid_transition(GWilliam, GMonster)
    print('Done')
