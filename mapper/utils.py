import torch
from nlp.parser import get_embedding
import re
import py_trees
from config import dirs_tasks_reuse
import xml.etree.ElementTree as ET
from lxml import etree

# from memory.lingua_robot import actions
# from memory.lingua_robot import conditions

# from memory.cleaning import actions
# from memory.cleaning import conditions
# from memory.cooking import actions
# from memory.cooking import conditions
# from memory.logistics import actions
# from memory.logistics import conditions
from memory.assembly import actions
from memory.assembly import conditions


def find_memory(token, token_embedding, infos):
    """
    memory_infos[
        bt_info{
            'bt_name': string,
            'bt_name_embedding': [int_list],
            'bt_explanation': string,
            'bt_explanation_embedding': [int_list],
            'synonyms': [{'synonyms_name': string,
                          'synonyms_embedding': [int_list]} * N ]
            'pattern':[ string1, string2 *N ]
        } * N ]
    """
    if infos is None or len(infos) == 0: return None
    try:
        for info in infos:
            bt_name = info['bt_name']
            if bt_name == token:
                print("### << bt_name >> match ==> '" + token + "' : " + bt_name)
                return bt_name
            if torch.cosine_similarity(info['bt_name_embedding'], token_embedding) > 0.9:
                print("### << bt_name_embedding >> match ==> '" + token + "' : " + bt_name)
                return bt_name
            if info.get('bt_explanation_embedding') is not None and torch.cosine_similarity(info['bt_explanation_embedding'], token_embedding) > 0.9:
                print("### << bt_explanation_embedding >> match ==> '" + token + "' : " + bt_name)
                return bt_name
            if info.get('synonyms') is not None:
                for synonyms in info['synonyms']:
                    synonym_name = synonyms['synonyms_name']
                    if synonym_name == token:
                        print("### << synonyms_name >> match ==> '" + token + "' : " + synonym_name)
                        return bt_name
                    synonyms_embedding = synonyms['synonyms_embedding']
                    if torch.cosine_similarity(synonyms_embedding, token_embedding) > 0.9:
                        print("### << synonyms_embedding >> match ==> '" + token + "' : " + synonym_name)
                        return bt_name
            if info.get("pattern") is not None:
                for pattern in info['pattern']:
                    try:
                        if re.match(pattern, token, re.IGNORECASE):
                            print("### << pattern >> match ==> '" + token + "' : " + pattern)
                            return bt_name
                    except Exception as e:
                        print("Error: pattern match fail " + str(e))
    except Exception as e:
        print("Error: find memory fail " + str(e))
    return None


def find_bt(token, message):
    """
    Find "bt_name" and "type" in memory based on token
    type:
        1: controller
        2: condition
        3: action
        4: reuse_node
       -1: Not find
    :return: bt_name, type
    """
    token_embedding = get_embedding(token)
    if token is None or len(token) == 0: return None, -1
    node_name = find_memory(token, token_embedding, message.reuse_infos)
    if node_name is not None:
        return node_name, 4
    node_name = find_memory(token, token_embedding, message.controller_infos)
    if node_name is not None:
        return node_name, 1
    node_name = find_memory(token, token_embedding, message.condition_infos)
    if node_name is not None:
        return node_name, 2
    node_name = find_memory(token, token_embedding, message.action_infos)
    if node_name is not None:
        return node_name, 3
    else:
        return None, -1


def create_bt_reuse(bt_name):
    with open(dirs_tasks_reuse + bt_name + ".xml", 'r', encoding='utf-8') as f:
        task_root = ET.fromstring(f.read())[0].find("bt")[0]

        def convert_element(element):
            bt = create_bt(element.get("name"))
            bt.qualified_name = ""
            for child_element in element:
                bt.add_child(convert_element(child_element))
            return bt

        tree = convert_element(task_root)
    return tree


def create_bt(bt_name):
    # controller
    if "parallel" in bt_name:
        return py_trees.composites.Parallel(name=bt_name, policy=py_trees.common.ParallelPolicy.Base)
    if "sequence" in bt_name:
        return py_trees.composites.Sequence(name=bt_name, memory=False)
    if "selector" in bt_name:
        return py_trees.composites.Selector(name=bt_name, memory=False)

    # -------------------------------------------------------------------------------------
    # -------------------------- lingua_robot_init robot -------------------------------------
    # -------------------------------------------------------------------------------------
    # # conditions
    # if "battery_check" in bt_name:
    #     return conditions.BatteryCheck(name=bt_name)
    # if "obstacle_detection" in bt_name:
    #     return conditions.ObstacleDetection(name=bt_name)
    # if "reachable" in bt_name:
    #     return conditions.Reachable(name=bt_name)
    # if "visible" in bt_name:
    #     return conditions.Visible(name=bt_name)
    # # actions
    # if "bypass" in bt_name:
    #     return actions.Bypass(name=bt_name)
    # if "charging" in bt_name:
    #     return actions.Charging(name=bt_name)
    # if "drop" in bt_name:
    #     return actions.Drop(name=bt_name)
    # if "grab" in bt_name:
    #     return actions.Grab(name=bt_name)
    # if "move_back" in bt_name:
    #     return actions.MoveBack(name=bt_name)
    # if "move_forward" in bt_name:
    #     return actions.MoveForward(name=bt_name)
    # if "move_left" in bt_name:
    #     return actions.MoveLeft(name=bt_name)
    # if "move_right" in bt_name:
    #     return actions.MoveRight(name=bt_name)
    # if "request_help" in bt_name:
    #     return actions.RequestHelp(name=bt_name)
    # if "rest" in bt_name:
    #     return actions.Rest(name=bt_name)
    # if "rotate" in bt_name:
    #     return actions.Rotate(name=bt_name)
    # if "scanning" in bt_name:
    #     return actions.Scanning(name=bt_name)

    # -------------------------------------------------------------------------------------
    # --------------------------- cleaning robot --------------------------------
    # -------------------------------------------------------------------------------------
    # # conditions
    # if "clean_area_detection" in bt_name:
    #     return conditions.CleanAreaDetection(name=bt_name)
    # if "cleaning_tool_detection" in bt_name:
    #     return conditions.CleaningToolDetection(name=bt_name)
    # if "cleanliness" in bt_name:
    #     return conditions.Cleanliness(name=bt_name)
    # if "envs_safety" in bt_name:
    #     return conditions.EnvsSafety(name=bt_name)
    # # actions
    # if "check_cleanliness" in bt_name:
    #     return actions.CheckCleanliness(name=bt_name)
    # if "clean_area" in bt_name:
    #     return actions.CleanArea(name=bt_name)
    # if "interrupt_operation" in bt_name:
    #     return actions.InterruptOperation(name=bt_name)
    # if "navigate_to_area" in bt_name:
    #     return actions.NavigateToArea(name=bt_name)
    # if "request_help" in bt_name:
    #     return actions.RequestHelp(name=bt_name)
    # if "use_cleaning_tools" in bt_name:
    #     return actions.UseCleaningTools(name=bt_name)

    # -------------------------------------------------------------------------------------
    # --------------------------- cooking robot -----------------------------------
    # -------------------------------------------------------------------------------------
    # # conditions
    # if "cooking_utensils" in bt_name:
    #     return conditions.CookingUtensils(name=bt_name)
    # if "envs_safety" in bt_name:
    #     return conditions.EnvsSafety(name=bt_name)
    # if "food_preparation" in bt_name:
    #     return conditions.FoodPreparation(name=bt_name)
    # if "step_complete_detection" in bt_name:
    #     return conditions.StepCompleteDetection(name=bt_name)
    # # actions
    # if "execution_steps" in bt_name:
    #     return actions.ExecutionSteps(name=bt_name)
    # if "finish_cooking" in bt_name:
    #     return actions.FinishCooking(name=bt_name)
    # if "interrupt_operation" in bt_name:
    #     return actions.InterruptOperation(name=bt_name)
    # if "prepare_food" in bt_name:
    #     return actions.PrepareFood(name=bt_name)
    # if "request_intervention" in bt_name:
    #     return actions.RequestIntervention(name=bt_name)
    # if "use_cooking_tools" in bt_name:
    #     return actions.UseCookingTools(name=bt_name)

    # ------------------------------------------------------------------------------------
    # --------------------------- logistics robot ------------------------------
    # ------------------------------------------------------------------------------------
    # # conditions
    # if "envs_safety" in bt_name:
    #     return conditions.EnvsSafety(name=bt_name)
    # if "package_detection" in bt_name:
    #     return conditions.PackageDetection(name=bt_name)
    # if "package_type" in bt_name:
    #     return conditions.PackageType(name=bt_name)
    # if "correct_positioning" in bt_name:
    #     return conditions.CorrectPositioning(name=bt_name)
    # # actions
    # if "grab_package" in bt_name:
    #     return actions.GrabPackage(name=bt_name)
    # if "interrupt_operation" in bt_name:
    #     return actions.InterruptOperation(name=bt_name)
    # if "moving_package" in bt_name:
    #     return actions.MovingPackage(name=bt_name)
    # if "notification_exception" in bt_name:
    #     return actions.NotificationException(name=bt_name)
    # if "place_package" in bt_name:
    #     return actions.PlacePackage(name=bt_name)
    # if "route_plan" in bt_name:
    #     return actions.RoutePlan(name=bt_name)

    # -------------------------------------------------------------------------------------
    # --------------------------- assembly robot ----------------------------
    # -------------------------------------------------------------------------------------
    # conditions
    if "correct_positioning" in bt_name:
        return conditions.CorrectPositioning(name=bt_name)
    if "envs_safety" in bt_name:
        return conditions.EnvsSafety(name=bt_name)
    if "part_status" in bt_name:
        return conditions.PartStatus(name=bt_name)
    if "parts_detection" in bt_name:
        return conditions.PartDetection(name=bt_name)
    # actions
    if "assembly" in bt_name:
        return actions.Assembly(name=bt_name)
    if "check_assembly" in bt_name:
        return actions.CheckAssembly(name=bt_name)
    if "grab_parts" in bt_name:
        return actions.GrabPart(name=bt_name)
    if "interrupt_assembly" in bt_name:
        return actions.InterruptAssembly(name=bt_name)
    if "positioning_parts" in bt_name:
        return actions.PositioningPart(name=bt_name)
    if "request_help" in bt_name:
        return actions.RequestHelp(name=bt_name)
    return None


def create_bt_by_type(bt_name, bt_type):
    if bt_type == 4:
        bt_reuse = create_bt_reuse(bt_name)
        bt_reuse.qualified_name = bt_name
        return bt_reuse
    else:
        bt = create_bt(bt_name)
        bt.qualified_name = ""
        return bt


def bt2xml(bt):
    xml_root = etree.Element(bt.name)

    def convert_node(node, parent):
        bt_name = node.name
        xml_node = etree.Element(bt_name, {"name": node.name})
        parent.append(xml_node)
        for children in node.children:
            convert_node(children, xml_node)

    for child in bt.children:
        convert_node(child, xml_root)
    return xml_root


def xml2bt(xml_root):
    bt_root = create_bt(xml_root.get("name"))

    def convert_xml(xml_node, parent=None):
        # 递归处理所有子节点
        for child in xml_node:
            bt_node = create_bt(child.get("name"))
            parent.add_child(bt_node)
            convert_xml(child, bt_node)

    convert_xml(xml_root, bt_root)
    return bt_root


def save_bt(message, reuse_name="temp", path=dirs_tasks_reuse + "temp/temp.xml"):
    root = etree.Element('root')
    task_node = etree.SubElement(root, "task", {"name": reuse_name})
    bt_node = etree.SubElement(task_node, "bt")

    def convert_node(node, parent):
        bt_name = node.name
        xml_node = etree.Element(bt_name, {"name": node.name})
        parent.append(xml_node)
        for child in node.children:
            convert_node(child, xml_node)

    convert_node(message.main_bt, bt_node)
    xml_tree = etree.ElementTree(root)
    xml_tree.write(path, encoding='utf-8', pretty_print=True, xml_declaration=True)
    # Update memory infos NOTE: 先只加名字
    if reuse_name != "temp":
        info = {"bt_name": reuse_name,
                "bt_embedding": get_embedding(reuse_name),
                "synonyms": [{"synonyms_name": reuse_name}],
                "pattern": ["^(" + reuse_name + ")$"]}
        message.reuse_infos.append(info)
    return root
