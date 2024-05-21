# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 19:55:20 2023

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

#Veri Ekleme Fonksiyonumuz
def veri_ekle():
    ogrenci_adi = input("Öğrenci Adı: ")
    ogrenci_soyadi = input("Öğrenci Soyadı: ")
    cinsiyet = input("Cinsiyet (Erkek/Kız): ")
    dogum_tarihi = input("Doğum Tarihi (Yıl.Ay.Gün): ")
    basari_puani = float(input("Başarı Puanı: "))

    cursor.execute("INSERT INTO ogrenciler (OgrenciAdi, OgrenciSoyadi, Cinsiyet, DogumTarihi, BasariPuani) VALUES (%s, %s, %s, %s, %s)", (ogrenci_adi, ogrenci_soyadi, cinsiyet, dogum_tarihi, basari_puani))
    mydb.commit()
    print("Öğrenci başarıyla eklendi.")

#Veri Güncelleme Fonksiyonumuz
def veri_guncelle():
    ogrenci_id = input("Güncellenecek Öğrenci ID: ")
    ogrenci_adi = input("Yeni Öğrenci Adı: ")
    ogrenci_soyadi = input("Yeni Öğrenci Soyadi: ")
    cinsiyet = input("Yeni Cinsiyet (Erkek/Kız): ")
    dogum_tarihi = input("Yeni Doğum Tarihi (Yıl.Ay.Gün): ")
    basari_puani = float(input("Yeni Başarı Puanı: "))

    cursor.execute("UPDATE ogrenciler SET OgrenciAdi = %s, OgrenciSoyadi = %s, Cinsiyet = %s, DogumTarihi = %s, BasariPuani = %s WHERE id = %s", 
                   (ogrenci_adi, ogrenci_soyadi, cinsiyet, dogum_tarihi, basari_puani, ogrenci_id))
    mydb.commit()
    print("Öğrenci başarıyla güncellendi.")

#Veri Silme Fonksiyonumuz
def veri_sil():
    idsi = input("Silinecek Öğrenci ID: ")

    cursor.execute("DELETE FROM ogrenciler WHERE id = %s", (idsi,))
    mydb.commit()
    print("Öğrenci başarıyla silindi.")
    
#Verileri Listeleme Fonksiyonumuz
def veri_listele():
    cursor.execute("SELECT * FROM ogrenciler")
    rows = cursor.fetchall()

    print("Öğrenci Listesi")
    print("----------------")
    for row in rows:
        print("ID:",row[0])
        print("Öğrenci Adı:",row[1])
        print("Öğrenci Soyadı:",row[2])
        print("Cinsiyet:", row[3])
        print("Doğum Tarihi:", row[4])
        print("Başarı Puanı:", row[5])
        print("----------------")
        
        
def veri_okuma():
   dosya_adi = input("Okunacak Dosya Adı: ")

   try:
       with open(dosya_adi, "r") as dosya:
           for satir in dosya:
               print(satir)
   except FileNotFoundError:
       print("Belirtilen dosya bulunamadı.")


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    db="projem"
)

cursor = mydb.cursor()

print("Yapmak İstediğiniz İşlemi Seçiniz..")


print("1. Veri Ekle")
print("2. Veri Güncelle")
print("3. Veri Sil")
print("4. Veri Listele")
print("5. Pasta Grafiği")
print("6. Scatter Grafiği")
print("7. Histogram Grafiği")
print("8. Veri Okuma")
menu_secimi = int(input("Seçiniz Lütfen (1-8): "))

if menu_secimi == 1:
    # Veri Ekle
    veri_ekle()

elif menu_secimi == 2:
    # Veri Güncelle
    veri_guncelle()

elif menu_secimi == 3:
    # Veri Sil
    veri_sil()

elif menu_secimi == 4:
    # Veri Listele
    veri_listele()

elif menu_secimi == 5:
    # Pasta Grafiği
    cursor.execute("SELECT Cinsiyet, BasariPuani FROM ogrenciler")
    rows = cursor.fetchall()

    Cinsiyet = []
    BasariPuani = []

    for row in rows:
        Cinsiyet.append(row[0])
        BasariPuani.append(row[1])

    plt.pie(BasariPuani, labels=Cinsiyet, autopct='%1.1f%%')
    plt.title("Öğrencilerin Cinsiyet Dağılımı")
    plt.show()

elif menu_secimi == 6:
    # Scatter Grafiği
    cursor.execute("SELECT Cinsiyet, BasariPuani FROM ogrenciler")
    rows = cursor.fetchall()

    Cinsiyet = []
    BasariPuani = []

    for row in rows:
        Cinsiyet.append(row[0])
        BasariPuani.append(row[1])

    plt.scatter(Cinsiyet, BasariPuani)
    plt.xlabel("Öğrenci Cinsiyetleri")
    plt.ylabel("Öğrenci Başarı Puanları")
    plt.title("Cinsiyete Göre Puan Dağılımları")
    plt.show()

elif menu_secimi == 7:
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
    
    
 
elif menu_secimi == 8:
    # Veri Okuma
    veri_okuma()








else:
    print("Hatalı Seçim!")

cursor.close()
mydb.close()
