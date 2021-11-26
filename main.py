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
        open("settings.txt", "w").write(('{"settings" : {\n\t"NAME": "X N C E", \n\t"THREADS": "500",\n\t"MSG": "Claimed"\n}}'))
        settings = json.loads(open("settings.txt", "r").read())
    name = settings["settings"]["NAME"]
    threads = int(settings["settings"]["THREADS"])
    msg = settings["settings"]["MSG"]
    bannerr = requests.get(f'http://artii.herokuapp.com/make?text={name}').text
    print(f"{DESIGN.RED}{bannerr}")
    print(f"\n{DESIGN.blueplus} Successfully Load {DESIGN.BLUE}settings.txt")
class FILES():
    try:
        my_list = list(open("list.txt","r").read().split("\n"))
        print(f"\n{DESIGN.blueplus} Successfully Load {DESIGN.BLUE}list.txt")
    except:
        print(f"\n{DESIGN.redminus} Failed Load {DESIGN.RED}list.txt ", end="")
        input()
        exit()
    try:
        proxies = list(open("proxies.txt","r").read().split("\n"))
        print(f"\n{DESIGN.blueplus} Successfully Load {DESIGN.BLUE}proxies.txt")
    except:
        print(f"\n{DESIGN.redminus} Failed Load {DESIGN.RED}proxies.txt ", end="")
        input()
        exit()
    try:
        accounts = list(open("accounts.txt","r").read().split("\n"))
        print(f"\n{DESIGN.blueplus} Successfully Load {DESIGN.BLUE}accounts.txt")
    except:
        print(f"\n{DESIGN.redminus} Failed Load {DESIGN.RED}accounts.txt ", end="")
        input()
        exit()
    try:
        discord = json.loads(open("discord.txt", "r").read())
    except:
        print(f"\n{DESIGN.redminus} {DESIGN.WHITE}Discord = {DESIGN.RED}False {DESIGN.WHITE}, Failed Load {DESIGN.RED}discord.txt")
        open("discord.txt", "w").write(('{"discord" : {\n\t"image": "",\n\t"title": "#xnce claimer",\n\t"description": "claimed @"\n}}'))
class Xnce():
    def __init__(self):
        self.done, self.error, self.turn, self.aturn, self.run = 0, 0, 0, 0, True
        self.lock = threading.Lock()
        self.rq = requests.Session()
    def claimed(self, username, sessionid):
        print(f"\n\r{DESIGN.blueplus} {SETTINGS.msg} {DESIGN.BLUE}@{username}")
        open(f"{username}.txt","a").write(f"\nusername: {username}\nsessionid: {sessionid}\nattempts: {self.done}\nR/s: {self.Rs}\n")
    def discord(self, username):
        pass
    def random_proxy(self):
        prox = random.choice(FILES.proxies)
        proxy = {"http": prox, "https": prox}
        return proxy
    def remove_user(self, username):
        FILES.my_list.remove(username)
    def remove_session(self, sessionid):
        FILES.accounts.remove(sessionid)
    def check(self):
        if len(FILES.my_list) < 1:
            self.run = False
            print(f"\n{DESIGN.redminus} {DESIGN.WHITE}run = {DESIGN.RED}False {DESIGN.WHITE}, No Users")
            threading.Event.set()
        if len(FILES.accounts) < 1:
            self.run = False
            print(f"\n{DESIGN.redminus} {DESIGN.WHITE}run = {DESIGN.RED}False {DESIGN.WHITE}, No Accounts")
            threading.Event.set()
    def set_username(self, username, sessionid):
            ep = {
                "url": "https://i.instagram.com/api/v1/accounts/set_username/", 
                "head": {"user-agent": f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}/{''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; en_GB;)", "cookie": f"sessionid={sessionid}"}, 
                "data": {"username": username}
            }
            req = self.rq.post(ep.get("url"), headers=ep.get("head"), data=ep.get("data"), proxies=self.random_proxy())
            #print(req.text, req.status_code)
            if '"username"' in req.text and req.status_code==200:
                self.done += 1
                self.remove_session(sessionid)
                self.remove_user(username)
                self.claimed(username, sessionid)
                self.discord(username)
                self.turn += 1
                self.check()
            elif "isn't" in req.text:
                self.done += 1
            elif "already exists" in req.text:
                self.done += 1
            elif req.status_code==429:
                self.error += 1
            elif req.status_code==403:
                self.remove_session(sessionid)
                self.check()
            elif "challenge_required" in req.text or "checkpoint_required" in req.text:
                self.remove_session(sessionid)
                self.check()
            elif '"spam":true' in req.text:
                self.error += 1
            else:
                print(f"\n{DESIGN.redminus} {req.text} {req.status_code}")
            self.rs()
    def rs(self):
        before = self.done
        time.sleep(1)
        after = self.done
        self.Rs = int(after - before)
        os.system(f"title Attempts : {self.done} / Ratelimt : {self.error} / R/s : {self.Rs} / Acc : {len(FILES.accounts)} / @ : {len(FILES.my_list)}")
    def main(self):
        while self.run:
            try:
                my_user = FILES.my_list[self.turn]
                self.turn += 1
            except:
                self.turn = 0
                my_user = FILES.my_list[self.turn]
            try:
                sessionid = FILES.accounts[self.aturn]
                self.aturn += 1
            except:
                self.aturn = 0
            try:
                self.set_username(my_user, sessionid)
            except:
                pass
x = Xnce()
print(f"\n{DESIGN.blueplus} Enter To Start: ", end="")
input()
clear()
print(f"{DESIGN.RED}{SETTINGS.bannerr}")
t = THRIDING(x.main)
t.gen(SETTINGS.threads)
t.start()
t.join()
print(f"\n{DESIGN.redminus} Enter To Exit: ", end="")
input()
exit()
