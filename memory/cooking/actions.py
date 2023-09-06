import py_trees
from py_trees import common


class PrepareFood(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(PrepareFood, self).__init__(name)

    def update(self) -> common.Status:
        print("PrepareFood")
        return py_trees.common.Status.SUCCESS


class UseCookingTools(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(UseCookingTools, self).__init__(name)

    def update(self) -> common.Status:
        print("UseCookingTools")
        return py_trees.common.Status.SUCCESS


class ExecutionSteps(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(ExecutionSteps, self).__init__(name)

    def update(self) -> common.Status:
        print("ExecutionSteps")
        return py_trees.common.Status.SUCCESS


class FinishCooking(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(FinishCooking, self).__init__(name)

    def update(self) -> common.Status:
        print("FinishCooking")
        return py_trees.common.Status.SUCCESS


class InterruptOperation(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(InterruptOperation, self).__init__(name)

    def update(self) -> common.Status:
        print("InterruptOperation")
        return py_trees.common.Status.SUCCESS


class RequestIntervention(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(RequestIntervention, self).__init__(name)

    def update(self) -> common.Status:
        print("RequestIntervention")
        return py_trees.common.Status.SUCCESS

