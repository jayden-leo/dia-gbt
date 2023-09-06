from mapper.utils import create_bt
from disambiguator.status import status_info, Status
from combiner.utils import Combiner


def combine_bt_list(message):
    """
    parse the "cur_bt" from bt_list or bt_lists
    :param message: (code, info, error_count, use_llm, instruction,
                    bt, cur_bt, main_bt,
                    split_instruction, split_instruction_type,
                    intents, pattern, bt_list,
                    step, steps, bt_lists,
                    unambiguous_infos, ambiguous_infos
                    reuse_infos, controller_infos, condition_infos, action_infos)
    :return: message that containing cur_bt
    """
    if message.bt_list is None or len(message.bt_list) == 0: return message
    # STEP 1: bt_list quantity limit
    # NOTE: 最多8个节点，2个控制节点
    controller_count = 0
    for bt_node in message.bt_list:
        if bt_node["type"] == 1:
            controller_count += 1
    if controller_count == 0:
        message.bt_list.append({'name': "sequence", "type": 1})
    if controller_count > 2:
        print("BT_LIST TOO LARGE ERROR:" + status_info[Status.ERROR_TOO_LARGE_BT_LIST])
        return message
    if len(message.bt_list) > 8:
        message.bt_list = message.bt_list[-8:]
    print("### COMBINE BT_LIST("+str(len(message.bt_list))+"): " + str(message.bt_list))
    # STEP 2: Traverse "bt_list" and select the "BT" that best matches the instruction
    most_similar_bt, bt_count = Combiner().combine(message)
    print("### BT COMBINE COUNTS: " + str(bt_count))
    message.cur_bt = most_similar_bt
    return message


def combiner_bt_lists(message):
    """
    parse the "cur_bt" from bt_list or bt_lists
    :param message: (code, info, error_count, use_llm, instruction,
                    bt, cur_bt, main_bt,
                    split_instruction, split_instruction_type,
                    intents, pattern, bt_list,
                    step, steps, bt_lists,
                    unambiguous_infos, ambiguous_infos
                    reuse_infos, controller_infos, condition_infos, action_infos)
    :return: message that containing cur_bt
    """
    if message.bt_lists is None or len(message.bt_lists) == 0: return message
    root_node = create_bt("sequence")
    for bt_list in message.bt_lists:
        if bt_list is None or len(bt_list) == 0:
            continue
        # Only one bt
        if len(bt_list) == 1:
            root_node.add_child(create_bt(bt_list[0]['name']))
        else:
            message = combine_bt_list(message)
            if message.cur_bt is not None:
                try:
                    root_node.add_child(message.cur_bt)
                except Exception as e:
                    print("ERROR: ADD CHILD FAILED : " + str(e))
    message.cur_bt = root_node
    return message


def combine_bts(message):
    """
    parse the "cur_bt" from bt_list or bt_lists
    :param message: (code, info, error_count, use_llm, instruction,
                    bt, cur_bt, main_bt,
                    split_instruction, split_instruction_type,
                    intents, pattern, bt_list,
                    step, steps, bt_lists,
                    unambiguous_infos, ambiguous_infos
                    reuse_infos, controller_infos, condition_infos, action_infos)
    :return: message that containing cur_bt
    """
    if message.split_instruction_type != 3:
        return combine_bt_list(message)
    else:
        return combiner_bt_lists(message)


def combine_inner_loop(message):
    message.bt = message.cur_bt
    return message


def combine_outer_loop(message):
    message.main_bt = message.bt
    return message


def combine_between_bts(message, loop_type):
    if loop_type == 1:
        return combine_inner_loop(message)
    elif loop_type == 2:
        return combine_outer_loop(message)
    else:
        print("LOOP TYPE is ERROR!!")
        return message
