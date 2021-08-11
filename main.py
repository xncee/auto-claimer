import os, uuid, subprocess, threading, random, string
clear = lambda: subprocess.call('cls||clear', shell = True)
try:
    import requests
except ImportError:
    os.system("pip install requests")
    import requests
try:
    import autopy
except ImportError:
    os.system("pip install autopy")
    import autopy
class Xnce():
    def __init__(self):
        self.done, self.error, self.run = 0, 0, True
        try:
            self.proxies = list(open("proxies.txt","r").read().split('\n'))
        except:
            print("[-] 'proxies.txt' is missing")
            input()
            exit()
        try:
            self.webhook = open("webhook.txt", "r").read()
            self.dis = True
        except:
            print("[-] 'webhook.txt' is missing")
            self.dis = False
        self.sessionid = input("[+] Sessionid: ")
        self.current_user = {
            "url": "https://i.instagram.com/api/v1/accounts/current_user/?edit=true", 
            "head": {"user-agent": f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}/{''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; en_GB;)", "cookie": f"sessionid={self.sessionid}"}
        }
        self.info()
        print(f"[+] Logged In '{self.username}'")
        self.target = input("[+] Target: ")
        self.edit = {
            "url": "https://www.instagram.com/accounts/edit/", 
            "head": {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36", "x-asbd-id": "437806", "x-csrftoken": "zv2oqqnabfXcWz68VHdVpdhNtpc6KJVz", "x-ig-app-id": "936619743392459", "x-ig-www-claim": "hmac.AR1uhDVWHpujEPjZpqAEgLeWrl-mXAJV-ExZi4lbOalu9MJp", "x-instagram-ajax": "3cda3093f072", "x-requested-with": "XMLHttpRequest", "cookie": f"sessionid={self.sessionid}"}, 
            "data": {"first_name": self.full_name, "email": self.email, "username": self.target, "phone_number": self.phone_number, "biography": self.biography, "external_url": self.external_url, "chaining_enabled": ""}, 
        }
        self.edit_profile = {
            "url": "https://i.instagram.com/api/v1/accounts/edit_profile/", 
            "head": {"user-agent": f"Instagram 195.0.0.0.000 Android (29/10; 300dpi; 720x1440; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}/{''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; en_GB;)", "cookie": f"sessionid={self.sessionid}"}, 
            "data": {"external_url": self.external_url, "phone_number": self.phone_number, "username": self.target, "first_name": self.full_name, "_uid": uuid.uuid4(), "device_id": uuid.uuid4(), "biography": self.biography, "_uuid": uuid.uuid4(), "email": self.email}
        }
        self.set_username = {
            "url": "https://i.instagram.com/api/v1/accounts/set_username/", 
            "head": {"user-agent": f"Instagram 195.0.0.0.000 Android (29/10; 300dpi; 720x1440; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}/{''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; en_GB;)", "cookie": f"sessionid={self.sessionid}"}, 
            "data": {"username": self.target}
        }
        self.att()
        while self.run:
            threading.Thread(target = self.att, daemon = True).start()
    def discord(self):
        if self.dis:
            if len(self.target) <= 4:
                timenow = requests.get("http://worldclockapi.com/api/json/est/now").text
                data = {
                    "embeds": [{
                        "description": f"username: {self.target}", 
                        "color": 1600899, 
                        "author": {"name": "xnce", "icon_url": "https://cdn.discordapp.com/attachments/775671093662449697/870058819902910514/image0.jpg"}, 
                        "timestamp": timenow[30:52]}]}
                req = requests.post(self.webhook, json=data)
                if req.status_code != 204:
                    print(f"\n[-] Discord: {req}")
    def claimed(self):
        print(f"\n[+] Claimed: {self.target}")
        self.discord()
        autopy.alert.alert(f"[+] Claimed: {self.target}", "xnce")
        self.run = False
    def random_proxy(self):
        proxy = random.choice(self.proxies)
        self.my_proxy = {"http": proxy, "https": proxy}
        return self.my_proxy
    def info(self):
        req = requests.get(self.current_user.get("url"), headers=self.current_user.get("head"))
        #print(req.text)
        if "pk" in req.text:
            self.username = req.json()["user"]["username"]
            self.full_name = req.json()["user"]["full_name"]
            self.biography = req.json()["user"]["biography"]
            self.external_url = req.json()["user"]["external_url"]
            self.email = req.json()["user"]["email"]
            self.phone_number = req.json()["user"]["phone_number"]
        else: 
            print(f"[-] {req.text}")
            input()
            exit()
    def att(self):
        urls = [self.edit, self.edit_profile, self.set_username]
        for url in urls:
            try:
                req = requests.post(url.get("url"), headers=url.get("head"), data=url.get("data"), proxies=self.random_proxy())
                #print(req.text, req.status_code)
                if req.status_code == 200:
                    self.claimed()
                elif req.status_code == 400:
                    self.done += 1
                    print(f"\r[+] Done: {self.done} / Error: {self.error}", end = "")
                elif req.status_code == 429:
                    self.error += 1
                    print(f"\r[+] Done: {self.done} / Error: {self.error}", end = "")
            except Exception as err:
                pass
Xnce()
