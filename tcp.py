import socket
tcpserver=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcpserver.bind(('',12345))
tcpserver.listen()
while True:
    tcpget,addr=tcpserver.accept()
    date=tcpget.recv(1024)

    tcpget.send("recok".encode())
    k=0
    lenof=date[1]*256+date[2]
    print(lenof)
    snnum=''
    for i in range(3,11):
        snnum=snnum+str(date[i])







