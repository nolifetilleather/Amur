import tiger
import read_input as inp
from menu import menu

line = '\n\n'+'-' * 100
while True:

    try:

        plc = inp.read()
        plc.input_data_reformation()
        # plc.print_signals()
        menu(plc)

    except FileNotFoundError as e:
        print(
            'ОШИБКА!\n\n',
            e,
            '\n\nНажмите Enter, повторите '
            f'ввод пути до input.xlsx{line}'
        )
    """
    except Exception as e:
        print(
            'ОШИБКА!\n\n',
            e.__class__,
            e,
            '\n\nДля продолжения нажмите Enter'
            f'{line}'
        )
    """
    input()
