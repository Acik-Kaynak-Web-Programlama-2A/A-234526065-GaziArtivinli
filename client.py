from socket import * #soket programlama icin modul
from threading import * #coklu is parcacıgı icin modul
from tkinter import *  #kullanıcı arayuzu olusturmak icin modul

client = socket(AF_INET, SOCK_STREAM) #Bir soket nesnesi olusturur ve client adıyla tanımlanır. Istemcinin sunucu ile iletisim kurmasını saglar

ip = '127.0.0.1'
port = 12345

client.connect((ip,port))   #Belirtilen IP adresi ve port numarasına sahip sunucuya bağlantı kurar

pencere = Tk() #Bir Tkinter penceresi oluşturur.
pencere.title("Bağlandı : "   +ip      +" "      + str(port)) # Pencerenin başlığını belirler. Başlık, sunucuya bağlanıldığını gösterir.

message = Text(pencere, width=50) #Bir metin kutusu oluşturur. Bu metin kutusu, sohbet mesajlarını görüntülemek için kullanılacak.
message.grid(row=0,column=0, #0.satır 0. sutun yani sol üst köseye yerlestirir.Padx sol ve sağ üst kenar.Pady sol ve sağ alt kenar 10 pixel boşluk bırakmasını sağlar.
             padx=10, pady=10) #Metin kutusunu pencere içinde düzenlemek için yerleştirme işlemlerini yapar. Ayrıca, kullanıcı adının girileceği bir giriş kutusu da oluşturur.

mesaj_giris= Entry(pencere, width=50) ## Sohbet kutusu olusturur.Ilk hangi pencereye ait olduğu ikincisi genisliği 50px
mesaj_giris.insert(0, "Adınız") # Sohbet Kutusuna Adınız metnini ekler.

mesaj_giris.grid(row=1, column=0,  #Sohbet kutusunu pencere içinde düzenlemek için yerleştirme işlemlerini yapar. 1 satır ekler ust alt kenarlardan 10px
                 padx=10, pady=10)
mesaj_giris.focus() # klavye girislerini sohbet kutusuna dogrudan yönlendirmek icin odaklar.
mesaj_giris.selection_range(0, END) # kullanıcının giriş kutusundaki mevcut içeriği hızlı bir şekilde silmesini ve yeni bir mesaj girmeye yarar.

def mesaj_gonder():
    istemci_mesaji = mesaj_giris.get() # Kullanıcının mesaj kutusuna yazdıgı metni alır ve istemci mesajı adlı değişkende saklar.
    message.insert(END, '\n' + 'Sen :'
                   + istemci_mesaji) #metin kutusuna kullanıcının gönderdiği metni ekler. Bu kullanıcının kendi gönderdiği mesajları metin kutusunda görmesini sağlar. '/n' satır atlama karakteri
    client.send(istemci_mesaji.encode('utf8')) #sunucuya utf8 formatında metni gönderir.
    mesaj_giris.delete(0, END) #giriş kutusunun içeriğini temizler.
    
btn_msg_gonder = Button(pencere, text='Gönder',
                        width=30, 
                        command=mesaj_gonder) #Gonder dugmesini olusturur ve gönder dugmesine tıklanması durumunda 'mesaj_gonder' fonksiyonunu cagırır.
btn_msg_gonder.grid(row=2, column=0, 
                    padx=10, pady=10)

def gelen_mesaj_kontrol(): #gelen mesajları sürekli olarak kontrol eder 
    while True:
        server_msg=client.recv(1024).decode('utf8') # .recv soketten en fazla 1024 bayt veri alır. Alınan metni utf8 formatına cevirir. 
        message.insert(END, '\n'+ server_msg)   #sunucudan gelen mesajları message metin kutusuna ekler.
        
recv_kontrol = Thread(target=gelen_mesaj_kontrol) #mesajları almak için thread oluşturur.
recv_kontrol.daemon = True # Threadi arka plan olarak ayarlar. İş bittiğinde otomatik kapanır.
recv_kontrol.start() # Thread başlatır ve sürekli olarak kontrol eder.
pencere.mainloop()  # tkinter pencereyi ana döngüye alır ve sürekli çalışmasını sağlar. Kullanıcı bu sayede etkileşime geçebilir. Uygulama ya da pencere kapatıldığında bu ana döngüyü sonlandırır.



