from disambiguator.status import *


class BtMessage:
    def __init__(self, code=Status.OK.value, info=status_info[Status.OK],
                 error_count=0, use_llm=True, instruction=None,
                 bt=None, cur_bt=None, main_bt=None,
                 split_instruction=None, split_instruction_type=None, split_instruction_embedding=None,
                 intents=None, pattern=None, bt_list=None,
                 steps=None, step=None, bt_lists=None,
                 unambiguous_infos=None, ambiguous_infos=None,
                 reuse_infos=None, controller_infos=None, condition_infos=None, action_infos=None):
        self.code = code  # "current state"
        self.info = info  # necessary "feedback"
        self.error_count = error_count  # "accumulation" of the necessary feedback
        self.use_llm = use_llm  # whether to use large language model

        self.instruction = instruction  # user input task description
        self.bt = bt  # the BT of instruction
        self.split_instruction = split_instruction  # split text of instruction
        self.split_instruction_type = split_instruction_type  # current split_instruction's level(-1 1 2 3 4)
        self.split_instruction_embedding = split_instruction_embedding  # embedding of the split_instruction
        self.cur_bt = cur_bt  # the BT of split_instruction
        self.main_bt = main_bt  # the finally BT of the online running

        self.intents = intents  # current split_instruction's intents in instruction
        self.pattern = pattern  # pattern of split_instruction
        self.bt_list = bt_list  # bt_list of split_instruction

        self.steps = steps  # steps of split_instruction
        self.step = step  # current step from steps
        self.bt_lists = bt_lists  # bt_lists of steps

        self.unambiguous_infos = unambiguous_infos
        self.ambiguous_infos = ambiguous_infos
        self.reuse_infos = reuse_infos
        self.controller_infos = controller_infos
        self.condition_infos = condition_infos
        self.action_infos = action_infos
