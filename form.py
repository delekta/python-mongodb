from tkinter import *
from tkcalendar import *
from pymongo import MongoClient
from password import password as pswd, dbname as db, collection as coll

cluster = MongoClient("mongodb+srv://kamil:" + pswd + "@cluster0.byius.mongodb.net/" +
                      db + "?retryWrites=true&w=majority")

db = cluster[db]
collection = db[coll]


root = Tk()
root.title("Formularz")
root.geometry("500x500")


def submit():
    date_array = cal.get_date().split('.')
    day, month, year = list(map(lambda x: int(x[1:]) if x[0] == '0' else int(x), date_array))

    if collection.find_one({"_id": year}) is not None:
        doc = collection.find_one({"_id": year})

        if str(month) in doc:
            month_dict = doc.get(str(month))
            if str(day) in month_dict:
                print(str(day) + " " + str(month) + " " + str(year) + " " + "Jest już uzupełniona")
            else:
                month_dict.update({str(day): {
                        "income_value": income_value.get(),
                        "spent_value": spent_value.get()
                    }
                })
                # print(doc, "before")
                doc.update({str(month): month_dict})
                # print(doc, "after")
                collection.replace_one({"_id": year}, doc)
        else:
            doc.update({str(month): {
                str(day): {
                    "income_value": income_value.get(),
                    "spent_value": spent_value.get()
                }
            }
            })
            collection.replace_one({"_id": year}, doc)
    else:
        collection.insert_one({
            # Does keys must be string
            "_id": year,
            str(month): {
                str(day): {
                    "income_value": income_value.get(),
                    "spent_value": spent_value.get()
                }
            }
        })

    print(f"You clicked submit! {day, month, year}, {income_value.get()}, {spent_value.get()}")


Label(root, text="Wpisz wartość sprzedaży i zakupu:", font="arial 15 bold").grid(row="0", column="3", pady="20")
Label(root, text="Data:").grid(row="1", column="2")
Label(root, text="Wartość sprzedaży:").grid(row="2", column="2")
Label(root, text="Wartość zakupu:").grid(row="3", column="2")

income_value = IntVar()
spent_value = IntVar()

cal = Calendar(root, selectmode="day", year=2020, month=1, day=1, headersforeground="white",
               selectforeground="red", selectbackground="white", normalforeground="white")
cal.grid(row="1", column="3", pady="20")

Entry(root, textvariable=income_value, fg="red").grid(row="2", column="3", pady="20")
Entry(root, textvariable=spent_value, fg="red").grid(row="3", column="3", pady="20")

Button(text="Zatwierdź", command=submit).grid(row="4", column="3")

root.mainloop()
