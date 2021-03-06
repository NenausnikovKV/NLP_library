import inspect
import sys


def get_punctuation_list(file_processing=None):
    # address = file_processing.get_general_address("clusterization_components_excerpts//in//punctuation_mark")
    folder_address = __file__[:__file__.rindex("\\")]
    local_address = "punctuation_mark"
    address = f"{folder_address}//{local_address}"
    f = open(address, "r", encoding="utf-8")
    punctuation_text = ""
    for line in f:
        punctuation_text = punctuation_text + line
    punctuation_list = punctuation_text.split()
    return punctuation_list

class Token:
    """
    текст токена и его тип (знак препинания, число или слово)
    """
    punctuation_list = get_punctuation_list()

    def __init__(self, text, type):
        self.text = text.upper()
        self.type = type

    def __lt__(self, other):
        return self.text < other.text

    def __str__(self):
        return self.text + " (" + self.type + ")" + " - "


    @staticmethod
    def define_type(word_text):
        if word_text in list(Token.punctuation_list):
            token_type = "punctuation"
        elif word_text.isdigit():
            token_type = "digit"
        else:
            token_type = "word"
        return token_type

class SentenceToken(Token):
    """
    Определение положения токена в предложении
    """
    def __init__(self, text, type, num =-1, start=-1, stop=-1, source_sentence_text=None):
        super().__init__(text, type)
        self.start = start
        self.stop = stop
        self.num = num
        self.source_sentence = source_sentence_text

    @staticmethod
    def find_normal_token_text(token, normal_tokens):
        start = token.start
        for norm_token in normal_tokens:
            if norm_token.start == start:
                return norm_token.text
        return None

