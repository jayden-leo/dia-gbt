import py_trees
from py_trees import common


class NavigateToArea(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(NavigateToArea, self).__init__(name)

    def update(self) -> common.Status:
        print("NavigateToArea")
        return py_trees.common.Status.SUCCESS


class UseCleaningTools(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(UseCleaningTools, self).__init__(name)

    def update(self) -> common.Status:
        print("UseCleaningTools")
        return py_trees.common.Status.SUCCESS


class CleanArea(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(CleanArea, self).__init__(name)

    def update(self) -> common.Status:
        print("CleanArea")
        return py_trees.common.Status.SUCCESS


class CheckCleanliness(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(CheckCleanliness, self).__init__(name)

    def update(self) -> common.Status:
        print("CheckCleanliness")
        return py_trees.common.Status.SUCCESS


class InterruptOperation(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(InterruptOperation, self).__init__(name)

    def update(self) -> common.Status:
        print("InterruptOperation")
        return py_trees.common.Status.SUCCESS


class RequestHelp(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(RequestHelp, self).__init__(name)

    def update(self) -> common.Status:
        print("RequestHelp")
        return py_trees.common.Status.SUCCESS

