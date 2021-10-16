import os, uuid, string, random, threading
from queue import Queue

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

class Xnce():
    def __init__(self):
        self.done, self.error, self.run, self.turn = 0, 0, True, 0
        try:
            self.users = list(open("list.txt","r").read().split("\n"))
        except:
            print("[-] list.txt is missing")
            input()
            exit()
        try:
            self.proxies = list(open("proxies.txt","r").read().split("\n"))
        except:
            print("[-] proxies.txt is missing")
            input()
            exit()
        try:
            self.accounts = list(open("accounts.txt","r").read().split("\n"))
        except:
            print("[-] accounts.txt is missing")
            input()
            exit()
        try:
            self.webhook = open("webhook.txt","r").read()
            self.dis = True
        except:
            print("[-] webhook.txt is missing")
        
        self.UQue = Queue()
        for x in self.users:
            self.UQue.put(x)
        
        #print(f"[+] list: {len(self.users)} / proxies: {len(self.proxies)} / accounts: {len(self.accounts)}")
    def claimed(self, username, sessionid):
        print(f"\r[+] claimed: {username}")
        open(f"{username}.txt","a").write(f"username: {username}\nsessionid: {sessionid}")
    def discord(self, username):
        if self.dis:
            if len(username) <= 4:
                timenow = requests.get("http://worldclockapi.com/api/json/est/now").text
                data = {
                    "embeds": [{
                        "description": f"username: {username}", 
                        "color": 1600899, 
                        "author": {"name": "xnce", "icon_url": "https://cdn.discordapp.com/attachments/775671093662449697/870058819902910514/image0.jpg"}, 
                        "timestamp": timenow[30:52]}]}
                req = requests.post(self.webhook, json=data)
                if req.status_code != 204:
                    print(f"\n[-] Discord: {req}")
    def random_proxy(self):
        prox = random.choice(self.proxies)
        proxy = {"http": prox, "https": prox}
        return proxy
    def check(self, username):
        for sessionid in self.accounts:
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
                print(f"\r[+] Done: {self.done} Error: {self.error}", end="")
                self.turn += 1
            elif req.status_code==429:
                self.error += 1
                print(f"\r[+] Done: {self.done} Error: {self.error}", end="")
            elif req.status_code==403:
                self.accounts.remove(sessionid)
                if len(self.accounts) < 1:
                    self.run = False
            else:
                #print(req.text, req.status_code)
                pass
    def main(self):
        while not self.UQue.empty():
            try:
                my_user = self.UQue.get()
                self.check(my_user)
                self.UQue.task_done()
            except:
                pass
    def main2(self):
        while self.run:
            try:
                my_user = self.users[self.turn]
            except:
                self.turn = 0
            try:
                self.check(my_user)
            except:
                pass
x = Xnce()
th = int(input("[+] Threads : "))
input("[+] Enter To Start: ")
t = THRIDING(x.main2)
t.gen(th)
t.start()
t.join()
input("[-] Enter To Exit: ")
exit()
