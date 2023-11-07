from socket import *  # ağ soketleri icin
from threading import * #coklu is parcacıgı icin modullerin hepsini aktarır
 
clients = []  # bağlı istemcilerin ve kullanıcı adlarını saklamak icin liste
names = []
 
def clientThread(client):
    bayrak = True  #Bir bayrak (bayrak) oluşturulur ve başlangıçta True olarak ayarlanır.
    while True: #Sonsuz bir döngü başlatılır.
        try:  
            message = client.recv(1024).decode('utf8') #istemciden gelen veriyi utf8 kullanarak cözümler
            if bayrak:
                names.append(message) #names listesine messagedan gelen veriyi ekler.
                print(message, 'bağlandı') #cıktı icin
                bayrak = False  
            for c in clients: #listedeki her istemci icin dongu baslatır
                if c != client: #Eğer döngüdeki istemci, mesajı gönderen istemci değilse
                    index = clients.index(client) #Mesajı gönderen istemcinin indeksini alır.
                    name = names[index] #İstemcinin kullanıcı adını alır.
                    c.send((name + ':' + message).encode('utf8')) #Diğer istemcilere, gönderenin kullanıcı adı ile birlikte mesajı gönderir.
        except:
            index = clients.index(client) #Hata durumunda, istemcinin indeksini alır.
            clients.remove(client) #Hata alan istemciyi clients listesinden kaldırır.
            name=names[index] #İstemcinin kullanıcı adını alır.
            names.remove(name) # Kullanıcı adını names listesinden kaldırır.
            print(name + ' çıktı')
            break
 
 
server = socket(AF_INET, SOCK_STREAM) #TCP ve UDP için IPv4 protokolleri kullanarak TCP soketi olusturur
 
ip = '127.0.0.1' #Sunucunun IP adresini ve port numarasını belirler.
port = 12345
server.bind((ip, port)) #Sunucuyu belirtilen IP ve port ile bağlar.
server.listen() #Bağlantıları dinlemeye başlar.
print('Server dinlemede...')
 
 
while True:
    client, address = server.accept() #Yeni bir istemci bağlantısını kabul eder ve client ve adres bilgisini alır.
    clients.append(client) #Yeni istemci soketini clients listesine ekler.
    print('Bağlantı yapıldı..', address[0] + ':' + str(address[1])) 
    thread = Thread(target=clientThread, args=(client, )) #Yeni istemci için bir iş parçacığı oluşturur ve clientThread işlevini hedefler.
    thread.start() #İş parçacığını başlatır.
    
    