from pkg_resources import resource_filename
from types import ModuleType
from PyKomoran import Komoran
from konlpy.tag import *
from transformers import BertTokenizer
from functools import partial
from transformers import *

import os


# try:
#     import importlib.resources as pkg_resources
# except ImportError:
#     # Try backported to PY<37 `importlib_resources`.
#     import importlib_resources as pkg_resources

class Tokenizer:
    def __init__(self, tokenizer_name="komoran"):
        assert (tokenizer_name.lower() == "komoran") or (tokenizer_name.lower() == "mecab") \
               or (tokenizer_name.lower() == "subword"), "Only 'komoran', 'mecab', and 'subword' is acceptable."
        if tokenizer_name == "komoran":
            self.tokenizer = Komoran("STABLE")
        elif tokenizer_name == "mecab":
            self.tokenizer = Mecab()
        elif tokenizer_name == "subword":
            self.tokenizer = BertTokenizer(resource_filename(__package__, "vocab_noised.txt"), do_lower_case=False)
        self.tokenizer_name = tokenizer_name

    def tokenize(self, text):
        if self.tokenizer_name == "komoran":
            return self.tokenizer.get_morphes_by_tags(text)
        elif self.tokenizer_name == "mecab":
            return self.tokenizer.morphs(text)
        else:  # self.tokenizer_name 이 None
            return self.tokenizer.tokenize(text)

    def post_process(self, tokens):
        if self.tokenizer_name == "komoran":
            return " ".join(tokens)
        elif self.tokenizer_name == "mecab":
            return " ".join(tokens)
        else:  # self.tokenizer_name 이 subword 또는 moduletype
            return self.tokenizer.convert_tokens_to_string(tokens)


# proposed

def load_list():
    with open('./huggingface_pretrained_tokenizers.txt', 'r') as r:
        hf_list = r.read().splitlines()
    return hf_list

KONLPY = ['Kkma', 'Hannanum', 'Komoran', 'Twitter', 'Okt', 'Mecab']
HUGGINGFACE = load_list()

def get_tokenizer(keyword):
    if keyword in KONLPY:
        return eval(f'{keyword}()')
    elif keyword in HUGGINGFACE:
        return AutoTokenizer.from_pretrained(keyword)
    else:
        raise KeyError('Not Defined!')


def get_tokenize(tokenizer):
    class_name = tokenizer.__class__.__name__

    if class_name in KONLPY:
        return tokenizer.morphs

    return lambda x: x.split()


# TODO:define the method for the uncased tokens
def convert_tokens_to_string(tokens):
    new_tokens = [[]]
    for token in tokens:
        if token.startswith('##'):
            new_tokens[-1].append(token.replace('##', ''))
            continue
        new_tokens.append([token])
    return ' '.join([''.join(tset) for tset in new_tokens if tset])


def wrapping_tokenizer(self, tokenizer=None):
    if isinstance(tokenizer, str):
        tokenizer = get_tokenizer(tokenizer)

    if 'tokenize' not in dir(tokenizer):
        tokenizer.tokenize = partial(get_tokenize(tokenizer), tokenizer)

    if 'convert_tokens_to_string' not in dir(tokenizer):
        tokenizer.convert_tokens_to_string = partial(convert_tokens_to_string, tokenizer)

    return tokenizer


if __name__ == '__main__':
    pass
