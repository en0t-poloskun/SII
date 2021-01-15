from math import sqrt
import json
from PyQt5 import QtWidgets, uic
import sys
import csv

Form, _ = uic.loadUiType("window.ui")
user = ''
likes = []
dislikes = []


class Ui(QtWidgets.QDialog, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.button1_pressed)
        self.label_15.hide()
        self.spinBox_10.hide()
        self.spinBox_9.hide()
        self.spinBox_8.hide()
        self.spinBox_7.hide()
        self.spinBox_6.hide()
        self.pushButton_2.hide()
        self.pushButton_2.clicked.connect(self.button2_pressed)

    def button1_pressed(self):
        global likes, dislikes, user
        likes = []
        dislikes = []
        dog = dict()
        user = self.lineEdit.text()
        dog["health"] = self.spinBox_3.value()
        dog["intelligence"] = self.spinBox.value()
        dog["friendliness"] = self.spinBox_2.value()
        dog["noise"] = self.spinBox_4.value()
        dog["endures_loneliness"] = self.spinBox_5.value()
        size = self.comboBox.currentText()
        if size == 'Маленький':
            dog["size"] = 'small'
        elif size == 'Средний':
            dog["size"] = 'medium'
        else:
            dog["size"] = 'big'
        good_for_apartment = self.comboBox_2.currentText()
        if good_for_apartment == 'Да':
            dog["good_for_apartment"] = True
        else:
            dog["good_for_apartment"] = False
        best_matches = make_recommendation_for_one(dog, 5)
        labels = [self.label_6, self.label_13, self.label_12, self.label_10, self.label_11]
        for i in range(len(labels)):
            labels[i].setText(best_matches[i][0])
        self.label_15.show()
        self.spinBox_10.show()
        self.spinBox_9.show()
        self.spinBox_8.show()
        self.spinBox_7.show()
        self.spinBox_6.show()
        self.pushButton_2.show()

    def button2_pressed(self):
        global likes, dislikes
        labels = [self.label_6, self.label_13, self.label_12, self.label_10, self.label_11]
        spins = [self.spinBox_10, self.spinBox_9, self.spinBox_8, self.spinBox_7, self.spinBox_6]
        save(labels, spins)
        for i in range(len(labels)):
            if spins[i].value() > 2:
                likes.append(labels[i].text())
            else:
                dislikes.append(labels[i].text())
        best_matches = make_recommendation_with_dislikes(likes, dislikes, 3)
        user_matches = collaborative_filtering(user, 5, 5)
        labels = [self.label_6, self.label_13, self.label_12, self.label_10, self.label_11]
        for u in user_matches:
            for j in range(len(best_matches)):
                if best_matches[j][0] == u[0]:
                    user_matches.remove(u)
        for i in range(3):
            labels[i].setText(best_matches[i][0])
        for i in range(2):
            labels[i+3].setText(user_matches[i][0])
        print(user)


def save(labels, spins):
    f = open("rates.csv", "a")
    for i in range(len(labels)):
        string = user + ',' + labels[i].text() + ',' + str(spins[i].value()) + '\n'
        f.write(string)
    f.close()


def make_recommendation_with_dislikes(likes, dislikes, n_best_products):
    if len(likes) == 0:
        return make_recommendation_for_array(dislikes, likes)[:-n_best_products]
    best = make_recommendation_for_array(likes, dislikes)
    if len(dislikes) == 0:
        return best[:n_best_products]
    worst = make_recommendation_for_array(dislikes, likes)
    result = list()
    for breed1 in best:
        n = 1
        for breed2 in worst:
            if breed1[0] == breed2[0]:
                result.append((breed1[0], breed1[1] - breed2[1]/n))
                break
            n = n + 1
    best_matches = sorted(result, key=lambda x_y: (x_y[1], x_y[0]), reverse=True)[:n_best_products]
    return best_matches


def make_recommendation_for_array(array, dislikes):
    matches = dict()
    dogs = prepare_data()
    for dog in dogs:
        if dog['name'] not in array and dog['name'] not in dislikes:
            matches[dog['name']] = 0
    for dog in array:
        for u in dogs:
            if u['name'] not in array and u['name'] not in dislikes:
                matches[u['name']] = matches[u['name']] + correlation_coefficient(find_dog(dogs, dog), u)
    for k in matches.keys():
        matches[k] = matches[k] / len(array)
    best_matches = sorted(matches.items(), key=lambda item: item[1], reverse=True)
    return best_matches


def readfile(filename="C:/Users/User/Desktop/SII/rk1/rates.csv"):
    f = open(filename)
    r = csv.reader(f)
    mentions = dict()
    for line in r:
        u = line[0]
        product = line[1]
        rate = float(line[2])
        if u not in mentions:
            mentions[u] = dict()
        mentions[u][product] = rate
    f.close()
    return mentions


def collaborative_filtering(user_id, n_best_users, n_best_products):
    user_rates = readfile()
    matches = [(u, correlation_user(user_rates[user_id], user_rates[u]))
               for u in user_rates if u != user_id]
    best_matches = sorted(matches, key=lambda x_y: (x_y[1], x_y[0]), reverse=True)[:n_best_users]
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
    return [(x[0], x[1]) for x in best_products]


def correlation_user(par1, par2):
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
    try:
        cc = a / sqrt(b * c)
    except ZeroDivisionError:
        cc = 0
    return cc


def prepare_data():
    with open("lab02.json") as json_file:
        dogs = json.load(json_file)
        return dogs


def find_dog(dogs, name):
    for dog in dogs:
        if dog["name"] == name:
            dog1 = dog
    return dog1


def make_recommendation_for_one(breed, n_best_products):
    dogs = prepare_data()
    matches = [(u["name"], correlation_coefficient(breed, u))
               for u in dogs]
    best_matches = sorted(matches, key=lambda x_y: (x_y[1], x_y[0]), reverse=True)[:n_best_products]
    return best_matches


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec())
