import socket
import threading
import tkinter  # ubuntu: sudo apt-get install python3-tk
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'  # Your Public Ip
PORT = 9090


class Client:
    """ Client class """
    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))  # connecting with host at port

        # Nickname prompt
        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname:", parent=msg)

        # flags
        self.gui_done = False
        self.running = True

        # establishing threads
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        # starting threads
        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        """ maintains GUI """
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgrey")  # background colour

        # chat label
        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgrey")  # same bg applied to component to blend it with window (self.win) bg
        self.chat_label.config(font=("Ariel", 12))  # font family & font size
        self.chat_label.pack(padx=20, pady=5)  # padding

        # chat display area with scrolling ability
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)  # padding
        self.text_area.config(state='disabled')  # text area disabled

        # message label
        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgrey")  # same bg applied to component to blend it with window (self.win) bg
        self.msg_label.config(font=("Ariel", 12))  # font family & font size
        self.msg_label.pack(padx=20, pady=5)  # padding

        # input area (msg will be typed here)
        self.input_area = tkinter.Text(self.win, height=3)  # text box for input/msg
        self.input_area.pack(padx=20, pady=5)  # padding

        # send msg button
        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)  # onclick write() will be called
        self.send_button.config(font=("Ariel", 12))  # font family & font size
        self.send_button.pack(padx=20, pady=5)  # padding

        # GUI done flag
        self.gui_done = True

        # when window gets closed
        self.win.protocol("WM_DELETE_WINDOW", self.stop)  # stop() will be called

        self.win.mainloop()

    def write(self):
        """ gets text from input text box, sends it to server and clears the input box """

        # create entire msg along with client nickname
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}".encode('utf-8')
        self.sock.send(message)  # message sent
        self.input_area.delete('1.0', 'end')  # text area cleared

    def stop(self):
        """ terminates whole program """
        self.running = False  # flag
        self.win.destroy()  # window destroyed
        self.sock.close()  # socket closed
        exit(0)  # exit with code 0

    def receive(self):
        """ Deals with server connection """
        while self.running:  # while running flag is UP
            try:
                message = self.sock.recv(1024).decode('utf-8')  # 1024 Bytes
                if message == 'NICK':  # check for Nickname
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:  # is GUI done? (flag)
                        self.text_area.config(state='normal')  # enabling text area to append msg
                        self.text_area.insert('end', message)  # msg appended at the end
                        self.text_area.yview('end')  # autoscroll to the end
                        self.text_area.config(state='disabled')  # disabling the text area
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()  # socket close
                break


client = Client(HOST, PORT)  # obj created
