import os, random, threading, time, json, colorama, subprocess, string
clear = lambda: subprocess.call('cls||clear', shell=True)

colorama.init()

try:
    import requests
except ImportError:
    os.system("pip install requests")
    import requests

class THRIDING():
    def __init__(self, target):
        self.threads_list = []
        self.target = target
    
    def gen(self, threads):
        for i in range(threads):
            t = threading.Thread(target=self.target)
            t.setDaemon(True)
            self.threads_list.append(t)
        return self.threads_list

    def start(self):
        for thread_start in self.threads_list:
            thread_start.start()

    def join(self):
        for thread_join in self.threads_list:
            thread_join.join()
class DESIGN():
    WHITE = '\x1b[1;37;40m'
    YELLOW = '\x1b[1;33;40m'
    RED = '\x1b[1;31;40m'
    BLUE = '\x1b[36m\x1b[40m'
    GREEN = '\x1b[32m\x1b[40m'
    greenplus = f"{WHITE}[ {GREEN}+{WHITE} ]"
    blueplus = f"{WHITE}[ {BLUE}+{WHITE} ]"
    redminus = f"{WHITE}[ {RED}-{WHITE} ]"
    
class SETTINGS():
    try:
        settings = json.loads(open("settings.txt", "r").read())
    except:
        open("settings.txt", "w").write(('{"settings" : {\n\t"NAME": "X N C E", \n\t"THREADS": "100",\n\t"MSG": "Claimed",\n\t"PROXY_MODE": "1",\n\t"WEBHOOK": ""\n}}'))
        settings = json.loads(open("settings.txt", "r").read())
    name = settings["settings"]["NAME"]
    threads = int(settings["settings"]["THREADS"])
    msg = settings["settings"]["MSG"]
    proxy_mode = settings["settings"]["PROXY_MODE"]
    webhook = settings["settings"]["WEBHOOK"]
    bannerr = requests.get(f'http://artii.herokuapp.com/make?text={name}').text
    print(f"{DESIGN.RED}{bannerr}")
    print(f"{DESIGN.greenplus} Successfully Load {DESIGN.BLUE}settings.txt\n")
    try:
        my_list = list(open("list.txt","r").read().split("\n"))
        print(f"{DESIGN.greenplus} Successfully Load {DESIGN.BLUE}list.txt\n")
    except:
        print(f"{DESIGN.redminus} Failed Load {DESIGN.RED}list.txt ", end="")
        input()
        exit()
    try:
        proxies = list(open("proxies.txt","r").read().split("\n"))
        print(f"{DESIGN.greenplus} Successfully Load {DESIGN.BLUE}proxies.txt\n")
    except:
        print(f"{DESIGN.redminus} Failed Load {DESIGN.RED}proxies.txt ", end="")
        input()
        exit()
    try:
        accounts = list(open("accounts.txt","r").read().split("\n"))
        print(f"{DESIGN.greenplus} Successfully Load {DESIGN.BLUE}accounts.txt\n")
    except:
        print(f"{DESIGN.redminus} Failed Load {DESIGN.RED}accounts.txt ", end="")
        input()
        exit()
class Xnce():
    def __init__(self):
        self.done, self.error, self.run, self.turn = 0, 0, True, 0
        self.lock = threading.Lock()
    def claimed(self, username, sessionid):
        print(f"\r{DESIGN.blueplus} {SETTINGS.msg} {DESIGN.BLUE}@{username}\n")
        open(f"{username}.txt","a").write(f"\nusername: {username}\nsessionid: {sessionid}\nattempts: {self.done}\n")
    def discord(self, username):
        if self.dis:
            if len(username) <= 4:
                pass
    def random_proxy(self):
        prox = random.choice(SETTINGS.proxies)
        if SETTINGS.proxy_mode=="1":
            proxy = {"http": prox, "https": prox}
        else:
            proxy = {f"http":f"socks4://{prox}","https":f"socks4://{prox}"}
        return proxy
    def set_username(self, username):
        for sessionid in SETTINGS.accounts:
            ep = {
                "url": "https://i.instagram.com/api/v1/accounts/set_username/", 
                "head": {"user-agent": f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}/{''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; en_GB;)", "cookie": f"sessionid={sessionid}"}, 
                "data": {"username": username}
            }
            req = requests.post(ep.get("url"), headers=ep.get("head"), data=ep.get("data"), proxies=self.random_proxy())
            #print(req.text, req.status_code)
            if '"username"' in req.text and req.status_code==200:
                self.claimed(username, sessionid)
                self.discord(username)
                self.users.remove(username)
                self.accounts.remove(sessionid)
                if len(self.users) < 1:
                    self.run = False
                if len(self.accounts) < 1:
                    self.run = False
            elif req.status_code==400:
                self.done += 1
                self.turn += 1
                os.system(f"title Attempts : {self.done} / Ratelimt : {self.error} / R/s : {self.Rs} / Acc : {len(SETTINGS.accounts)} / @ : {len(SETTINGS.my_list)}")
            elif req.status_code==429:
                self.error += 1
                os.system(f"title Attempts : {self.done} / Ratelimt : {self.error} / R/s : {self.Rs} / Acc : {len(SETTINGS.accounts)} / @ : {len(SETTINGS.my_list)}")
            elif req.status_code==403:
                self.accounts.remove(sessionid)
                if len(self.accounts) < 1:
                    self.run = False
            else:
                #print(req.text, req.status_code)
                pass
    def rs(self):
        before = self.done
        time.sleep(1)
        after = self.done
        self.Rs = int(after - before)
    def main(self):
        while self.run:
            try:
                my_user = SETTINGS.my_list[self.turn]
            except:
                self.turn = 0
            try:
                self.set_username(my_user)
            except:
                pass
            self.rs()
SETTINGS()
x = Xnce()
print(f"{DESIGN.greenplus} Enter To Start: ", end="")
input()
clear()
print(f"{DESIGN.RED}{SETTINGS.bannerr}")
t = THRIDING(x.main)
t.gen(SETTINGS.threads)
t.start()
t.join()
print(f"{DESIGN.redminus} Enter To Exit: ", end="")
input()
exit()
