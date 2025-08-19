import json
from difflib import get_close_matches as yakin_sonuclari_getir

# Veritabanını yükleme
def veritabanini_yukle():
    with open('C:\\Users\\LenovoPC\\Desktop\\kayra_yz\\database.json', 'r', encoding='utf-8') as dosya:
        return json.load(dosya)

# Veritabanına yazma
def veritabanina_yaz(veriler):
    with open('C:\\Users\\LenovoPC\\Desktop\\kayra_yz\\database.json', 'w', encoding='utf-8') as dosya:
        json.dump(veriler, dosya, indent=2, ensure_ascii=False)

# Benzer soru bulma
def yakin_sonuc_bul(soru, sorular):
    eslesen = yakin_sonuclari_getir(soru, sorular, n=1, cutoff=0.6)
    return eslesen[0] if eslesen else None

# Cevabı bulma
def cevabini_bul(soru, veritabani):
    for soru_cevaplar in veritabani["sorular"]:
        if soru_cevaplar["soru"] == soru:
            return soru_cevaplar["cevap"]
    return None

# ChatCPT ana fonksiyonu
def chat_bot():
    veritabani = veritabanini_yukle()

    while True:
        soru = input("Siz: ")

        if soru.lower() == 'çık':
            print("ChatCPT: Görüşürüz!\n")
            break

        gelen_sonuc = yakin_sonuc_bul(soru, [s["soru"] for s in veritabani["sorular"]])

        if gelen_sonuc:
            verilecek_cevap = cevabini_bul(gelen_sonuc, veritabani)
            print(f"ChatCPT: {verilecek_cevap}\n")
        else:
            print("ChatCPT: Bunu nasıl cevaplayacağımı bilmiyorum. Öğretir misiniz?\n")
            yeni_cevap = input("Öğretmek için yazabilir veya 'geç' diyebilirsiniz: ")

            if yeni_cevap.lower() != 'geç':
                veritabani["sorular"].append({
                    "soru": soru,
                    "cevap": yeni_cevap
                })
                veritabanina_yaz(veritabani)
                print("ChatCPT: Teşekkürler, sayenizde yeni bir şey öğrendim!\n")

if __name__ == '__main__':
    chat_bot()
