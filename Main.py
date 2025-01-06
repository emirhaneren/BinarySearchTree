import tkinter as tk
from tkinter import messagebox
from AgacMetotlari import BSTDiziOlustur, AgacCiz, IndexAra, DugumBoya,DugumSil,AgacDengele
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def Ciz():
    # textboxtan değerleri al
    inputData = txt_inputDizi.get("1.0", tk.END).strip()
    global numbers #numbers'ı global yapmamız gerekiyor çünkü Ara fonksiyonunda bu listeye ihtiyacımız olacak
    try:
        # textboxtan alınan değerleri , ile ayırarak bir listeye at
        numbers = [int(num.strip()) for num in inputData.split(",") if num.strip()]
    except ValueError:
        messagebox.showerror("Hata", "Lütfen yalnızca sayılardan oluşan bir liste girin!")
        return

    if len(numbers) > 100:
        messagebox.showerror("Hata", "Maksimum 100 elemanlı bir liste girebilirsiniz!")
        return

    # 100 elemanlı bir dizi başlat (hepsi 0)
    AgacDizisi = [0] *(2**25)   #4000 #((2**len(numbers)-1))

    # aldığımız input listesini BST dizisine dönüştür
    for number in numbers:
        AgacDizisi = BSTDiziOlustur(AgacDizisi, number)


    # BST çizimini oluştur
    fig = AgacCiz(AgacDizisi)

    new_window = tk.Toplevel(root)
    new_window.title("Binary Search Tree")
    
    # Matplotlib grafiğini tkinter penceresine yerleştir
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas.draw()
    
    plt.close('all')
    
    # kullanıcının girdiği eleman sayısını gui üzerine yazdırma
    girilenElemanSayisi = len(numbers)
    lbl_inputSayisi.config(text=f"Girilen Toplam Eleman Sayısı : {girilenElemanSayisi}")
    
    #agaç dizisi için gerekli yer ayrılamadığında ağaca eklenen toplam eleman sayısını gui üzerine yazdırır
    eklenenElemanSayisi=0
    for i in range(len(AgacDizisi)):
        if(AgacDizisi[i]!=0):
            eklenenElemanSayisi=eklenenElemanSayisi+1
    lbl_eklenenSayisi.config(text=f"Ağaca Eklenen Eleman Sayısı : {eklenenElemanSayisi}")
            
def Ara():
    #kullanıcıdan alınan değeri ağaçta arar ve eğer o değer varsa o düğümü yeşil renge boyar
    try:
        arananDeger = int(txt_inputAranacak.get())
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin!")
        return
 
    # başlangıçtaki ağaç dizisi
    AgacDizisi = [0] *(2**25)

    # aldığımız input listesini BST dizisine dönüştür
    for number in numbers:
        AgacDizisi = BSTDiziOlustur(AgacDizisi, number)

    # input olarak alınan değerin indexini ara
    bulunanIndex = IndexAra(AgacDizisi, arananDeger)

    new_window = tk.Toplevel(root)
    new_window.title("Arama Sonucu")

    if bulunanIndex != -1:
        fig = DugumBoya(AgacDizisi, bulunanIndex,"green")
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        canvas.draw()
        plt.close('all')
    else:
        messagebox.showinfo("Hata", "Aranan değer bulunamadı !")
  
def Ekle():
    try:
        #eklemeden önce ağaç için değer eklenip eklenmediğine bakmamız gerek
        inputData = txt_inputDizi.get("1.0", tk.END).strip()
        if(inputData == ""):
            messagebox.showerror("Hata","Ağaç Dizisi Boş")
            return
        
        eklenecekDeger = int(txt_inputEklenecek.get())
        inputData = txt_inputDizi.get("1.0", tk.END).strip()
        lastData = inputData + "," + str(eklenecekDeger)
        txt_inputDizi.delete("1.0", tk.END)
        txt_inputDizi.insert("1.0", lastData)
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin!")
        return
    
    if(len(numbers)>=100):
        messagebox.showerror("Hata","Eleman Sayısı 100'den fazla olduğu için yeni eleman eklenemez !!")
    else:
        numbers.append(eklenecekDeger)
    
    # başlangıçtaki ağaç dizisi
    AgacDizisi = [0] *(2**25)

    # aldığımız input listesini BST dizisine dönüştür
    for number in numbers:
        AgacDizisi = BSTDiziOlustur(AgacDizisi, number)
        
    bulunanIndex = IndexAra(AgacDizisi, eklenecekDeger)

    new_window = tk.Toplevel(root)
    new_window.title("Yeni Eklenen Değer")

    fig = DugumBoya(AgacDizisi, bulunanIndex,"yellow")
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas.draw()
    plt.close('all')

def Sil():
    try:
        silinecekDeger = int(txt_inputSilinecek.get())
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin!")
        return 
      
    # başlangıçtaki ağaç dizisi
    AgacDizisi = [0] *(2**25)
    # aldığımız input listesini BST dizisine dönüştür
    for number in numbers:
        AgacDizisi = BSTDiziOlustur(AgacDizisi, number)
 
    # input olarak alınan değerin indexini ara
    bulunanIndex = IndexAra(AgacDizisi, silinecekDeger)
   
    if(bulunanIndex==-1):
        messagebox.showerror("Hata","Aranan Değer Ağaçta Mevcut Değil")
        return
    else:
        #numbers listesinden değeri çıkar
        numbers.remove(silinecekDeger)
        #textboxı güncelleme
        updatedData = ",".join([str(num) for num in numbers])
        txt_inputDizi.delete("1.0", tk.END)
        txt_inputDizi.insert("1.0", updatedData)
   
    AgacDizisi=DugumSil(AgacDizisi,bulunanIndex)
        
    new_window = tk.Toplevel(root)
    new_window.title("Ağaç Güncellendi")

    fig = AgacCiz(AgacDizisi)  # Ağacı çiz
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas.draw()
    plt.close('all')
   
def Dengele():
    inputData = txt_inputDizi.get("1.0", tk.END).strip()
    global numbers #numbers'ı global yapmamız gerekiyor çünkü Ara fonksiyonunda bu listeye ihtiyacımız olacak
    try:
        # textboxtan alınan değerleri , ile ayırarak bir listeye at
        numbers = [int(num.strip()) for num in inputData.split(",") if num.strip()]
    except ValueError:
        messagebox.showerror("Hata", "Lütfen yalnızca sayılardan oluşan bir liste girin!")
        return

    if len(numbers) > 100:
        messagebox.showerror("Hata", "Maksimum 100 elemanlı bir liste girebilirsiniz!")
        return
     
    numbers = AgacDengele(numbers)
    print(numbers)
    # 100 elemanlı bir dizi başlat (hepsi 0)
    AgacDizisi = [0] *(2**25)   #4000 #((2**len(numbers)-1))

    # aldığımız input listesini BST dizisine dönüştür
    for number in numbers:
        AgacDizisi = BSTDiziOlustur(AgacDizisi, number)
    
    fig = AgacCiz(AgacDizisi)

    # kullanıcının girdiği eleman sayısını gui üzerine yazdırma
    girilenElemanSayisi = len(numbers)
    lbl_inputSayisi.config(text=f"Girilen Toplam Eleman Sayısı : {girilenElemanSayisi}")
    
    #agaç dizisi için gerekli yer ayrılamadığında ağaca eklenen toplam eleman sayısını gui üzerine yazdırır
    eklenenElemanSayisi=0
    for i in range(len(AgacDizisi)):
        if(AgacDizisi[i]!=0):
            eklenenElemanSayisi=eklenenElemanSayisi+1
    lbl_eklenenSayisi.config(text=f"Ağaca Eklenen Eleman Sayısı : {eklenenElemanSayisi}")
    
    new_window = tk.Toplevel(root)
    new_window.title("Dengelenmiş Ağaç")

    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas.draw()
    plt.close('all')
     
# GUI penceresi
root = tk.Tk()
root.title("Binary Search Tree")

# kullanıcıdan dizi alınacak input
tk.Label(root, text="Virgüllerle ayrılmış pozitif tamsayıları girin:").pack(pady=5)
txt_inputDizi = tk.Text(root, height=5, width=50)
txt_inputDizi.pack(pady=5)
# çizim butonu
tk.Label(root, text="Ağacı Çiz:").pack(pady=5)
btn_ciz = tk.Button(root, text="Ağacı Çiz", command=Ciz)
btn_ciz.pack(pady=5)
# Ağacı dengele ve çiz
tk.Label(root, text="Ağaç Dengele ve Çiz:").pack(pady=5)
btn_dengele=tk.Button(root,text="Dengele ve Çiz",command=Dengele)
btn_dengele.pack(pady=5)

#kullanıcının girdiği toplam eleman sayısını yazdırma
lbl_inputSayisi = tk.Label(root, text="Girilen Toplam Eleman Sayısı: 0")
lbl_inputSayisi.pack(pady=10)
#ağaca eklenen toplam veri
lbl_eklenenSayisi = tk.Label(root, text="Ağaca Eklenen Eleman Sayısı: 0")
lbl_eklenenSayisi.pack(pady=10)

# aranacak değerin girildiği textbox
tk.Label(root, text="Aranacak değeri girin:").pack(pady=5)
txt_inputAranacak = tk.Entry(root)
txt_inputAranacak.pack(pady=5)
# arama butonu
btn_ara = tk.Button(root, text="Arama Yap", command=Ara)
btn_ara.pack(pady=5)

# eklenecek değerin girildiği textbox
tk.Label(root, text="Eklenecek değeri girin:").pack(pady=5)
txt_inputEklenecek = tk.Entry(root)
txt_inputEklenecek.pack(pady=5)
# ekleme butonu
btn_ekle = tk.Button(root, text="Eleman Ekle", command=Ekle)
btn_ekle.pack(pady=5)

# silinecek değerin girildiği textbox
tk.Label(root, text="Silinecek değeri girin:").pack(pady=5)
txt_inputSilinecek = tk.Entry(root)
txt_inputSilinecek.pack(pady=5)
# ekleme butonu
btn_sil = tk.Button(root, text="Eleman Sil", command=Sil)
btn_sil.pack(pady=5)

# GUI başlatma
root.mainloop()
