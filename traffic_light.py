from enums import Menu, State
from traffic_light_class import TrafficLight


def initialize_traffic_light(traffic_light):
    """
    Initialize the traffic light system.
    :param traffic_light: The traffic light object to be initialized.
    :return: None
    """
    traffic_light.initialize()
    traffic_light.start_thread()
    traffic_light.state = State.MENU_STATE


def process_menu_state(traffic_light):
    """
    In the menu state show menu options and execute the option the user chose.
    :param traffic_light: An instance of the TrafficLight class that manages the state and behavior of a traffic light
    system, including menu options and state transitions.
    :return: None
    """
    command = Menu.ADD
    while command not in (Menu.QUIT, Menu.OPEN_SYSTEM):
        selected_option = traffic_light.select_menu_option()
        command = traffic_light.execute_menu_option(selected_option)
    traffic_light.state = State.QUIT_STATE if command == Menu.QUIT else State.SYSTEM_STATE


def process_system_state(traffic_light):
    """
    Navigate to menu state when user presses enter.
    :param traffic_light: An instance of TrafficLight, representing the current state of the traffic light system.
    :return: None
    """
    if input() == '':
        traffic_light.state = State.MENU_STATE
        TrafficLight.clear_console()


def main():
    """
    Controls the operation of a traffic light system. Depending on the current state of the traffic system,
    the function will either initialize the system, process the menu state, or process the system state.
    The loop will continue until the state changes to QUIT_STATE.

    :return: None
    """
    traffic_light = TrafficLight()
    traffic_light.state = State.NOT_STARTED
    while traffic_light.state != State.QUIT_STATE:
        if traffic_light.state == State.NOT_STARTED:
            initialize_traffic_light(traffic_light)
        elif traffic_light.state == State.MENU_STATE:
            process_menu_state(traffic_light)
        elif traffic_light.state == State.SYSTEM_STATE:
            process_system_state(traffic_light)


if __name__ == '__main__':
    main()
