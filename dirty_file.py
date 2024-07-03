import csv 

with open(r"c:\Users\allga\Downloads\Новая таблица - Лист1.csv", "r") as csv_f:
    # print(csv_f)
    # print(csv_f.read())
    for i in csv_f.read().split("\t"):
        print(i)