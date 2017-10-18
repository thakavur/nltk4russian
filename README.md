# Морфологический анализ русского языка с помощью nltk
# Russian texts tagging with Natural Language Toolkit

## Требования
Установите nltk, pymorphy2, opencorpora-tools. Например, так:

`pip install nltk`

## Установка
Скачайте и распакуйте репозиторий или склонируйте его:

`git clone https://github.com/named-entity/nltk4russian.git`
Затем перейдите в папку *nltk4russian* запустите установочный скрипт:

`python setup.py install`

## Теггеры
В модуле реализованы два варианта разметки:
- выбор наиболее частого разбора с помощью pymorphy2;
- выбор разбора с учетом биграммной модели, если pymorphy дает несколько вариантов разбора.

## Разметка

Можно работать как с теггерами модуля, так и с консольным приложением.

### 1. PMContextTagger и PymorphyTagger

Теггеры наследуются от `nltk.tag.sequential.NgramTagger`, поэтому описание методов можно смотреть в [nltk.tag](http://www.nltk.org/api/nltk.tag.html).
Импортировать их можно обычным образом:

`from nltk4russian.tagger import PMContextTagger`

### 2. Консольное приложение train_tagger

Позволяет обучить заданный теггер на корпусе, разметить заданный корпус.
Параметры запуска:

`  -h, --help            выводит help`

`  -n {1gram,3gram,pymorphy,2gram,pmcontext}, --name {1gram,3gram,pymorphy,2gram,pmcontext}  Название теггера в сокращенном виде.`
                        
`  -f FILE, --file FILE  Корпус для разметки (в plain text или tab-separated формате).`
  
`  -o O                  Выходной файл.`
  
`  -full                 Указывается для обучения и разметки полным тегом.`
  
`  -t T                  Обучающий корпус в tab-separated формате`
  
`  -tab                  Указывается, если корпус для разметки имеет tab-separated формат`
  
В tab-separated формате поля записываются в следующем виде:

- sent (/sent) - указатели начала (конца) предложения;
- номер слова в предложении;
- слово;
в размеченном корпусе далее следуют поле с морфологической информацией: лемма (пока не заполнено), морфологические пометы в формате pymorphy.
