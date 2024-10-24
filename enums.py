from enum import Enum, auto


class Menu(Enum):
    """
    Menu is an enumeration representing various menu actions.

    Attributes:
        ADD (int): Represents the action to add a road.
        DELETE (int): Represents the action to delete a road.
        OPEN_SYSTEM (int): Represents the action to go to system state.
        QUIT (int): Represents the action to quit the application.
    """
    ADD = 1
    DELETE = 2
    OPEN_SYSTEM = 3
    QUIT = 0


class State(Enum):
    """
    Represents the different states in an application.

    Attributes:
        NOT_STARTED: Initial state indicating traffic system has not started.
        MENU_STATE: State indicating the application is displaying the menu.
        SYSTEM_STATE: State indicating the application is performing system operations.
        QUIT_STATE: State indicating the application should quit.
    """
    NOT_STARTED = auto()
    MENU_STATE = auto()
    SYSTEM_STATE = auto()
    QUIT_STATE = auto()
