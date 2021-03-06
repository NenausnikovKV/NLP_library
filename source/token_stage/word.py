#! / usr / bin / env Python
# coding = utf-8
import copy


class Word:
    """
    Описание слова вне контекста, словарный токен, нормальная форма слова, лексическая информация
    """
    def __init__(self, token, normal_text, speech_part=None, grammemes=None):
        if token.type != "word":
            raise Exception('предложенный токен не явяляется словом')
        self.token = token
        self.text = normal_text.upper()
        self.speech_part = speech_part
        self.grammemes = grammemes

    def __str__(self):
        return self.text + " (" + self.speech_part + ")"



class SentenceWord(Word):
    """
    Расширенная версия слова, в контексте предложения включает в себя рейтинг (количество повторов в предложении) и
    текст предложения (для поиска источника)
    """
    def __init__(self, sen_token, normal_text, speech_part=None, grammemes = None,
                 rating=0, num=0, source_sentence_text=None):
        super().__init__(sen_token, normal_text, speech_part, grammemes)
        self.rating = rating
        self.source = source_sentence_text
        self.num = num

    def __add__(self, other):
        """
        Сложение рейтингов предложения, предполагается, что источник у них единый, а также нормальная форма слов
        эквивалентна
        """
        # todo неочевидный, небезопасный метод - вынести в __init__ или ограничить приватным методом
        result = copy.copy(self)
        if result.text == other.text:
            result.rating += other.rating
        else:
            raise Exception('Для сложения текст двух элементов должен быть одинаковым')
        return result

    def __str__(self):
        return self.text + " (" + str(self.rating) + ")"

    @staticmethod
    def get_word_dict_from_word_list(word_list):
        words = {}
        for word in word_list:
            if not words.get(hash(word.text)):
                words[hash(word.text)] = copy.deepcopy(word)
            else:
                words[hash(word.text)].rating += word.rating
        return words


class TextWord():
    """
    Описание слова в контексте текста, урезанная версия - нормальная форма, рейтинг в тексте
    """

    class WordSource:
        """
            Пара слово, источник, где источник вынут из предложения
        """
        def __init__(self, sen_word, source):
            self.sen_word = sen_word
            self.source = source


    def __init__(self, sen_word):
        self.text = sen_word.text
        self.rating = sen_word.rating
        self.word_sources = {hash(sen_word.source): self.WordSource(sen_word, sen_word.source)}

    def involve_new_source(self, sen_word):
        self.rating = self.rating + sen_word.rating
        new_sentence_text = sen_word.source
        if not self.word_sources.get(hash(new_sentence_text)):
            self.word_sources[hash(new_sentence_text)] = self.WordSource(sen_word, new_sentence_text)

    def __add__(self, other):
        result = copy.copy(self)
        result.rating += other.rating
        if result.text == other.text:
            for key in other.word_sources:
                if not result.word_sources.get(key):
                    result.word_sources[key] = other.word_sources[key]
        else:
            raise Exception('Для сложения текст двух элементов должен быть одинаковым')
        return result

    def __str__(self):
        return self.text + " (" + str(self.rating) + ")"


