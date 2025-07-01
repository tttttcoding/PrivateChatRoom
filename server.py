import socket
import threading
import time
socket_list = []
admin_list = []
Socket_Admin = {}
num=0
def send_info():
    global admin_list
    while(True):
        time.sleep(1.5)
        adminString = ""
        admin_list = list(set(admin_list))
        admin_list = sorted(admin_list,key=lambda x:x[1])
        for i in admin_list:
            client,admin = i
            adminString = adminString + ";"+admin
        for i in admin_list:
            client, admin = i
            Text = ";007;" + str(len(admin_list))+adminString+"; ;"
            try:
                client.send(Text.encode('utf8'))
            except:
                continue
def recveData(SocketClient,SocketAddr):
    global num,admin_list, admin
    while True:
        try:
            RecveData = SocketClient.recv(2048).decode('utf8')
        except:
            print(SocketAddr,"已断开")
            if (SocketClient,Socket_Admin[SocketClient]) in admin_list:
                admin_list.remove((SocketClient,Socket_Admin[SocketClient]))
                del Socket_Admin[SocketClient]
                num = num -1
                for i in socket_list:
                    client, addr = i
                    text = "005;" + admin + "离开聊天室;"
                    try:
                        client.send(text.encode('utf8'))
                    except:
                        continue
            break
        if(RecveData==""):
            continue
        print("来自", SocketAddr, "的消息：", RecveData)
        dataParse = RecveData.split(";")
        try:
            code,admin,content=dataParse
        except:
            code=dataParse[0]
        if(code=="003"):
            # sql = "select * from admin"
            # cur.execute(sql)
            # flag = False
            # for i in cur:
            #     if(i['name']==admin and i['password']==pwd):
            #         num+=1
            #         SocketClient.send("001;".encode("utf8"))
            #         admin_list.append((SocketClient,admin))
            #         Socket_Admin[SocketClient] = admin
            #         for j in socket_list:
            #             client,addr=j
            #             text = "005;欢迎"+admin+"加入聊天室;"
            #             try:
            #                 client.send(text.encode('utf8'))
            #             except:
            #                 continue
            #         flag = True
            #         break
            SocketClient.send("001;".encode("utf8"))
            admin_list.append((SocketClient,admin))
            Socket_Admin[SocketClient] = admin
            for j in socket_list:
                client, addr = j
                text = "005;欢迎" + admin + "加入聊天室;"
                try:
                    client.send(text.encode('utf8'))
                except:
                    continue
            # if(not flag):
            #     SocketClient.send("002".encode("utf8"))
            SocketClient.send("002".encode("utf8"))
        elif(code=="004"):
            # sql = "select * from admin"
            # cur.execute(sql)
            # flag = True
            # for i in cur:
            #     if(i['name']==admin):
            #         flag = False
            #         break
            # if(not flag):
            #     SocketClient.send("002".encode("utf8"))
            # else:
            #     sql = "insert into admin(name,password) value (\'"+admin+"\',\'"+pwd+"\')"
            #     cur.execute(sql)
            #     con.commit()
            SocketClient.send("001".encode("utf8"))
        elif(code=="006"):
            for i in socket_list:
                client, addr = i
                Text = "006;"+dataParse[1]+";"+dataParse[2]
                try:
                    client.send(Text.encode('utf8'))
                except:
                    continue
def Listen(tcp):
    while (True):
        global socket_list
        tcp.listen()
        SocketClient, SocketAddr = tcp.accept()
        SocketClient.send("001".encode("utf8"))
        print(SocketAddr,"已连接")
        socket_list.append((SocketClient, SocketAddr))
        t = threading.Thread(target=recveData,args=(SocketClient,SocketAddr))
        t.start()
        t1 = threading.Thread(target=send_info)
        t1.start()
# if __name__ == '__main__':
#     print("正在链接数据库")
#     try:
#         con = pymysql.connect(user='root', passwd='C_xt123456',
#                               host='127.0.0.1',
#                               port=3306,
#                               db='chatroomadmin')
#         # 创建游标
#         cur = con.cursor(pymysql.cursors.DictCursor)  # 查询的结果是字典
#         sql = "select * from admin"
#         cur.execute(sql)
#         re = cur.fetchall()
#         print('数据库链接成功！')
#         print(re)
#     except:
#         print("数据库链接失败！")
#     else:
#         tcp = socket.socket()
#         addr = ('0.0.0.0', 8080)
#         tcp.bind(addr)
#         link = threading.Thread(target=Listen, args=(tcp,))
#         link.start()
if __name__ == '__main__':
    tcp = socket.socket()
    addr = ('0.0.0.0', 8080)
    tcp.bind(addr)
    link = threading.Thread(target=Listen, args=(tcp,))
    link.start()


