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


# $$$$$$$$$$$$$$$$$$$$$$$ INPUT, OUTPUT, ALARMING $$$$$$$$$$$$$$$$$$$$$$

sigtypes_for_input = []
sigtypes_for_output = []
sigtypes_for_alarming = []

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ COUNTING $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

sigtypes_for_counting = []
sigtypes_for_imitations_in_counting = []
sigtypes_for_repairs_in_counting = []
sigtypes_for_faults_in_counting = []
sigtypes_for_falsities_in_counting = []

cntrs_dict = {}

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ WEINTEK $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

sigtypes_di_for_weintek = []
sigtypes_do_for_weintek = []

# ТУТ ПОРЯДОК ТИПОВ ДЛЯ ТИПОВ, НАЗВАНИЯ ТИПОВ МЕНЯТЬ НЕ МЕНЯТЬ, НУЖНЫ ПРАВКИ
# В КОДЕ
sigtypes_diag_for_weintek = []

weintek_upg_tails_reg = []
weintek_upg_tails_coils = []

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ DIAG_ST $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

sigtypes_for_diag_st = []
sigtypes_di_for_diag_st = []
sigtypes_modules_for_types = []

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ MOPS_MUPS $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# на основе /config/config.txt

styp_for_m_in_mops3a = 1
styp_for_s_in_mops3a = 0

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
