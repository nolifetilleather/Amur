from classes import *


def read():

    import pandas as pd

    input_path = str(input('Введите путь до input.xlsx\n'))
    print('\n\tВыполняется чтение входных данных...\n')

    input_frame = pd.read_excel(
        fr'{input_path}\input.xlsx', dtype=str
    ).fillna('')

    # Проверка минимальной наполненности input_frame
    if len(input_frame) == 0:
        raise ValueError('Отсутствуют входные данные! Проверьте input.xlsx')
    if set(input_frame['Signal']) == {''}:
        raise ValueError('Столбец Signal пуст! Проверьте input.xlsx')

    # Заполнение атрибутов объекта контроллера
    if input_frame['PLC_Name'][0] == '':
        raise ValueError('Введите имя контроллера в input.xlsx')

    if input_frame['Cabinet_Category'][0] == '':
        raise ValueError('Введите категорию шкафа в input.xlsx')

    if input_frame['Reset_Position'][0] == '':
        raise ValueError('Введите позицию для сброса в input.xlsx')

    plc = PLC(

        name=input_frame['PLC_Name'][0],
        cabinet_category=input_frame['Cabinet_Category'][0],
        reset_position=input_frame['Reset_Position'][0],

        diag_addr=input_frame['DIAG_addr'][0]
        if input_frame['DIAG_addr'][0] != ''
        else None,

        reg=input_frame['REG'][0]
        if input_frame['REG'][0] != ''
        else None,

        coil=input_frame['COIL'][0]
        if input_frame['COIL'][0] != ''
        else None,

    )

    plc.output_path = input_path

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$ ПОЗИЦИИ $$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    # сохрание множества имен всех позиций на этом контроллере
    positions = set()
    for i in range(len(input_frame)):
        string_number = str(i+2)
        if (
            input_frame['Position'][i].replace(' ', '') == ''
            and
            input_frame['Signal'][i].replace(' ', '') != ''
            and
            input_frame['Sigtype'][i] not in config.sigtypes_diag_for_weintek
        ):
            # ошибка при отсутствии заполнения позиции для сигнала
            raise ValueError(
                f'Строка {string_number} столбца Position не заполнена '
                f'при заполненной строке {string_number}\n столбца Signal.'
                'Проверьте входные данные.\n'
            )
        elif input_frame['Position'][i].replace(' ', '') != '':
            positions.add(input_frame['Position'][i])

    # отсортируем имена позиций
    positions = list(positions)
    positions.sort()

    # создадим объекты позиций, сохраним ссылки на них
    for position_name in positions:
        position = Position(
                plc=plc,
                name=position_name,
        )
        for i in range(len(input_frame)):
            string_number = i+2
            if (
                    input_frame['Weintek_Position'][i] != ''
                    and
                    (input_frame['IZV_addr'][i] == ''
                     or
                     input_frame['OPV_addr'][i] == '')
            ):
                raise ValueError(
                    f'В строке {string_number} столбца Weintek_Position '
                    f'введено имя поциции {position_name}, при этом\n'
                    f'отсутствуют необходимые значения в столбцах IZV_addr '
                    f'и OPV_addr строки {string_number}.\n'
                    f'Проверьте input.xlsx.'
                )
            elif (
                    (input_frame['Weintek_Position'][i] != '')
                    and
                    (Position.format_position_name(
                        input_frame['Weintek_Position'][i]
                    ))
                    == position.name
            ):
                position.izv_addr = input_frame['IZV_addr'][i]
                position.opv_addr = input_frame['OPV_addr'][i]
                position.tush_addr = (
                    input_frame['TUSH_addr'][i]
                    if input_frame['TUSH_addr'][i] != ''
                    else None
                )
                position.xsy_addr = (
                    input_frame['XSY_addr'][i]
                    if input_frame['XSY_addr'][i] != ''
                    else None
                )
        plc.append_position(position)

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$ СИГНАЛЫ $$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    """
    Создание экземпляров Signal,
    сохранение ссылок на них в список
    сигналов экземпляра PLC.
    """

    for i in range(len(input_frame)):
        if input_frame['Signal'][i].replace(' ', '') != '':
            signal = Signal(

                plc=plc,

                name=input_frame['Signal'][i],

                sigtype=input_frame['Sigtype'][i],

                styp=input_frame['Styp'][i],

                # на данном этапе в position и location записываются
                # строковые значения из input_frame, они необходимы
                # чтобы в дальнейшем перезаписать в эти атрибуты
                # ссылки на экземпляры Position и Location к которым
                # относится сигнал
                position=Position.format_position_name(
                    (input_frame['Position'][i])
                )
                if input_frame['Sigtype'][i]
                not in
                config.sigtypes_diag_for_weintek
                else plc.diag_position,

                location=input_frame['Location'][i]
                if input_frame['Location'][i] != ''
                else None,

                ff_out=input_frame['FF_Out'][i].split(', ')
                if input_frame['FF_Out'][i] != ''
                else None,

                address=input_frame['Address'][i]
                if input_frame['Address'][i] != ''
                else None,

                device=input_frame['Device'][i]
                if input_frame['Device'][i] != ''
                else None,

            )
            plc.append_signal(signal)

    # список сигналов заполнен
    plc.signals_list_filled = True
    print(
        f'Cписок сигналов экземпляра '
        f'контроллера {plc.name} заполнен: '
        f'{plc.signals_list_filled}'
    )
    # отсортируем список сигналов
    plc.sort_signals_by_them_names()

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$ ЛОКАЦИИ (С&E) $$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    """
    Создадим локацию для сигналов исключений.
    В ней будем сохранять сигналы, исходя из
    .sigtype которых их следовало использовать
    в Сounting, однако их принадлежность к
    локации exc исключит их из формирования
    текста Counting.txt
    """
    exceptions_location = Location(
        name='exc'
        )
    plc.append_location(exceptions_location)
    plc.exceptions_location = exceptions_location

    """
    Проверка заполнения информации о C&E в input_frame
    по заполнению столбцов Location и Location_CE.
    Проверка корректности заполнения по равенству множеств
    от значений в столбцах Location и Locations.
    """
    loc_set = set(list(input_frame['Location']))
    loc_set.discard('')
    loc_set.discard('exc')

    loc_ce_set = set(list(input_frame['Location_CE']))
    loc_ce_set.discard('')

    sets_equal = loc_set == loc_ce_set
    sets_not_empty = (
            loc_ce_set != set()
            and
            loc_set != set()
    )

    print(
        f'Столбцы Location и Location_CE заполнены: {sets_not_empty}'
    )
    print(
        'Множества названий локаций в столбцах '
        f'Location и Location_CE равны: {sets_equal}'
    )

    if sets_equal and sets_not_empty:

        seen = []
        for location in input_frame['Location_CE']:
            if location != '' and location in seen:
                raise ValueError(
                    'В столбце Location_CE обнаружены дублирующиеся\n'
                    'названия локаций! Проверьте input.xlsx'
                )
            if location != '':
                seen.append(location)

        """
        Создание экземпляров Location,
        сохранение ссылок на них в список
        локаций экземпляра PLC.
        """
        # заполняем атрибуты на основе input_frame
        from re import findall
        for i in range(len(input_frame)):
            if input_frame['Location_CE'][i] != '':
                string_number = str(i + 2)
                location = Location(

                    name=input_frame['Location_CE'][i],

                    warning_cntr=True
                    if 'X' in input_frame['Warning'][i]
                    else False,

                    fire_cntr=True
                    if 'X' in input_frame['Fire'][i]
                    else False,

                    voting_logic=findall(
                        r'\d+', input_frame['Voting_Logic'][i]
                    )
                    if input_frame['Voting_Logic'][i] != ''
                    else None,

                    conterminal_systems_cntrs=(
                        input_frame['Conterminal_Systems'][i].split(', '))
                    if input_frame['Conterminal_Systems'][i] != ''
                    else None,

                    fire_fightings_cntrs=(
                        input_frame['Fire_Fightings'][i].split(', '))
                    if input_frame['Fire_Fightings'][i] != ''
                    else None,

                )

                # $$$$$$$$$$$$$$$$$$$$$ ПРОВЕРКИ $$$$$$$$$$$$$$$$$$$$$$

                # Voting_Logic
                if (
                    location.voting_logic is not None
                    and
                    len(location.voting_logic) != 2
                ):
                    raise ValueError(
                        f'В строке {string_number} столбца Voting_Logic '
                        'количество чисел отличается от двух! Проверьте '
                        'input.xlsx'
                    )

                if (
                    location.voting_logic is None
                    and
                    not location.warning_cntr
                ):
                    raise ValueError(
                        f'В строке {string_number} отсутствует заполнение'
                        ' столбца Voting_Logic при отсутствующем маркере '
                        'маркере в столбце Warning! Проверьте input.xlsx'
                    )

                if (
                    location.voting_logic is None
                    and
                    (location.fire_cntr
                     or
                     location.fire_fightings_cntrs is not None
                     or
                     location.conterminal_systems_cntrs is not None)
                ):
                    raise ValueError(
                        f'В строке {string_number} отсутствует'
                        ' заполнение Voting_Logic при наличии\n'
                        'заполнения минимум в одном '
                        'из столбцов (Fire, Fire_Fightings,\n'
                        'Conterminal_Systems), заполнение '
                        'которых указывает на необходимость\n'
                        'заполнения Voting_Logic в этой строке. '
                        'Проверьте input.xlsx'
                    )

                # Conterminal_Systems
                if (
                    location.conterminal_systems_cntrs is not None
                    and
                    (len(set(location.conterminal_systems_cntrs))
                     !=
                     len(location.conterminal_systems_cntrs))
                ):
                    raise ValueError(
                        f'В строке {string_number} cтолбца '
                        'Conterminal_Systems обнаружены дублирующиеся\n'
                        'названия смежных систем! Проверьте input.xlsx'
                    )

                # Fire_Fightings
                if (
                    location.fire_fightings_cntrs is not None
                    and
                    (len(set(location.fire_fightings_cntrs))
                     !=
                     len(location.fire_fightings_cntrs))
                ):
                    raise ValueError(
                        f'В строке {string_number} cтолбца '
                        'Fire_Fightings обнаружены дублирующиеся\n'
                        'названия пожаротушений! Проверьте input.xlsx'
                    )

                if (
                    location.fire_fightings_cntrs is not None
                    and
                    location.fire_cntr
                ):
                    raise ValueError(
                        f'В строке {string_number} обнаружено недопустимое '
                        'одновременное\nзаполнение столбцов '
                        'Fires и Fire_Fightings! Проверьте input.xlsx'
                    )

                plc.append_location(location)

        plc.ce_locations_filled = True
        print(
            'Список локаций экземпляра контроллера заполнен: '
            f'{plc.ce_locations_filled}'
        )

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$ УСТРОЙСТВА $$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    """
    Проверка заполнения информации об устройствах в input_frame
    по заполнению столбцов Device и Devices.
    Проверка корректности заполнения по равенству множеств
    от значений в столбцах Device и Devices.
    """
    sets_equal = (
            set(list(input_frame['Device'])).discard('')
            == set(list(input_frame['Devices'])).discard('')
    )
    sets_not_empty = (
            set(list(input_frame['Device'])).discard('') != set()
            and
            set(list(input_frame['Devices'])).discard('') != set()
    )

    print(
        f'Столбцы Device и Devices заполнены: {sets_not_empty}'
    )
    print(
        'Множества названий устройств в столбцах '
        f'Device и Devices равны: {sets_equal}'
    )

    if sets_equal and sets_not_empty:

        seen = []
        for device in input_frame['Devices']:
            if device != '' and device in seen:
                raise ValueError(
                    'В столбце Devices обнаружены дублирующиеся\n'
                    'названия устройств! Проверьте input.xlsx'
                )
            if device != '':
                seen.append(device)

        """
        Создание экземпляров Device,
        сохранение ссылок на них в список
        устройств экземпляра PLC.
        """
        # заполняем атрибуты на основе input_frame
        from re import findall
        for i in range(len(input_frame)):
            if input_frame['Devices'][i] != '':

                string_number = str(i + 2)
                devtype = input_frame['Dev_Type'][i]

                device = Device(

                    plc=plc,

                    name=input_frame['Devices'][i],

                    devtype=devtype,

                    input_index=input_frame['Input_Index'][i],

                    output_index=input_frame['Output_Index'][i],

                    m=findall(
                        r'\d+', input_frame['MOPS3a_M'][i]
                    )
                    if devtype == 'MOPS3a'
                    else None,

                    s=findall(
                        r'\d+', input_frame['MOPS3a_S'][i]
                    )
                    if devtype == 'MOPS3a'
                    else None,

                )

                # $$$$$$$$$$$$$$$$$$$$$ ПРОВЕРКИ $$$$$$$$$$$$$$$$$$$$$$

                # Dev_Type
                if (
                    device.devtype not in config.devtypes
                ):
                    raise ValueError(
                        f'В строке {string_number} столбца Dev_Type '
                        'обнаружено недопустимое значение!\n Проверьте '
                        'input.xlsx'
                    )

                # $$$$$$$$$$$$$$$$$$$ SIGNALS LIST $$$$$$$$$$$$$$$$$$$$
                if device.devtype == 'MOPS':
                    device.signals_list += \
                        ['0' for _ in range(len(config.mops_args))]

                if device.devtype == 'MUPS':
                    device.signals_list += \
                        ['0' for _ in range(len(config.mups_args))]

                plc.append_device(device)

        plc.devices_list_filled = True
        print(
            'Список устройств экземпляра контроллера заполнен: '
            f'{plc.devices_list_filled}'
        )

    return plc
