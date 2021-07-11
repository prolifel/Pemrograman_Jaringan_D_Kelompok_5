import socket
import threading
import os
SEPARATOR = "<SEPARATOR>"

class ServerForChatroom:
    def __init__(self, addr):
        self.connection_addr = addr
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_msg = "Welcome to Chatroom"
        self.msg_size = 2048
        self.users = []
        self.connection_status = True

    def listen_for_messages(self, client_data):
        is_connected = True
        while is_connected:
            if len(self.users) > 0:
                try:
                    msg = client_data[1].recv(self.msg_size).decode()

                except:
                    is_connected = False
                    self.users.remove(client_data)
                
                data_kirim = str(msg).split(SEPARATOR)
                print(data_kirim)
                # print(data_kirim[0])
                if(data_kirim[0]=="FILE"):
                    nama_file = os.path.basename(data_kirim[1])
                    ukuran_file = int(data_kirim[2])
                    with open(nama_file, "wb") as f:
                        while True:
                            print("Menerima...")
                            bytes_baca = client_data[1].recv(self.msg_size)
                            if not bytes_baca:
                                break
                            f.write(bytes_baca)
                        f.close()
                    print("file berhasil terkirim")
                    # f = open('hasil.txt', 'wb')
                    # while True:
                    #     msg = client_data[1].recv(self.msg_size)
                    #     while (msg):
                    #         print
                    #         "Receiving..."
                    #         f.write(msg)
                    #         msg = client_data[1].recv(self.msg_size)
                else:
                    msg = f"{client_data[0]} : {msg}"

                for user in self.users:
                    try:
                        user[1].send(str.encode(msg))
                    except:
                        continue


    def connection(self):
        self.s.bind((self.connection_addr[0], self.connection_addr[1]))
        self.s.listen(5)
        print("Listening to connections....")
        while self.connection_status:
            conn, addr = self.s.accept()
            new_user = conn.recv(self.msg_size).decode()
            user_taken = False
            for user in self.users:
                if user[0] == new_user:
                    conn.send(str.encode("ERROR : USER NAME TAKEN!"))
                    user_taken = True

            if user_taken:
                continue

            for user in self.users:
                user[1].send(str.encode(f"{new_user} has entered the chat"))

            self.users.append((new_user, conn))

            new_user_thread = threading.Thread(target=self.listen_for_messages, args=((new_user, conn),))
            new_user_thread.start()

            print(f"Connection established with {new_user} at {addr}")
            conn.send(str.encode(self.connection_msg))


if __name__ == "__main__":
    server_connection = ServerForChatroom(('127.0.0.1', 8000))
    server_connection.connection()