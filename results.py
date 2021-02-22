from tkinter import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pymongo import MongoClient
from password import password as pswd, dbname as db, collection as coll
import pandas as pd
from matplotlib import pyplot as plt

cluster = MongoClient("mongodb+srv://kamil:" + pswd + "@cluster0.byius.mongodb.net/" +
                      db + "?retryWrites=true&w=majority")

db = cluster[db]
collection = db[coll]
all_years = collection.find().distinct("_id")


def get_values_in_arrays(_month, _year):
    _dict = collection.find_one({"_id": _year}).get(str(_month))
    _income_array = []
    _spending_array = []
    dict_array = list(_dict.values())
    day_array = list(_dict.keys())
    for d in dict_array:
        _income_array.append(d['income_value'])
        _spending_array.append(d['spent_value'])
    return _income_array, _spending_array, day_array


def plot_chart():
    month = month_entry.get()
    year = year_entry.get()
    if if_date_exists(month, year):
        month_array = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień",
                       "Październik", "Listopad", "Grudzień"]
        income_array, spending_array, day_array = get_values_in_arrays(month, year)
        # print(day_array)
        # print(income_array, "\n", spending_array)
        # print(len(income_array), len(spending_array))
        # print(sum(income_array), sum(spending_array))

        bottom_frame = Frame(window)
        bottom_frame.grid(row="7", column="2")

        fig = Figure()
        plt1 = fig.add_subplot()
        plt1.plot(day_array, income_array, label="sprzedaż")
        plt1.plot(day_array, spending_array, label="zakup")
        # plt1.title("Sprzedaż/Zakup " + month_array[month - 1] + " " + str(year))
        popup.set("Sprzedaż/Zakup " + month_array[month - 1] + " " + str(year))
        plt1.legend()
        canvas = FigureCanvasTkAgg(fig, bottom_frame)

        canvas.draw()
        canvas.get_tk_widget().grid(row="0", column="0")
        average_income.set("Średnia sprzedaż w miesiącu: " + str(round(sum(income_array) / len(income_array), 2)))
        average_spending.set("Średnie zakup w miesiącu: " + str(round(sum(spending_array) / len(spending_array), 2)))
        sum_income.set("Suma sprzedaży: " + str(sum(income_array)))
        sum_spending.set("Suma zakupów: " + str(sum(spending_array)))


def if_date_exists(month, year):
    print(month, year)
    dict = collection.find_one({"_id": year})
    if dict is not None and str(month) in dict:
        popup.set("")
        average_income.set("")
        average_spending.set("")
        return True
    else:
        popup.set("Nie ma danych o miesiąc: " + str(month) + ", rok: " + str(year) + " w bazie!")
        return False


def display_months(self):
    all_months = list(filter(lambda x: (x != "_id"), collection.find_one({"_id": year_entry.get()}).keys()))
    month_entry.set(all_months[0])
    drop_month = OptionMenu(window, month_entry, *all_months)
    drop_month.grid(row="2", column="2", pady="20")


window = Tk()
window.title("Podsumowanie sprzedaży")
window.geometry("1000x1000")

month_entry = IntVar()
year_entry = IntVar()
popup = StringVar()
average_income = StringVar()
average_spending = StringVar()
sum_income = StringVar()
sum_spending = StringVar()

popup.set("")
average_income.set("")
average_spending.set("")
sum_income.set("")
sum_spending.set("")
year_entry.set(all_years[0])

drop_year = OptionMenu(window, year_entry, *all_years, command=display_months).grid(row="1", column="2", pady="20")

Label(window, text="").grid(row="0", column="0", padx="50")
Label(window, text="Rok: ").grid(row="1", column="1", padx="100")
Label(window, text="Miesiąc: ").grid(row="2", column="1")


# Entry(window, textvariable=year_entry, fg="red").grid(row="1", column="2", pady="20")
# Entry(window, textvariable=month_entry, fg="red").grid(row="2", column="2", pady="20")


Label(window, textvariable=popup, font=("Arial", 25)).grid(row="5", column="2", pady="20")
Label(window, textvariable=average_income, font=("Arial", 15)).grid(row="9", column="2", pady="5")
Label(window, textvariable=average_spending, font=("Arial", 15)).grid(row="10", column="2", pady="5")
Label(window, textvariable=sum_income, font=("Arial", 15)).grid(row="11", column="2", pady="5")
Label(window, textvariable=sum_spending, font=("Arial", 15)).grid(row="12", column="2", pady="5")


Button(text="Rysuj wykres", command=plot_chart).grid(row="4", column="2", padx="100")

window.mainloop()


