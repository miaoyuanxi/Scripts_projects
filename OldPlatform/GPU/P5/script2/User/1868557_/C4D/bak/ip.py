import socket
myname = socket.getfqdn(socket.gethostname(  ))
myaddr = socket.gethostbyname(myname)
print myname
print myaddr