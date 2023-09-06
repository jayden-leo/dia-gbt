from nlp.parser import get_embedding, get_seg_model
import torch
import re
from nlp import prompt, openai
from disambiguator.status import status_info, Status
import xml.etree.ElementTree as ET
from config import dir_unambiguous_rules, dir_ambiguous_rules, dirs_tasks_reuse, dirs_controllers, dirs_conditions, dirs_actions
import ast


def build_pattern(mark_intents):
    last_pattern = ""
    inner_string = ""
    inner_pattern = ""
    bracket_flag = False
    VB_flag = False
    model = get_seg_model(mark_intents)
    doc = model(mark_intents)
    for word in doc:
        if word.text == "(":
            bracket_flag = True
            VB_flag = False
            inner_pattern = ""
            inner_string = ""
        elif word.text == ")":
            bracket_flag = False
            if VB_flag:
                last_pattern += inner_pattern.lower().strip(",.;!? ，。；！？") + ".*"
                inner_pattern = ""
                inner_string = ""
            else:
                last_pattern += inner_string.lower().strip(",.;!? ，。；！？")
                inner_pattern = ""
                inner_string = ""

        if bracket_flag:
            if "(" == word.text:
                inner_pattern += "("
                inner_string += "("
            elif "VB" in str(word.tag_):
                VB_flag = True
                inner_pattern += word.text + " "
            else:
                inner_string += word.text + " "
        else:
            if ")" == word.text:
                last_pattern += word.text
            else:
                last_pattern += word.text + " "
    last_pattern = "^" + last_pattern.lower().strip(",.;!? ，。；！？") + "$"
    return last_pattern


def extract_intents(text_intents):
    """
    (grab the package) and (mail it to the target location) (at the same time)
    ['grab the package', 'mail it to the target location', 'at the same time']
    """
    intents = []
    inner_string = ""
    bracket_flag = False
    model = get_seg_model(text_intents)
    doc = model(text_intents)
    for word in doc:
        if word.text == "(":
            bracket_flag = True
            continue
        elif word.text == ")":
            bracket_flag = False
            intents.append(inner_string.lower().strip(",.;!? ，。；！？"))
            inner_string = ""
        if bracket_flag:
            inner_string += word.text + " "
    return intents


def save_memory(intent, node_name, dirs):
    bt_file_path = dirs + node_name + ".xml"
    """
    infos[
    bt_info{
        'bt_name': xxx,
        'bt_name_embedding': xxx,
        'bt_explanation': xxx,
        'bt_explanation_embedding':xxx,
        'synonyms': [{'synonyms_name':xxx,'synonyms_embedding'xxx} * N ]
        'pattern':[ pattern1, pattern2 *N ]
    } * N ]
    """
    try:
        synonyms_xml = ET.Element("synonyms")
        synonyms_xml.text = intent
        # parse and find father element
        tree = ET.parse(bt_file_path)
        root = tree.getroot()[0]
        synonyms_elements = root.findall("synonyms")
        # insert before pattern according parent_node&pattern_node
        root.insert(synonyms_elements.index(synonyms_elements[-1]) + 1, synonyms_xml)
        tree.write(bt_file_path)
        print("### LLM INTENT SAVE SUCCESS: '" + intent + "'")
    except Exception as e:
        print("ERROR: " + str(e))


def save_intent(intent, node_name, node_type, message):
    """
    message: (code, info, error_count, use_llm, instruction,
            bt, cur_bt, main_bt,
            split_instruction, level,
            intents, pattern, bt_list,
            step, steps, bt_lists,
            unambiguous_infos, ambiguous_infos
            reuse_infos, controller_infos, condition_infos, action_infos)
    memory_infos[
        bt_info{
            'bt_name': xxx,
            'bt_name_embedding': xxx,
            'bt_explanation': xxx,
            'bt_explanation_embedding':xxx,
            'synonyms': [{'synonyms_name':xxx,'synonyms_embedding'xxx} * N ]
            'pattern':[ pattern1, pattern2 *N ]
        } * N ]
    """
    if node_type == 1:
        # save to memory
        save_memory(intent, node_name, dirs_controllers)
        # update memory infos
        for idx, info in enumerate(message.controller_infos):
            if info['bt_name'] == node_name:
                synonyms = {'synonyms_name': intent, 'synonyms_embedding': get_embedding(intent)}
                message.controller_infos[idx]['synonyms'].append(synonyms)
                break
    elif node_type == 2:
        # save to memory
        save_memory(intent, node_name, dirs_conditions)
        # update memory infos
        for idx, info in enumerate(message.condition_infos):
            if info['bt_name'] == node_name:
                synonyms = {'synonyms_name': intent, 'synonyms_embedding': get_embedding(intent)}
                message.condition_infos[idx]['synonyms'].append(synonyms)
                break
    elif node_type == 3:
        # save to memory
        save_memory(intent, node_name, dirs_actions)
        # update memory infos
        for idx, info in enumerate(message.action_infos):
            if info['bt_name'] == node_name:
                synonyms = {'synonyms_name': intent, 'synonyms_embedding': get_embedding(intent)}
                message.action_infos[idx]['synonyms'].append(synonyms)
                break
    elif node_type == 4:
        # save to memory
        save_memory(intent, node_name, dirs_tasks_reuse)
        # update memory infos
        for idx, info in enumerate(message.reuse_infos):
            if info['bt_name'] == node_name:
                synonyms = {'synonyms_name': intent, 'synonyms_embedding': get_embedding(intent)}
                message.reuse_infos[idx]['synonyms'].append(synonyms)
                break
    else:
        print("ERROR: node_name '" + node_name + "' is not a bt_name")


def save_ambiguous_rule(message):
    """
    {"instruction": instruction, "embedding": embedding, "steps": steps_info}
    """
    try:
        # save steps
        # build new rule xml
        rule_element = ET.Element('rule')
        instruction_element = ET.SubElement(rule_element, 'instruction')
        instruction_element.text = message.instruction
        steps_element = ET.SubElement(rule_element, 'steps')
        real_steps = []
        for step in message.steps:  # NOTE step 有可能是列表
            if isinstance(step, list):
                continue
            real_steps.append(step)
            step_element = ET.SubElement(steps_element, 'step')
            step_element.text = step
        # parse and find father element
        tree = ET.parse(dir_ambiguous_rules)
        parent_element = tree.getroot()
        parent_element.append(rule_element)
        tree.write(dir_ambiguous_rules)
        print("### SAVE STEPS SUCCESS: " + str(message.steps))
        info = {'instruction': message.instruction, 'embedding': get_embedding(message.instruction), 'steps': real_steps}
        # update memory infos
        message.ambiguous_infos.append(info)
    except Exception as e:
        print("ERROR: SAVE PATTERN FAIL " + str(e))


def save_unambiguous_rule(mark_intents, message):
    """
    save the "demo","intent","pattern" from each split_instruction
    :param mark_intents:
    :param message: (code, info, error_count, use_llm, instruction,
                    bt, cur_bt, main_bt,
                    split_instruction, level,
                    intents, pattern, bt_list,
                    step, steps, bt_lists,
                    unambiguous_infos, ambiguous_infos
                    reuse_infos, controller_infos, condition_infos, action_infos)
    :return: message that containing intents
    """
    try:
        # build new rule xml
        rule = ET.Element('rule')
        child_demo = ET.SubElement(rule, 'demo')
        child_intent = ET.SubElement(rule, 'intent')
        child_pattern = ET.SubElement(rule, 'pattern')
        child_demo.text = message.split_instruction
        child_intent.text = mark_intents
        child_pattern.text = message.pattern
        # parse and find father element
        tree = ET.parse(dir_unambiguous_rules)
        parent_element = tree.getroot()
        parent_element.append(rule)
        tree.write(dir_unambiguous_rules)
        message.unambiguous_infos.append({'demo': message.split_instruction,
                                          'embedding': get_embedding(message.split_instruction),
                                          'intent': mark_intents,
                                          'pattern': message.pattern})
        print("### SAVE PATTERN SUCCESS: " + message.pattern)
    except Exception as e:
        print("ERROR: SAVE PATTERN FAIL " + str(e))


def parse_intents(message):
    """
    parse the "bt_list" from each split_instruction
    message: (code, info, error_count, use_llm,
              instruction, bt, cur_bt, main_bt,
              split_instruction, split_instruction_type, split_instruction_embedding,
              intents, pattern, bt_list,
              steps, step, bt_lists,
              unambiguous_infos, ambiguous_infos,
              reuse_infos, controller_infos, condition_infos, action_infos)
    unambiguous_infos = [{'demo':string,
                          'embedding':[int_list],
                          'intent':string,
                          'pattern':string},
                         {},...]
    """
    # STEP 1: Match from unambiguous_infos
    if message.unambiguous_infos is not None and len(message.unambiguous_infos) != 0:
        try:
            for info in message.unambiguous_infos:
                if message.split_instruction == info['demo']:
                    print("### UNAMBIGUOUS RULES << demo >> MATCH ==> '" + message.split_instruction + "'")
                    intents = extract_intents(info['intent'])
                    message.intents = intents
                    return message
                if torch.cosine_similarity(info['embedding'], message.split_instruction_embedding) > 0.8:
                    print("### UNAMBIGUOUS RULES << embedding >> MATCH ==> '" + message.split_instruction + "'")
                    intents = extract_intents(info['intent'])
                    message.intents = intents
                    return message
                match = re.search(info['pattern'], message.split_instruction, re.IGNORECASE)
                if match:
                    intents = []
                    for part in match.groups():
                        intents.append(part)
                    print("### UNAMBIGUOUS RULES << pattern >> MATCH ==> '" + message.info['pattern'] + "'")
                    message.intents = intents
                    message.pattern = info['pattern']
                    return message
        except Exception as e:
            print("ERROR: " + str(e))

    # STEP 2: Match from LLM
    if not message.use_llm:
        return message
    prompt_mark_intents = prompt.mark_intents(message.split_instruction, message.unambiguous_infos)
    llm_result = openai.get_completion(prompt_mark_intents)
    if status_info[Status.ERROR_LLM] in llm_result:
        print("LLM ERROR: " + llm_result)
        return message
    mark_intents = llm_result.lower().strip(",.;'!? ，。；“”'！？")
    print("### LLM mark_intents: " + mark_intents)
    intents = extract_intents(mark_intents)
    message.intents = intents
    # STEP 3: Reuse the rule from LLM
    prompt_pattern = prompt.get_pattern(mark_intents, message.unambiguous_infos)
    llm_result = openai.get_completion(prompt_pattern)
    if status_info[Status.ERROR_LLM] in llm_result:
        print("LLM ERROR: " + llm_result)
        return message
    if llm_result is not None and llm_result != "" and re.match(llm_result, message.split_instruction, re.IGNORECASE):
        print("### LLM PATTERN Match SUCCESS: " + llm_result)
        message.pattern = llm_result
        save_unambiguous_rule(mark_intents, message)
        return message
    print("ERROR: pattern generated from LLM is not match!")
    custom_pattern = build_pattern(mark_intents)
    if custom_pattern is not None and custom_pattern != "" and re.match(custom_pattern, message.split_instruction, re.IGNORECASE):
        print("### CUSTOM PATTERN Match SUCCESS: " + custom_pattern)
        message.pattern = custom_pattern
        save_unambiguous_rule(mark_intents, message)
        return message
    print("ERROR: pattern generated from Custom is not match!")
    return message


def ambiguous2unambiguous(message):
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
    # STEP 1: Match from ambiguous_infos
    if message.ambiguous_infos is not None and len(message.ambiguous_infos) != 0:
        try:
            # {"instruction": instruction, "embedding": embedding, "steps": steps_info}
            for info in message.ambiguous_infos:
                if message.split_instruction == info['instruction']:
                    print("### AMBIGUOUS RULES << instruction >> MATCH ==> '" + message.split_instruction + "'")
                    steps = []
                    for step in info['steps']:
                        steps.append(step)
                    message.steps = steps
                    return message
                if torch.cosine_similarity(info['embedding'], message.split_instruction_embedding) > 0.85:
                    print("### AMBIGUOUS RULES << embedding >> MATCH ==> '" + message.split_instruction + "'")
                    steps = []
                    for step in info['steps']:
                        steps.append(step)
                    message.steps = steps
                    return message
        except Exception as e:
            print("ERROR: " + str(e))

    # STEP 2: Match from LLM
    if not message.use_llm:
        return message
    prompt_ambiguous2unambiguous = prompt.ambiguous2unambiguous(message.split_instruction, message)
    llm_result = openai.get_completion(prompt_ambiguous2unambiguous)
    if status_info[Status.ERROR_LLM] in llm_result:
        print("LLM ERROR: " + llm_result)
        return message
    try:
        steps = ast.literal_eval(llm_result)
    except Exception as e:
        print("ERROR: LIST PARSE Fail: " + llm_result + str(e))
        return message
    print("### LLM STEPS GENERATE SUCCESS: " + str(steps))
    message.steps = steps
    # STEP 3: Reuse the rule from LLM
    if message.steps is not None and len(message.steps) != 0:
        save_ambiguous_rule(message)
        return message
    print("ERROR: steps generated from LLM is not match!")
    return message


if __name__ == '__main__':
    print(extract_intents("(get the necessary workpiece), (position it correctly), and then (assemble it)"))
    print(build_pattern("(get the necessary workpiece), (position it correctly), and then (assemble it)"))
