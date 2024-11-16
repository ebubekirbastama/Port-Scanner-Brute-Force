import socket
import time

# Hedef IP
target_ip = "192.168.2.1"  # Hedef IP adresi

# Brute force denemelerinde kullanılacak kullanıcı adı ve şifreler
usernames = ["root", "admin", "user"]
passwords = ["password123", "123456", "admin123"]

# Yaygın olarak kullanılan portlar (Protokoller için)
common_ports = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    80: "HTTP",
    443: "HTTPS",
    110: "POP3",
    143: "IMAP",
    3306: "MySQL",
    3389: "RDP",  # Remote Desktop Protocol (RDP)
}

# Port taraması yapan fonksiyon
def scan_ports(target_ip, port_list):
    open_ports = []
    print(f"Port taraması başlatılıyor: {target_ip} adresi üzerinde belirtilen portlar taranacak...")
    for port, service in port_list.items():
        try:
            # Bağlantı denemesi
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)  # Bağlantı zaman aşımı
            result = s.connect_ex((target_ip, port))
            if result == 0:  # Port açıksa
                open_ports.append((port, service))
                print(f"Port {port} ({service}) açık!")
            s.close()
        except socket.error:
            pass  # Bağlantı hatası, devam et
    return open_ports

# Brute force saldırısını gerçekleştiren fonksiyon
def brute_force_attack(target_ip, open_ports, usernames, passwords):
    if not open_ports:
        print("Açık port bulunamadı. Brute force saldırısı yapılamaz.")
        return
    
    print(f"Açık portlar bulundu: {[port[0] for port in open_ports]}")
    for port, service in open_ports:
        print(f"\nPort {port} ({service}) üzerinde brute force saldırısı başlatılıyor...")
        for username in usernames:
            for password in passwords:
                try:
                    print(f"Deneme: {username}:{password} Port: {port}")
                    # Bağlantıyı kurmaya çalış
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(1)  # Timeout süresi
                        result = s.connect_ex((target_ip, port))
                        if result == 0:
                            print(f"Başarıyla bağlanıldı: {username}:{password} Port: {port} ({service})")
                        else:
                            print(f"Bağlantı hatası: {username}:{password} Port: {port} ({service})")
                except socket.error as err:
                    print(f"Bağlantı hatası: {err}")
                time.sleep(1)  # Fazla yüklenmeme için kısa bir bekleme süresi

# Portları tarayıp açılan portları bulma
print("Port taraması başlatılıyor...")
open_ports = scan_ports(target_ip, common_ports)

# Açık port varsa brute force saldırısını başlat
if open_ports:
    print("\nAçık portlar bulundu, brute force saldırısı başlatılıyor...")
    brute_force_attack(target_ip, open_ports, usernames, passwords)
else:
    print("\nAçık port bulunamadı. Brute force saldırısı yapılamaz.")
