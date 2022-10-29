import argparse
from typing import List
import requests
import LID_tool.getLanguage
import time
import os

os.environ['MALLET_HOME']="C:\\Users\\Aditya\\Desktop\\sem8\\AdvancedML\\Project\\aml-project\\src\\data\\preprocess\\LID_tool\\mallet-2.0.8"

def detect_word_langid(sent: str, classifier_path: str):
    langids = LID_tool.getLanguage.langIdentify(sent, classifier_path)
    return langids[0]

def transliterate(sentences: List, subscription_key, subscription_region):
    headers = {'Accept': 'application/json;text/xml',
               'Content-Type': 'application/json',
               'Ocp-Apim-Subscription-Key': subscription_key,
               'Ocp-Apim-Subscription-Region': subscription_region,
               }
    base_url = 'https://api.cognitive.microsofttranslator.com'
    path = '/transliterate?api-version=3.0&language=hi&fromScript=Latn&toScript=Deva'
    constructed_url = base_url + path
    body = []
    trans = {}
    for sent in sentences:
        body.append({'Text': sent})
    # print("Body: ", body)
    response = requests.post(constructed_url, headers=headers, json=body)
    result = response.json()
    # print("Result: ", result)
    for j, i in enumerate(result):
        trans.update({body[j]['Text']: i['text']})

    return trans

def transliterate_latn2deva(sentences: List,
                            classifier_path: str,
                            subscription_key: str,
                            subscription_region: str) -> List:
    print("Transliterating "+str(len(sentences))+" sentences")
    start_time = time.time()
    transliterated_sentences = []
    transliterated_mapping = {}
    BATCH_SIZE = 100
    for i in range(0, len(sentences), BATCH_SIZE):
        batch = sentences[i:(i+BATCH_SIZE)]
        sents_langids = []
        hindi_words = set()
        for sent in batch:
            langids = detect_word_langid(sent, classifier_path)
            sents_langids.append(langids)
            hi_words = list(map(lambda x: x[0], filter(lambda x: x[1] == 'HI' and x[0] not in transliterated_mapping, langids)))
            hindi_words.update(hi_words)

        if len(hindi_words) == 0:
            transliterated_sentences.extend(batch)
            continue
        # print("Hindi words: ", hindi_words)
        hindi_words = list(hindi_words)
        for j in range(0, len(hindi_words), 10):
            hi_word_batch = hindi_words[j:(j+10)]
            transliterated_mapping.update(transliterate(hi_word_batch, subscription_key, subscription_region))

        for langids in sents_langids:
            transliterated_sent = list(map(lambda x: transliterated_mapping[x[0]] if x[1] == 'HI' else x[0], langids))
            transliterated_sentences.append(' '.join(transliterated_sent))
        # print("Trans sent: ", transliterated_sentences[len(transliterated_sentences)-1])
        if i%9 == 0 and i!=0:
            print("Finished 10 batches in "+str(time.time()-start_time)+" seconds")
            start_time = time.time()
    return transliterated_sentences

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--subscription_key", default='0cc37825ec874106aac7712ddad34b59', type=str,
                        help="Azure Subscription key for downloading transliterations")
    parser.add_argument("--subscription_region", default='eastus', type=str,
                        help="Azure Subscription region for downloading transliterations")
    parser.add_argument("--classifier", type=str, default='C:\\Users\\Aditya\\Desktop\\sem8\\AdvancedML\\Project\\aml-project\\src\\data\\preprocess\\LID_tool\\classifiers\\HiEn.classifier',
                        help="The path to the classifier in the cloned repo https://github.com/microsoft/LID-tool/blob/main/classifiers/HiEn.classifier")
    parser.add_argument("--input_file", default=None, type=str, required=True,
                        help="The input file in which latin hindi words are to be transliterated to devanagari")
    parser.add_argument("--offset", default=None, type=int, required=True)
    parser.add_argument("--num", default=20000, type=int)
    parser.add_argument("--output_file", default=None, type=str, required=True,
                        help="The output file in which transliterated output is to be stored")

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    subscription_key = args.subscription_key
    subscription_region = args.subscription_region
    classifier = args.classifier
    offset = args.offset
    num = args.num

    input_sentences = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            input_sentences.append(line.strip())

    print("Loaded input file with "+str(len(input_sentences))+" sentences")

    # offset = 2892
    # output_sentences = input_sentences[:offset]
    output_sentences = transliterate_latn2deva(sentences=input_sentences[offset:(offset+num)],
                                                classifier_path=classifier,
                                               subscription_key=subscription_key,
                                               subscription_region=subscription_region)

    with open(output_file, 'w', encoding='utf-8') as f:
        for sent in output_sentences:
            f.write(sent+'\n')

    # x = transliterate(['mein theek hu'], subscription_key, subscription_region)
    # print(x)