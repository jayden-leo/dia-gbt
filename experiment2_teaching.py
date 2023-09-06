from nlp.preprocessor import pre_process
from mapper.mapper import instruction2bt
from mapper.utils import *
from mapper.message import BtMessage
from config import dirs_tasks_reuse
from disambiguator.status import status_info, Status
import py_trees
import os

if __name__ == '__main__':
    unambiguous_infos, ambiguous_infos, reuse_infos, controller_infos, condition_infos, action_infos = pre_process()
    # STEP 1：Interrupt the assembly if the environment is unsafe
    instruction = "Interrupt the assembly if the environment is unsafe."

    message = BtMessage(instruction=instruction, use_llm=True,
                        unambiguous_infos=unambiguous_infos, ambiguous_infos=ambiguous_infos,
                        controller_infos=controller_infos, condition_infos=condition_infos,action_infos=action_infos)
    message = instruction2bt(message)
    if message.code == Status.OK.value:
        print(message.info)
        print(py_trees.display.unicode_tree(message.bt))  # 打印行为树
        save_bt(message)
        py_trees.display.render_dot_tree(message.bt, name="temp", target_directory=dirs_tasks_reuse + "temp")
    else:
        print(message.info)

    # STEP 2：Check for obstacles while checking parts status
    instruction = "Check for obstacles while checking parts status"
    message.instruction = instruction
    message = instruction2bt(message)
    if message.code == Status.OK.value:
        print(message.info)
        print(py_trees.display.unicode_tree(message.bt))  # 打印行为树
        save_bt(message)
        py_trees.display.render_dot_tree(message.bt, name="temp", target_directory=dirs_tasks_reuse + "temp")
        # User command: reuse
        reuse_name = "check env safety".replace(" ", "_")
        # NOTE: 重用策略，命名，如何重用。 扩展同义词及其正则表达式
        dir_save_images = dirs_tasks_reuse + "images/" + reuse_name
        if not os.path.exists(dir_save_images):
            os.makedirs(dir_save_images)
        save_bt(message.bt, reuse_name, dirs_tasks_reuse + reuse_name + ".xml")
        py_trees.display.render_dot_tree(message.bt, name=reuse_name, target_directory=dir_save_images)
    else:
        print(message.info)

    # STEP 3：Interrupt the assembly if the environment is unsafe, otherwise assemble the parts and check the quality.
    instruction = "Interrupt the assembly if the environment is unsafe, otherwise assemble the parts and check the quality."
    message = BtMessage(instruction=instruction, use_llm=True)
    message = instruction2bt(message)
    if message.code == Status.OK.value:
        print(message.info)
        print(py_trees.display.unicode_tree(message.bt))  # 打印行为树
        save_bt(message)
        py_trees.display.render_dot_tree(message.bt, name="temp", target_directory=dirs_tasks_reuse + "temp")
    else:
        print(message.info)

