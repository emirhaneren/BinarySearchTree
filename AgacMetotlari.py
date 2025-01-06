import matplotlib
import matplotlib.pyplot as plt
import networkx as nx

matplotlib.use("TkAgg")

def BSTDiziOlustur(AgacDizisi, inputValue):
    # textbox'tan okunan değerleri BTS yapısına uygun bir diziye aktarır
    if(AgacDizisi[0]==0):#Kok değeri 0 ise gelen değeri başlangıç kök değeri yapar
        AgacDizisi[0]=inputValue
    else:
        kokIndeks = 0
        while kokIndeks < len(AgacDizisi):
            # sol alt ağaca mı ?
            if inputValue < AgacDizisi[kokIndeks]:
                solIndeks = 2 * kokIndeks + 1  # solun indeksini al
                if solIndeks <= len(AgacDizisi) and AgacDizisi[solIndeks] == 0:  # solunda yer var mı ?
                    AgacDizisi[solIndeks] = inputValue #solunda yer varsa yerleş
                    break
                kokIndeks = solIndeks  # yer yoksa solu kök olarak al
                # sağ alt ağaç mı ?
            elif inputValue > AgacDizisi[kokIndeks]:
                    sagIndeks = 2 * kokIndeks + 2  # sağın indeksini al
                    if sagIndeks <= len(AgacDizisi) and AgacDizisi[sagIndeks] == 0:  # sağında yer var mı ?
                        AgacDizisi[sagIndeks] = inputValue
                        break
                    kokIndeks = sagIndeks  # sağında yer varsa yerleş
            else:
                break  #aynı değer varsa ekleme
    return AgacDizisi

def AgacGraphOlustur(graph, AgacDizisi, pos=None, index=0, x=0, y=0, layer=1):
    #ağaç dizisini kullanarak düğümler arasında kenarları oluşturur
    if index >= len(AgacDizisi) or AgacDizisi[index] == 0:
        return pos

    pos = pos or {}
    pos[AgacDizisi[index]] = (x, y)

    # sağ-sol indekslerin hesaplamaları
    left_index = 2 * index + 1
    right_index = 2 * index + 2

    #kendini recursice olarak çağırarak agaç dizisi içerisinde sol ve sağ düğümleri arayarak birer kenar çizer
    if left_index < len(AgacDizisi) and AgacDizisi[left_index] != 0:
        graph.add_edge(AgacDizisi[index], AgacDizisi[left_index])
        AgacGraphOlustur(graph, AgacDizisi, pos, left_index, x - 1 / (2 ** layer), y - 1, layer + 1)
    if right_index < len(AgacDizisi) and AgacDizisi[right_index] != 0:
        graph.add_edge(AgacDizisi[index], AgacDizisi[right_index])
        AgacGraphOlustur(graph, AgacDizisi, pos, right_index, x + 1 / (2 ** layer), y - 1, layer + 1)

    return pos

def AgacCiz(AgacDizisi):
    #ağaç dizisi ile ağacı görsel olarak çizer
    graph = nx.DiGraph()
    pos = {}
    pos = AgacGraphOlustur(graph, AgacDizisi, pos)

    # graph ayarlarını ekleme
    fig, ax = plt.subplots(figsize=(10, 6))
    nx.draw(
        graph, pos, with_labels=True, node_size=800, node_color="lightblue",
        font_size=10, font_weight="bold", arrows=False, ax=ax
    )
    ax.set_title("Binary Search Tree", fontsize=14)

    #eksenleri kapama
    ax.axis("off")
    return fig

def IndexAra(AgacDizisi, arananDeger):
    #ağaç dizisi üzerinde kullancının girdiği değeri arıyoruz
    # ilk kökten başlayarak arıyoruz
    idx = 0
    while idx < len(AgacDizisi):
        if AgacDizisi[idx] == arananDeger:
            return idx  #bulunan değerin indexi
        elif arananDeger < AgacDizisi[idx]:  # Sol alt ağaç
            idx = 2 * idx + 1
        elif arananDeger > AgacDizisi[idx]:  # Sağ alt ağaç
            idx = 2 * idx + 2
    return -1  # değer yoksa -1 dönülür

def DugumBoya(AgacDizisi, boyanacakDugum,renk):
    graph = nx.DiGraph()
    pos = AgacGraphOlustur(graph, AgacDizisi)

    # Sıfır olmayan değerlerden düğüm listesi oluştur
    nodes = [value for value in AgacDizisi if value != 0]

    # Düğüm renklerini ayarla
    node_colors = []
    for idx, value in enumerate(AgacDizisi):
        if idx == boyanacakDugum:  # Highlight edilen indeks kontrolü
            node_colors.append(str(renk))
        elif value != 0:
            node_colors.append("lightblue")

    # Görselleştirme
    fig, ax = plt.subplots(figsize=(10, 6))
    nx.draw(
        graph, pos, with_labels=True, nodelist=nodes, node_size=800, node_color=node_colors,
        font_size=10, font_weight="bold", arrows=False, ax=ax
    )

    ax.set_title("Binary Search Tree", fontsize=14)
    ax.axis("off")  # Eksenleri kapat
    return fig

def DugumSil(AgacDizisi, bulunanIndex):
    idx=bulunanIndex

    left_child = 2 * idx + 1
    right_child = 2 * idx + 2

   # Yaprak düğümse (çocukları yoksa), direkt sil
    if (left_child <= len(AgacDizisi) and AgacDizisi[left_child] == 0) and (right_child <= len(AgacDizisi) and AgacDizisi[right_child] == 0):
        AgacDizisi[idx] = 0
        return AgacDizisi

    # Tek çocuğu olan düğüm
    if (right_child <= len(AgacDizisi) and AgacDizisi[right_child] == 0):# Sadece sol çocuk var
        sol_sol_cocuk =2*left_child+1 #sol çocuk eğer bir ağaçsa bu ağacı yukarı taşımamız gerekiyor
        sol_sag_cocuk =2*left_child+2
        if(sol_sol_cocuk<len(AgacDizisi) and sol_sag_cocuk<len(AgacDizisi) and AgacDizisi[sol_sol_cocuk]!=0 and AgacDizisi[sol_sag_cocuk]!=0):
            AltAgacTasi(AgacDizisi, left_child, idx)
            return AgacDizisi
        else:  
            AgacDizisi[idx] = AgacDizisi[left_child]
            DugumSil(AgacDizisi, left_child)  #sol çocuk bir ağaç değilse sadece sol çocuğu taşı
        
    elif (left_child <= len(AgacDizisi) and AgacDizisi[left_child] == 0):  # Sadece sağ çocuk var
        sag_sol_cocuk =2*right_child+1 #sag çocuk eğer bir ağaçsa bu ağacı yukarı taşımamız gerekiyor
        sag_sag_cocuk =2*right_child+2
        if(sag_sol_cocuk<len(AgacDizisi) and sag_sag_cocuk<len(AgacDizisi) and AgacDizisi[sag_sol_cocuk]!=0 and AgacDizisi[sag_sag_cocuk]!=0):
            AltAgacTasi(AgacDizisi, right_child, idx)
            return AgacDizisi
        else:
            AgacDizisi[idx] = AgacDizisi[right_child]
            DugumSil(AgacDizisi, right_child)  # sağ çocuğu sil
    else:
        # İki çocuğu varsa: sol alt ağaçtan en büyük değeri al
        min_in_left = left_child
        while 2 * min_in_left + 2 < len(AgacDizisi) and AgacDizisi[2 * min_in_left + 2] != 0:
            min_in_left = 2 * min_in_left + 2

        # Bulunan değeri düğümün yerine koy ve sil
        AgacDizisi[idx] = AgacDizisi[min_in_left]
        DugumSil(AgacDizisi, min_in_left)  # Min düğümü sil

    return AgacDizisi

def AltAgacTasi(AgacDizisi, kaynakIndex, hedefIndex,sifirla=0):
    #alt ağacı yukarı taşıma
    
    #bu kontrolü yapmamızdaki amaç fonksiyon kendini tekrarlı çağırdığı için
    #en son adımda hedef indisi 0 olarak setleme sorununun önüne geçmek
    if kaynakIndex >= len(AgacDizisi) or AgacDizisi[kaynakIndex] == 0:
        return

    AgacDizisi[hedefIndex] = AgacDizisi[kaynakIndex]

    # taşınacak indisler ve taşınılacak indisler
    kaynak_sol_cocuk = 2 * kaynakIndex + 1
    kaynak_sag_cocuk = 2 * kaynakIndex + 2
    hedef_sol_cocuk = 2 * hedefIndex + 1
    hedef_sag_cocuk = 2 * hedefIndex + 2

    # Sol alt ağacı taşı
    if kaynak_sol_cocuk < len(AgacDizisi) and AgacDizisi[kaynak_sol_cocuk] != 0:
        AltAgacTasi(AgacDizisi, kaynak_sol_cocuk, hedef_sol_cocuk,1)

    # Sağ alt ağacı taşı
    if kaynak_sag_cocuk < len(AgacDizisi) and AgacDizisi[kaynak_sag_cocuk] != 0:
        AltAgacTasi(AgacDizisi, kaynak_sag_cocuk, hedef_sag_cocuk,1)

    if sifirla==1:
        AgacDizisi[kaynakIndex] = 0
        
def BSTDengeliAgacOlustur(nums, start, end, tree):
    if start > end:
        return -1  #başlangıç bitiş kontrolü

    mid = (start + end) // 2  # dizinin ortasındaki eleman alınır
    root_index = len(tree)  # kök indisi için dizinin uzunluğu alınır
    tree.append(nums[mid])  # Diziye kök elemanı ekle

    # dizinin solu ve sağı için fonksiyon tekrarlı olarak çağırılır
    BSTDengeliAgacOlustur(nums, start, mid - 1, tree)
    BSTDengeliAgacOlustur(nums, mid + 1, end, tree)
    
    return root_index  # kök indis

def AgacDengele(nums):
    DengeliDizi = []  # dengeli numbers dizisi
    BSTDengeliAgacOlustur(nums, 0, len(nums) - 1, DengeliDizi)  # diziyi oluştur
    return DengeliDizi  # numbersı dön