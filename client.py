import os
import socket
import sys
import threading
import tkinter
from tkinter.scrolledtext import ScrolledText
import time
from TaoGeKey import TaoGeKey
import yaml

IP=""
PORT=""
ADMIN=""
TCP = ""
num=""
taoGeKey: TaoGeKey

def send(admin,meesage,content):
    send_time = time.strftime("%Y-%m-%c %H:%M:%S",time.localtime(time.time()))
    content.insert(tkinter.END,admin+" "+send_time+"\n",'green')
    content.insert(tkinter.END,"  "+meesage+"\n")
    content.yview_scroll(3,tkinter.UNITS)
def Listen_Claim(content,tcp,TextBox,var,member):
    while(True):
        Text = tcp.recv(2048).decode('utf8')
        if("005" in Text.split(";")):
            Text = Text.split(";")[Text.split(";").index("005")+1]
            content.insert(tkinter.END,Text+"\n",'green')
        elif("006" in Text.split(";")):
            index = Text.split(";").index("006")
            admin = Text.split(";")[index+1]
            message = Text.split(";")[index+2]
            try:
                message = taoGeKey.decodeText(message)
            except:
                message = "无法解析"
            send(admin,message,content)
        elif("007" in Text.split(";")):
            global num
            num = Text.split(";").index("007")
            var.set("聊天室(" + Text.split(";")[num+1] + ")")
            adminlist = Text.split(";")[num+2::]
            member.delete(0,100)
            for i in adminlist:
                if(i==" "):
                    break
                member.insert(tkinter.END,i)
def sendto(admin,meesage,tcp,TextBox):
    if(meesage[-1]=="\n"): meesage = meesage[:-1]
    if(meesage!="\n"):
        Text = "006;"+admin+";"+taoGeKey.encodeText(meesage)
        tcp.send(Text.encode('utf8'))
        TextBox.delete(0.0,tkinter.END)

def main_process():
    root.destroy()
    window = tkinter.Tk()
    window.title('网络聊天室v1.0')
    window.geometry('1000x600')
    var = tkinter.StringVar()
    var.set("聊天室("+num+")")
    window.resizable(False,False)
    content = ScrolledText(window,width = 120,height=35)
    content.tag_config('green',foreground='#008B00')
    member = tkinter.Listbox(window,width = 17,height=24,selectmode=tkinter.BROWSE)
    members = tkinter.Label(window,textvariable=var,font=('',10))
    Text_Box = tkinter.Text(window,width=120,height=5)
    sendbnt = tkinter.Button(window,text="发送",font=('',16),command=lambda:sendto(ADMIN,Text_Box.get(0.0,tkinter.END),TCP,Text_Box),width='10')
    window.bind("<Return>", lambda event:sendto(ADMIN,Text_Box.get(0.0,tkinter.END),TCP,Text_Box))
    content.grid()
    member.place(x=860,y=25)
    sendbnt.place(x=860,y=500)
    members.place(x=860,y=5)
    Text_Box.place(x=5,y=490)
    #Text = "欢迎" + ADMIN + "加入聊天室"
    #content.insert(tkinter.END, Text + "\n", 'green')
    t = threading.Thread(target=Listen_Claim,args=(content,TCP,Text_Box,var,member))
    t.start()
    window.mainloop()
def Port(ip,port,admin,var,key):
    if(key == ""):
        key = "123456"
    global taoGeKey
    taoGeKey = TaoGeKey(key)
    str = "003;"+admin+";NULL"
    tcp = socket.socket()
    addr = (ip,eval(port))
    try:
        tcp.connect(addr)
    except:
        print("服务器离线")
        var.set('服务器离线')
    RecvData = tcp.recv(2048).decode("utf8")
    if("001" in RecvData.split(";")):
        print("连接成功")
        tcp.send(str.encode('gbk'))
        Code = tcp.recv(2048).decode("utf8")
        if("001" in Code.split(";")):
            print("登录成功")
            var.set("登录成功")
            global IP,PORT,ADMIN,TCP
            IP = ip
            PORT = port
            ADMIN = admin
            TCP = tcp
            time.sleep(0.5)
            main_process()
        elif("002" in Code.split(";")):
            print("登录失败")
            var.set("登录失败")
# def reg(ip,port,admin,var):
#     str = "004;" + admin + ";" +";NULL"
#     tcp = socket.socket()
#     addr = (ip, eval(port))
#     try:
#         tcp.connect(addr)
#     except:
#         print("服务器离线")
#         var.set('服务器离线')
#     RecvData = tcp.recv(2048).decode("utf8")
#     if (RecvData == "001"):
#         print("连接成功")
#         tcp.send(str.encode('utf8'))
#         Code = tcp.recv(2048).decode("utf8")
#         if (Code == "001"):
#             print("注册成功")
#             var.set("注册成功")
#         elif(Code == "002"):
#             print("注册失败，该用户已存在")
#             var.set("该用户已存在")

def getIpAndPort(path):
    with open(path,"r") as f:
        data = yaml.safe_load(f)
    return {"ip":data["ip"],"port":data["port"]}
def Login():
    var = tkinter.StringVar()
    loginText = tkinter.Label(root, text='用户登录', font=('', 16))
    ip_Text = tkinter.Label(root,text='ipv4地址',font =('',12))
    port_Text = tkinter.Label(root,text='端口',font=('',12))
    admin_Text = tkinter.Label(root,text='用户名',font=(',12'))
    # pwd_Text = tkinter.Label(root, text='密码', font=(',12'))
    key_Text = tkinter.Label(root,text="请输入密钥", font=('',12))
    ipv4 = tkinter.Entry(root)
    try:
        data = getIpAndPort(os.path.abspath('.')+"\\config.yaml")
    except Exception as e:
        print(e)
        input("可能是缺少config.yaml文件，按回车键退出")
        sys.exit(1)
    ipv4.insert(0,data["ip"])
    port = tkinter.Entry(root)
    port.insert(0,data["port"])
    admin = tkinter.Entry(root,width=60)
    # pwd = tkinter.Entry(root, width=60)
    key = tkinter.Entry(root,width=57)
    btn = tkinter.Button(root,text="登录",font=('',16),command=lambda:Port(ipv4.get(),port.get(),admin.get(),var,key.get()),width='10')
    # btn1 = tkinter.Button(root, text="注册", font=('', 16),command=lambda: reg(ipv4.get(), port.get(), admin.get(), pwd.get(),var), width='10')
    tip_Text = tkinter.Label(root,textvariable=var,font=('',16))
    loginText.pack()
    ip_Text.place(x=100,y=50)
    port_Text.place(x=400,y=50)
    admin_Text.place(x=100,y=115)
    # pwd_Text.place(x=100, y=180)
    ipv4.place(x=175,y=50)
    port.place(x=450,y=50)
    admin.place(x=180,y=115)
    # pwd.place(x=180, y=180)
    key.place(x=200,y=180)
    btn.place(relx=0.4,y=400)
    # btn1.place(relx=0.4,y=450)
    tip_Text.place(relx=0.4,y=275)
    key_Text.place(x=100,y=180)
    root.mainloop()
if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('网络聊天室v1.0')
    root.geometry('750x500')
    Login()