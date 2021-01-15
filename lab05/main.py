from math import sqrt
import json
from PyQt5 import QtWidgets, uic
import sys

Form, _ = uic.loadUiType("window.ui")


class Ui(QtWidgets.QDialog, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.button1_pressed)
        self.comboBox_3.hide()
        self.comboBox_7.hide()
        self.comboBox_6.hide()
        self.comboBox_5.hide()
        self.comboBox_4.hide()
        self.pushButton_2.hide()
        likes = []
        dislikes = []
        self.pushButton_2.clicked.connect(lambda: self.button2_pressed(likes, dislikes))

    def button1_pressed(self):
        dog = dict()
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
        self.comboBox_3.show()
        self.comboBox_7.show()
        self.comboBox_6.show()
        self.comboBox_5.show()
        self.comboBox_4.show()
        self.pushButton_2.show()

    def button2_pressed(self, likes, dislikes):
        labels = [self.label_6, self.label_13, self.label_12, self.label_10, self.label_11]
        combos = [self.comboBox_3, self.comboBox_7, self.comboBox_6, self.comboBox_5, self.comboBox_4]
        for i in range(len(labels)):
            if combos[i].currentText() == 'Мне нравится':
                likes.append(labels[i].text())
            else:
                dislikes.append(labels[i].text())
        best_matches = make_recommendation_with_dislikes(likes, dislikes, 5)
        labels = [self.label_6, self.label_13, self.label_12, self.label_10, self.label_11]
        for i in range(len(labels)):
            labels[i].setText(best_matches[i][0])


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
