import os
import re
import const

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@ ============================================================== @@@
# @@@ ======== СОЗДАНИЕ И/ИЛИ ЧТЕНИЕ КОНФИГУРАЦИОННОГО ФАЙЛА ======= @@@
# @@@ ============================================================== @@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

"""
Проверка наличия директории для хранения конфигурационного файла.
При отсутствии - создаем.
"""
config_cat_path = r'.\config'
if not os.path.exists(config_cat_path):
    os.makedirs(config_cat_path)

"""
Проверка наличия конфигурационного файла. При отстутствии -
создаем и заполняем из модуля const.py.
"""
config_file_path = r'.\config\config.txt'
if not os.path.exists(config_file_path):
    with open(config_file_path, 'w') as config_file:
        for config_file_part in const.config_file_text:
            config_file.write(config_file_part)

# Сохраняем содержимое конфигурациооного файла в одну строку
config_file = open(config_file_path, 'r')
config_file_read = config_file.read()
config_file.close()

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@ ============================================================== @@@
# @@@ ================= КОНФИГУРАЦИОННЫЕ ПЕРЕМЕННЫЕ ================ @@@
# @@@ ============================================================== @@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

"""
Вспомогательная функция для поиска содержимого, которым будут
заполнены конфигурационные переменные.
"""


def between_two_markers_search(marker, strng):
    """
    В строке strng находит подстроку между двух "маркеров".
    Возвращает список из строк, разделенных символом начала
    новой строки в этой подстроке.
    Если число "маркеров" в строке отличается от двух,
    бросит ошибку.
    """
    result = re.split(marker, strng)
    if len(result) != 3:
        raise ValueError(
            f'Число маркеров {marker} в передаваемой для поиска между '
            f'маркерами строке не равно двум.'
        )
    else:
        return result[1][1:-1].split('\n')
    # [1] - т.к. нулевым вхождением будет все, что до первого "маркера".
    # [1:-1] - т.к. нулевым и последним эл-том строки будут '\n' после
    # первого и перед вторым "маркером".


# ******************************* COMMON *******************************

sigtypes_of_diagnostic_signals = [
    'DIAG_DI',
    'DIAG_Mod',
    'Mops3',
    'Mups3',
    'Mops3A',
]

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ INPUT $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

"""
Типы сигналов (signal.sigtype) для которых в Input.txt формируются строки вида:
{signal.name}(.IVXX, .MBIN, {plc.reset_position}_CORS.XORS, .IDVX, .IFXX, 
SYS_LNG.XLNG, {signal.styp});

Пример:
P0_15_04HS1002(.IVXX, .MBIN, P0_22_CORS.XORS, .IDVX, .IFXX, SYS_LNG.XLNG, 4);
"""
sigtypes_discrete_m_for_input = [
    'DI_M',
]

sigtypes_special_discrete_m_for_input = ['DI_M']

"""
DI_NM
P0_15_04HS1002(.IVXX, .MBIN, .INVR, SYS_LNG.XLNG);
"""
sigtypes_discrete_nm_for_input = [
    'DI_NM',
]

"""
sigtypes_analog_for_input - типы сигналов (signal.sigtype) для которых в 
Input.txt формируются строки вида:

Если signal.styp входит в styp_ai_reservation_for_input:
{sgnl_end(signal)}(.IN1, .IN2, 1, FALSE);
{signal.name}({sgnl_end(signal)}.XAXX, {sgnl_end(signal)}.XVLX1, 
{sgnl_end(signal)}.XVLX2, .MBIN, SYS_LNG.XLNG, FALSE);

Если signal.styp НЕ входит в styp_ai_reservation_for_input:
{sgnl_end(signal)}(.IN1, .IN2, 1, TRUE);
{signal.name}({sgnl_end(signal)}.XAXX, {sgnl_end(signal)}.XVLX1, 
{sgnl_end(signal)}.XVLX2, .MBIN, SYS_LNG.XLNG, TRUE);

*функцию sgnl_end() см. внутри метода Position.input_write_to_txt(),
модуль classes.py

Примеры:
Если signal.styp входит в styp_ai_reservation_for_input:
HS0001(.IN1, .IN2, 1, FALSE);
P0_15_04HS0001(HS0001.XAXX, HS0001.XVLX1, HS0001.XVLX2, .MBIN, 
SYS_LNG.XLNG, FALSE);

Если signal.styp НЕ входит в styp_ai_reservation_for_input:
HS0004(.IN1, .IN2, 1, TRUE);
P0_15_04HS0004(HS0004.XAXX, HS0004.XVLX1, HS0004.XVLX2, .MBIN, 
SYS_LNG.XLNG, TRUE);
"""
sigtypes_analog_for_input = ['AI']
styp_ai_reservation_for_input = ['res']

sigtypes_for_input = sigtypes_discrete_m_for_input + sigtypes_analog_for_input

styp_special_discrete_for_input = ['6']

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ OUTPUT $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

sigtypes_for_m_output = ['DO_M']
sigtypes_for_nm_output = ['DO_NM']

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$ ALARMING $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

sigtypes_for_alarming = ['DO_M']
styp_except_for_alarming = ['-']

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ COUNTING $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

sigtypes_for_counting = [
    'DI_M',
    'DI_NM',
    'DO_M',
    'DO_NM',
    'AI',
    'MOV',
    'PMP',
    'FD',
]
sigtypes_for_imitations_in_counting = [
    'DI_M',
    'DI_NM',
    'AI',
]
sigtypes_for_repairs_in_counting = [
    'DI_M',
    'DI_NM',
    'DO_M',
    'DO_NM',
    'AI',
    'MOV',
    'PMP',
    'FD',
]
sigtypes_for_faults_in_counting = [
    'DI_M',
    'DO_M',
    'AI',
    'MOV',
    'PMP',
    'FD',
]
sigtypes_for_falsities_in_counting = [
    'DI_M',
    'DI_NM',
    'DO_M',
    'DO_NM',
    'AI',
    'MOV',
    'PMP',
    'FD',
]

sigtypes_for_kspa_faults_in_counting = [
    'DIAG_DI',
    'DIAG_Mod',
    'Mops3',
    'Mups3',
    'Mops3A',
]

sigtypes_for_kspa_falsities_in_counting = [
    'DIAG_DI'
]

"""
Словарь для классификации счетчиков в котором каждый
ключ - назначение счетчика на русском, каждое значение -
принятые в проекте отличительные части названий для счетчиков.
"""
cntrs_dict = {}
for key_value_couple in between_two_markers_search(
    const.cntrs_dict_marker, config_file_read
):
    kv = key_value_couple.split(': ')
    cntrs_dict[kv[0]] = kv[1]

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ WEINTEK $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

sigtypes_di_for_weintek = [
    'DI_M',
]
sigtypes_do_for_weintek = [
    'DO_M',
]

sigtypes_analog_for_weintek = [
    'AI',
]

# ТУТ ПОРЯДОК ТИПОВ, НАЗВАНИЯ ТИПОВ НЕ МЕНЯТЬ, НУЖНЫ ПРАВКИ В КОДЕ
sigtypes_diag_for_weintek = [
    'DIAG_DI',
    'DIAG_Mod',
    'Mops3',
    'Mups3',
    'Mops3A',
]

sigtypes_xsy_for_weintek = [
    'DO_NM',
]

sigtypes_di_nm_for_weintek = [
    'DI_NM',
]

weintek_upg_tails_reg = ('Status1', 'Status2', 'XFTD', 'XFT1', 'XFT2')
weintek_upg_tails_coils = ('Blnk', 'XFDN', 'OF1N', 'OF2N', 'XBON')

sigtypes_valves_for_weintek = [
    'MOV',
    'PMP',
]

weintek_valves_tails_with_comments = (
    ['.MBIN', '// Входной массив с Weintek на Tekon'],
    ['.STSM', '// Время перестановки (от Weintek)'],
    ['.SRQM', '// Уставка наработки (от Weintek)'],
    ['.STPM', '// Время дожима концевика (от Weintek)'],
    ['.STCM', '// Время подачи команды (от Weintek)'],
    ['.Status1', '// Положение на Weintek'],
    ['.Status2', '// Индикатор команд управления на Weintek'],
    ['.STSX', '// Время перестановки (обратная связь)'],
    ['.SRQX', '// Уставка наработки концевиков (обратная связь)'],
    ['.STPR', '// Время дожима концевика (обратная связь)'],
    ['.STCX', '// Время подачи команды (обратная связь)'],
    ['.XRON', '// Наработка концевика открыт/кол-во включений'],
    ['.XROF', '// Наработка концевика закрыт/кол-во отключений'],
    ['.Blnk_Fr', '// Мигающая рамка'],
    ['.XRPX', '// Ремонт'],
    ['.FONX', '// Не включился/не открылся'],
    ['.FOFX', '// Не отключился/не закрылся'],
    ['.FFON', '// Несанционнированое включение/открытие'],
    ['.FFOF', '// Несанционнированое отключение/закрытие'],
    ['.FCOM', '// Противоречивость команд управления'],
    ['.FUCX', '// Неопределенный режим управления'],
    ['.FUSX', '// Неопределенное состояние'],
    ['.FDSX', '// Двойное состояние'],
    ['.FDCX', '// Двойной режим управления'],
    ['.FRQX', '// Сработала уставка по наработке концевиков'],
    ['.XRCX', '// Дист режим'],
    ['.XMMX', '// Ручной режим'],
    ['.IFXX.ValueBOOL', '// Внешняя неисправность'],
    ['.FXXX', '// Обобщенная неисправность'],
)

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ TO_SAU $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
sigtypes_for_to_sau = [
    'DO_NM',
]

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ DIAG $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

sigtypes_for_diag = [
    'DIAG_DI',
    'DIAG_Mod',
]
sigtypes_di_for_diag = [
    'DIAG_DI',
]
sigtypes_modules_for_types = [
    'DIAG_Mod',
]

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ MOPS_MUPS $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# на основе /config/config.txt

styp_for_m_in_mops3a = ['1']
styp_for_s_in_mops3a = ['0']

# без "внешнего" конфигурирования
"""
Список типов устройств.
"""
devtypes = ('MOPS', 'MOPS3a', 'MUPS')

"""
Аргументы функциональных блоков МОПС/МОПС3а/МУПС.
У МОПС и МУПС соответствуют каналам устройств.
"""
mops_args = ('CH01', 'CH02', 'CH03', 'CH04',
             'CH05', 'CH06', 'CH07', 'CH08')

mups_args = ('CH01', 'CH02', 'CH03', 'CH04')

mops3a_args = (
              '.INSC',
              '.CRST',
              '.CTST',
              '.ADRS',
              '.RST_CNT',
              '.TST_CNT',
)

"""
Адресные пространства.
"""
addresses_areas = {}
cnt1 = 0
cnt2 = 0
kont = []
for i in range(1, 151):
    kont.append(i)
    cnt2 += 1
    if cnt2 == 16:
        addresses_areas[cnt1] = kont
        cnt1 += 1
        kont = []
        cnt2 = 0

"""
Словарь адрес-бит.
"""
address_bit = {}
cnt1 = 0
cnt2 = 0
for i in range(1, 151):
    cnt1 += 1
    cnt2 += 1
    address_bit[cnt1] = cnt2
    if cnt2 == 16:
        cnt2 = 0
