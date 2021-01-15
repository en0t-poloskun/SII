import csv
from math import sqrt


def readfile(filename="C:/Users/User/Desktop/SII/lab03/rates.csv"):
    f = open(filename)
    r = csv.reader(f)
    mentions = dict()
    for line in r:
        user = line[0]
        product = line[1]
        rate = float(line[2])
        if user not in mentions:
            mentions[user] = dict()
        mentions[user][product] = rate
    f.close()
    return mentions


def correlation_coefficient(par1, par2):
    avg1 = 0
    avg2 = 0
    for dim in par1:
        avg1 = avg1 + par1[dim]
    for dim in par2:
        avg2 = avg2 + par2[dim]
    avg1 = avg1 / len(par1)
    avg2 = avg2 / len(par2)
    a = 0
    b = 0
    c = 0
    for dim in par1:
        if dim in par2:
            a = a + (par1[dim] - avg1) * (par2[dim] - avg2)
            b = b + ((par1[dim] - avg1) ** 2)
            c = c + ((par2[dim] - avg2) ** 2)
    try:
        cc = a / sqrt(b * c)
    except ZeroDivisionError:
        cc = 0
    return cc


def make_recommendation(user_id, user_rates, n_best_users, n_best_products):
    matches = [(u, correlation_coefficient(user_rates[user_id], user_rates[u]))
               for u in user_rates if u != user_id]
    best_matches = sorted(matches, key=lambda x_y: (x_y[1], x_y[0]), reverse=True)[:n_best_users]
    print("Пользователи наиболее похожие на '%s':" % user_id)
    for line in best_matches:
        print("  - %6s,  Коэффициент корреляции: %6.4f" % (line[0], line[1]))
    sim = dict()
    sim_all = sum([x[1] for x in best_matches])
    best_matches = dict([x for x in best_matches if x[1] > 0.0])
    for relatedUser in best_matches:
        for product in user_rates[relatedUser]:
            if product not in user_rates[user_id]:
                if product not in sim:
                    sim[product] = 0.0
                sim[product] += user_rates[relatedUser][product] * best_matches[relatedUser]
    for product in sim:
        sim[product] /= sim_all
    best_products = sorted(sim.items(), key=lambda x_y: (x_y[1], x_y[0]), reverse=True)[:n_best_products]
    print("Рекомендации пород:")
    for prodInfo in best_products:
        print("  - %6s,  Коэффициент корреляции: %6.4f" % (prodInfo[0], prodInfo[1]))
    return [(x[0], x[1]) for x in best_products]


def main():
    mentions = readfile()
    while True:
        print('1. Сделать рекомендации\n2. Больше не интересует')
        n = int(input())
        if n == 1:
            print('Введите имя человека для рекомендации:')
            name = input()
            rec = make_recommendation(name, mentions, 5, 5)
        if n == 2:
            print('Введите имя пользователя:')
            name = input()
            print('Введите породу:')
            breed = input()
            mentions[name][breed] = 0


if __name__ == "__main__":
    main()
