import json
import random

import pymorphy2
import re

with open("C:/Users/User/Desktop/SII/lab07/breed.txt", encoding='utf-8') as file:
    breeds = [row.strip() for row in file]
with open("lab02.json", encoding='utf-8') as json_file:
    dogs = json.load(json_file)
morph = pymorphy2.MorphAnalyzer()
session = -1


def parser(s):
    phrase = re.sub(r'[^\w\s]', '', s.lower()).split()
    norm_phrase = list()
    for word in phrase:
        norm_phrase.append(morph.parse(word)[0].normal_form)
    return norm_phrase


def handle(phrase):
    global session
    if len(set(phrase) & {'привет', 'добрый', 'приветствовать', 'здравствуй', 'здравствуйте'}) != 0:
        greed()
        return

    if len(set(phrase) & {'пока'}) != 0:
        print('Пока!')
        exit(0)

    if (len(set(phrase) & {'вывести', 'написать', 'показать', 'перечислить'}) != 0
            and len(set(phrase) & {'список', 'всё', 'весь', 'перечень', 'каталог'}) != 0
            and len(set(phrase) & {'собака', 'порода'}) != 0):
        show_all()
        return

    for i in range(len(breeds)):
        if str(parser(breeds[i]))[1:-1] in str(phrase)[1:-1]:
            if 'рассказать' in phrase:
                print_info(i)
                return
            if ('хотеть' in phrase and len(set(phrase) & {'узнать', 'спросить', 'услышать', 'изучить', 'почитать',
                                                          'расспросить'}) != 0):
                print_info(i)
                return
            session = i
            if 'ты' in phrase and len(set(phrase) & {'нравиться', 'любить'}) != 0:
                do_you_like()
                return
            check_params(phrase)

    if 'собака' in phrase or 'порода' in phrase:
        if 'рассказать' in phrase:
            if len(set(phrase) & {'любой', 'угодный', 'неважно', 'безразличный', 'какойнибудь', 'какойлибо',
                                  'случайный', 'рандомный', 'рандомна'}) != 0:
                get_random()
            else:
                print('О какой породе ты бы хотел узнать?')
                tell_without_breed()
            return
        if ('хотеть' in phrase and len(set(phrase) & {'узнать', 'спросить', 'услышать', 'изучить', 'почитать',
                                                      'расспросить'}) != 0):
            if len(set(phrase) & {'любой', 'угодный', 'неважно', 'безразличный', 'какойнибудь', 'какойлибо',
                                  'случайный', 'рандомный', 'рандомна'}) != 0:
                get_random()
            else:
                print('О какой породе ты бы хотел узнать?')
                tell_without_breed()
                return

    if len(set(phrase) & {'он', 'она', 'собака', 'порода', 'они', 'её', 'его'}) != 0:
        if 'ты' in phrase and len(set(phrase) & {'нравиться', 'любить'}) != 0:
            do_you_like()
            return
        check_params(phrase)

    else:
        print('Прости, я не понимаю, что ты говоришь :(')


def greed():
    print('Привет! Чем могу помочь?')


def show_all():
    print('Вот о каких породах я могу рассказать:')
    for i in range(len(dogs)):
        print(str(i+1) + '. ' + dogs[i]['name'])


def tell_without_breed():
    string = parser(input())
    if len(set(string) & {'любой', 'угодный', 'неважно', 'безразличный', 'какойнибудь', 'какойлибо', 'случайный',
                          'рандомный'}) != 0:
        get_random()
        return
    if (len(set(string) & {'вывести', 'написать', 'показать', 'перечислить'}) != 0
            and len(set(string) & {'список', 'всё', 'весь', 'перечень', 'каталог'}) != 0
            and len(set(string) & {'собака', 'порода'}) != 0):
        show_all()
        tell_without_breed()
        return
    if str(['не', 'знать'])[1:-1] in str(string)[1:-1]:
        get_random()
        return
    for i in range(len(breeds)):
        if str(parser(breeds[i]))[1:-1] in str(string)[1:-1]:
            print_info(i)
            return
    print("Прости, я ничего не знаю об этой породе :(")
    tell_without_breed()


def get_random():
    i = random.randint(0, 50)
    print('Хм... Сейчас что-нибудь придумаю.')
    print_info(i)


def do_you_like():
    if dogs[session]['name'] == 'Мопс':
        print('Я просто ОБОЖАЮ мопсов!')
    elif dogs[session]['size'] == 'small':
        print('Мне больше по душе крупные собаки, из маленьких собак я не равнодушен к мопсам.')
    else:
        print('Да, мне нравится эта порода.')


def check_params(phrase):
    a = ''
    b = ''
    d = 0
    if len(set(phrase) & {'интеллект', 'умный', 'ум', 'умственный', 'неглупый', 'сообразительный', 'смышленый'}) != 0:
        a = morph.parse('умная')[0]
        b = 'Интеллект'
        d = dogs[session]["intelligence"]

    if len(set(phrase) & {'дружелюбие', 'дружелюбный', 'доброжелательный', 'ласковый', 'приветливый', 'добрый',
                          'неагрессивный'}) != 0:
        a = morph.parse('дружелюбная')[0]
        b = 'Дружелюбие'
        d = dogs[session]['friendliness']

    if len(set(phrase) & {'шум', 'шумный', 'громкий', 'лаять'}) != 0:
        a = morph.parse('шумная')[0]
        b = 'Шум от'
        d = dogs[session]['noise']

    if d == 1:
        print('Это совсем не ' + a.inflect({'femn'}).word + ' собака.')
        return
    elif d == 2:
        print('Это не очень ' + a.inflect({'femn'}).word + ' собака.')
        return
    elif d == 3:
        print(b + ' этой собаки на среднем уровне.')
        return
    elif d == 4:
        print('Это очень ' + a.inflect({'femn'}).word + ' собака.')
        return
    elif d == 5:
        print('Это одна из самых ' + a.inflect({'gent', 'plur'}).word + ' собак.')
        return

    if len(set(phrase) & {'здоровье', 'здоровый'}) != 0:
        b = 'со здоровьем.'
        d = dogs[session]["health"]
    if len(set(phrase) & {'одиночество', 'разлука', 'один'}) != 0:
        b = 'с прибыванием в одиночестве.'
        d = dogs[session]["health"]

    if d == 1:
        print('У этой породы очень часто бывают проблемы ' + b)
        return
    elif d == 2:
        print('У этой породы часто бывают проблемы ' + b)
        return
    elif d == 3:
        print('У этой породы иногда бывают проблемы ' + b)
        return
    elif d == 4:
        print('У этой породы редко бывают проблемы ' + b)
        return
    elif d == 5:
        print('У этой породы почти не бывает проблем ' + b)
        return

    if (len(set(phrase) & {'квартира', 'апартаменты'}) != 0
            and len(set(phrase) & {'жить', 'содержать', 'держать', 'проживать', 'обитать'}) != 0):
        if dogs[session]["good_for_apartment"]:
            print('Я считаю, эта порода подходит для жизни в квартире.')
        else:
            print('Я считаю, эта порода не подходит для жизни в квартире.')


def print_info(i):
    global session
    session = i
    info = dogs[i]['name'] + ' - порода собак родом из'
    country = dogs[i]["country_of_origin"].split()
    for c in country:
        info = info + ' ' + morph.parse(c)[0].inflect({'gent'}).word.title()
    info = info + '.\n'
    info = info + 'Характеристики породы:'
    print(info)
    print('Здоровье: ' + str(dogs[i]["health"]) + '/5')
    print('Интеллект: ' + str(dogs[i]["intelligence"]) + '/5')
    print('Дружелюбие: ' + str(dogs[i]["friendliness"]) + '/5')
    print('Шум: ' + str(dogs[i]["noise"]) + '/5')
    print('Отношение к одиночеству: ' + str(dogs[i]["endures_loneliness"]) + '/5')


def main():
    p = True
    while p:
        string = input()
        norm_phrase = parser(string)
        handle(norm_phrase)


if __name__ == "__main__":
    main()
