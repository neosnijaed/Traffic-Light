import os
import time
from collections import deque
from threading import Thread

from enums import Menu, State
from exceptions import InvalidOptionError, NotPositiveIntegerValueError

ANSI_RED = '\u001B[31m'
ANSI_GREEN = '\u001B[32m'
ANSI_YELLOW = '\u001B[33m'
ANSI_RESET = '\u001B[0m'


class TrafficLight:
    """
    TrafficLight class for managing a traffic system with multiple roads.

    Methods
    -------
    __init__()
        Initializes the traffic light system with default values.

    initialize()
        Prompts for user inputs to initialize the number of roads and interval time.

    clear_console()
        Clears the console screen depending on the operating system.

    get_positive_integer_input(prompt: str) -> int
        Prompts the user for a positive integer input with the given prompt message.

    validate_input(user_input: str) -> int
        Validates the user input ensuring it is a positive integer.

    display_menu()
        Displays the main menu with options to the user.

    validate_menu_option(user_input: str) -> str
        Validates the menu option entered by the user.

    select_menu_option() -> Menu
        Displays the menu and validates the user's choice.

    execute_menu_option(option: Menu) -> Menu or State
        Executes the selected menu option.

    add_road()
        Adds a new road to the system and starts managing it.

    delete_road()
        Removes a road from the system and updates the management of roads.

    start_thread()
        Starts the system information loop in a separate thread.

    count_seconds()
        Increments the elapsed time and the road time by one second.

    calculate_road_time()
        Calculates the remaining open time for the current road.

    manage_roads()
        Manages the switching of current open roads based on the remaining time.

    system_info_loop()
        Continuously runs the system information loop until a quit state is encountered.

    display_system_info()
        Displays the current system status including elapsed time, number of roads, and intervals.

    display_roads_status()
        Displays the status of each road, indicating open and closed times.
    """

    def __init__(self):
        self.num_roads = 0
        self.interval_seconds = 0
        self.elapsed_time = 0
        self.road_time = 0
        self.state = None
        self.queue = None
        self.current_open_road = None
        self.remaining_time = 0

    def initialize(self):
        print('Welcome to the traffic management system!')
        self.num_roads = self.get_positive_integer_input('Input the number of roads: ')
        self.interval_seconds = self.get_positive_integer_input('Input the interval: ')
        self.queue = deque(maxlen=self.num_roads)
        self.clear_console()

    @staticmethod
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_positive_integer_input(self, prompt: str) -> int:
        user_input = input(prompt).strip()
        return self.validate_input(user_input)

    def validate_input(self, user_input: str) -> int:
        try:
            if not user_input.isdigit() or int(user_input) <= 0:
                raise NotPositiveIntegerValueError
        except NotPositiveIntegerValueError as err:
            return self.validate_input(input(err).strip())
        else:
            return int(user_input)

    @staticmethod
    def display_menu():
        menu_options = {Menu.ADD: 'Add road',
                        Menu.DELETE: 'Delete road',
                        Menu.OPEN_SYSTEM: 'Open system',
                        Menu.QUIT: 'Quit'}
        print('Menu:')
        for key, value in menu_options.items():
            print(f'{key.value}. {value}')

    def validate_menu_option(self, user_input: str) -> str:
        try:
            if not user_input.isdigit() or int(user_input) not in range(4):
                raise InvalidOptionError
        except InvalidOptionError as err:
            _ = input(f'{err}\n')
            self.clear_console()
            self.display_menu()
            return self.validate_menu_option(input().strip())
        else:
            return user_input

    def select_menu_option(self) -> Menu:
        self.display_menu()
        option = self.validate_menu_option(input().strip())
        return Menu(int(option))

    def execute_menu_option(self, option: Menu) -> Menu or State:
        if option == Menu.QUIT:
            print('Bye')
        elif option == Menu.ADD:
            self.add_road()
        elif option == Menu.DELETE:
            self.delete_road()
        elif option == Menu.OPEN_SYSTEM:
            self.clear_console()
        return option

    def add_road(self):
        road_name = input('Input road name: ')
        if len(self.queue) < self.num_roads:
            self.queue.append(road_name)
            if len(self.queue) == 1:
                self.current_open_road = self.queue[0]
                self.road_time = 0
            print(f'{road_name} Added!')
        else:
            print('Queue is full')
        input()
        self.clear_console()

    def delete_road(self):
        if len(self.queue) == 0:
            print('Queue is empty')
        else:
            current_index = self.queue.index(self.current_open_road)
            road_removed = self.queue.popleft()
            if self.current_open_road == road_removed and len(self.queue) > 0:
                self.current_open_road = self.queue[current_index]
            print(f'{road_removed} deleted!')
            if len(self.queue) == 0:
                self.current_open_road = None
        input()
        self.clear_console()

    def start_thread(self):
        queue_thread = Thread(target=self.system_info_loop)
        queue_thread.setName('QueueThread')
        queue_thread.start()

    def count_seconds(self):
        self.elapsed_time += 1
        self.road_time += 1
        time.sleep(1)

    def calculate_road_time(self):
        self.remaining_time = self.interval_seconds - (self.road_time % self.interval_seconds)

    def manage_roads(self):
        if self.remaining_time == 1 and len(self.queue) > 0:
            current_index = self.queue.index(self.current_open_road)
            self.current_open_road = self.queue[(current_index + 1) % len(self.queue)]

    def system_info_loop(self):
        while self.state != State.QUIT_STATE:
            if self.state == State.SYSTEM_STATE:
                self.calculate_road_time()
                self.display_system_info()
                self.manage_roads()
                self.count_seconds()
                if self.state != State.MENU_STATE:
                    self.clear_console()
            else:
                if len(self.queue) != 0:
                    self.manage_roads()
                self.count_seconds()

    def display_system_info(self):
        print(f'! {self.elapsed_time}s. have passed since system startup !\n'
              f'! Number of roads: {self.num_roads} !\n'
              f'! Interval: {self.interval_seconds} !\n')
        self.display_roads_status()
        print('\n! Press "Enter" to open menu !')

    def display_roads_status(self):
        for road in self.queue:
            if road == self.current_open_road:
                print(f'{road} will be ' + ANSI_GREEN + f'open for {self.remaining_time}s.' + ANSI_RESET)
            else:
                factor = (self.queue.index(road) - self.queue.index(self.current_open_road) - 1) % len(self.queue)
                print(
                    f'{road} will be ' + ANSI_RED +
                    f'closed for {self.interval_seconds * factor + self.remaining_time}s.' + ANSI_RESET
                )
