# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 16:47:04 2023

@author: Furkan
"""

import matplotlib.pyplot as plt
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    db="projem"
)

cursor = mydb.cursor()


print("Görüntülemek İstediğiniz Grafiği Seçiniz..")
print("1. Pasta Grafiği")
print("2. Scatter Grafiği")
print("3. Histogram Grafiği")
grafik_secimi = int(input("Seçiniz Lütfen (1-3): "))


if grafik_secimi == 1:
    # Pasta Grafiği
    cursor.execute("SELECT Cinsiyet,BasariPuani FROM ogrenciler")
    rows = cursor.fetchall()

    Cinsiyet = []
    BasariPuani=[]

    for row in rows:
        BasariPuani.append(row[0])
        Cinsiyet.append(row[1])

    plt.pie(Cinsiyet, labels=BasariPuani, autopct='%1.1f%%')
    plt.title("Öğrencilerin Cinsiyet Dağılımı")
    plt.show()

elif grafik_secimi == 2:
    # Scatter Grafiği
    cursor.execute("SELECT Cinsiyet, BasariPuani FROM ogrenciler")
    rows = cursor.fetchall()

    Cinsiyet    = []
    BasariPuani = []

    for row in rows:
        Cinsiyet.append(row[0])
        BasariPuani.append(row[1])

    plt.scatter(Cinsiyet, BasariPuani)
    plt.xlabel("Öğrenci Cinsiyetleri")
    plt.ylabel("Öğrenci Başarı Puanları")
    plt.title("Cinsiyete Göre Puan Dağılımları")
    plt.show()

elif grafik_secimi == 3:
    # Histogram Grafiği
    cursor.execute("SELECT Cinsiyet FROM ogrenciler")
    rows = cursor.fetchall()

    Cinsiyet = []

    for row in rows:
        Cinsiyet.append(row[0])

    plt.hist(Cinsiyet, bins=10)
    plt.xlabel("Cinsiyet Aralığı")
    plt.ylabel("Cinsiyet Dağılımları")
    plt.title("Cinsiyet Dağılımı")
    plt.show()

else:
    print("Hatalı Seçim!")

cursor.close()
mydb.close()
    
            

    
    
    






    
