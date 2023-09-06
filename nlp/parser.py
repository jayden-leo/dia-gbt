import os
import re
import torch
from transformers import AutoTokenizer, AutoModel
import spacy
import xml.etree.ElementTree as ET
from glob import glob
import jieba

os.environ['http_proxy'] = "http://localhost:7890"
os.environ['https_proxy'] = "http://localhost:7890"

bert_tokenizer = AutoTokenizer.from_pretrained("ToolBench/ToolBench_IR_bert_based_uncased")
bert_model = AutoModel.from_pretrained("ToolBench/ToolBench_IR_bert_based_uncased")


def mean_pooling(model_output, attention_mask):
    """
        Mean Pooling - Take attention mask into account for correct averaging
    """
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def get_embedding(token):
    """
        embedding of token (sentence is also can use it)
    """
    encoded_input = bert_tokenizer(token, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = bert_model(**encoded_input)
    embedding = mean_pooling(model_output, encoded_input['attention_mask'])
    return embedding


def load_memory(dir_memory):
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
    memory_infos = []
    files = glob(os.path.join(dir_memory, '*'))
    try:
        for file in files:
            if file.endswith('xml'):
                bt_info = {}
                bt = ET.parse(file).getroot()[0]
                bt_name = bt.get('name')
                jieba.add_word(bt_name)  # jieba adaption
                bt_name_embedding = get_embedding(bt_name.replace('_', ' '))
                bt_info['bt_name'] = bt_name
                bt_info['bt_name_embedding'] = bt_name_embedding
                if bt.find('explanation') is not None:
                    bt_explanation = bt.find('explanation').text
                    bt_name_embedding = get_embedding(bt_explanation)
                    bt_info['bt_explanation'] = bt_explanation
                    bt_info['bt_explanation_embedding'] = bt_name_embedding
                if bt.find('synonyms') is not None:
                    synonyms_infos = []
                    for synonyms_node in bt.findall('synonyms'):
                        synonyms_name = synonyms_node.text.replace("_", " ")
                        jieba.add_word(synonyms_name)  # jieba adaption
                        synonyms_embedding = get_embedding(synonyms_name)
                        synonyms_infos.append({'synonyms_name': synonyms_name, 'synonyms_embedding': synonyms_embedding})
                    bt_info['synonyms'] = synonyms_infos
                if bt.find('pattern') is not None:
                    pattern_infos = []
                    for pattern in bt.findall('pattern'):
                        pattern_infos.append(pattern.text.lower())
                    bt_info['pattern'] = pattern_infos
                memory_infos.append(bt_info)
    except Exception as e:
        return "ERROR: << XML " + dir_memory + " PARSE FAIL >>" + str(e)
    return memory_infos


def load_ambiguous_rules(dir_ambiguous_rules):
    """
    ambiguous_infos = [{'instruction':string,
                        'embedding':[int_list],
                        'steps':[string_list]
                       {},...]
    """
    ambiguous_infos = []
    try:
        rules = ET.parse(dir_ambiguous_rules).getroot().findall("rule")
        for rule in rules:
            instruction = rule.find("instruction").text
            embedding = get_embedding(instruction)
            steps = rule.find("steps").findall("step")
            steps_info = []
            for step in steps:
                steps_info.append(step.text)
            ambiguous_infos.append({"instruction": instruction,
                                    "embedding": embedding,
                                    "steps": steps_info})
    except Exception as e:
        return "ERROR: << XML " + dir_ambiguous_rules + " PARSE FAIL >>" + str(e)
    return ambiguous_infos


def load_unambiguous_rules(dir_unambiguous_rules):
    """
    unambiguous_infos = [{'demo':string,
                          'embedding':[int_list],
                          'intent':string,
                          'pattern':string},
                         {},...]
    """
    unambiguous_infos = []
    try:
        rules = ET.parse(dir_unambiguous_rules).getroot().findall("rule")
        for rule in rules:
            demo = rule.find("demo").text.lower().strip(",.;'!? ，。；“”'！？")
            embedding = get_embedding(demo)
            intent = rule.find("intent").text.lower().strip(",.;'!? ，。；“”'！？")
            pattern = rule.find("pattern").text.lower().strip(",.;'!? ，。；“”'！？")
            unambiguous_infos.append({"demo": demo,
                                      "embedding": embedding,
                                      "intent": intent,
                                      "pattern": pattern})
    except Exception as e:
        return "ERROR: << XML " + dir_unambiguous_rules + " PARSE FAIL >>" + str(e)
    return unambiguous_infos


def judge_ambiguity(text):
    """
    -1 非指令 1：行为树描述级(无歧义)  2：流程描述级(无歧义)  3：任务描述级(有歧义)
    """
    level3_pattern = "(perform|execut).*task|task.*execut.*"
    if "node" in text:
        return 1
    elif re.match(level3_pattern, text, re.IGNORECASE):
        return 3
    else:
        return 2


def get_seg_model(text):
    """
    When there are Chinese characters, use the Chinese model, otherwise use the English model clause
    """
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return spacy.load("zh_core_web_sm")
    return spacy.load("en_core_web_sm")
