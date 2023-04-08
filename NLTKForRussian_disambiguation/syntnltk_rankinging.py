# Программа использует морфологические данные разбора PyMorphy2 и синтаксические правила для автоматического синтаксического разобра текста на русском языки в NLTK.
# Python 3, NLTK, pymorphy2
# -*- coding: utf-8 -*-
# Это обучающая программа для модуля разрешения неоднозначностей на базе вероятностей поддеревьев (по корпусу) @sukhan
import nltk
from nltk import *
import pymorphy2 as pm
import codecs
from bs4 import BeautifulSoup
import re

## загружаем PyMorphy2
m = pm.MorphAnalyzer()
## открываем (создаем)файл с грамматикой, куда будут записываться правила
f = codecs.open("C:/Users/Dmeezz/AppData/Roaming/nltk_data/grammars/book_grammars/test.fcfg", mode="w", encoding="utf-8")
rules = codecs.open("rules.txt", mode= "r", encoding = "utf-8")
## записываем правила, которые вручную делаем (некоторые на основе правил из АОТ)
for rule in rules:
    f.writelines(rules)

rules.close()
f.close()

def unrussianize(text):
    text = list(text)
    rus_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяѣ'
    for i in text[::-1]:
        if i in rus_alphabet:
            text.remove(i)
    return str(''.join(text))

def ungrammar(dic): # функция убирает грамматические показатели токенов в разборах
    new_dic = {}
    for x in dic.keys():
        new_text = re.sub(r'\[.{,200}?\]', r'', x)
        new_dic[new_text] = new_dic.get(new_text, 0) + dic[x]
    return new_dic

## функция, которая переводит нужную нам информацию из пайморфи в вид, читаемый парсером NLTK
## принимает (токенизированное) словосочетание на входе, записывает правила (lexical productions) в тот же файл с грамматикой

def pm2fcfg (phrase, number): ## phrase - это словосочетание, которое мы разбираем
    m = pm.MorphAnalyzer()
    ## открываем (создаем)файл с грамматикой, куда будут записываться правила
    f1 = codecs.open(f"C:/Users/Dmeezz/AppData/Roaming/nltk_data/grammars/book_grammars/test_{number}.fcfg", mode="w",
                    encoding="utf-8")
    rules = codecs.open("rules.txt", mode="r", encoding="utf-8")
    ## записываем правила, которые вручную делаем (некоторые на основе правил из АОТ)
    for rule in rules:
        f1.writelines(rules)
    rules.close()
    f1.close()

    f = codecs.open(f"C:/Users/Dmeezz/AppData/Roaming/nltk_data/grammars/book_grammars/test_{number}.fcfg", mode= "a", encoding = "utf-8")
    for x in phrase:
        a = m.parse(x) ## a - список возможных вариантов морфологического разбора слова, предлагаемых пайморфи
        ## от части речи зависит, какие признаки отправляются в грамматику, осюда условия
        # print(a)
        for y in a:
            if (y.tag.POS == "NOUN") or (y.tag.POS == "ADJF") or (y.tag.POS == "PRTF"):
                strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", G=" + str(y.tag.gender) + ", NUM=" + str(y.tag.number) + ", PER=3" + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
            elif (y.tag.POS == "ADJS") or (y.tag.POS == "PRTS"):
                strk = str(y.tag.POS) + "[G=" + str(y.tag.gender) + ", NUM=" + str(y.tag.number) + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
            elif (y.tag.POS == "NUMR"):
                strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
            elif (y.tag.POS == "ADVB") or (y.tag.POS == "GRND") or (y.tag.POS == "COMP") or (y.tag.POS == "PRED") or (y.tag.POS == "PRCL") or (y.tag.POS == "INTJ"):
                strk = str(y.tag.POS) + "[NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
            elif (y.tag.POS == "PREP") or (y.tag.POS == "CONJ"):
                strk = str(y.tag.POS) + "[NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
                break
            elif (y.tag.POS == "NPRO") & (y.normal_form != "это")& (y.normal_form != "нечего"):
                if ((y.tag.person[0] == "3") & (y.tag.number == "sing")):
                    strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", G=" + str(y.tag.gender) + ", NUM=" + str(y.tag.number) + ", PER=" + str(y.tag.person)[0] + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                else:
                    strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", NUM=" + str(y.tag.number) + ", PER=" + str(y.tag.person)[0] + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
            elif (y.tag.POS == "VERB")  or (y.tag.POS == "INFN"):
                if (y.tag.tense == "past"):
                    strk = str(y.tag.POS) + "[TR=" + str(y.tag.transitivity) + ", TENSE=" + str(y.tag.tense) + ", G=" + str(y.tag.gender) + ", NUM=" + str(y.tag.number) + ", PER=" + "0" + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                elif (y.tag.POS == "INFN"):
                    strk = str(y.tag.POS) + "[TR=" + str(y.tag.transitivity) + ", TENSE=0, G=0, NUM=0, PER=0, NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                else:
                    strk = str(y.tag.POS) + "[TR=" + str(y.tag.transitivity) + ", TENSE=" + str(y.tag.tense) + ", G=" + "0" + ", NUM=" + str(y.tag.number) + ", PER=" + str(y.tag.person)[0] + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
    f.close()

#загружаем файл с предложениями из OpenCorpora
with open('C:\\Users\\Dmeezz\\PycharmProjects\\pythonProject1\\annot_opcorpora_no_ambig_xml.txt', mode='r', encoding='UTF-8') as example:
    bs_example = BeautifulSoup(example, 'xml')
    sents = bs_example.find_all('source') #вычлениям собственно предложения

    sent_list = [] #список наших предложений, которые будет анализировать парсер
    for sent in sents:
        if len(sent.text.split()) <= 10: #здесь не пропускаются предложения длиной более 10 токенов;
            # можно установить и другие ограничения
            new_text = re.sub(r'[^\w\s]+|[\d]', r'', sent.text).strip() #позволяет убрать из предложения разные элементы, которых парсер не понимает
            # (излишне, т.к. впоследствии всё равно есть try-except)
            sent_list.append(new_text.strip('.'))

'''Запускаем работу парсера на всех отобранных предложениях'''

sum_tree = 0
head_frequency = {}
treeset = {}

for i, text in enumerate(sent_list):
    words = word_tokenize(text.lower()) ## разбиваем словосочетание на токены

    print(words, i)
    try: #это нужно, чтобы парсер не спотыкался на ошибках разбора; они не будут учтены
        pm2fcfg(words, i) ## запускаем функцию, описанную выше
        cp = load_parser(f'grammars/book_grammars/test_{i}.fcfg', trace=0) ## открываем нашу грамматику, смотрим на разбор в консоли или ещё где
        for tree in cp.parse(words):
            for subtree in tree.subtrees(lambda t: t.height() >= 2):
                # print (tree)
                head = subtree.label()
                head_type = re.search(r"'.{,10}?'", str(head))
                head_type_full = head_type[0].replace(" '", "").replace("'", "")
                head_frequency[head_type_full] = head_frequency.get(head_type_full, 0) + 1
                s_tree = unrussianize(str(subtree))
                # print(f'дерево {s_tree}')
                treeset[s_tree] = treeset.get(s_tree, 0) + 1
                sum_tree += treeset[s_tree]  # для общей суммы
    except:
        pass

print(f'Словарь вершин:\n{head_frequency}')
#словарь вершин нужен, чтобы реализовать вероятность каждого поддерева среди всех поддеревьев с такой вершиной

'''записываем словарь вершин в файл'''
with open("C:/Users/Dmeezz/AppData/Roaming/nltk_data/grammars/book_grammars/frequency.txt", mode="w",
                    encoding="utf-8") as tree_head_file:
    tree_head_file.write(str(head_frequency))

treeset_ung = ungrammar(treeset)

#переходим от абсолютной частоты к вероятностям относительно вершины (похоже на биграммы):
for key in treeset_ung.keys():
    head_tree = str(Tree.fromstring(key).label())
    treeset_ung[key] = treeset_ung[key] / head_frequency[head_tree]

#записываем все уникальные деревья с их вероятностью в файл
with open("C:/Users/Dmeezz/AppData/Roaming/nltk_data/grammars/book_grammars/trees_subtrees.txt", mode="w",
                    encoding="utf-8") as tree_file:

    tree_file.write(str(treeset_ung))

print(f'Обучение закончено. Всего {len(treeset)} вариантов разборов с разметкой, {sum_tree} - кол-во рзаборов'
      f' всего (в тч одинковых) и {len(treeset_ung)} деревьев без разметки')
