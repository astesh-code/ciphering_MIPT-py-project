from abc import ABC
from random import randint
from collections import Counter


def key_map(in_fun):
    def g_args(self, key=None):
        if self.key == None:
            self.key = self.__gen_key__()
        if key == None:
            key = self.key
        return in_fun(self, key)
    g_args.__name__ = in_fun.__name__
    g_args.__doc__ = in_fun.__doc__
    g_args.__module__ = in_fun.__module__
    return g_args


class SimpleCode(ABC):
    text = None
    key = None
    uncoded = True

    def __init__(self, text, key=None):
        self.text = text
        self.key = key
        with open('lang.txt', 'r') as file:
            exec(file.read())

    def __def_alph__(self, letter) -> str:
        for alph in self.__lang__.values():
            if letter in alph[0]:
                return alph[0]
            if letter in alph[1]:
                return alph[1]
        else:
            return None

    def __gen_key__():
        pass

    def __change_let__():
        pass

    def code():
        pass

    def decode():
        pass


class Caesar(SimpleCode):

    def __gen_key__(self) -> int:
        return randint(0, 100)

    def __change_let__(self, l, key) -> str:
        alph = self.__def_alph__(l)
        if alph:
            key = (not self.uncoded)*(len(alph)-2*key)+key
            return alph[(alph.find(l)+key) % len(alph)]
        else:
            return l

    @key_map
    def code(self, key=None) -> str:
        self.uncoded = True
        key = int(key)
        return ''.join([self.__change_let__(l, key) for l in self.text])

    @key_map
    def decode(self, key=None) -> str:
        self.uncoded = False
        key = int(key)
        return ''.join([self.__change_let__(l, key) for l in self.text])

    def show_all(self) -> list:
        for lan in self.__lang__.values():
            if list(filter(str.isalpha, list(self.text)))[0].lower() in lan[0]:
                lf = lan[2]
        return [(self.decode(i), lf) for i in range(len(lf))]

    def intel_hack(self) -> str:

        def metric(string, lang) -> int:
            count = Counter(string)
            freq = sum([abs(lang[l]-(count[l]/len(string))*100)
                       for l in lang.keys()])
            return freq

        for lan in self.__lang__.values():
            if list(filter(str.isalpha, list(self.text)))[0].lower() in lan[0]:
                lf = lan[2]
        metrics = [metric(self.decode(i), lf) for i in range(len(lf))]
        self.key = metrics.index(min(metrics))
        return self.decode()


class Vigenere(SimpleCode):
    def __gen_key__(self) -> str:
        lis = [chr(randint(ord('a'), ord('z')))
               for i in range(randint(5, 120))]
        return ''.join(lis)

    def __change_let__(self, pair) -> str:
        l, k = pair[0], pair[1]
        l_al = self.__def_alph__(l)
        k_al = self.__def_alph__(k)
        if l_al:
            key = self.uncoded*(len(l_al)-2*k_al.find(k)-2)+1+k_al.find(k)
            if self.uncoded:
                return l_al[(l_al.find(l)+key) % len(l_al)]
            else:
                return l_al[(l_al.find(l)+key) % len(l_al)]
        else:
            return l

    @key_map
    def code(self, key=None) -> str:
        self.uncoded = True
        pack = list(zip(self.text, key*(len(self.text)//len(key)+1)))
        return ''.join([self.__change_let__(pair) for pair in pack])

    @key_map
    def decode(self, key=None) -> str:
        self.uncoded = False
        pack = list(zip(self.text, self.key*(len(self.text)//len(self.key)+1)))
        return ''.join([self.__change_let__(pair) for pair in pack])


class Vernam():

    def __init__(self, text, key=None):
        self.text = text
        self.key = key
        if key and key[0].isalpha():
            self.key = ' '.join(str(ord(l)) for l in self.key)

    def __gen_key__(self) -> str:
        lis = [str(randint(0, 111206)) for i in range(len(self.text))]
        return ' '.join(lis)

    @key_map
    def code(self, key=None) -> str:
        pairs = list(zip(self.text, key.split()))
        return ' '.join([str(ord(pair[0]) ^ int(pair[1])) for pair in pairs])

    @key_map
    def decode(self, key=None) -> str:
        pairs = list(zip(self.text.split(), key.split()))
        return ''.join([chr(int(pair[0]) ^ int(pair[1])) for pair in pairs])
