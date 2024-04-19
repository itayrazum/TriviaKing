import socket
from socket import *
from scapy.all import *
import time
import struct
import random
from Statistics import Statistics
from config import *
from Utils import get_wifi_ip
import time
def __init__(self, statistics, flag=True):
    # Socket objects for UDP and TCP communication
    self.server_socket_udp = None
    self.server_socket_tcp = None

    # Port number and IP address for the server
    self.server_port = None
    self.server_ip = get_wifi_ip()

    # Flag for broadcast messages
    self.broadcast_flag = flag

    # Lists to store game participants and their sockets
    self.game_participants = []
    self.game_participants_dict = {}
    self.clients_sockets = []
    self.clients_sockets_dict = {}

    # List to store client threads
    self.client_threads = []

    # Flags to indicate game status and start message
    self.game_started = False
    self.start_game_msg = ""

    # Threads for UDP and TCP communication
    self.udp_thread = None
    self.tcp_thread = None

    # Lists for questions and answers
    self.first_list = []
    self.second_list = []

    # Message to display the winner
    self.winner_message = ""

    # Object for statistics tracking
    self.statistics = statistics

    # Client count and game readiness flag
    self.client_count = 0
    self.ready4game = False

    # Access to questions and answers from config.py
    self.questions = conspquestions
    self.answers = conspanswers

    # Dictionary to store client scores
    self.clients_scores = {}

    # List to track wrong answers
    self.wrong_answer_list = []

    # Variables for current question and answer
    self.question = None
    self.answer = None

    # Variable to store the winner and a lock for synchronization
    self.winner = None
    self.winner_lock = threading.Lock()

    # Lock for question updates and flag for new questions
    self.question_lock = threading.Lock()
    self.new_question = False

    # Flag for winner determination
    self._we_got_a_winner = False

    # Flag for readiness
    self.ready_flag = False

    # List to track question order and current index
    self.indexes_order = []
    self.current_index = 0
    self.winner_dict = {}

    self.locky_event = threading.Event()
    self.ready_dict = {}
    self.current_question = None
    self.welcome_message = "Welcome to the RazumWeiz server, Facts vs. Conspiracy Theories." + Colors.END_COLOR + '\n'

    self.welcome_message2 = "Hello im the server of the conspiracy theory game! come and play!"


def initiate_server(self):
    """
    Initialize the server, starts TCP tread and UDP thread for getting and sending messages
    :return: None
    """
    try:
        print(f"{Colors.CONNECT}Server started, listening on IP address {self.server_ip}{Colors.END_COLOR}")
        # Find an available port for the server
        self.server_port = self.find_available_port()

        # Create UDP and TCP sockets
        self.server_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.server_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set socket options for reusability
        self.server_socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Create threads for UDP and TCP communication
        self.udp_thread = Thread(target=self.activate_server_udp)
        self.tcp_thread = Thread(target=self.activate_server_tcp)

        # Start the threads
        self.udp_thread.start()
        self.tcp_thread.start()

        # Wait for threads to complete
        self.udp_thread.join()
        self.tcp_thread.join()

        # Initiate the game
        self.initiate_game()

        # Close connections with clients
        self.close_connections_with_clients()

        # Reset the server
        time.sleep(0.5)
        self.reset_server()
    except Exception as e:
        print(e)
        time.sleep(1)
        self.server_socket_tcp.close()


def find_available_port(self):
    for port in range(1024, 65536):  # Iterate over all possible port numbers
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.bind(('', port))
            test_socket.close()
            return port
        except OSError:
            continue
    raise RuntimeError("No available port found in the range 1024-65535")


def activate_server_udp(self):
    """
    Opens UDP socket to send messages to broadcast
    :return: None
    """
    # Pack the message with magic cookie, message type, and server port
    message = struct.pack('Ibh', 0xfeedbeef, 0x2, self.server_port) + b"Hello"

    # Send the second message

    # Set socket options for reusability and broadcast
    self.server_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.server_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bind the UDP socket
    self.server_socket_udp.bind((self.server_ip, 13117))

    # Track the time the broadcast started
    time_started = time.time()

    # Broadcast the message until the game starts
    while True:
        while not self.game_started:
            self.server_socket_udp.sendto(message, ('<broadcast>', 13117))
            time.sleep(1)
        self.server_socket_udp.close()
        return


def activate_server_tcp(self):
    """
    Open TCP connection to get clients responses, Collecting Clients.
    :return: None
    """
    print(f'{Colors.CONNECT}opened tcp on {self.server_ip} with port num {self.server_port}{Colors.END_COLOR}')
    self.server_socket_tcp.bind(('', self.server_port))
    self.server_socket_tcp.listen(1)
    self.server_socket_tcp.setblocking(False)
    countdown = False
    countthread = Thread(target=self.start_game_countdown)

    ready = False
    ID_gen = 1
    while self.game_started == False:
        try:
            if (self.game_started == True):
                break
            connection_socket, addr = self.server_socket_tcp.accept()
            msg = connection_socket.recv(1024)
            client_name = msg.decode('utf-8')
            if (client_name in self.clients_sockets_dict and self.clients_sockets_dict[client_name] != "Not Alowed"):
                client_name = client_name + str(ID_gen)
                ID_gen += 1
            print(f"{Colors.PLAYER}Player{Colors.END_COLOR} ", ' >> ', client_name)
            self.clients_sockets.append(connection_socket)
            self.clients_sockets_dict[client_name] = connection_socket
            self.game_participants.append(client_name)
            if (countdown == False):
                countdown = True
                countthread.start()

        except Exception as ex:
            if str(ex) == "[Errno 35] Resource temporarily unavailable":
                continue
            time.sleep(1)
    countthread.join()


def start_game_countdown(self):  # TODO to check every sec if someone left!
    print(f"{Colors.TIMER}Coundown started\n{Colors.END_COLOR}")

    countdown_duration = 8  # Countdown duration in seconds
    size = len(self.clients_sockets)
    while countdown_duration > 0:
        print(str(countdown_duration) + "...")
        time.sleep(1)
        if size < len(self.clients_sockets):
            print(f"{Colors.TIMER}Someone new joined the room, we will wait again\n{Colors.END_COLOR}")
            size = len(self.clients_sockets)

            countdown_duration = 10
        elif len(self.clients_sockets) == 0:
            print(
                f"{Colors.TIMER_V2}Someone leaved the room, we dont have the minimum number of players\n{Colors.END_COLOR}")

            return
        countdown_duration -= 1

    self.game_started = True


def generate_question(self):  # generating new question with random, removing the choosen one
    self.question = self.questions[self.current_index]
    self.answer = self.answers[self.current_index]
    self.current_index += 1
    if (self.current_index == len(self.questions)):
        self.current_index = 0


def initiate_game(self):
    """
    Initialize game for every client connected,where every client is a thread.
    :return:
    """

    self.cool_logo_print()
    # self.generate_question()
    self.set_winner(False)
    self.locky_event.clear()
    indexes = list(range(len(self.questions)))
    # Shuffle the list of indexes in-place
    random.shuffle(indexes)
    self.indexes_order = indexes
    ready_thread = Thread(target=self.ready_set_go)
    ready_thread.start()
    for client_socket in self.clients_sockets_dict:
        self.game_participants_dict[client_socket] = 0
        client_thread = Thread(target=self.new_game_for_client,
                               args=(self.clients_sockets_dict[client_socket], client_socket))

        client_thread.start()
        self.client_threads.append(client_thread)

    for client_thread in self.client_threads:
        client_thread.join()
    # winner_name = self.calc_winner()
    # print(self.winner_dict)
    # winner_msg = winner_name + " wins"
    # for s in self.clients_sockets:
    #     s.send(winner_msg.encode())
    print(f'{Colors.LOVE} Starting new game, dont worry, it will take about 10 secs, JUNGLE BEGINS{Colors.END_COLOR}')
    self.game_started = False
    self.reset_server()
    self.close_connections_with_clients()


def new_game_for_client(self, client_socket, client_name):
    """
    Sends welcome message to a client and starts the game for the client.
    :param client_socket: The Client socket
    :param client_name: The Client name
    :return: None
    """
    # msg = Colors.PLAYER + "Welcome to the RazumWeiz server, Facts vs. Conspiracy Theories." + Colors.END_COLOR + '\n'
    msg = self.welcome_message
    i = 1
    for client in self.game_participants:
        msg += Colors.TITLE + "Player " + str(i) + ":" + client + Colors.END_COLOR + '\n'
        i += 1
    msg += f"{Colors.JUNGLE}Welcome to the jungle {client_name}{Colors.END_COLOR}"
    try:
        client_socket.send(msg.encode())
        print(msg)
    except ConnectionError:
        print("Socket disconnected. Unable to send message.")
    self.run_game(client_name, client_socket)
    return

    # TODO we need to check it with multiple clients


#def run_game(self, client_name, client_socket):