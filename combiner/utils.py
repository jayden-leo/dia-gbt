from mapper.utils import create_bt, create_bt_by_type
import torch
from nlp.parser import get_embedding


def copy_bt(real_root):
    copy_root = create_bt(real_root.name)
    if real_root.qualified_name == "":
        copy_root.qualified_name = ""

    def convert_bt(real_node, copy_node):
        if len(real_node.children) != 0 and real_node.children is not None:
            for child in real_node.children:
                bt_node = create_bt(child.name)
                if child.qualified_name == "":
                    bt_node.qualified_name = ""
                copy_node.add_child(bt_node)
                convert_bt(child, bt_node)

    convert_bt(real_root, copy_root)
    return copy_root


def bt2sentence(root):
    """
    Get a "sentence" describing the BT according to the template
    NOTE : 1 加入控制节点的类型，生成更加友好的翻译句子。
           2 加入位置关系，让翻译的句子是一个无歧义翻译成行为树的句子
    """
    if root.children is None or len(root.children) == 0:
        translate_sentence = "execute a " + str(root.name) + " task."
        return translate_sentence
    translate_sentence = ""

    def convert_bt(node, sentence):
        if node.children is None or len(node.children) == 0:
            return sentence
        first_child = True
        for child in node.children:
            if first_child:
                first_child = False
                if "sequence" in str(node.name).lower().strip(" "):
                    if node.qualified_name is not None and str(node.qualified_name) != "":
                        sentence += str(node.qualified_name) + " sequentially executes "
                    else:
                        sentence += str(node.name) + " sequentially executes "
                    if child.qualified_name is not None and str(child.qualified_name) != "":
                        sentence += str(child.qualified_name) + "(" + str(child.name) + ")"
                    else:
                        sentence += str(child.name)
                elif "parallel" in str(node.name).lower().strip(" "):
                    if node.qualified_name is not None and str(node.qualified_name) != "":
                        sentence += str(node.qualified_name) + " simultaneously executes "
                    else:
                        sentence += str(node.name) + " simultaneously executes "
                    if child.qualified_name is not None and str(child.qualified_name) != "":
                        sentence += str(child.qualified_name) + "(" + str(child.name) + ")"
                    else:
                        sentence += str(child.name)

                elif "selector" in str(node.name).lower().strip(" "):
                    if node.qualified_name is not None and str(node.qualified_name) != "":
                        sentence += str(node.qualified_name) + " executes arbitrarily selecting one of "
                    else:
                        sentence += str(node.name) + " executes arbitrarily selecting one of "
                    if child.qualified_name is not None and str(child.qualified_name) != "":
                        sentence += str(child.qualified_name) + "(" + str(child.name) + ")"
                    else:
                        sentence += str(child.name)
                else:
                    if node.qualified_name is not None and str(node.qualified_name) != "":
                        sentence += str(node.qualified_name) + " executes "
                    else:
                        sentence += str(node.name) + " executes "
                    if child.qualified_name is not None and str(child.qualified_name) != "":
                        sentence += str(child.qualified_name) + "(" + str(child.name) + ")"
                    else:
                        sentence += str(child.name)
            else:
                if child.qualified_name is not None and str(child.qualified_name) != "":
                    sentence += ", " + str(child.qualified_name) + "(" + str(child.name) + ")"
                else:
                    sentence += ", " + str(child.name)
        sentence += ". "
        for child in node.children:
            sentence = convert_bt(child, sentence)
        return sentence

    return convert_bt(root, translate_sentence)


class Combiner(object):
    def __init__(self):
        self.instruction = None
        self.instruction_embedding = None
        self.bt_count = 0
        self.temp_bt = None
        self.most_similarity = -1
        self.most_similar_bt = None

    def combine(self, message):
        """
        Traverse "bt_list" and Select the "BT" that best matches the instruction
NOTE: 剪枝优化：
    1 相同控制节点在同一位置跳过
    2 条件节点优先放在行为节点前
    3 类人算法： 人也不可能递归所有元素，而是想了几个模板过后发现差不多，然后在进行适当修改，逐渐成功（进化组合）
        """
        self.instruction = message.split_instruction
        self.instruction_embedding = message.split_instruction_embedding
        used = [0] * len(message.bt_list)
        self.backtracking(message.bt_list, used, 0, None, -1)
        return self.most_similar_bt, self.bt_count

    def backtracking(self, bt_list, used, bt_len, node, node_type):
        if bt_len == len(bt_list):
            # Turn to "root node"
            while node.parent:
                node = node.parent
            temp_bt = copy_bt(node)
            self.temp_bt = temp_bt
            self.bt_count += 1
            # STEP 2: Get a "sentence" describing the BT according to the template
            temp_bt_sentence = bt2sentence(temp_bt)
            # STEP 3: Select the "BT" that best matches the instruction
            similarity = torch.cosine_similarity(self.instruction_embedding, get_embedding(temp_bt_sentence))
            if similarity > self.most_similarity:
                self.most_similarity = similarity
                self.most_similar_bt = temp_bt
            return
        for i in range(len(bt_list)):
            if used[i] == 0:  # 只生成链接没有使用过的节点
                bt_node = create_bt_by_type(bt_list[i]["name"], node_type)
                by_type = bt_list[i]["type"]
                # 除非列表中只有一个节点，否则只有控制节点才能作为根节点
                if node is None:
                    if by_type == 1 or len(bt_list) == 1:
                        bt_len += 1
                        used[i] = 1
                        self.backtracking(bt_list, used, bt_len, bt_node, by_type)
                        bt_len -= 1
                        used[i] = 0
                else:
                    if node_type == 1:  # 只有父节点是控制节点才可以添加孩子节点
                        node.add_child(bt_node)
                        bt_len += 1
                        used[i] = 1
                        self.backtracking(bt_list, used, bt_len, bt_node, by_type)
                        if bt_len != len(bt_list):
                            self.backtracking(bt_list, used, bt_len, node, node_type)
                        bt_len -= 1
                        used[i] = 0
                        node.children.pop()


if __name__ == '__main__':
    pass
