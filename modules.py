import datetime
from colorama import Fore, Style, init

init(autoreset=True)

class Console:
    def __init__(self, log_file='console.log'):
        """
        Initializes the Console with a specified log file.

        Args:
            log_file (str): The file path where logs will be stored. Defaults to 'console.log'.
        """
        self.log_file = log_file

    def _get_color_code(self, color):
        """
        Gets the color code for the specified color.

        Args:
            color (str): The name of the color.

        Returns:
            str: The color code corresponding to the color name.
        """
        color_map = {
            'red': Fore.RED,
            'green': Fore.GREEN,
            'cyan': Fore.CYAN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'magenta': Fore.MAGENTA,
            'white': Fore.WHITE,
            'black': Fore.BLACK,
            'default': Style.RESET_ALL
        }
        return color_map.get(color, Style.RESET_ALL)

    def log(self, message, color='default'):
        """
        Logs a message with a timestamp to the log file and prints it to the console with optional color.

        Args:
            message (str): The message to be logged and printed.
            color (str): The color of the text ('red', 'green', 'cyan', 'yellow', 'blue', 'magenta', 'white', 'black'). Defaults to 'default'.
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f'[{timestamp}] {message}'

        with open(self.log_file, 'a') as f:
            f.write(log_message + '\n')

        color_code = self._get_color_code(color)
        timestamp_color = Fore.BLACK + Style.BRIGHT
        reset_code = Style.RESET_ALL

        print_message = f'{timestamp_color}{timestamp} {reset_code}{color_code}> {message}{reset_code}'
        print(print_message)