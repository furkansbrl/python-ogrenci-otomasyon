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
    kayit_yili = input("Kayıt Yılı: ")
    basari_puani = float(input("Başarı Puanı: "))

    cursor.execute("INSERT INTO ogrenciler (OgrenciAdi, OgrenciSoyadi, Cinsiyet, KayitYili, BasariPuani) VALUES (%s, %s, %s, %s, %s)", (ogrenci_adi, ogrenci_soyadi, cinsiyet, kayit_yili, basari_puani))
    mydb.commit()
    print("Öğrenci başarıyla eklendi.")

#Veri Güncelleme Fonksiyonumuz
def veri_guncelle():
    ogrenci_id = input("Güncellenecek Öğrenci ID: ")

    # Veritabanında belirtilen ID'nin var olup olmadığını kontrol ediyoruz
    cursor.execute("SELECT COUNT(*) FROM ogrenciler WHERE id = %s", (ogrenci_id,))
    ogrenci_sayisi = cursor.fetchone()[0]

    if ogrenci_sayisi == 0:
        print("Belirtilen ID'ye sahip bir öğrenci bulunamadı.")
        return

    ogrenci_adi = input("Yeni Öğrenci Adı (Boş bırakmak için Enter'a basınız): ")
    ogrenci_soyadi = input("Yeni Öğrenci Soyadı (Boş bırakmak için Enter'a basınız): ")
    cinsiyet = input("Yeni Cinsiyet (Erkek/Kız) (Boş bırakmak için Enter'a basınız): ")
    kayit_yili = input("Yeni Kayıt Yılı (Boş bırakmak için Enter'a basınız): ")
    basari_puani = input("Yeni Başarı Puanı (Boş bırakmak için Enter'a basınız): ")

    #Kullanıcının girdiği değerleri kontrol ediyoruz ve boş bırakılanları güncellemiyoruz
    if ogrenci_adi:
        cursor.execute("UPDATE ogrenciler SET OgrenciAdi = %s WHERE id = %s", (ogrenci_adi, ogrenci_id))
    if ogrenci_soyadi:
        cursor.execute("UPDATE ogrenciler SET OgrenciSoyadi = %s WHERE id = %s", (ogrenci_soyadi, ogrenci_id))
    if cinsiyet:
        cursor.execute("UPDATE ogrenciler SET Cinsiyet = %s WHERE id = %s", (cinsiyet, ogrenci_id))
    if kayit_yili:
        cursor.execute("UPDATE ogrenciler SET KayitYili = %s WHERE id = %s", (kayit_yili, ogrenci_id))
    if basari_puani:
        try:
            basari_puani = float(basari_puani)
            cursor.execute("UPDATE ogrenciler SET BasariPuani = %s WHERE id = %s", (basari_puani, ogrenci_id))
        except ValueError:
            print("Geçerli bir sayı giriniz.")

    mydb.commit()
    print("Öğrenci başarıyla güncellendi.")



#Veri Silme Fonksiyonumuz
def veri_sil():
    idler = input("Silinecek Öğrenci ID'leri (birden fazla id girecekseniz eğer virgülle ayırın) girin: ")
    id_listesi = idler.split(",")

    ogrenci_sayisi = 0  #Kullanıcının kaç tane ID girdiğini kontrol ediyoruz

    for ogrenci_id in id_listesi:
        cursor.execute("SELECT COUNT(*) FROM ogrenciler WHERE id = %s", (ogrenci_id,))
        ogrenci_sayisi += cursor.fetchone()[0]

    if ogrenci_sayisi == 0:
        print("Belirtilen ID'lere sahip öğrenciler bulunamadı.")
        return

    for ogrenci_id in id_listesi:
        cursor.execute("DELETE FROM ogrenciler WHERE id = %s", (ogrenci_id,))
        mydb.commit()

    print(f"{ogrenci_sayisi} öğrenci başarıyla silindi.")


    
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
        print("Kayıt Yılı:", row[4])
        print("Başarı Puanı:", row[5])
        print("----------------")
        
#Dosya okuma işlemi yapıp dosyları veri tabanına kaydettirme        
def veri_okuma():
    dosya_yolu = input("Okunacak Dosya Yolu: ")
    print("----------------")

    try:
        with open(dosya_yolu, "r", encoding="UTF-8") as dosya:
            veriler = []
            for satir in dosya:
                veri = satir.strip().split(";")
                veriler.append(veri)

            for veri in veriler:
                print(*veri)
        
        print("----------------")
        
        secim = input("Verileri kaydetmek istiyor musunuz? (Evet/Hayır): ")
        if secim.lower() == "evet":
            for veri in veriler:
                ogrenci_adi = veri[0]
                ogrenci_soyadi = veri[1]
                cinsiyet = veri[2]
                kayit_yili = veri[3]
                basari_puani = float(veri[4])

                cursor.execute("INSERT INTO ogrenciler (OgrenciAdi, OgrenciSoyadi, Cinsiyet, KayitYili, BasariPuani) VALUES (%s, %s, %s, %s, %s)",
                               (ogrenci_adi, ogrenci_soyadi, cinsiyet, kayit_yili , basari_puani))
            mydb.commit()

            print("Veriler veritabanına başarıyla eklendi.")
        else:
            print("Veriler kaydedilmedi.")

    except FileNotFoundError:
        print("Belirtilen dosya bulunamadı.")
    except IndexError:
        print("Dosyadaki verilerin formatı hatalı.")


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
print("5. Dosya Okuma")
print("6. Pasta Grafiği")
print("7. Scatter Grafiği")
print("8. Histogram Grafiği")

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
        # Veri Okuma
        veri_okuma()

elif menu_secimi == 6:
    # Pasta Grafiği
    cursor.execute("SELECT COUNT(*) FROM ogrenciler WHERE Cinsiyet = 'Erkek'")
    erkek_sayisi = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM ogrenciler WHERE Cinsiyet = 'Kız'")
    kiz_sayisi = cursor.fetchone()[0]
    
    labels = ['Erkek', 'Kız']
    sizes = [erkek_sayisi, kiz_sayisi]
    colors = ['blue', 'pink']
    
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title("Öğrencilerin Cinsiyet Dağılım Grafiği")
    plt.show()

elif menu_secimi == 7:
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

elif menu_secimi == 8:
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
