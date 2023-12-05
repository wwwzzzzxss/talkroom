import socket
import time

#初始化並建立監聽socket部分
send_msg = {
    'server' : "",
    'client' : ""
}

def set_server(IP,PORT):
    back_log = 1                #設定客戶端最大監聽數量         
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # 初始化TCP連線的socket
    server.settimeout(50)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  # 對socket的配置重複使用ip和連接埠號
    server.bind((IP,PORT))              #綁定連接埠號碼和socket
    server.listen(back_log)           #設定socket端監聽
    print("成功创建socket,等待client端連線中...")
    server.setblocking(False)
    return server

def room(server):
    buf_size = 1024    
    #server = set_server('127.0.0.1',6666)
    connect_num= 0
    clients = []
    play_clients = []
    gamestart = 0
    while 1:
        try:
            c,address = server.accept()  #阻塞式等待client端的連線
            if(connect_num< 4):
                connect_num += 1
                clients.append(c)
                time.sleep(0.01)
                """msg0 = "S" + "current headcount: " + str(connect_num)
                for current_clients in clients:
                    current_clients.send(msg0.encode('utf-8'))"""
                msg0=("{}".format(connect_num))
                c.send(msg0.encode('utf-8'))   #向client端傳遞客戶機編號
                print("接收到來自%s位址的client端連線,連線編號為 %sclient" % (address, connect_num))
            else:
                print("已達到最大連接client數量！")
                msg0=("end")
                c.send(msg0.encode('utf-8'))   #向client端傳遞終止連線命令       
        except BlockingIOError:
            pass
        for j in clients:
            try:
                msg0 = ""
                msg0 = j.recv(buf_size).decode('utf-8')
                if msg0 == '-*-start-*-':
                    print("收到")
                    gamestart += 1
                    play_clients.append(j)       
                elif msg0 != "":
                    msg0 = "C" + msg0
                    for send_client_msg in clients:
                        if send_client_msg != j:
                            send_client_msg.send(msg0.encode('utf-8'))
                if gamestart == 2:
                    for play_client in play_clients:
                        msg = 'S'+ 'ready start'
                        play_client.send(msg.encode('utf-8'))
                    time.sleep(0.01)
                    msg = 'S'+ 'exit'
                    for j in clients:
                        j.send(msg.encode('utf-8'))
                    print("遊戲開始")
                    time.sleep(4)
                    #return play_clients   
            except BlockingIOError:
                pass
            except ConnectionError:   
                for check_ready_player in play_clients:
                    if check_ready_player == j:
                        play_clients.remove(j)
                        gamestart -= 1
                        break
                print("準備人數",gamestart)
                connect_num -= 1
                clients.remove(j)
                


