import tkinter as tk
from tkinter import ttk
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# MySQL bağlantısı oluşturma
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="erendb"
)

# Tkkinter uygulama başlatma
window = tk.Tk()

cinsiyet_secenekleri = ["Erkek", "Kadın"]
ogrenim_durumu_secenekleri = ["Ortaokul", "Lise", "Üniversite"]

# Kayıt ekleme işlemi
def add_record():
    name = entry_name.get()
    age = entry_age.get()
    gender = combo_gender.get()
    education = combo_education.get()

    cursor = db.cursor()
    query = "INSERT INTO kisiler (name, age, gender, education) VALUES (%s, %s, %s, %s)"
    values = (name, age, gender, education)
    cursor.execute(query, values)
    db.commit()

    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    combo_gender.set("")
    combo_education.set("")

    refresh_records()
    save_to_excel()

# Kayıtları silme işlemi
def delete_record():
    selected_item = tree.focus()
    if selected_item:
        item_values = tree.item(selected_item, "values")
        record_id = item_values[0]

        cursor = db.cursor()
        query = "DELETE FROM kisiler WHERE ID = %s"
        values = (record_id,)
        cursor.execute(query, values)
        db.commit()

        refresh_records()
        save_to_excel()

# Kayıtları düzenleme işlemi
def edit_record():
    selected_item = tree.focus()
    if selected_item:
        item_values = tree.item(selected_item, "values")
        record_id = item_values[0]

        name = entry_name.get()
        age = entry_age.get()
        gender = combo_gender.get()
        education = combo_education.get()

        cursor = db.cursor()
        query = "UPDATE kisiler SET name = %s, age = %s, gender = %s, education = %s WHERE ID = %s"
        values = (name, age, gender, education, record_id)
        cursor.execute(query, values)
        db.commit()

        entry_name.delete(0, tk.END)
        entry_age.delete(0, tk.END)
        combo_gender.set("")
        combo_education.set("")

        refresh_records()
        save_to_excel()

# Kayıtları görüntüleme işlemi
def refresh_records():
    cursor = db.cursor()
    query = "SELECT * FROM kisiler"
    cursor.execute(query)
    records = cursor.fetchall()

    # Tabloyu temizleme
    tree.delete(*tree.get_children())

    # Kayıtları ekleme
    for record in records:
        tree.insert("", tk.END, values=record)

# Excele kaydetme işlemi
def save_to_excel():
    cursor = db.cursor()
    query = "SELECT id, name, age, gender, education FROM kisiler"
    cursor.execute(query)
    records = cursor.fetchall()

    df = pd.DataFrame(records, columns=["ID", "Name", "Age", "Gender", "Education"])
    df.to_excel("kisiler.xlsx", index=False)

# Histogram 
def plot_histogram():
    cursor = db.cursor()
    query = "SELECT education, COUNT(*) FROM kisiler GROUP BY education"
    cursor.execute(query)
    results = cursor.fetchall()

    labels = [result[0] for result in results]
    counts = [result[1] for result in results]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, counts)
    plt.xlabel("Öğrenim Durumu")
    plt.ylabel("Kayıt Sayısı")
    plt.title("Öğrenim Durumu Dağılımı")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Pasta 
def plot_pie_chart():
    cursor = db.cursor()
    query = "SELECT gender, COUNT(*) FROM kisiler GROUP BY gender"
    cursor.execute(query)
    results = cursor.fetchall()

    labels = [result[0] for result in results]
    counts = [result[1] for result in results]

    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title("Cinsiyet Dağılımı")
    plt.tight_layout()
    plt.show()

# Saçılım 
def plot_scatter_plot():
    cursor = db.cursor()
    query = "SELECT age, education FROM kisiler"
    cursor.execute(query)
    results = cursor.fetchall()

    ages = [result[0] for result in results]
    educations = [result[1] for result in results]

    plt.figure(figsize=(8, 5))
    plt.scatter(educations, ages)
    plt.xlabel("Öğrenim Durumu")
    plt.ylabel("Yaş")
    plt.title("Öğrenim Durumu ve Yaş Arasındaki İlişki")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# GUI
label_name = tk.Label(window, text="Öğrenci İsim:")
label_name.pack()
entry_name = tk.Entry(window)
entry_name.pack()

label_age = tk.Label(window, text=" Öğrenci Yaş:")
label_age.pack()
entry_age = tk.Entry(window)
entry_age.pack()

label_gender = tk.Label(window, text="Öğrenci Cinsiyet:")
label_gender.pack()
combo_gender = ttk.Combobox(window, values=cinsiyet_secenekleri, state="readonly")
combo_gender.pack()

label_education = tk.Label(window, text="Öğrenim Durumu:")
label_education.pack()
combo_education = ttk.Combobox(window, values=ogrenim_durumu_secenekleri, state="readonly")
combo_education.pack()

button_add = tk.Button(window, text="Ekle", command=add_record)
button_add.pack()

button_delete = tk.Button(window, text="Sil", command=delete_record)
button_delete.pack()

button_edit = tk.Button(window, text="Düzenle", command=edit_record)
button_edit.pack()

# Excele kaydet butonu
button_save_excel = tk.Button(window, text="Excele Kaydet", command=save_to_excel)
button_save_excel.pack()

# Histogram  butonu
button_histogram = tk.Button(window, text="Histogram Grafiği", command=plot_histogram)
button_histogram.pack()
#  Pasta Grafiği  butonu
button_pie_chart = tk.Button(window, text="Pasta Grafiği", command=plot_pie_chart)
button_pie_chart.pack()
#  Sacılım Grafiği  butonu
button_scatter_plot = tk.Button(window, text="Saçılım Grafiği", command=plot_scatter_plot)
button_scatter_plot.pack()

# Kayıt listesi
tree = ttk.Treeview(window, columns=("ID", "Name", "Age", "Gender", "Education"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="İsim")
tree.heading("Age", text="Yaş")
tree.heading("Gender", text="Cinsiyet")
tree.heading("Education", text="Öğrenim Durumu")
tree.pack()

refresh_records()
save_to_excel()

window.mainloop()
