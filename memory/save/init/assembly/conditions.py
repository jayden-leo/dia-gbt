import py_trees
import random


class PartDetection(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(PartDetection, self).__init__(name)

    def update(self):
        if parts_detection_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def parts_detection_impl():
    # 在这里编写检查条件的代码
    print("parts_detection_impl")
    random_number = random.uniform(0, 1)
    if random_number < 0.5:
        return False
    return True


class CorrectPositioning(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(CorrectPositioning, self).__init__(name)

    def update(self):
        if correct_positioning_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def correct_positioning_impl():
    # 在这里编写检查条件的代码
    print("correct_positioning_impl")
    random_number = random.uniform(0, 1)
    if random_number < 0.5:
        return False
    return True


class PartStatus(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(PartStatus, self).__init__(name)

    def update(self):
        if part_status_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def part_status_impl():
    # 在这里编写检查条件的代码
    print("part_status_impl")
    random_number = random.uniform(0, 1)
    if random_number < 0.5:
        return False
    return True


class EnvsSafety(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(EnvsSafety, self).__init__(name)

    def update(self):
        if envs_safety_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def envs_safety_impl():
    # 在这里编写检查条件的代码
    print("envs_safety_impl")
    random_number = random.uniform(0, 1)
    if random_number < 0.5:
        return False
    return True
