import sys


def menu(plc):

    line = '-' * 100 + '\n'

    while True:

        # В каждом подсписке:
        # [0] - название операции
        # [1] - условие для возможности ее выполнения
        # [2] - операция
        # [3] - флаг указатель для пункта "сформировать всё"
        operations = [
            # [
            #     'Вывести все сигналы на экран',
            #     plc.signals_reformed,
            #     plc.print_signals,
            #     False,
            # ],
            # [
            #     'Вывести все локации на экран',
            #     plc.locations_reformed,
            #     plc.print_locations,
            #     False,
            # ],
            [
                'Сформировать Input.txt',
                plc.ready_for_input(),
                plc.establishing_input_txt,
                True,
            ],
            [
                'Сформировать Output.txt',
                plc.ready_for_output(),
                plc.establishing_output_txt,
                True,
            ],
            [
                'Сформировать Alarming.txt',
                plc.ready_for_alarming(),
                plc.establishing_alarming_txt,
                True,
            ],
            [
                'Сформировать Counting.txt',
                plc.ready_for_counting(),
                plc.establishing_counting_txt,
                True,
            ],
            [
                'Сформировать MOPS_MUPS.txt',
                plc.ready_for_mops_mups(),
                plc.establishing_mops_mups_txt,
                True,
            ],
            [
                'Сформировать Reset_MOPS3a.txt',
                plc.ready_for_reset_mops3a(),
                plc.establishing_reset_mops3a_txt,
                True,
            ],
            [
                'Сформировать Oxon.txt',
                plc.ready_for_oxon(),
                plc.establishing_oxon_txt,
                True,
            ],
            [
                'Сформировать Weintek.txt',
                plc.ready_for_weintek(),
                plc.establishing_weintek_txt,
                True,
            ],
            [
                'Сформировать To_SAU.txt',
                plc.ready_for_to_sau(),
                plc.establishing_to_sau_txt,
                True,
            ],
            [
                'Сформировать Diag_ST.txt',
                plc.ready_for_diag_st(),
                plc.establishing_diag_st_txt,
                True,
            ],
            # [
            #    'Сформировать таблицу исходных данных',
            #    plc.ready_for_datatable(),
            #    plc.establishing_datatable_to_xlsx,
            #    True,
            # ],
            [
                'Сформировать все доступные для формирования файлы',
                True,
                None,
                False,
            ],
            [
                'Вывести инструкцию на экран',
                True,
                print,
                False,
            ],
            [
                'Изменить директорию для выходных файлов\n\t'
                '(по умолчанию та же, что у input.xlsx)',
                True,
                plc.change_output_path,
                False,
            ],
            [
                'Выход',
                True,
                sys.exit,
                False,
            ],
        ]

        available_operations = {}
        operation_num = 1
        for lst in operations:
            if lst[1] and lst[0] != 'Выход':
                available_operations[operation_num] = []
                available_operations[operation_num] += lst[0:4]
                operation_num += 1
            elif lst[1] and lst[0] == 'Выход':
                available_operations[0] = []
                available_operations[0] += lst[0:4]

        print(
            '\tВведите через пробел номера необходимых операций.\n'
            '\tДоступные операции:\n'
        )

        for key in range(len(available_operations) - 1):
            print(f'{key+1}.\t{available_operations[key + 1][0]}')
        print(f'{0}.\t{available_operations[0][0]}')

        choice = input().split()

        if (

            int(choice[0]) in available_operations
            and
            available_operations[int(choice[0])][0] != 'Выход'

        ):
            print('\n'+line)

        elif int(choice[0]) not in available_operations:
            print('\n' + line)

        choice = list(int(n) for n in choice)
        for i in range(len(choice)):
            key = choice[i]
            if available_operations[key][0] == \
                    'Сформировать все доступные для формирования файлы':
                all_available_nums = []
                for num in available_operations:
                    if available_operations[num][3]:
                        all_available_nums.append(num)
                if -(len(choice)-i)+1 != 0:
                    choice = choice[0:i] + \
                        all_available_nums + \
                        choice[-(len(choice)-i)+1:]
                elif -(len(choice)-i)+1 == 0:
                    choice = choice[0:i] + \
                          all_available_nums

        for key in choice:

            # Операции требующие обработки не по шаблону
            if key not in available_operations.keys():
                print(f'{key} - неизветная операция!')

            elif available_operations[key][0] == 'Выход':
                available_operations[key][2]()

            elif available_operations[key][0] == \
                'Изменить директорию для выходных файлов\n\t' \
                    '(по умолчанию та же, что у input.xlsx)':
                available_operations[key][2]()

            elif available_operations[key][0] == \
                    'Вывести инструкцию на экран':
                available_operations[key][2]('Инструкция')
                input('\nДля продолжения нажмите любую клавижу')

            # Шаблон для выполнения операций
            elif available_operations[key][1]:
                print(
                    f'Выполняется операция '
                    f'"{available_operations[key][0]}"'
                )
                # available_operations[key][2]()
                try:
                    available_operations[key][2]()
                    print(
                        '\nУСПЕХ!\n'
                        f'\nОперация "{available_operations[key][0]}"'
                        ' выполнена!'
                    )
                except Exception as e:
                    print(
                        '\nОШИБКА!\n\n',
                        e.__class__,
                        e,
                        f'\n\nОперация "{available_operations[key][0]}"'
                        ' НЕ выполнена!'
                    )

            print(f'\n{line}')
