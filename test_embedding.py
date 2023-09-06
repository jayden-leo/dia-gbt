import os
import torch
from nlp.parser import get_embedding
from transformers import AutoTokenizer, AutoModel

os.environ['http_proxy'] = "http://localhost:7890"
os.environ['https_proxy'] = "http://localhost:7890"


def test_sentence_similarity():
    # Mean Pooling - Take attention mask into account for correct averaging
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    # input_texts1 = 'query: Grab the package and mail it to the target location at the same time.'
    # input_texts2 = 'query: Parallel execute grab_the_package and mail it to the target location.'  # 0.9150
    # input_texts2 = 'query: Sequence execute grab_the_package and mail it to the target location' # 0.9037
    # input_texts2 = 'query: Sequence execute grab_the_package node and mail node'  # 0.8669
    # input_texts2 = 'query: Parallel execute grab_the_package node and mail node'  # 0.8721
    # input_texts2 = 'query: please go around this obstacle and get me your phone on the table.'  # 0.8076
    # input_texts2 = 'query: Task execution: help me put the toilet clothes on the balcony'  # 0.8149
    # input_texts2 = 'query: grab and mail those items to the location the same time'  # 0.9444
    # input_texts2 = 'query: grab and mail those items to the location step by step'  # 0.9029
    # input_texts2 = 'query: grab and mail those items parallel'  # 0.8930

    # Sentences we want sentence embeddings for
    sentences = ["parallel execute grab_the_package and mail it to the target location",
                 "Grab the package to the target location at the same time.",
                 "simultaneous execute grab_the_package and mail it to target"]

    # Load model from HuggingFace Hub
    tokenizer = AutoTokenizer.from_pretrained('ToolBench/ToolBench_IR_bert_based_uncased')
    model = AutoModel.from_pretrained('ToolBench/ToolBench_IR_bert_based_uncased')

    # Tokenize sentences
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    # Perform pooling. In this case, mean pooling.
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    print("Sentence embeddings:", sentence_embeddings.shape)
    sentence1 = torch.reshape(sentence_embeddings[0], (1, 768))
    sentence2 = torch.reshape(sentence_embeddings[1], (1, 768))
    sentence3 = torch.reshape(sentence_embeddings[2], (1, 768))
    soccers = torch.cosine_similarity(sentence1, sentence2)
    print(soccers)
    soccers = torch.cosine_similarity(sentence1, sentence3)
    print(soccers)


if __name__ == '__main__':
    token1 = "parallel execution"
    # token2 = "Parallel"
    token2 = "parallel execute"
    embedding1 = get_embedding(token1)
    embedding2 = get_embedding(token2)
    soccer = torch.cosine_similarity(embedding1, embedding2)
    print(soccer)
