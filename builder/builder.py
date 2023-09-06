import jieba
import re
from mapper.utils import find_bt
from disambiguator.status import status_info, Status
from builder.utils import parse_intents, save_intent, ambiguous2unambiguous
from nlp import prompt, openai


def parse_bt_desc(message):
    """
    parse the "bt_list" from each split_instruction
    message: (code, info, error_count, use_llm,
              instruction, bt, cur_bt, main_bt,
              split_instruction, split_instruction_type, split_instruction_embedding,
              intents, pattern, bt_list,
              steps, step, bt_lists,
              unambiguous_infos, ambiguous_infos,
              reuse_infos, controller_infos, condition_infos, action_infos)
    """
    # STEP 1: Jieba participle. At this point the participle has been optimized for local adaptation
    words = jieba.cut(message.split_instruction, cut_all=False)
    bt_list = []
    for word in words:
        # filter
        if word is None or len(word) == 0 or bool(re.match(r'^[\s\W]+$', word)): continue
        # STEP 2: Find "bt node" in memory
        node_name, node_type = find_bt(word, message)
        # STEP 3: Add bt_info into "bt_list"
        if node_name is not None or node_type != -1:
            bt_info = {"name": node_name, "type": node_type}
            bt_list.append(bt_info)
    if bt_list is not None and len(bt_list) > 0:
        message.bt_list = bt_list
    return message


def parse_unambiguous_desc(message):
    """
    parse the "bt_list" from each split_instruction
    message: (code, info, error_count, use_llm,
              instruction, bt, cur_bt, main_bt,
              split_instruction, split_instruction_type, split_instruction_embedding,
              intents, pattern, bt_list,
              steps, step, bt_lists,
              unambiguous_infos, ambiguous_infos,
              reuse_infos, controller_infos, condition_infos, action_infos)
    """
    bt_list = []
    # STEP 1: Get "intents"
    message = parse_intents(message)
    if message.intents is None or len(message.intents) == 0:
        message.error_count += 1
        message.info += "\n<< Error " + str(message.error_count) + " >> " + status_info[Status.ERROR_NO_INTENTS]
        print("INTENTS ERROR: " + status_info[Status.ERROR_NO_INTENTS])
        return message
    # message.info += "INTENTS: " + str(message.intents)
    print("### INTENTS: " + str(message.intents))
    # STEP 2: Get "bt_list"
    for intent in message.intents:
        intent = intent.lower().strip(",.;'!? ，。；“”'！？")
        node_name, node_type = find_bt(intent, message)
        if node_name is not None and node_type != -1:
            bt_info = {"name": node_name, "type": node_type}
            bt_list.append(bt_info)
        # STEP 3: Use LLM parse "bt name" from intent
        elif message.use_llm:
            prompt_intent2bt = prompt.get_intent2bt(intent, message)
            llm_result = openai.get_completion(prompt_intent2bt)
            if status_info[Status.ERROR_LLM] in llm_result:
                print("LLM ERROR: " + llm_result)
                continue
            if "None" in llm_result:
                print("LLM judges there is no matching BT about '" + intent + "'")
                continue
            print("### ### LLM judges match '" + intent + "' : " + llm_result)
            node_name, node_type = find_bt(llm_result, message)
            if node_name is None and node_type == -1:
                print("LLM ANSWER ERROR:  '" + intent + "' as " + llm_result + " not in memory!")
                continue
            print("### LLM PARSE INTENT SUCCESS: '" + intent + "' : " + llm_result)
            bt_info = {"name": node_name, "type": node_type}
            bt_list.append(bt_info)
            # STEP 4: Reuse the bt_desc as synonyms or pattern
            save_intent(intent, node_name, node_type, message)
        else:
            print("ERROR: Parse '" + intent + "' to bt_node fail! You can use LLM to parse!")
    message.bt_list = bt_list
    return message


def parse_ambiguous_desc(message):
    """
    parse the "bt_lists" from each split_instruction
    :param message: (code, info, error_count, use_llm, instruction,
                    bt, cur_bt, main_bt,
                    split_instruction, split_instruction_type,
                    intents, pattern, bt_list,
                    step, steps, bt_lists,
                    unambiguous_infos, ambiguous_infos
                    reuse_infos, controller_infos, condition_infos, action_infos)
    :return: message that containing bt_lists
    """
    # STEP 1: Ambiguous To Unambiguous
    message = ambiguous2unambiguous(message)
    if message.steps is None or len(message.steps) == 0:
        message.error_count += 1
        message.info += "\n<< Error " + str(message.error_count) + " >> " + status_info[Status.ERROR_NO_STEPS]
        print("STEPS ERROR: " + status_info[Status.ERROR_NO_STEPS])
        return message
    # message.info += "\nSTEPS: " + str(message.steps)
    print("### STEPS: " + str(message.steps))
    message.bt_lists = []
    last_steps = []
    # STEP 2: Convenience for every Step
    for step in message.steps:  # NOTE: step 有可能是列表, 如果step的数量大于4个词，说明是一句话，调用无歧义解析函数
        if isinstance(step, list):
            continue
        node_name, node_type = find_bt(str(step), message)
        if node_name is not None and node_type != -1:
            message.bt_list = [{"name": node_name, "type": node_type}]
            message.bt_lists.append(message.bt_list)
            last_steps.append(str(step))
            continue
        # STEP 3: Use LLM parse "bt name" from intent
        if message.use_llm:
            prompt_intent2bt = prompt.get_intent2bt(str(step), message)
            llm_result = openai.get_completion(prompt_intent2bt)
            if status_info[Status.ERROR_LLM] in llm_result:
                print("LLM ERROR: " + llm_result)
                continue
            if "None" in llm_result:
                print("LLM judges there is no matching STEP about '" + str(step) + "'")
                continue
            print("### ### LLM judges STEP '" + str(step) + "' : " + llm_result)
            node_name, node_type = find_bt(llm_result, message)
            if node_name is None and node_type == -1:
                print("LLM ANSWER ERROR:  '" + str(step) + "' as " + llm_result + " not in memory!")
                continue
            print("### LLM PARSE STEP SUCCESS: '" + str(step) + "' : " + llm_result)
            message.bt_list = [{"name": node_name, "type": node_type}]
            message.bt_lists.append(message.bt_list)
            last_steps.append(str(step))
            # STEP 4: Reuse the bt_desc as synonyms or pattern
            save_intent(str(step), node_name, node_type, message)
        else:
            print("ERROR: Parse '" + str(step) + "' to bt_node fail! You can use LLM to parse!")
    message.steps = last_steps
    return message


def parse_bt_list(message):
    """
    parse the "bt_list" from each split_instruction
    message: (code, info, error_count, use_llm,
              instruction, bt, cur_bt, main_bt,
              split_instruction, split_instruction_type, split_instruction_embedding,
              intents, pattern, bt_list,
              steps, step, bt_lists,
              unambiguous_infos, ambiguous_infos,
              reuse_infos, controller_infos, condition_infos, action_infos)
    """
    if message.split_instruction_type == 1:
        return parse_bt_desc(message)
    elif message.split_instruction_type == 2:
        return parse_unambiguous_desc(message)
    else:
        return parse_ambiguous_desc(message)
