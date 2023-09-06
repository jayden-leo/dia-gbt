def unambiguous_intent_pattern(infos):
    """
    {"demo": demo, "embedding": embedding, "intent": intent, "pattern": pattern})
    """
    if infos is None or len(infos) == 0:
        return ""
    intents_pattern_prompt = ""
    for info in infos[:8]:
        intent = info['intent']
        pattern = info['pattern']
        intents_pattern_prompt += intent + "\n" + pattern + "\n\n"
    return intents_pattern_prompt


def get_pattern(mark_intent, unambiguous_infos):
    """
    message: (code, info, error_count, use_llm, instruction,
            bt, cur_bt, main_bt,
            split_instruction, level,
            intents, pattern, bt_list,
            step, steps, bt_lists,
            unambiguous_infos, ambiguous_infos
            reuse_infos, controller_infos, condition_infos, action_infos)
    """
    unambiguous_intent_patterns = unambiguous_intent_pattern(unambiguous_infos)
    prompt = f"""
Please do an in-place rewrite of @@. 
Requires:
1 If there is a verb in "()", replace the parts in the brackets "()" with ".*?" or ".*"
2 No change if there is no verb in "()".
3 Just output the result of the rewritten sentence
4 Don't output @@

For examples:

{unambiguous_intent_patterns}
@{mark_intent}@
"""
    return prompt


def unambiguous_demo_intent(infos):
    """
    {"demo": demo, "embedding": embedding, "intent": intent, "pattern": pattern})
    """
    if infos is None or len(infos) == 0:
        return ""
    demo_intent_prompt = ""
    for info in infos[:8]:
        demo = info['demo']
        intent = info['intent']
        demo_intent_prompt += demo + "\n" + intent + "\n\n"
    return demo_intent_prompt


def mark_intents(instruction, unambiguous_infos):
    """
    message: (code, info, error_count, use_llm, instruction,
            bt, cur_bt, main_bt,
            split_instruction, level,
            intents, pattern, bt_list,
            step, steps, bt_lists,
            unambiguous_infos, ambiguous_infos
            reuse_infos, controller_infos, condition_infos, action_infos)
    """
    unambiguous_demo_intents = unambiguous_demo_intent(unambiguous_infos)
    prompt = f"""
Please do an in-place rewrite of @@.
Requires:
1 Wrap the verb and the content pointed to by the verb as a whole in "brackets", that is, ()
2 Wrap the relationship between the verbs in "brackets", such as "as the same time"
3 Wrap the part of conditional judgment, such as "if something condition"
4 Just output the result of the rewritten sentence
5 Don't output @@

For examples:

request human assistance and grab the phone at the same time if necessary"
(Request human assistance) and (grab the phone) (at the same time) if necessary.

{unambiguous_demo_intents}
@{instruction}@
    """
    return prompt


def local_memory(message):
    """ structure
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
    memory_info = ""
    infos = [message.reuse_infos, message.controller_infos, message.condition_infos, message.action_infos]
    for special_infos in infos:
        if special_infos is None or len(special_infos) == 0:
            continue
        for info in special_infos:
            memory_info += "BT NAME: '" + info['bt_name'] + "'"
            if info.get('bt_explanation') is not None: memory_info += "; BT COMPETENCE EXPLANATION: " + info['bt_explanation'] + ""
            if info.get('synonyms') is not None and len(info['synonyms']) != 0:
                memory_info += "; ITS SYNONYMS: " + "".join("'" + synonyms['synonyms_name'] + "' " for synonyms in info['synonyms'][:6])
            memory_info += "\n"
    return memory_info


def get_intent2bt(intent, message):
    memory_info = local_memory(message)
    prompt = f"""
Please Select one from the corresponding "bt_list" according to @@'s semantics.

The specific "bt name" and its "competence explanation", "synonyms" from bt_list are as follows:
{memory_info}

Requires:
1 Only print the corresponding behavior tree node name.
2 If there really is no corresponding node in the semantics, return "None"
3 Don't output @@

For examples:

"ask for help"
request_help

"obtaining power"
charging

"approachable"
reachable

@{intent}@
    """
    return prompt


def local_steps(infos):
    """
    {"instruction": instruction, "embedding": embedding, "steps": steps_info}
    """
    if infos is None or len(infos) == 0:
        return ""
    intents_pattern_prompt = ""
    for info in infos[:3]:
        instruction = info['instruction']
        intents_pattern_prompt += instruction+"\n"+str(info['steps'])+"\n\n"
    return intents_pattern_prompt


def ambiguous2unambiguous(instruction, message):
    local_step = local_steps(message.ambiguous_infos)
    memory_info = local_memory(message)
    prompt = f"""
Please disassemble the instruction in @@ into atomic tasks.
All atomic tasks are as follows (behavior tree list):
{memory_info}

Require:
1 The steps need to be designed according to the capabilities of the robot
2 Only generate "list" structure, do not print redundant information
3 Don't output @@

For examples:

{local_step}
@{instruction}@
    """
    return prompt
