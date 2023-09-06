from nlp.preprocessor import pre_process
from mapper.mapper import instruction2bt
from mapper.message import BtMessage
from mapper.utils import save_bt
from disambiguator.status import Status
from third_party.py_trees import py_trees
from config import dirs_tasks_reuse

if __name__ == '__main__':
    unambiguous_infos, ambiguous_infos, reuse_infos, controller_infos, condition_infos, action_infos = pre_process()
    # TODO: level 1
    instruction = "Create a sequence node with child nodes correct_positioning and check_assembly."
    # TODO: level 2
    # instruction = "Grab and position the parts, then start the assembly process."
    # instruction = "Interrupt the assembly if the environment is unsafe, otherwise assemble the parts and check the quality."
    # instruction = "Get the necessary workpiece, position it correctly, and then assemble it."
    # instruction = "move the package to the specified location and confirm the environment is safe before placing it down."
    # LLM mark_intents: (move the package to the specified location) and (confirm the environment is safe) before (placing it down)
    # TODO: level 3
    # instruction = "Execution task: Assemble the workpiece with high precision and quality."
    message = BtMessage(instruction=instruction, use_llm=True,
                        unambiguous_infos=unambiguous_infos, ambiguous_infos=ambiguous_infos,
                        reuse_infos=reuse_infos, controller_infos=controller_infos,
                        condition_infos=condition_infos, action_infos=action_infos)
    message = instruction2bt(message)
    if message.code == Status.OK.value:
        print(message.info)
        print(py_trees.display.unicode_tree(message.main_bt))  # 打印行为树
        # temp save
        save_bt(message)
        # reuse save
        # reuse_name = "correct positioning and check assembly".replace(" ", "_")
        # save_bt(message, reuse_name, dirs_tasks_reuse + reuse_name + ".xml")
