from nlp.parser import load_unambiguous_rules, load_ambiguous_rules, load_memory
from config import dirs_tasks_reuse, dirs_controllers, dirs_conditions, dirs_actions, dir_unambiguous_rules, dir_ambiguous_rules


def print_memory_infos(infos):
    """ structure
    memory_infos[bt_info{
                    'bt_name': xxx,
                    'bt_name_embedding': xxx,
                    'bt_explanation': xxx,
                    'bt_explanation_embedding':xxx,
                    'synonyms': [{'synonyms_name':xxx,'synonyms_embedding'xxx} * N ]
                    'pattern':[ pattern1, pattern2, * N ]
        } * N ]
    """
    print("All bt_names are:  " + str([str(info['bt_name']) for info in infos]))
    for info in infos:
        print("--- '" + info['bt_name'] + "'  node's specific mapping:")
        if info.get('bt_explanation') is not None:
            print("competence explanation: " + info['bt_explanation'])
        if info.get('synonyms') is not None:
            print("synonyms: " + str([str(synonyms['synonyms_name']) for synonyms in info['synonyms']]))
        if info.get('pattern') is not None:
            print("pattern: " + str([str(pattern) for pattern in info['pattern']]))


def print_preprocess_infos(reuse_infos, controller_infos, condition_infos, action_infos):
    print("#" * 20 + "   BEGIN:   LANGUAGE PREPROCESS   " + "#" * 70)
    if reuse_infos is not None and len(reuse_infos) != 0:
        print("\n" + "^" * 30 + "   REUSE TASK  " + "^" * 80)
        print_memory_infos(reuse_infos)
    if controller_infos is not None and len(controller_infos) != 0:
        print("\n" + "^" * 30 + "   CONTROLLER  " + "^" * 80)
        print_memory_infos(controller_infos)
    if condition_infos is not None and len(condition_infos) != 0:
        print("\n" + "^" * 30 + "   CONDITION   " + "^" * 80)
        print_memory_infos(condition_infos)
    if action_infos is not None and len(action_infos) != 0:
        print("\n" + "^" * 30 + "    ACTION     " + "^" * 80)
        print_memory_infos(action_infos)
    print("\n" + "#" * 20 + "   END:     LANGUAGE PREPROCESS   " + "#" * 70 + "\n")


def pre_process():
    unambiguous_infos = load_unambiguous_rules(dir_unambiguous_rules)
    ambiguous_infos = load_ambiguous_rules(dir_ambiguous_rules)
    reuse_infos = load_memory(dirs_tasks_reuse)
    controller_infos = load_memory(dirs_controllers)
    condition_infos = load_memory(dirs_conditions)
    action_infos = load_memory(dirs_actions)
    print_preprocess_infos(reuse_infos, controller_infos, condition_infos, action_infos)
    return unambiguous_infos, ambiguous_infos, reuse_infos, controller_infos, condition_infos, action_infos
