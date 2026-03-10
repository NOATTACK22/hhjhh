import os
import json
import base64
import time
import threading
t MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list impor
# Grafik kartı hatalarını önlemek için backend ayarı
os.environ['KIVY_GL_BACKEND'] = 'glew'

from github import Github 
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.config import Config
from kivymd.app import MDApp
from kivymd.uix.screen import ThreeLineListItem

# Uygulama Pencere Ayarları
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

# --- GITHUB AYARLARI ---
GITHUB_TOKEN = "os.environ.get('MY_GITHUB_TOKEN', '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')"
REPO_OWNER = "NOATTACK22"
REPO_NAME  = "noatak1"
DB_FILE    = "database.json"

class LoginScreen(MDScreen):
    pass

class MainDashboard(MDScreen):
    pass

# --- ARARYÜZ TASARIMI (KV) ---
KV = '''
MDScreenManager:
    LoginScreen:
    MainDashboard:

<LoginScreen>:
    name: 'login'
    md_bg_color: 0.01, 0.01, 0.05, 1
    MDBoxLayout:
        orientation: 'vertical'
        padding: "40dp"
        spacing: "20dp"
        MDLabel:
            text: "SUPREME TERMINAL V16"
            halign: "center"
            font_style: "H4"
            text_color: 1, 0, 0, 1
            theme_text_color: "Custom"
            bold: True
        MDTextField:
            id: login_key
            hint_text: "Master Access Key"
            text: "W4YWEKNMEAWK"
            password: True
        MDRaisedButton:
            text: "SİSTEME GİRİŞ"
            pos_hint: {"center_x": .5}
            md_bg_color: 1, 0, 0, 1
            on_release: app.login_check(login_key.text)

<MainDashboard>:
    name: 'dashboard'
    md_bg_color: 0, 0, 0, 1
    MDBottomNavigation:
        panel_color: 0.05, 0.05, 0.1, 1
        text_color_active: 1, 0, 0, 1

        MDBottomNavigationItem:
            name: 'users'
            text: 'Üyeler'
            icon: 'account-group'
            MDBoxLayout:
                orientation: 'vertical'
                MDScrollView:
                    MDList:
                        id: user_list_view

        MDBottomNavigationItem:
            name: 'power'
            text: 'Yetki'
            icon: 'shield-crown'
            MDBoxLayout:
                orientation: 'vertical'
                padding: "10dp"
                spacing: "8dp"
                
                MDGridLayout:
                    cols: 2
                    spacing: "10dp"
                    size_hint_y: None
                    height: "45dp"
                    MDRaisedButton:
                        text: "STOP SİSTEM"
                        md_bg_color: 1, 0, 0, 1
                        on_release: app.toggle_system(False)
                    MDRaisedButton:
                        text: "START SİSTEM"
                        md_bg_color: 0, 0.6, 0, 1
                        on_release: app.toggle_system(True)

                MDTextField:
                    id: target_key
                    hint_text: "Hedef Kullanıcı Key"
                MDTextField:
                    id: new_val
                    hint_text: "Yeni Veri (İsim/Key)"
                
                MDGridLayout:
                    cols: 2
                    spacing: "4dp"
                    MDRaisedButton: 
                        text: "ADMİN YAP"
                        on_release: app.update_user_logic("yetki", "ADMIN")
                    MDRaisedButton: 
                        text: "MOD YAP"
                        on_release: app.update_user_logic("yetki", "MODERATOR")
                    MDRaisedButton: 
                        text: "ÜYE YAP"
                        on_release: app.update_user_logic("yetki", "UYE")
                    MDRaisedButton: 
                        text: "BANLA"
                        md_bg_color: 0.8, 0, 0, 1
                        on_release: app.update_user_logic("yetki", "IZINSIZ")
                    MDRaisedButton: 
                        text: "İSİM DEĞİŞ"
                        on_release: app.update_user_logic("isim")
                    MDRaisedButton: 
                        text: "KEY DEĞİŞ"
                        on_release: app.update_user_logic("key")

                MDRaisedButton:
                    text: "YASAKLI KELİME EKLE"
                    md_bg_color: 0.5, 0, 0.5, 1
                    pos_hint: {"center_x": .5}
                    on_release: app.ban_word()

        MDBottomNavigationItem:
            name: 'global'
            text: 'Global'
            icon: 'earth'
            MDBoxLayout:
                orientation: 'vertical'
                MDScrollView:
                    MDList:
                        id: global_chat_view
                MDBoxLayout:
                    size_hint_y: None
                    height: "60dp"
                    padding: "5dp"
                    MDTextField:
                        id: global_input
                        hint_text: "Mesaj..."
                    MDIconButton:
                        icon: "send"
                        on_release: app.send_msg_logic("global")

        MDBottomNavigationItem:
            name: 'dm'
            text: 'DM'
            icon: 'message-secret'
            MDBoxLayout:
                orientation: 'vertical'
                MDScrollView:
                    MDList:
                        id: dm_chat_view
                MDBoxLayout:
                    size_hint_y: None
                    height: "60dp"
                    padding: "5dp"
                    MDTextField:
                        id: dm_input
                        hint_text: "Key:Mesaj"
                    MDIconButton:
                        icon: "account-arrow-right"
                        on_release: app.send_msg_logic("dm")
'''

class MobileMasterApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        self.db = {} # Yerel veritabanı yedeği
        return Builder.load_string(KV)

    def connect_github(self):
        self.g = Github(GITHUB_TOKEN)
        self.repo = self.g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

    def login_check(self, key):
        if key == "W4YWEKNMEAWK":
            try:
                self.connect_github()
                self.root.current = 'dashboard'
                self.sync_worker("load")
                Clock.schedule_interval(self.auto_sync, 5)
            except Exception as e:
                self.show_msg("BAĞLANTI HATASI", str(e))
        else:
            self.show_msg("HATA", "Master Key Geçersiz!")

    def sync_worker(self, action="load"):
        threading.Thread(target=self._sync_task, args=(action,), daemon=True).start()

    def _sync_task(self, action):
        try:
            # GitHub'dan taze veriyi çek
            f = self.repo.get_contents(DB_FILE)
            sha = f.sha
            content = base64.b64decode(f.content).decode('utf-8')
            fresh_db = json.loads(content)

            if action == "save":
                # Yerel db'deki değişiklikleri GitHub'a it
                updated_json = json.dumps(self.db, indent=4, ensure_ascii=False)
                self.repo.update_file(DB_FILE, "Supreme Sync Update", updated_json, sha)
                # Yeni SHA'yı almak için tekrar çek
                f = self.repo.get_contents(DB_FILE)
                self.db = json.loads(base64.b64decode(f.content).decode('utf-8'))
            else:
                self.db = fresh_db

            # UI Güncellemesini ana thread'de yap
            Clock.schedule_once(lambda dt: self.update_ui())
        except Exception as e:
            print(f"Senkronizasyon Hatası: {e}")

    def auto_sync(self, dt):
        if self.root.current == 'dashboard':
            self.sync_worker("load")

    def toggle_system(self, status):
        self.db["sistem_aktif"] = status
        self.sync_worker("save")
        durum = "AKTİF" if status else "KAPALI"
        self.show_msg("SİSTEM KONTROL", f"Sistem şu an {durum}")

    def update_user_logic(self, field, fixed_val=None):
        scr = self.root.get_screen('dashboard')
        target = scr.ids.target_key.text.strip()
        val = fixed_val if fixed_val else scr.ids.new_val.text.strip()
        
        if target in self.db.get("kullanicilar", {}):
            if field == "key":
                # Key'i değiştirip veriyi yeni key'e taşıyoruz
                self.db["kullanicilar"][val] = self.db["kullanicilar"].pop(target)
            else:
                self.db["kullanicilar"][target][field] = val
            
            self.sync_worker("save")
            self.show_msg("BAŞARILI", f"{target} güncellendi.")
        else:
            self.show_msg("HATA", "Key bulunamadı!")

    def send_msg_logic(self, mode):
        scr = self.root.get_screen('dashboard')
        if mode == "global":
            txt = scr.ids.global_input.text.strip()
            if txt:
                if "global_chat" not in self.db: self.db["global_chat"] = []
                self.db["global_chat"].append({
                    "user": "👑 MASTER", "msg": txt, "time": time.strftime("%H:%M")
                })
                scr.ids.global_input.text = ""
        else:
            txt = scr.ids.dm_input.text.strip()
            if ":" in txt:
                target, msg = txt.split(":", 1)
                if "ozel_mesajlar" not in self.db: self.db["ozel_mesajlar"] = []
                self.db["ozel_mesajlar"].append({
                    "sender": "👑 MASTER", 
                    "receiver": target.strip(), 
                    "msg": msg.strip(), 
                    "time": time.strftime("%H:%M")
                })
                scr.ids.dm_input.text = ""
        
        self.sync_worker("save")

    def ban_word(self):
        word = self.root.get_screen('dashboard').ids.new_val.text.strip()
        if word:
            if "yasakli_kelimeler" not in self.db: self.db["yasakli_kelimeler"] = []
            self.db["yasakli_kelimeler"].append(word.lower())
            self.sync_worker("save")
            self.root.get_screen('dashboard').ids.new_val.text = ""

    def update_ui(self):
        try:
            scr = self.root.get_screen('dashboard')
            # Listeleri temizle
            scr.ids.user_list_view.clear_widgets()
            scr.ids.global_chat_view.clear_widgets()
            scr.ids.dm_chat_view.clear_widgets()

            # Kullanıcılar
            for k, v in self.db.get("kullanicilar", {}).items():
                scr.ids.user_list_view.add_widget(ThreeLineListItem(
                    text=f"ID: {k} | {v.get('isim')}",
                    secondary_text=f"Yetki: {v.get('yetki')} | IP: {v.get('ip')}",
                    tertiary_text=f"Mail: {v.get('eposta')} | Tarih: {v.get('kayit_tarihi')}"
                ))

            # Global Chat
            for m in self.db.get("global_chat", [])[-20:]:
                scr.ids.global_chat_view.add_widget(ThreeLineListItem(
                    text=m.get('user'), secondary_text=m.get('msg'), tertiary_text=m.get('time')
                ))

            # DM Chat
            for d in self.db.get("ozel_mesajlar", [])[-20:]:
                scr.ids.dm_chat_view.add_widget(ThreeLineListItem(
                    text=f"{d.get('sender')} -> {d.get('receiver')}", 
                    secondary_text=d.get('msg'), tertiary_text=d.get('time')
                ))
        except:
            pass

    def show_msg(self, title, text):
        MDDialog(title=title, text=text).open()

if __name__ == "__main__":
    MobileMasterApp().run()
