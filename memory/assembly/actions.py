import py_trees
from py_trees import common


class GrabPart(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(GrabPart, self).__init__(name)

    def update(self) -> common.Status:
        print("GrabPart")
        return py_trees.common.Status.SUCCESS


class PositioningPart(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(PositioningPart, self).__init__(name)

    def update(self) -> common.Status:
        print("PositioningPart")
        return py_trees.common.Status.SUCCESS


class Assembly(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(Assembly, self).__init__(name)

    def update(self) -> common.Status:
        print("Assembly")
        return py_trees.common.Status.SUCCESS


class CheckAssembly(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(CheckAssembly, self).__init__(name)

    def update(self) -> common.Status:
        print("CheckAssembly")
        return py_trees.common.Status.SUCCESS


class InterruptAssembly(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(InterruptAssembly, self).__init__(name)

    def update(self) -> common.Status:
        print("InterruptAssembly")
        return py_trees.common.Status.SUCCESS


class RequestHelp(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(RequestHelp, self).__init__(name)

    def update(self) -> common.Status:
        print("RequestHelp")
        return py_trees.common.Status.SUCCESS

