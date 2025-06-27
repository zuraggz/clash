import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('fexburti.sqlite3')
cur = conn.cursor()

def gapitvra(info):
    cur.execute('SELECT * FROM clash_royale_cards WHERE field1 = :z', {"z": info})
    rows = cur.fetchall()
    for row in rows:
        print(row)

def chamateba(*args):
    cur.execute('''
        INSERT INTO clash_royale_cards VALUES (:a, :b, :c, :d, :e, :f, :g, :h, :i)
    ''', {
        "a": args[0],
        "b": args[1],
        "c": int(args[2]),
        "d": args[3],
        "e": args[4],
        "f": args[5],
        "g": int(args[6]),
        "h": int(args[7]),
        "i": float(args[8])
    })
    conn.commit()

def ganaxleba(*args):
    cur.execute("UPDATE clash_royale_cards SET field9 = :z WHERE field2 = :id", {
        "z": float(args[0]),
        "id": args[1]
    })
    conn.commit()

# შეყვანა
x = input("შეიყვანე ქარდის სახელი: ")
y = input("დაამატეთ ახალი ქარდი (მძიმით გამოყოფილი, 9 ველი): ")
z = input("შეიყვანე გასანახლებელი ქარდის ID და შემდეგ სტატისტიკა (გამოყავით მძიმეთი!): ")
w= input("შეიყვანე წასაშლელი ქარდის ID: ")


# ძებნა
gapitvra(x)

# დამატება
dasplituli = y.split(",")
dasstripuli = [element.strip() for element in dasplituli]

if len(dasstripuli) != 9:
    print("‼️ შეცდომა: უნდა შეყვანო ზუსტად 9 მონაცემი მძიმით გამოყოფილი!")
else:
    try:
        chamateba(*dasstripuli)
        print("✅ ქარდი წარმატებით დაემატა!")
    except Exception as e:
        print("‼️ შეცდომა დამატებისას:", e)

# განახლება
dasplituli1 = z.split(",")
dasstripuli1 = [element.strip() for element in dasplituli1]

if len(dasstripuli1) != 2:
    print("‼️ შეცდომა: უნდა შეყვანო ზუსტად 2 მონაცემი მძიმით გამოყოფილი!")
else:
    try:
        ganaxleba(*dasstripuli1)  # ✅ აქ შეცვლილია!
        print("✅ ქარდი წარმატებით განახლდა!")
    except Exception as e:
        print("‼️ შეცდომა განახლებისას:", e)

def washla(aidi):
    cur.execute('DELETE FROM clash_royale_cards WHERE field2 = :z', {"z": aidi})
    conn.commit()


try:
    washla(w)
    print("✅ ქარდი წარმატებით წაიშალა!")
except Exception as e:
    print("‼️ შეცდომა წაშლისას:", e)

conn.close

conn = sqlite3.connect('fexburti.sqlite3')
cur = conn.cursor()


cur.execute("SELECT field5, COUNT(*) FROM clash_royale_cards GROUP BY field5")
rarity_counts = cur.fetchall()
rarity_labels = [row[0] for row in rarity_counts]
rarity_values = [row[1] for row in rarity_counts]

cur.execute("SELECT field4, COUNT(*) FROM clash_royale_cards GROUP BY field4")
elixir_counts = cur.fetchall()
elixir_labels = [row[0] for row in elixir_counts]
elixir_values = [row[1] for row in elixir_counts]


cur.execute("SELECT field1, field6 FROM clash_royale_cards")
winrate_raw = cur.fetchall()


winrate_data = []
for name, rate in winrate_raw:
    try:
        winrate_data.append((name, float(rate)))
    except:
        continue


winrate_data.sort(key=lambda x: x[1], reverse=True)
top10 = winrate_data[:10]
winrate_names = [row[0] for row in top10]
winrate_rates = [row[1] for row in top10]


conn.close()


fig, axs = plt.subplots(3, 1, figsize=(10, 15))
fig.tight_layout(pad=5)


axs[0].bar(rarity_labels, rarity_values, color='skyblue')
axs[0].set_title("ბარათების რაოდენობა იშვიათობის მიხედვით")
axs[0].set_xlabel("იშვიათობა")
axs[0].set_ylabel("რაოდენობა")


axs[1].pie(elixir_values, labels=elixir_labels, autopct='%1.1f%%', startangle=140)
axs[1].set_title("ელიქსირის ფასის მიხედვით ბარათების გადანაწილება")
axs[1].axis('equal')  


axs[2].barh(winrate_names, winrate_rates, color='lightgreen')
axs[2].set_title("გამარჯვების პროცენტული მაჩვენებელი (Top 10)")
axs[2].set_xlabel("Win Rate (%)")
axs[2].invert_yaxis()  

plt.show()