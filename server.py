import socket

s = socket.socket()
s.bind(("localhost", 9999))
s.listen(1)

sc, addr = s.accept()

while True:
    recibido = sc.recv(1024)
    if recibido == "quit":
        break
    print "Message received:", recibido
    sc.send(recibido)

print "bye..."

sc.close()
s.close()
