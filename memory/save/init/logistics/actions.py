import py_trees
from py_trees import common


class GrabPackage(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(GrabPackage, self).__init__(name)

    def update(self) -> common.Status:
        print("GrabPackage")
        return py_trees.common.Status.SUCCESS


class RoutePlan(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(RoutePlan, self).__init__(name)

    def update(self) -> common.Status:
        print("RoutePlan")
        return py_trees.common.Status.SUCCESS


class MovingPackage(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(MovingPackage, self).__init__(name)

    def update(self) -> common.Status:
        print("MovingPackage")
        return py_trees.common.Status.SUCCESS


class PlacePackage(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(PlacePackage, self).__init__(name)

    def update(self) -> common.Status:
        print("PlacePackage")
        return py_trees.common.Status.SUCCESS


class InterruptOperation(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(InterruptOperation, self).__init__(name)

    def update(self) -> common.Status:
        print("InterruptOperation")
        return py_trees.common.Status.SUCCESS


class NotificationException(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(NotificationException, self).__init__(name)

    def update(self) -> common.Status:
        print("NotificationException")
        return py_trees.common.Status.SUCCESS

