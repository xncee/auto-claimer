import random, threading, uuid, os, string, time, subprocess
clear = lambda: subprocess.call('cls||clear', shell=True)
try:
    import requests
except:
    os.system("pip install requests")
    import requests
try:
    import autopy
except:
    os.system("pip install autopy")
    import autopy
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
class IP():
    ip = requests.get("https://api64.ipify.org").text
    database = requests.get("https://pastebin.com/raw/WCyf6ktJ").text
    if ip not in database:
        print(f"[-] Your IP: {ip}\nPls Contact Devloper\n")
        input()
        exit()
    else:
        print("[+] Loggin Success")
class FILES():
    try:
        accounts = list(open('accounts.txt','r').read().split("\n"))
    except:
        print("[-] accounts.txt is missing ", end="")
        input()
        exit()
    try:
        users = list(open('list.txt','r').read().split("\n"))
    except:
        print("[-] list.txt is missing ", end="")
        input()
        exit()
    try:
        proxies = list(open("proxies.txt", "r").read().split("\n"))
    except:
        print("[-] proxies.txt is missing ", end="")
        input()
        exit()
class AUTO():
    def __init__(self):
        self.done, self.error, self.turn, self.Rs, self.run = 0, 0, 0, 0, True
        self.reqs = requests.Session()
        self.lock = threading.Lock()
        print()
    def discord(self, username):
        webhook = 'https://discord.com/api/webhooks/905804389564973076/8-aUIaigtudPMMulfJ1YeUJc0metd9GHSr42aFDfIV1p02mppa131WI4Q0LMBID13nTI'
        timenow = requests.get("http://worldclockapi.com/api/json/est/now").text
        data = {
                "embeds": [{
                    "description": f"New Claim: {username}\n Attempts : {self.done}\n R/s : {self.CRs}",
                    "color": 000000,
                    "author": {
                        "name": "New Claim",
                        "icon_url": "https://cdn.discordapp.com/attachments/837786141591339073/899980910320037888/photo1634460084.jpeg"},
                    "timestamp": timenow[30:52]}
                    ]}
        req = requests.post(webhook, json=data)
        #if req.status_code!=204:
            #print(f"\n[-] Discord: {req}")
    def claimed(self, username, sessionid):
        self.discord(username)
        open(f"{username}.txt", "a").write(f"username: {username}\nsessionid: {sessionid}\nR/s: {self.Rs}\n")
        print(f"\n[+] Claimed: {username} R/s: {self.CRs}")
    def remove_user(self, username):
        if username in FILES.users:
            FILES.users.remove(username)
    def remove_session(self, sessionid):
        if sessionid in FILES.accounts:
            FILES.accounts.remove(sessionid)
    def set_username(self, username, sessionid):
        head = {
            "user-agent": f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}/{''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k = 16))}; en_GB;)",
            "cookie": f"sessionid={sessionid}"
        } 
        data = {"username": username}
        req = requests.post("https://i.instagram.com/api/v1/accounts/set_username/", headers=head, data=data)
        #print(req.text, req.status_code)
        if '"username"' in req.text and req.status_code==200:
            #with self.lock():
            self.claimed(username, sessionid)
            self.remove_user(username)
            self.remove_session(sessionid)
        elif req.status_code==400:
            print(f"\n[-] Failed To Claim -> {username} '{req.status_code}'")
            #self.remove_user(username)
        elif req.status_code==429:
            print(f"\n[-] Failed To Claim -> {username} '{req.status_code}'")

        elif req.status_code==403:
            print(f"\n[-] Failed To Claim -> {username} 'Bad Sessionid -> {sessionid}'")
            FILES.accounts.remove(sessionid)
        if len(FILES.users) < 1:
            self.run = False
        if len(FILES.accounts) < 1:
            self.run = False
    def random_proxy(self):
        prox = random.choice(FILES.proxies)
        my_proxy = {"http": prox, "https": prox}
        return my_proxy
    def check_username(self, username, sessionid):
        head = {'User-Agent': 'Instagram 207.0.0.39.120 Android (25/7.1.2; 266dpi; 800x1280; samsung; SM-N975F; SM-N975F; intel; ar_EG; 321039115)'}
        data = {"username": username, "_uuid": uuid.uuid4()}
        req = self.reqs.post('https://i.instagram.com/api/v1/users/check_username/', headers=head, data=data, proxies=self.random_proxy())
        if '"available":true' in req.text:
            self.CRs = self.Rs
            self.set_username(username, sessionid)
        elif '"available":false' in req.text:
            self.done += 1
            os.system(f"title Done: {self.done} / Error: {self.error} / R/s {self.Rs}")
            self.turn += 1
        elif req.status_code==429:
            self.error += 1
            os.system(f"title Done: {self.done} / Error: {self.error} / R/s {self.Rs}")
    def rs(self):
        before = self.done
        time.sleep(1)
        after = self.done
        self.Rs = int(after - before)
    def main(self):
        while self.run:
            try:
                my_user = FILES.users[self.turn]
            except:
                self.turn = 0
            my_session = random.choice(FILES.accounts)
            try:
                self.check_username(my_user, my_session)
            except:
                pass
            self.rs()
bnr = requests.get(f'http://artii.herokuapp.com/make?text=N A M E').text
print(bnr)
IP()
FILES()
a = AUTO()
threads = int(input("[+] Threads: "))
print(f"[+] Enter To Start: ", end="")
input()
clear()
print(bnr)
t = THRIDING(a.main)
t.gen(threads)
t.start()
t.join()
print(f"[-] Enter To Exit: ", end="")
input()
exit()
