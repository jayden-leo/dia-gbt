import py_trees
import random


class CleanAreaDetection(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(CleanAreaDetection, self).__init__(name)

    def update(self):
        if clean_area_detection_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def clean_area_detection_impl():
    # 在这里编写检查条件的代码
    print("clean_area_detection_impl")
    random_number = random.uniform(0, 1)
    if random_number < 0.5:
        return False
    return True


class CleaningToolDetection(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(CleaningToolDetection, self).__init__(name)

    def update(self):
        if cleaning_tool_detection_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def cleaning_tool_detection_impl():
    # 在这里编写检查条件的代码
    print("cleaning_tool_detection_impl")
    random_number = random.uniform(0, 1)
    if random_number < 0.5:
        return False
    return True


class Cleanliness(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(Cleanliness, self).__init__(name)

    def update(self):
        if cleanliness_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def cleanliness_impl():
    # 在这里编写检查条件的代码
    print("cleanliness_impl")
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
