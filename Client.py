import msvcrt
from socket import *
from scapy.all import *
import sys
import traceback
from config2 import *
from Utils import get_wifi_ip
from Utils import get_and_remove_name
import struct
import time
import traceback
from inputimeout import inputimeout, TimeoutOccurred
import keyboard



class Client:
    def __init__(self, name):
        """
        Constructor
        :param name: Client group name
        :return: None
        """
        self.c_name = name
        self.client_socket = None
        self.server_socket = None
        self.active = False
        self.ipme = get_wifi_ip()
        self.input = None
        self.press_time = None
        self.winner_event = threading.Event()
        self.key_type_event = threading.Event()
        self.message_event = threading.Event()
        self.answer_event = threading.Event()
        self.question_message = None
        self.server_message = None
        self.servers_dict = {}




    def activate_client(self):
        """
        Listening for offers from servers through broadcast.
        Once an offer arrives, connect to it.
        :return:
        """
        self.servers_dict = {}
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print(f"{Colors.CONNECT}Client started, listening for offer requests{Colors.END_COLOR}"+'\n')
        self.client_socket.bind(("", 13117))
        ready_to_play = False
        while True:
            combined_data_rcv, addr = self.client_socket.recvfrom(1024)
            data_rcv = combined_data_rcv[:struct.calcsize('Ibh')]
            data_rcv2 = combined_data_rcv[struct.calcsize('Ibh'):]
          #  data_rcv2, addr2 = self.client_socket.recvfrom(1024)

            if (data_rcv2 not in self.servers_dict and isinstance(data_rcv2,bytes) and "Hello" in data_rcv2.decode('utf-8')):
                self.servers_dict[data_rcv2] = data_rcv
                print(Colors.PLAYER+data_rcv2.decode()+ Colors.END_COLOR + '\n')
                user_input = input(
                    "Do you want to play on this server? (Enter 'Y' to play, 'N' to keep searching, or any other key to restart the search): ")

                if user_input == "N":
                    print(f"{Colors.CONNECT}listening for new offer requests{Colors.END_COLOR}")
                    continue
                elif user_input == "Y":
                    print(f"{Colors.CONNECT}Connecting to server{Colors.END_COLOR}")
                    ready_to_play = True
                    data_rcv = self.servers_dict[data_rcv2]
                else:
                    print(f"{Colors.CONNECT}Restarting search{Colors.END_COLOR}")
                    self.servers_dict={}


            if(ready_to_play == False):
                continue


            try:
                print(f'got from {addr}')
                data = struct.unpack('Ibh', data_rcv)
                if hex(data[0]) == "0xfeedbeef" and hex(data[1]) == "0x2":
                    print(f'{Colors.CONNECT}Received offer from {addr[0]}, attempting to connect...{Colors.END_COLOR}')
                   # print(f'{Colors.CONNECT}{servermsg}{Colors.END_COLOR}')
                    self.activate_client_tcp(addr[0], int(data[2]))
                    return
            except struct.error:
                pass
            except Exception as err:
                print(err)

    def wait_for_game_start(self):
        """
        Waiting for game to begin - Until message from Server arrives.
        :return: None
        """
        modified_sentence = ""
        self.server_socket.setblocking(False)
        while not modified_sentence:
            try:
                sentence = self.server_socket.recv(1024)
                modified_sentence = sentence.decode('utf-8')
                if modified_sentence:
                    print(modified_sentence)
            except Exception as ex:
                if str(ex) == "[Errno 35] Resource temporarily unavailable":
                    time.sleep(0)
                    continue
                time.sleep(0.2)

    def activate_client_tcp(self, server_name, server_port):
        """
        Connecting to a server with TCP, handling potential server downtime.

        :param server_name: Server to connect name
        :param server_port: Server to connect port
        :return: None
        """
        print(f"connected to server {server_name} on port {server_port}")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.server_socket.connect((server_name, server_port))
            self.server_socket.send(str(self.c_name).encode())

            while True:
                message = self.server_socket.recv(1024).decode()
                if not message:
                    # Server closed the connection
                    break
                print(message)
                break  # Assuming you only expect one initial message
            self.key_type_event.clear()
            key_thread = Thread(target=self.key_handel)
            server_messeages_thread = Thread(target=self.message_handel)
            server_messeages_thread.start()
            key_thread.start()

            self.game_in_progress()
            self.input = None
            self.server_message = None
            self.input = None
            self.message_event.clear()
            self.winner_event.clear()
            self.key_type_event.clear()
        except (ConnectionRefusedError, TimeoutError) as e:
            print(f"Server connection failed: {e}")
            # Return to searching for server offers (UDP broadcast)
            self.activate_client()  # Call the UDP broadcast method again

        except Exception as e:

            print("activate_client_tcp: Error occurred:", e)

        finally:
            self.server_socket.close()
            self.game_ended()

    def game_in_progress(self):
        """
        Getting inputs from the user and sends them to the Server while the game is on.
        Waiting for the game to end.
        :return: None
        """
        while True:
            self.message_event.wait()
            self.message_event.clear()
            print(self.server_message)
            if (self.winner_event.is_set()):
                try:
                    #print(self.server_message)
                    break
                except Exception as e:
                    print("Error while receiving submission acknowledgment:", e)
                    return
                return
            if ("Question" not in self.server_message):
                continue
            #print("Press 'Y', 'T', or '1' for true, 'N', 'F', or '0' for false")

            start_time = time.time()
            self.input = "TIMEOUT"

            while ((time.time() - start_time < 10) and self.winner_event.is_set() == False):
                if(self.winner_event.is_set()):
                    break
                if(self.key_type_event.is_set()):
                    self.server_socket.send((self.input.encode()))
                    self.key_type_event.clear()
                    break
                time.sleep(0.1)
            self.answer_event.clear()

            if (self.winner_event.is_set()):
                try:
                    print(self.server_message)
                    break
                except Exception as e:
                    print("Error while receiving submission acknowledgment:", e)
                    return
                return
            if(self.input == "TIMEOUT"):
                self.server_socket.send((self.input.encode()))

            # Receive acknowledgment from the server
            # try:
            #     submission_ack = self.server_socket.recv(1024).decode()
            #     if submission_ack:
            #         print(submission_ack)
            # except Exception as e:
            #     print("Error while receiving submission acknowledgment:", e)

    def game_ended(self):
        """
        Game over, closes the sockets and returns to searching for servers.

        :return: None
        """
        print("Game over!")
        print()
        time.sleep(1)
        self.server_socket.close()
        self.client_socket.close()
        self.activate_client()  # Return to searching for server offers (UDP broadcast)

    def key_handel(self):

        while True:
            self.answer_event.wait()
            key_event = keyboard.read_event()
            if key_event.event_type == keyboard.KEY_DOWN:
                self.key_type_event.set()
                self.input =key_event.name
    def message_handel(self):
        while True:

            try:
                message = self.server_socket.recv(1024).decode()
                if ("Question" in message):
                    self.answer_event.set()
                self.message_event.set()
            except socket.error as e:
                return
            if not message:
                print("Server connection closed")
                # Server closed the connection
                break
            if ("The winner is:" in message): #there is winner
                try:
                    self.winner_event.set()
                    self.message_event.set()
                    self.server_message = message
                    break
                except Exception as e:
                    print("Error while receiving submission acknowledgment:", e)
                return

             #question message
            self.message_event.set()
            self.server_message = message






def main():
    """
    Main function, Initialize client consistently
    :return: None
    """
    while True:
        client_name = get_and_remove_name()
        client = Client(client_name)
        client.activate_client()
        time.sleep(3)

if __name__ == "__main__":
    main()