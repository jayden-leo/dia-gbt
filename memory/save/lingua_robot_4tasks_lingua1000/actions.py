import py_trees
from py_trees import common


class Bypass(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(Bypass, self).__init__(name)

    def update(self) -> common.Status:
        print("Bypass")
        return py_trees.common.Status.SUCCESS


class Charging(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(Charging, self).__init__(name)

    def update(self) -> common.Status:
        print("Charging")
        return py_trees.common.Status.SUCCESS


class Drop(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(Drop, self).__init__(name)

    def update(self) -> common.Status:
        print("Drop")
        return py_trees.common.Status.SUCCESS


class Grab(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(Grab, self).__init__(name)

    def update(self) -> common.Status:
        print("Grab")
        return py_trees.common.Status.SUCCESS


class MoveBack(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(MoveBack, self).__init__(name)

    def update(self) -> common.Status:
        print("MoveBack")
        return py_trees.common.Status.SUCCESS


class MoveForward(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(MoveForward, self).__init__(name)

    def update(self) -> common.Status:
        print("MoveForward")
        return py_trees.common.Status.SUCCESS


class MoveLeft(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(MoveLeft, self).__init__(name)

    def update(self) -> common.Status:
        print("MoveLeft")
        return py_trees.common.Status.SUCCESS


class MoveRight(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(MoveRight, self).__init__(name)

    def update(self) -> common.Status:
        print("MoveRight")
        return py_trees.common.Status.SUCCESS


class RequestHelp(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(RequestHelp, self).__init__(name)

    def update(self) -> common.Status:
        print("RequestHelp")
        return py_trees.common.Status.SUCCESS


class Rest(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(Rest, self).__init__(name)

    def update(self) -> common.Status:
        print("Rest")
        return py_trees.common.Status.SUCCESS


class Rotate(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(Rotate, self).__init__(name)

    def update(self) -> common.Status:
        print("Rotate")
        return py_trees.common.Status.SUCCESS


class Scanning(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(Scanning, self).__init__(name)

    def update(self) -> common.Status:
        print("Scanning")
        return py_trees.common.Status.SUCCESS
