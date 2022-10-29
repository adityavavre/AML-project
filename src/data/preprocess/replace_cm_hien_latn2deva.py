import argparse
from typing import List, Dict

def transliterate_latn2deva(sentences: List, transliteration_mapping: Dict) -> List:
    print("Transliterating " + str(len(sentences)) + " sentences")
    transliterated_sentences = []
    for sent in sentences:
        words = sent.split(' ')
        trans_words = list(map(lambda x: transliteration_mapping.get(x, x), words))
        transliterated_sentences.append(' '.join(trans_words))

    return transliterated_sentences

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--trans_map", type=str, default=None, required=True,
                        help="The path to the transliteration mapping created by transliterate_words.py on all_roman.txt")
    parser.add_argument("--input_file", default=None, type=str, required=True,
                        help="The input file in which latin hindi words are to be transliterated to devanagari")
    parser.add_argument("--offset", default=None, type=int, required=True)
    parser.add_argument("--output_file", default=None, type=str, required=True,
                        help="The output file in which transliterated output is to be stored")

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    trans_map_file = args.trans_map
    offset = args.offset

    trans_map = {}
    with open(trans_map_file, 'r', encoding='utf-8') as f:
        for line in f:
            word, trans = line.strip().split()
            trans_map[word] = trans

    input_sentences = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            input_sentences.append(line.strip())

    print("Loaded input file with "+str(len(input_sentences))+" sentences")

    output_sentences = transliterate_latn2deva(sentences=input_sentences[offset:], transliteration_mapping=trans_map)

    with open(output_file, 'w', encoding='utf-8') as f:
        for sent in output_sentences:
            f.write(sent + '\n')
