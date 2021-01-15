import json
from math import sqrt


def prepare_data():
    with open("lab02.json") as json_file:
        dogs = json.load(json_file)
        return dogs


def find_dog(dogs, name):
    for dog in dogs:
        if dog["name"] == name:
            dog1 = dog
    return dog1


def correlation_coefficient(dog1, dog2):
    par1 = [dog1["health"], dog1["intelligence"], dog1["friendliness"], dog1["noise"], dog1["endures_loneliness"]]
    par2 = [dog2["health"], dog2["intelligence"], dog2["friendliness"], dog2["noise"], dog2["endures_loneliness"]]
    if dog2["size"] == 'small':
        par2.append(1)
    elif dog2["size"] == 'medium':
        par2.append(3)
    else:
        par2.append(5)
    if dog2["good_for_apartment"]:
        par2.append(5)
    else:
        par2.append(1)
    if dog1["size"] == 'small':
        par1.append(1)
    elif dog1["size"] == 'medium':
        par1.append(3)
    else:
        par1.append(5)
    if dog1["good_for_apartment"]:
        par1.append(5)
    else:
        par1.append(1)
    avg1 = 0
    avg2 = 0
    for i in range(len(par1)):
        avg1 = avg1 + par1[i]
        avg2 = avg2 + par2[i]
    avg1 = avg1/len(par1)
    avg2 = avg2/len(par2)
    a = 0
    b = 0
    c = 0
    for i in range(len(par1)):
        a = a + (par1[i] - avg1) * (par2[i] - avg2)
        b = b + ((par1[i] - avg1)**2)
        c = c + ((par2[i] - avg2) ** 2)
    cc = a / sqrt(b * c)
    return cc


def make_recommendation_for_one(breed, dogs, n_best_products):
    matches = [(u["name"], correlation_coefficient(breed, u))
               for u in dogs if u != breed]
    best_matches = sorted(matches, key=lambda x_y: (x_y[1], x_y[0]), reverse=True)[:n_best_products]
    print("Породы наиболее похожие на '%s':" % breed['name'])
    for line in best_matches:
        print("-  %6s,  Коэффициент корреляции: %6.4f" % (line[0], line[1]))


def make_recommendation_for_array(array, dogs, n_best_products):
    matches = dict()
    for dog in dogs:
        if dog['name'] not in array:
            matches[dog['name']] = 0
    for dog in array:
        for u in dogs:
            if u['name'] not in array:
                matches[u['name']] = matches[u['name']] + correlation_coefficient(find_dog(dogs, dog), u)
    for k in matches.keys():
        matches[k] = matches[k] / len(array)
    best_matches = sorted(matches.items(), key=lambda item: item[1], reverse=True)[:n_best_products]
    print("Рекомендации на основе массива:")
    for line in best_matches:
        print("-  %6s,  Коэффициент корреляции: %6.4f" % (line[0], line[1]))


def make_recommendation_with_dislikes(array, dogs, dislikes, n_best_products):
    matches = dict()
    for dog in dogs:
        if dog['name'] not in array and dog['name'] not in dislikes:
            matches[dog['name']] = 0
    for dog in array:
        for u in dogs:
            if u['name'] not in array and u['name'] not in dislikes:
                matches[u['name']] = matches[u['name']] + correlation_coefficient(find_dog(dogs, dog), u)
    for k in matches.keys():
        matches[k] = matches[k] / len(array)
    best_matches = sorted(matches.items(), key=lambda item: item[1], reverse=True)[:n_best_products]
    print("Рекомендации на основе массива c дизлайками:")
    for line in best_matches:
        print("-  %6s,  Коэффициент корреляции: %6.4f" % (line[0], line[1]))


def main():
    dogs = prepare_data()
    while True:
        print('\n\n1. Рекомендации по одной породе\n2. Рекомендации на основе массива\n'
              '3. Рекомендации с учетом дизлайков')
        n = int(input())
        if n == 1:
            print("Введите название породы:")
            name = input()
            make_recommendation_for_one(find_dog(dogs, name), dogs, 5)
        if n == 2:
            print("Введите массив через ';':")
            array = [el for el in input().split(';')]
            # array = ['Pug', 'East European Shepherd', 'Australian Shepherd']
            make_recommendation_for_array(array, dogs, 5)
        if n == 3:
            print("Введите массив пород через ';':")
            array = [el for el in input().split(';')]
            print("Введите массив дизлайков через ';':")
            dislikes = [el for el in input().split(';')]
            # dislikes = ['Prague ratter', 'Staffordshire bull terrier']
            make_recommendation_with_dislikes(array, dogs, dislikes, 5)


if __name__ == "__main__":
    main()
