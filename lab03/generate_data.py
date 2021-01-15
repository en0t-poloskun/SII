import random


def main():
    with open("C:/Users/User/Desktop/SII/lab03/users.txt") as file:
        users = [row.strip() for row in file]
    with open("C:/Users/User/Desktop/SII/lab03/breeds.txt") as file:
        breeds = [row.strip() for row in file]
    result = open("rates.csv", "w")
    for i in range(len(users)):
        n = random.randint(13, 38)
        k = list(range(0, 50))
        random.shuffle(k)
        for j in range(n):
            string = str(users[i]) + ',' + str(breeds[k[j]]) + ',' + str(random.randint(1.0, 5.0)) + '\n'
            result.write(string)
    result.close()


if __name__ == "__main__":
    main()
