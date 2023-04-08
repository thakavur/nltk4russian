# Программа использует морфологические данные разбора PyMorphy2 и синтаксические правила для автоматического синтаксического разобра текста на русском языки в NLTK.
# Python 3, NLTK, pymorphy2
# -*- coding: utf-8 -*-
# Разрешение неоднозначностей - на базе вероятностей поддеревьев (по корпусу) и токенов (по PyMorphy2) @sukhan

import nltk
from nltk import *
import pymorphy2 as pm
import codecs
import ast

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

## функция, которая переводит нужную нам информацию из пайморфи в вид, читаемый парсером NLTK
## принимает (токенизированное) словосочетание на входе, записывает правила (lexical productions) в тот же файл с грамматикой

def pm2fcfg (phrase): ## phrase - это словосочетание, которое мы разбираем
    f = codecs.open("C:/Users/Dmeezz/AppData/Roaming/nltk_data/grammars/book_grammars/test.fcfg", mode= "a", encoding = "utf-8")
    g = codecs.open("C:/Users/Dmeezz/AppData/Roaming/nltk_data/grammars/book_grammars/test_only_tokens.fcfg", mode= "w", encoding = "utf-8")
    global phrase_list
    phrase_list = {} # список всех разборов
    for x in phrase:
        a = m.parse(x) ## a - список возможных вариантов морфологического разбора слова, предлагаемых пайморфи
        ## от части речи зависит, какие признаки отправляются в грамматику, осюда условия
        # print(a)
        x_dict = {} #словарь всех разборов слова
        for y in a:
            if (y.tag.POS == "NOUN") or (y.tag.POS == "ADJF") or (y.tag.POS == "PRTF"):
                strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", G=" + str(y.tag.gender) + ", NF='" + str(y.normal_form) + "'" + ", NUM=" + str(y.tag.number) + ", PER=3" + "] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
                g.writelines(strk)
                x_dict[strk] = y.score
            elif (y.tag.POS == "ADJS") or (y.tag.POS == "PRTS"):
                strk = str(y.tag.POS) + "[G=" + str(y.tag.gender) + ", NF='" + str(y.normal_form) + "'" + ", NUM=" + str(y.tag.number) + "] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
                g.writelines(strk)
                x_dict[strk] = y.score
            elif (y.tag.POS == "NUMR"):
                strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", NF='" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
                g.writelines(strk)
                x_dict[strk] = y.score
            elif (y.tag.POS == "ADVB") or (y.tag.POS == "GRND") or (y.tag.POS == "COMP") or (y.tag.POS == "PRED") or (y.tag.POS == "PRCL") or (y.tag.POS == "INTJ"):
                strk = str(y.tag.POS) + "[NF='" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
                g.writelines(strk)
                x_dict[strk] = y.score
            elif (y.tag.POS == "PREP") or (y.tag.POS == "CONJ"):
                strk = str(y.tag.POS) + "[NF='" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
                g.writelines(strk)
                x_dict[strk] = y.score
                break
            elif (y.tag.POS == "NPRO") & (y.normal_form != "это")& (y.normal_form != "нечего"):
                if ((y.tag.person[0] == "3") & (y.tag.number == "sing")):
                    strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", G=" + str(y.tag.gender) + ", NF='" + str(y.normal_form) + "'" + ", NUM=" + str(y.tag.number) + ", PER=" + str(y.tag.person)[0] + "] -> '" + str(y.word) + "'\n"
                    x_dict[strk] = y.score
                else:
                    strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", NF='" + str(y.normal_form) + "'" + ", NUM=" + str(y.tag.number) + ", PER=" + str(y.tag.person)[0] + "] -> '" + str(y.word) + "'\n"
                    x_dict[strk] = y.score
                f.writelines(strk)
                g.writelines(strk)
            elif (y.tag.POS == "VERB")  or (y.tag.POS == "INFN"):
                if (y.tag.tense == "past"):
                    strk = str(y.tag.POS) + "[G=" + str(y.tag.gender) + ", NF='" + str(y.normal_form) + "'" + ", NUM=" + str(y.tag.number) + ", PER=" + "0" + ", TENSE=" + str(y.tag.tense) + ", TR=" + str(y.tag.transitivity) + "] -> '" + str(y.word) + "'\n"
                    x_dict[strk] = y.score
                elif (y.tag.POS == "INFN"):
                    strk = str(y.tag.POS) + "[G=0" + ", NF='" + str(y.normal_form) + "'" + ", NUM=0" + ", PER=" + "0" + ", TENSE=0" + ", TR=" + str(y.tag.transitivity) + "] -> '" + str(y.word) + "'\n"
                    x_dict[strk] = y.score
                else:
                    strk = str(y.tag.POS) + "[G=0" + ", NF='" + str(y.normal_form) + "'" + ", NUM=" + str(y.tag.number) + ", PER=" + str(y.tag.person)[0] + ", TENSE=" + str(y.tag.tense) + ", TR=" + str(y.tag.transitivity) + "] -> '" + str(y.word) + "'\n"
                    x_dict[strk] = y.score
                f.writelines(strk)
                g.writelines(strk)
        phrase_list[x] = x_dict
    # print('Itogovyi slovary\n')
    # print(phrase_list)
    f.close()
    g.close()


text = input("введите предложение для разбора: ") ## сюда пишется словосочетание для разбора
words = word_tokenize(text.lower()) ## разбиваем словосочетание на токены

# print(f'наши токены:\n{words}')

pm2fcfg(words) ## запускаем функцию, описанную выше
cp = load_parser('grammars/book_grammars/test.fcfg', trace=0) ## открываем нашу грамматику, смотрим на разбор в консоли или ещё где
g1 = codecs.open("C:/Users/Dmeezz/AppData/Roaming/nltk_data/grammars/book_grammars/test_only_tokens.fcfg", mode= "r", encoding = "utf-8")
g1_all = g1.readlines()
#g1 - это файл, в котором отдельно собраны морфологические разборы слов из нашего предложения

'''Блок вычисления вероятностей токенов'''
tree_buchs = []
for tree in cp.parse(words):
    tree_prob = 1
    for word in words:
        for razbor in g1_all:
            # ogr = len(razbor) - len(word) - 6
            new_raz = razbor.split(']')[0]
            new_raz = new_raz.replace('nomn', "'nomn'").replace('gent', "'gent'").replace('datv', "'datv'").replace('accs', "'accs'").replace('ablt', "'ablt'").replace('loct', "'loct'")
            new_raz = new_raz.replace('femn', "'femn'").replace('masc', "'masc'").replace('neut', "'neut'")
            new_raz = new_raz.replace('past', "'past'").replace('pres', "'pres'").replace('futr', "'futr'")
            new_raz = new_raz.replace('plur', "'plur'").replace('sing', "'sing'")
            new_raz = new_raz.replace('tran', "'tran'").replace('intr', "'intr'")
            #замены выше нужны, чтобы сделать разметку в файле грамматики и разметку pymorphy одинаковой
            if new_raz in str(tree) and razbor in phrase_list[word].keys():
                #проверка, что текущий морфологический разбор слова есть как в данном древе, так и в словаре вероятностей такого разбора из pymorphy2
                token_prob = phrase_list[word][razbor]
                tree_prob *= token_prob

    tree_buchs.append((tree_prob, tree)) #составляем список из кортежей вида (вероятность, древо)


def ungrammar(dic): # функция убирает грамматические показатели токенов в разборах
    new_dic = {}
    for x in dic.keys():
        # x = "(XP[]\n  (S[-inv]\n    (NP[C='nomn', G='femn', NUM='sing', +gent]\n      (NP[C='nomn', G='femn', NUM='sing', PER=3]\n        (NOUN[C='nomn', G='femn', NF='', NUM='sing', PER=3]\n          ))\n      (NP[C='gent', G='neut', NUM='sing', PER=3]\n        (NOUN[C='gent', G='neut', NF='', NUM='sing', PER=3]\n          )))\n    (VP[G=0, NUM='sing', PER=3, TR='tran', +objt]\n      (VP[G=0, NUM='sing', PER=3, TR=?tr, +infn]\n        (VP[G=0, NUM='sing', PER=3, TENSE='pres', TR='tran']\n          (VERB[G=0, NF='', NUM='sing', PER=3, TENSE='pres', TR='tran']\n            ))\n        (VP[G=0, NUM=0, PER=0, TENSE=0]\n          (INFN[G=0, NF='', NUM=0, PER=0, TENSE=0, TR='tran']\n            )))\n      (NP[C='accs', G='masc', NUM='sing', PER=3]\n        (NOUN[C='accs', G='masc', NF='', NUM='sing', PER=3] )))))"
        new_text = re.sub(r'\[.{,200}?\]', r'', x)
        # print(f'новая схема{new_text}')
        new_dic[new_text] = new_dic.get(new_text, 0) + dic[x]
    return new_dic

def unrussianize(text): #функция, убирающая русский текст в разборах
    text = list(text)
    rus_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮѣЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    for i in text[::-1]:
        if i in rus_alphabet:
            text.remove(i)
    return str(''.join(text))


with open("C:/Users/Dmeezz/AppData/Roaming/nltk_data/grammars/book_grammars/trees_subtrees.txt", mode="r",
                    encoding="utf-8") as tree_file:
    #  в афйле выше находится словарь из вариантов разборов по корпусу с их весами. Извлекаем, создаём из н их словарь
    tree_string = tree_file.read()
    tree_set = ast.literal_eval(tree_string)

# код для выявления кривых вероятностей в исходном файле (архив)
# for key in tree_set.keys():
#     if tree_set[key] > 1:
#         print('Попалось древо с вероятностью больше 1')
#         print(key, tree_set[key])
print(cp.parse(words))
#считаем кол-во поддеревьев для всех разборов нашего предложения (минимальное число будет взято за мимнимум при перемножении вероятностей - для нормализации)
try:
    min_subtrees = len(list(list(cp.parse(words))[0].subtrees(lambda t: t.height() >= 2)))
except:
    min_subtrees = 0
    print('разборов нет')
for tree in cp.parse(words):
    if len(list(tree.subtrees(lambda t: t.height() >= 3))) < min_subtrees:
        min_subtrees = len(list(tree.subtrees(lambda t: t.height() >= 2)))
print(f'Минимальное число поддеревьев для всех разборов = {min_subtrees}')

# считываем наш словарь вершин деревьев (по корпусу)
with open("C:/Users/Dmeezz/AppData/Roaming/nltk_data/grammars/book_grammars/frequency.txt", mode="r",
                       encoding="utf-8") as file_labels:
    labels_string = file_labels.read()
    labels_set = ast.literal_eval(labels_string)

'''Блок вычисления вероятностей поддеревьев'''

tree_weights = []
chance = 1
subtree_probs = []
for tree in cp.parse(words):
    chance = 1
    subtree_probs = []
    for subtree in tree.subtrees(lambda t: t.height() >= 2): #вычисляем вероятности для каждого поддерева, кроме самых нижних, и собираем их в список
        s_tree = unrussianize(str(subtree)) #убираем русские символы
        new_tree = re.sub(r'\[.{,200}?\]', r'', s_tree) #и грамматические категории
        label = str(Tree.fromstring(new_tree).label())
        if new_tree in tree_set.keys():
            chance1 = tree_set[new_tree] + 1 / labels_set[label] #если нашли поддерево в словаре, даём ему вероятность из словаря
        else:
            chance1 = 1 / labels_set[label] # иначе он получает минимальную вероятность с учётом своей вершины по словарю вершин
        subtree_probs.append(chance1) #запись вероятностей каждого поддерева в список
    subtree_probs.sort(reverse=True) #сортировка списка вероятностей
    # print(f'список вероятностей = {subtree_probs}')
    chance2 = 1
    # чтобы уравнять все деревья по кол-ву поддеревьев (имеет смысл для случаев очень сильной неоднозначности,
    # обычно число поддеревьев одинаково):
    for j in range(min_subtrees):
        chance2 *= subtree_probs[j]
    tree_tuple = (chance2, tree)
    tree_weights.append(tree_tuple) #список вероятностей для каждого дерева разбора нашего предложения

ult_tree_list = [] #новый список, в котором перемножаются вероятности деревьев и токенов
for tr_tuple in tree_buchs:
    for tr_w_tuple in tree_weights:
        if tr_tuple[1] == tr_w_tuple[1]:
            ult_tuple = (tr_tuple[0] * tr_w_tuple[0], tr_tuple[1])
            # ult_tuple = (tr_tuple[0] * tr_w_tuple[0], tr_tuple[1].pformat(margin=300, indent=15))
            if ult_tuple not in ult_tree_list:
                ult_tree_list.append(ult_tuple)

# ult_tree_list = list(set(ult_tree_list)) #убираем одинаковые разборы
ult_tree_list.sort(reverse=True) #сортируем список в порядке убывания вероятностей

# if ult_tree_list[0] == ult_tree_list[1]:
#     print('Одинаковые деревья!!!')

# Печатаем наши деревья по убыванию вероятностей

print('Деревья разбора в порядке убывания вероятностей:\n')
print(f'Всего {len(ult_tree_list)} разборов. Приводим до {min(10, len(ult_tree_list))} первых\n')
for i, trees in enumerate(ult_tree_list):
    print('=======================================================================================')
    print(f'Разбор №{i+1}, вес = {trees[0]}, кол-во поддеревьев = {len(list(trees[1].subtrees(lambda t: t.height() >= 2)))}')
    print(trees[1])
    # trees[1].draw()
    # Tree.fromstring(trees[1]).pprint()
    # Tree.fromstring(trees[1]).pformat()
    # print(trees[1].label())
    # print(f'Поддеревья:')
    # for ttree in list(trees[1].subtrees(lambda t: t.height() >= 3)):
    # trees[1].set_label(str(trees[1].label))
    # print(type(trees[1]))
    # for subtree_0 in trees[1].subtrees():
    #     subtree_0.set_label(str(subtree_0.label()))
    # print(trees[1].productions())

g1.close()
print(sum(labels_set[i] for i in labels_set))