from mapper.message import BtMessage
from disambiguator.status import status_info, Status
from nlp.parser import get_seg_model, judge_ambiguity, get_embedding
from builder.builder import parse_bt_list
from combiner.combiner import combine_bts, combine_between_bts


def instruction2bt(message):
    """
    Main method: Get a BT based on the user input.
    :param message: (code, info, error_count, use_llm, instruction,
                    bt, cur_bt, main_bt,
                    split_instruction, level,
                    intents, pattern, bt_list,
                    step, steps, bt_lists,
                    unambiguous_infos, ambiguous_infos
                    reuse_infos, controller_infos, condition_infos, action_infos)
    :return: message contains main_bt
    """
    # safety verification
    if message is None or not isinstance(message, BtMessage) or message.instruction is None or len(message.instruction) == 0:
        message.code = Status.ERROR_NO_INSTRUCTION.value
        message.info = "<< ERROR >> " + status_info[Status.ERROR_NO_INSTRUCTION]
        print("ERROR: NO_INSTRUCTION  " + status_info[Status.ERROR_NO_INSTRUCTION])
        return message
    # STEP 1 Split sentence(simple)
    message.instruction = message.instruction.lower().strip(",.;'!? ，。；“”'！？")
    model = get_seg_model(message.instruction)
    nlp = model(message.instruction)
    for split_instruction in nlp.sents:
        split_instruction = split_instruction.text.lower().strip(",.;'!? ，。；“”'！？")
        message.split_instruction = split_instruction
        message.split_instruction_embedding = get_embedding(split_instruction)
        # message.info += "CURRENT SENT: " + str(message.split_instruction) + ": "
        print("### CURRENT SENT: " + message.split_instruction)
        # STEP 2: Sentence Ambiguity analysis NOTE: 模型优化
        message.split_instruction_type = judge_ambiguity(message.split_instruction)
        print("### SPLIT INSTRUCTION TYPE: " + str(message.split_instruction_type))
        # STEP 3: Parse BT LIST from instruction
        message = parse_bt_list(message)
        if message.split_instruction_type != 3:
            if message.bt_list is None or len(message.bt_list) == 0:
                message.error_count += 1
                message.info += "\n<< Error " + str(message.error_count) + " >> " + status_info[Status.ERROR_NO_BT_LIST]
                print("BT_LIST ERROR: " + status_info[Status.ERROR_NO_BT_LIST])
                continue
            # message.info += "BT_LIST(" + str(len(message.bt_list)) + "): " + str(message.bt_list)
            print("### BT_LIST(" + str(len(message.bt_list)) + "): " + str(message.bt_list))
        else:
            if message.bt_lists is None or len(message.bt_lists) == 0:
                message.error_count += 1
                message.info += "\n<< Error " + str(message.error_count) + " >> " + status_info[Status.ERROR_NO_BT_LISTS]
                print("BT_LISTS ERROR: " + status_info[Status.ERROR_NO_BT_LISTS])
                continue
            # message.info += "\nBT_LISTS(" + str(len(message.bt_lists)) + "): " + str(message.bt_lists)
            print("### BT_LISTS(" + str(len(message.bt_lists)) + "): " + str(message.bt_lists))
        # STEP 4: Get CUR_BT
        message = combine_bts(message)
        if message.cur_bt is None:
            message.error_count += 1
            message.info += "\n<< Error " + str(message.error_count) + " >>CUR_BT " + status_info[Status.ERROR_NO_BT]
            print("CUR_BT ERROR: " + status_info[Status.ERROR_NO_BT])
            continue
        # STEP 5: Get Inner_loop BT
        if message.bt is None:
            message.bt = message.cur_bt
        else:
            message = combine_between_bts(message, 1)

    if message.bt is None:
        message.code = Status.ERROR_NO_BT.value
        message.error_count += 1
        message.info += "\n<< Error " + str(message.error_count) + " >>INSTRUCTION BT: " + status_info[Status.ERROR_NO_BT]
        return message
    # STEP 6: Get Outer_loop BT NOTE: 1 到底是最原有的主行为树进行增删改查，还是执行另一个行为树 2 指令输入相同的命令时，进行用户输入重复校验
    if message.main_bt is None:
        message.main_bt = message.bt
        message.info = "SUCCESS"
        return message
    else:
        message = combine_between_bts(message, 2)
        if message.main_bt is None:
            message.error_count += 1
            message.info += "\n<< Error " + str(message.error_count) + " >>MAIN_BT " + status_info[Status.ERROR_NO_BT]
            print("MAIN_BT ERROR: " + status_info[Status.ERROR_NO_BT])
            return message
        message.info = "SUCCESS"
        return message

