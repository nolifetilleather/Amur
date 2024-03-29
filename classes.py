import config


class Signal:
    """
    Хранит информацию о сигнале, задействованном в работе
    АСУ ТП СТБ на базе контроллеров tecon, которая необходима
    для автоматического формирования программного кода на языке ST.

    Параметры
    ---------
    name: строковое наименование сигнала. Может быть передано
    как в формате используемом в коде на ST, так и в формате,
    который используют в проектной документации (преобразование
    в формат для ST-кода произойдет автоматически)

    plc: экземпляр PLC к которому относится сигнал

    sigtype: строковое наименование типа сигнала

    position: строковое наименование позиции или экземпляр Position

    location: строковое наименование локации, экземпляр Location или None

    ff_out: список строковых наименований смежных систем или None

    device: строковое наименование утсройстваб, экземпляр Device или None

    address: строковое значение адреса сигнала или None

    styp: строковое значение styp сигнала или None

    Свойства
    --------

    """
    def __init__(
            self,
            name,
            plc,
            sigtype,
            position,
            location=None,
            ff_out=None,
            device=None,
            address=None,
            styp=None,
    ):

        self.name = name
        self.plc = plc
        self.sigtype = sigtype
        self.position = position
        self.location = location
        self.ff_out = ff_out
        self.device = device
        self.address = address
        self.styp = styp

    # name
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        if type(new_name) is not str:
            raise TypeError(
                'Недопустимый тип для Signal.name'
            )
        elif len(new_name) == 0:
            raise ValueError(
                'Длина Signal.name должна быть больше нуля'
            )

        self.__name = new_name.replace('-', '_').replace(' ', '')
        if not self.__name[0].isalpha():
            self.__name = 'P' + self.__name

    # plc
    @property
    def plc(self):
        return self.__plc

    @plc.setter
    def plc(self, new_plc):
        if type(new_plc) is not PLC:
            raise TypeError(
                'Недопустимый тип для Signal.plc'
            )
        self.__plc = new_plc

    # sigtype
    @property
    def sigtype(self):
        return self.__sigtype

    @sigtype.setter
    def sigtype(self, new_sigtype):
        if type(new_sigtype) is not str:
            raise TypeError(
                'Недопустимый тип для Signal.sigtype'
            )
        elif len(new_sigtype) == 0:
            raise ValueError(
                'Длина Signal.sigtype должна быть больше нуля'
            )
        self.__sigtype = new_sigtype

    # position
    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, new_position):
        if not (
            type(new_position) is str
            or
            type(new_position) is Position
        ):
            raise TypeError(
                'Недопустимый тип для Signal.position'
            )
        elif type(new_position) is str and len(new_position) == 0:
            raise ValueError(
                'Длина строкового значения Signal.position '
                'должна быть больше нуля'
            )
        self.__position = new_position

    # location
    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, new_location):
        if not (
            type(new_location) is str
            or
            type(new_location) is Location
            or
            new_location is None
        ):
            raise TypeError(
                'Недопустимый тип для Signal.location'
            )
        elif type(new_location) is str and len(new_location) == 0:
            raise ValueError(
                'Длина строкового значения Signal.location '
                'должна быть больше нуля'
            )
        self.__location = new_location

    # ff_out
    @property
    def ff_out(self):
        return self.__ff_out

    @ff_out.setter
    def ff_out(self, new_ff_out):
        if not (
                (
                        type(new_ff_out) is list
                        and
                        not any(type(el) is not str
                                for el in new_ff_out)
                )
                or
                new_ff_out is None
        ):
            raise TypeError(
                'Недопустимый тип для Signal.ff_out'
            )
        self.__ff_out = new_ff_out

    # device
    @property
    def device(self):
        return self.__device

    @device.setter
    def device(self, new_device):
        if not (
            type(new_device) is str
            or
            type(new_device) is Device
            or
            new_device is None
        ):
            raise TypeError(
                'Недопустимый тип для Signal.device'
            )
        elif type(new_device) is str and len(new_device) == 0:
            raise ValueError(
                'Длина строкового значения Signal.device '
                'должна быть больше нуля'
            )
        self.__device = new_device

    # address
    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, new_address):
        if not (
            type(new_address) is str
            or
            new_address is None
        ):
            raise TypeError(
                'Недопустимый тип для Signal.address'
            )
        elif type(new_address) is str and len(new_address) == 0:
            raise ValueError(
                'Длина строкового значения Signal.address '
                'должна быть больше нуля'
            )
        self.__address = new_address

    # styp
    @property
    def styp(self):
        return self.__styp

    @styp.setter
    def styp(self, new_styp):
        if not (
            type(new_styp) is str
            or
            new_styp is None
        ):
            raise TypeError(
                'Недопустимый тип для Signal.styp'
            )
        elif type(new_styp) is str and len(new_styp) == 0:
            raise ValueError(
                'Длина строкового значения Signal.styp '
                'должна быть больше нуля'
            )
        self.__styp = new_styp


class SignalsList(list):
    """
    Наследник встроенного типа list. Предназначен для хранения ссылок
    на экземпляры Signal.
    Имеет методы для анализа собственного содержимого.
    """

    # $$$$$$$$$$$$$$$$$$$$$ ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ $$$$$$$$$$$$$$$$$$$$$

    def has_any_signal_with_sigtype_in(self, sigtypes_list):
        """
        Принимает список или кортеж.
        Возращает True если SignalsList содержит ссылку хотя бы на один
        экземпляр Signal, значение атрибута .sigtype которого содержится
        в этом списке/кортеже. В остальных случаях вернет False.
        """
        if not isinstance(sigtypes_list, (list, tuple)):
            raise TypeError(
                'Ожидается список или кортеж в качестве аргумента'
            )
        flg = False
        for signal in self:
            if type(signal) is Signal:
                if signal.sigtype in sigtypes_list:
                    flg = True
                    break
        return flg

    def has_any_ff_or_ffo_signal_with_sigtype_in(self, sigtypes_list):
        """
        Принимает список или кортеж.
        Возращает True если SignalsList содержит ссылку хотя бы на один
        экземпляр Signal, атрибуты которого удовлетворяют условиям:

            1) Signal.sigtype содержится в передаваемом списке/кортеже

            2) Signal.location.fire_fightings_cntrs не является None
               или
               Signal.ff_out не является None

        В остальных случаях возвращает False.
        """
        if not isinstance(sigtypes_list, (list, tuple)):
            raise TypeError(
                'Ожидается список или кортеж в качестве аргумента'
            )
        flg = False
        for signal in self:
            if (
                    type(signal) is Signal
                    and
                    signal.sigtype in sigtypes_list
                    and
                    ((type(signal.location) is Location
                      and
                      signal.location.fire_fightings_cntrs is not None)
                     or
                     signal.ff_out is not None)
            ):
                flg = True
                break
        return flg

    def has_any_no_ff_or_ffo_signal_with_sigtype_in(self, sigtypes_list):
        """
        Принимает список или кортеж.
        Возращает True если SignalsList содержит ссылку хотя бы на один
        экземпляр Signal, атрибуты которого удовлетворяют условиям:

            1) Signal.sigtype содержится в передаваемом списке/кортеже

            2) Signal.location является None
               или
               Signal.location.fire_fightings_cntrs является None

            3) Signal.ff_out не является None

        В остальных случаях возвращает False.
        """
        if not isinstance(sigtypes_list, (list, tuple)):
            raise TypeError(
                'Ожидается список или кортеж в качестве аргумента'
            )
        flg = False
        for signal in self:
            if (
                    type(signal) is Signal
                    and
                    signal.sigtype in sigtypes_list
                    and
                    (signal.location is None
                     or
                     signal.location.fire_fightings_cntrs is None)
                    and
                    signal.ff_out is None
            ):
                flg = True
                break
        return flg

    # $$$$$$$$$$$$$$$$$$$$$$$$$ ПРОВЕРКИ НАЛИЧИЯ $$$$$$$$$$$$$$$$$$$$$$$

    # INPUT
    def contains_signals_for_input(self):
        """
        Возвращает True если SignalsList содержит ссылку хотя бы на
        один экземпляр Signal, который должен участвовать в формировании
        текста программы Input.
        В остальных случаях возвращает False.
        """
        return self.has_any_signal_with_sigtype_in(
            config.sigtypes_for_input
        )

    # OUTPUT
    def contains_signals_for_output(self):
        """
        Возвращает True если SignalsList содержит ссылку хотя бы на
        один экземпляр Signal, который должен участвовать в формировании
        текста программы Output.
        В остальных случаях возвращает False.
        """
        return self.has_any_signal_with_sigtype_in(
            config.sigtypes_for_m_output
        )

    # ALARMING
    def contains_signals_for_alarming(self):
        """
        Возвращает True если SignalsList содержит ссылку хотя бы на
        один экземпляр Signal, который должен участвовать в формировании
        текста программы Alarming.
        В остальных случаях возвращает False.
        """
        return any(
                type(signal) is Signal
                and
                signal.sigtype in config.sigtypes_for_alarming
                and
                signal.ff_out is None
                for signal in self
            )

    # COUNTING
    def contains_signals_for_counting(self):
        """
        Возвращает True если SignalsList содержит ссылку хотя бы на
        один экземпляр Signal, который должен участвовать в формировании
        текста программы Counting.
        В остальных случаях возвращает False.
        """
        return any(
            type(signal) is Signal
            and
            signal.location is not signal.plc.exceptions_location
            and
            signal.sigtype in config.sigtypes_for_counting
            for signal in self
        )

    def contains_signals_with_ff_out_for_counting(self):
        """
        Возвращает True если SignalsList содержит ссылку хотя бы на
        один экземпляр Signal, атрибуты которого удовлетворяют условиям:

            1) Signal.ff_out не является None

            2) Signal.location не является Signal.plc.exceptions_location

        В остальных случаях возвращает False
        """
        return any(
            type(signal) is Signal
            and
            signal.ff_out is not None
            and
            signal.location is not signal.plc.exceptions_location
            for signal in self
        )

    def contains_signals_without_ff_out_for_counting(self):
        """
        Возвращает True если SignalsList содержит ссылку хотя бы на
        один экземпляр Signal, атрибуты которого удовлетворяют условиям:

            1) Signal.ff_out является None

            2) Signal.sigtype входит в перечень типов сигналов,
               которые указывают на то, что данный экземпляр должен
               участвовать в формировании текста программы Counting

            3) Signal.location не является Signal.plc.exceptions_location

        В остальных случаях возвращает False
        """
        return any(
            type(signal) is Signal
            and
            signal.ff_out is None
            and
            signal.sigtype in config.sigtypes_for_counting
            and
            signal.location is not signal.plc.exceptions_location
            for signal in self
        )

    def contains_signals_with_fire_fighting_for_counting(self):
        """
        Возвращает True если SignalsList содержит ссылку хотя бы на
        один экземпляр Signal, атрибуты которого удовлетворяют условиям:

            1) Signal.location.fire_fightings_cntrs не является None

        В остальных случаях возвращает False
        """
        return any(
                    type(signal) is Signal
                    and
                    type(signal.location) is Location
                    and
                    signal.location.fire_fightings_cntrs is not None
                    for signal in self
            )

    def contains_signals_without_fire_fighting_for_counting(self):
        """
        Возвращает True если SignalsList содержит ссылку хотя бы на
        один экземпляр Signal, атрибуты которого удовлетворяют условиям:

            1) Signal.location.fire_fightings_cntrs является None
               или
               Signal.location является None

            2) Signal.location не является Signal.plc.exceptions_location

            3) Signal.sigtype входит в перечень типов сигналов,
               которые указывают на то, что данный экземпляр должен
               участвовать в формировании текста программы Counting

        В остальных случаях возвращает False
        """
        return any(
                    type(signal) is Signal
                    and
                    ((type(signal) is Location
                      and
                      signal.location.fire_fightings_cntrs is None)
                     or
                     signal.location is None)
                    and
                    signal.sigtype in config.sigtypes_for_counting
                    and
                    signal.location is not signal.plc.exceptions_location
                    for signal in self
            )

    def contains_ff_or_ffo_signals_with_warning(self):
        """
        Возвращает True если SignalsList содержит ссылку хотя бы на
        один экземпляр Signal, атрибуты которого удовлетворяют условиям:

            1) Signal.location.fire_fightings_cntrs не является None
               или
               Signal.ff_out не является None

            2) Signal.location.warning_cntr является True

        В остальных случаях возвращает False
        """
        return any(
                    type(signal) is Signal
                    and
                    type(signal.location) is Location
                    and
                    signal.location.warning_cntr
                    and
                    (signal.ff_out is not None
                     or
                     signal.location.fire_fightings_cntrs is not None)
                    for signal in self
                )

    def contains_no_ff_or_ffo_signals_with_warning(self):
        """
        Возвращает True если SignalsList содержит ссылку хотя бы на
        один экземпляр Signal, атрибуты которого удовлетворяют условиям:

            1) Signal.location.fire_fightings_cntrs является None

            2) Signal.ff_out является None

            3) Signal.location.warning_cntr является True

        В остальных случаях возвращает False
        """
        return any(
                    type(signal) is Signal
                    and
                    type(signal.location) is Location
                    and
                    signal.location.warning_cntr
                    and
                    signal.ff_out is None
                    and
                    signal.location.fire_fightings_cntrs is None
                    for signal in self
                )

    # WEINTEK
    def contains_diagnostic_signals(self):
        """
        Возвращает True если SignalsList содержит ссылку
        хотя бы на один экземпляр Signal, значение Signal.sigtype
        которого позволяет отнести его к сигналам диагностики.
        В остальных случаях возвращает False.
        """
        return (
            any(signal.sigtype in config.sigtypes_of_diagnostic_signals
                for signal in self)
        )

    # TO SAU
    def contains_signals_for_to_sau(self):
        """
        Возвращает True если SignalsList содержит ссылку хотя бы на
        один экземпляр Signal, который должен участвовать в формировании
        текста программы To_SAU.
        В остальных случаях возвращает False.
        """
        return (
            any(signal.sigtype in config.sigtypes_for_to_sau
                for signal in self)
        )

    # DIAG
    def contains_signals_for_diag(self):
        """
        Возвращает True если SignalsList содержит ссылку хотя бы на
        один экземпляр Signal, который должен участвовать в формировании
        текста программы Diag.
        В остальных случаях возвращает False.
        """
        return self.has_any_signal_with_sigtype_in(
            config.sigtypes_for_diag
        )


class Location:
    """
    Хранит информацию о локации сигналов, задействованных в работе
    АСУ ТП СТБ на базе контроллеров tecon, которая необходима
    для автоматического формирования программного кода на языке ST.

    Параметры
    ---------

    name: строковое наименование локации

    warning_cntr: логическое значение

    fire_cntr: логическое значение

    fire_fightings_cntrs: список строковых наименований
    направлений пожаротушения или None

    conterminal_systems_cntrs: список строковых наименований
    смежных систем или None

    voting_logic: список из двух целых чисел или строковых
    представлений целых чисел или None
    """
    def __init__(
            self,
            name,
            warning_cntr=False,
            fire_cntr=False,
            fire_fightings_cntrs=None,
            conterminal_systems_cntrs=None,
            voting_logic=None,
    ):

        self.__signals_list = SignalsList()  # для ссылок на объекты сигналов
        self.__position = None  # см метод position_check_and_set

        self.name = name
        self.warning_cntr = warning_cntr
        self.fire_cntr = fire_cntr
        self.fire_fightings_cntrs = fire_fightings_cntrs
        self.conterminal_systems_cntrs = conterminal_systems_cntrs
        self.voting_logic = voting_logic

    @property
    def signals_list(self):
        """
        Копия Signal.__signals_list
        """
        return self.__signals_list.copy()

    def append_signal(self, signal):
        """
        Метод добавляет передаваемый экземпляр Signal
        в Location.__signals_list

        Если тип передаваемого объекта не является Signal
        возникнет ошибка
        """
        if type(signal) is Signal:
            self.__signals_list.append(signal)
        else:
            raise TypeError(
                'Недопустимый тип, ожидается экземпляр Signal'
            )

    @property
    def position(self):
        """
        Если метод Location.position_check_and_set() был
        выполнен - вернет экземпляр Position.
        В обратном случае вернет None.
        """
        return self.__position

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        if type(new_name) is not str:
            raise TypeError(
                'Недопустимый тип для Location.name'
            )
        elif len(new_name) == 0:
            raise ValueError(
                'Длина Location.name должна быть больше нуля'
            )
        self.__name = new_name

    @property
    def warning_cntr(self):
        return self.__warning_cntr

    @warning_cntr.setter
    def warning_cntr(self, new_warning_cntr):
        if type(new_warning_cntr) is not bool:
            raise TypeError(
                'Недопустимый тип для Location.warning_cntr'
            )
        self.__warning_cntr = new_warning_cntr

    @property
    def fire_cntr(self):
        return self.__fire_cntr

    @fire_cntr.setter
    def fire_cntr(self, new_fire_cntr):
        if type(new_fire_cntr) is not bool:
            raise TypeError(
                'Недопустимый тип для Location.fire_cntr'
            )
        self.__fire_cntr = new_fire_cntr

    @property
    def fire_fightings_cntrs(self):
        return self.__fire_fightings_cntrs

    @fire_fightings_cntrs.setter
    def fire_fightings_cntrs(self, new_fire_fightings_cntrs):
        if not (
                (
                        type(new_fire_fightings_cntrs) is list
                        and
                        # len(new_fire_fightings_cntrs) > 0
                        # and
                        not any(type(el) is not str
                                for el in new_fire_fightings_cntrs)
                )
                or
                new_fire_fightings_cntrs is None
        ):
            raise TypeError(
                'Недопустимый тип для Location.fire_fightings_cntrs'
            )
        self.__fire_fightings_cntrs = new_fire_fightings_cntrs

    @property
    def conterminal_systems_cntrs(self):
        return self.__conterminal_systems_cntrs

    @conterminal_systems_cntrs.setter
    def conterminal_systems_cntrs(self, new_conterminal_systems_cntrs):
        if not (
                (
                        type(new_conterminal_systems_cntrs) is list
                        and
                        # len(new_conterminal_systems_cntrs) > 0
                        # and
                        not any(type(el) is not str
                                for el in new_conterminal_systems_cntrs)
                )
                or
                new_conterminal_systems_cntrs is None
        ):
            raise TypeError(
                'Недопустимый тип для Location.conterminal_systems_cntrs'
            )
        self.__conterminal_systems_cntrs = new_conterminal_systems_cntrs

    @property
    def voting_logic(self):
        if type(self.__voting_logic) is list:
            return self.__voting_logic.copy()
        else:
            return None

    @voting_logic.setter
    def voting_logic(self, new_voting_logic):

        if type(new_voting_logic) is not list and new_voting_logic is not None:
            raise TypeError(
                'Недопустимый тип для Location.voting_logic'
            )

        elif (
                type(new_voting_logic) is list
                and
                len(new_voting_logic) != 0
                and
                any(not str(el).isdigit()
                    for el in new_voting_logic)
        ):
            raise TypeError(
                'Недопустимый для Location.voting_logic '
                'тип в списке'
            )

        elif (
                type(new_voting_logic) is list
                and
                len(new_voting_logic) != 2
                and
                not any(not str(el).isdigit()
                        for el in new_voting_logic)
        ):
            raise ValueError(
                'Недопустимое значение для Location.voting_logic\n'
                'Список должен содержать два эелемента'
            )

        self.__voting_logic = new_voting_logic

    def position_check_and_set(self):
        """
        Если Signal.position каждого из экземпляров Signal,
        ссылки на которые находятся в self.signals_list, ссылаются
        на один и тот же экземпляр Position, тогда:

            1) В self.position записывается ссылка на тот же
            экземпляр Position, что и у каждого Signal

            2) Ссылка на self сохраняется в Position.location_list

        Если условия не выполняются, возникнет ощибка TypeError.

        Если Signal.position хотя бы одного из экземпляров Signal
        ссылается на объект, который не является экземпляром Position,
        возникнет ошибка TypeError.
        """
        if len(self.__signals_list) == 0:
            raise ValueError(
                'Location.__signals_list пуст'
            )
        positions_set = set()
        for signal in self.signals_list:
            if type(signal.position) is Position:
                positions_set.add(signal.position)
            else:
                raise TypeError(
                    'Недопустимый тип для Signal.position'
                )
        if len(positions_set) != 1:
            report = (
                f'Список позиций сигналов локации {self.name}:\n'
            )

            for position in positions_set:
                report += f'{position.name}\n'

            raise ValueError(
                f'В локации {self.name} обнаружены '
                f'сигналы с разными позициями\n'
                f'{report}'
            )
        else:
            self.__position = list(positions_set)[0]
            self.position.locations_list.append(self)


class Position:
    """
    Хранит информацию о позиции сигналов, задействованных в работе
    АСУ ТП СТБ на базе контроллеров tecon, которая необходима
    для автоматического формирования программного кода на языке ST.

    Параметры
    ---------

    name: строковое наименование позиции. Может быть передано
    как в формате используемом в коде на ST, так и в формате,
    который используют в проектной документации (преобразование
    в формат для ST-кода произойдет автоматически)

    plc: экземпляр PLC к которому относится позиция

    di_m_addr: целое число или строковое представление целого числа
    (начальный адрес для DI_M сигналов данной позиции в программе
    Weintek)

    do_m_addr: целое число или строковое представление целого числа
    (начальный адрес для DO_M сигналов данной позиции в программе
    Weintek)

    do_nm_addr: целое число или строковое представление целого числа
    (начальный адрес для DO_M сигналов данной позиции в программе
    Weintek)

    ai_addr: целое число или строковое представление целого числа
    (начальный адрес для AI сигналов данной позиции в программе
    Weintek)

    tush_addr: целое число или строковое представление целого числа
    (начальный адрес для тушения по данной позиции в программе
    Weintek)

    mov_addr: целое число или строковое представление целого числа
    (начальный адрес для задвижек по данной позиции в программе
    Weintek)
    """
    def __init__(
            self,
            name,
            plc,
            di_m_addr=None,  # Weintek
            do_m_addr=None,  # Weintek
            do_nm_addr=None,  # Weintek
            ai_addr=None,  # Weintek
            tush_addr=None,  # Weintek
            mov_addr=None,  # Weintek
    ):

        if not isinstance(plc, PLC):
            raise TypeError(
                'Аргуметом plc при создании '
                'экземпляра Position '
                'может выступать только '
                'экземпляр/наследник класса PLC!'
            )

        self.name = self.format_position_name(name)
        self.name_for_comment = name
        self.plc = plc

        self.izv_addr = di_m_addr
        self.opv_addr = do_m_addr
        self.xsy_addr = do_nm_addr
        self.ai_addr = ai_addr
        self.tush_addr = tush_addr
        self.mov_addr = mov_addr

        self.signals_list = SignalsList()
        self.locations_list = []
        self.upg_counters = []
        self.upg_markers = []
        self.xsy_counters = []
        self.counters = []
        self.counters_for_sum = []
        self.bool_counters = set()

    # $$$$$$$$$$$$$$$$$$$$$ ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ $$$$$$$$$$$$$$$$$$$$$

    @staticmethod
    def format_position_name(name):
        """
        Принимает строковое наименование позиции в формате,
        используемом в проектной документации.

        Возвращает строковое наименование позиции в формате,
        изспользуемом в ST-коде.
        """
        frmt_name = name.replace(' ', '').replace('-', '_')
        if not frmt_name[0].isalpha():
            frmt_name = 'P' + frmt_name
        return frmt_name

    @staticmethod
    def counter_one_signal_actuation(
            signal,
            counter,
            cntr_marker,
    ):
        """
        Параметры
        ---------
        signal: экземпляр Signal

        counter: строковое значение (наименование переменной счетчика
        для использования в ST-кода)

        cntr_marker: строковое значение (атрибут функционального блока
        сигнала из библиотеки проекта в SCADA ТЕКОН)

        Возвращает строку ST-кода, описывающую "срабатывание" счетчика
        по сигналу
        """

        # ОШИБКИ

        # signal
        if type(signal) is not Signal:
            raise TypeError(
                'Для аргумента signal ожидается экземпляр Signal'
            )

        return (
            f'{counter}:=Count({signal.name}.{cntr_marker}, {counter});\n'
        )

    @staticmethod
    def __counter_with_condition_write_to_txt(
            txt,
            location,
            counter,
            cntr_marker,
    ):
        """
        Метод записывает в текстовый файл строки кода на языке ST,
        описывающие "срабатывание" счетчика по одному или двум сигналам
        из списка сигналов, принадлежащим к локации

        Параметры
        ---------
        txt: ссылка текстовый файл

        location: экземпляр Location

        counter:

        cntr_marker:
        """

        # ПО ОДНОМУ СИГНАЛУ
        if (
                location.voting_logic is not None
                and
                int(location.voting_logic[0]) == 1
        ):
            if len(location.signals_list) < 1:
                raise ValueError(
                    f'В локации {location.name} обнаружен '
                    'конфликт Voting_Logic с количеством\n'
                    'сигналов относящихся к локации! '
                    'Проверьте input.xlsx.'
                )
            else:
                for signal in location.signals_list:
                    txt.write(
                        Position.counter_one_signal_actuation(
                            signal,
                            counter,
                            cntr_marker,
                        )
                    )

        # TWO_OF_n
        if (
                location.voting_logic is not None
                and
                int(location.voting_logic[0]) == 2
                and
                int(location.voting_logic[1]) > 2
        ):
            if len(location.signals_list) < 3:
                raise ValueError(
                    f'В локации {location.name} обнаружен '
                    'конфликт Voting_Logic с количеством\n'
                    'сигналов относящихся к локации! '
                    'Проверьте input.xlsx.'
                )
            else:

                n = location.voting_logic[1]

                first_signal = location.signals_list[0].name
                txt.write(
                    f'{counter}:=Count(TWO_OF_{n}(\n'
                    f'{first_signal}.{cntr_marker},\n'
                )

                for signal in location.signals_list[1:-1]:
                    txt.write(
                        f'{signal.name}.{cntr_marker},\n'
                    )

                last_signal = location.signals_list[-1].name
                txt.write(
                    f'{last_signal}.{cntr_marker}), {counter});\n'
                )

        # AND
        if (
                location.voting_logic is not None
                and
                int(location.voting_logic[0]) == 2
                and
                int(location.voting_logic[1]) == 2
        ):

            if len(location.signals_list) != 2:
                raise ValueError(
                    f'В локации {location.name} обнаружен '
                    'конфликт Voting_Logic с количеством\n'
                    'сигналов относящихся к локации! '
                    'Проверьте input.xlsx.'
                )

            else:
                first_signal = location.signals_list[0].name
                second_signal = location.signals_list[-1].name
                txt.write(
                    f'{counter}:=Count({first_signal}.{cntr_marker} '
                    f'AND {second_signal}.{cntr_marker}, {counter});\n'
                )

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$ ПРОВЕРКИ НАЛИЧИЯ $$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def contains_locations_with_warning(self):
        """
        Возвращет True если в списке locations_list
        есть экземпляр Location атрибут .warning_cntr
        которого is True.
        Если такого экземпляра нет - возвращает False.
        """
        return (
            any(location.warning_cntr for location in self.locations_list)
        )

    def contains_locations_with_warning_and_fire_fighting(self):
        """
        Возвращет True если в списке locations_list
        есть экземпляр Location атрибут .warning_cntr
        которого True, а атрибут .fire_fightings_cntrs
        is not None.
        Если такого экземпляра нет - возвращает False.
        """
        return any(
            location.warning_cntr
            and
            location.fire_fightings_cntrs is not None
            for location in self.locations_list
        )

    def contains_locations_with_warning_without_fire_fighting(self):
        """
        Возвращет True если в списке locations_list
        есть экземпляр Location атрибут .warning_cntr
        которого is True, а атрибут .fire_fightings_cntrs
        is None.
        Если такого экземпляра нет - возвращает False.
        """
        return any(
            location.warning_cntr
            and
            location.fire_fightings_cntrs is None
            for location in self.locations_list
        )

    def is_diag(self):
        return any(
            signal.sigtype in config.sigtypes_of_diagnostic_signals
            for signal in self.signals_list
        )

    def contains_locations_with_fire(self):
        """
        Возвращет True если в списке locations_list
        есть экземпляр Location атрибут .fire_cntr
        которого == True.
        Если такого экземпляра нет - возвращает False.
        """
        return any(
            location.fire_cntr for location in self.locations_list
        )

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$ ЗАПИСЬ ST КОДА В ФАЙЛЫ $$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    # INPUT
    def input_write_to_txt(self, txt):
        """
        Метод записывает в txt строки кода на ST.
        В коде участвуют все сигналы из self.signals_list
        .sigtype которых входят в
        config.sigtypes_for_input_txt.
        """
        def sgnl_end(sgnl):
            from re import findall, split
            num = findall(r'\d+', sgnl.name)[-1]
            if split(r'\d+', sgnl.name)[-1].isalpha():
                let = findall(r'\D+', sgnl.name)[-2]
                let2 = findall(r'\D+', sgnl.name)[-1]
                result = let + num + let2
            else:
                let = findall(r'\D+', sgnl.name)[-1]
                result = let + num
            return result

        txt.write(f'// {self.name_for_comment}\n')

        # дискреты с контролем цепи
        for sigtype in config.sigtypes_discrete_m_for_input:
            txt.write(f'// {sigtype}\n')
            for signal in self.signals_list:
                if signal.sigtype == sigtype and signal.styp != '6':
                    txt.write(
                        f'{signal.name}(.IVXX, .MBIN, '
                        f'{signal.plc.reset_position}_CORS.XORS, '
                        f'.IDVX, .IFXX, SYS_LNG.XLNG, {signal.styp});\n'
                    )
                # BS
                elif (
                        signal.sigtype in
                        config.sigtypes_special_discrete_m_for_input
                        and
                        signal.styp in
                        config.styp_special_discrete_for_input
                ):
                    txt.write(
                        f'{sgnl_end(signal)}(_IO_{signal.address}_3);\n'
                        +
                        '{0}({1}.XVLX, .MBIN, {2}_CORS.XORS, '
                        '{1}.DVXX, .IFXX, SYS_LNG.XLNG, {3});\n\n'
                        .format(
                            signal.name,
                            sgnl_end(signal),
                            self.plc.reset_position,
                            signal.styp,
                        )
                    )
            txt.write('\n')

        # дискреты без контроля цепи
        for sigtype in config.sigtypes_discrete_nm_for_input:
            txt.write(f'// {sigtype}\n')
            for signal in self.signals_list:
                if signal.sigtype == sigtype:
                    inv = 'TRUE' if signal.styp == 'inv' else '.INVR'
                    txt.write(
                        f'{signal.name}'
                        f'(_IO_{signal.address}, .MBIN, {inv}, '
                        f'SYS_LNG.XLNG);\n'
                    )
            txt.write('\n')

        # аналоги
        def ai_write_to_txt(sgnl, file):
            dct = {
                True: 'TRUE',
                False: 'FALSE',
            }
            file.write(
                f'{sgnl_end(sgnl)}'
                f'(.IN1, .IN2, 1, {dct[sgnl.styp == "res"]});\n'
                +
                '{0}({1}.XAXX, {1}.XVLX1, {1}.XVLX2, '
                '.MBIN, SYS_LNG.XLNG, {2});\n'.format(
                    sgnl.name,
                    sgnl_end(sgnl),
                    dct[sgnl.styp == "res"],
                )
            )

        for sigtype in config.sigtypes_analog_for_input:
            txt.write(f'// {sigtype}\n')
            ai_with_res = [
                signal for signal in self.signals_list
                if (
                        signal.sigtype in config.sigtypes_analog_for_input
                        and
                        signal.styp in config.styp_ai_reservation_for_input
                )
            ]
            ai_without_res = [
                signal for signal in self.signals_list
                if (
                        signal.sigtype in config.sigtypes_analog_for_input
                        and
                        signal.styp not in config.styp_ai_reservation_for_input
                )
            ]
            if len(ai_with_res) > 0:
                txt.write('// Нерезервированные\n')
                for signal in ai_with_res:
                    ai_write_to_txt(signal, txt)
            if len(ai_without_res) > 0:
                if len(ai_with_res) > 0:
                    txt.write('\n')
                txt.write('// Резервированные\n')
                for signal in ai_without_res:
                    ai_write_to_txt(signal, txt)
            txt.write('\n')

    # OUTPUT
    def output_write_to_txt(self, txt):
        """
        Метод записывает в txt строки кода на ST.
        В коде участвуют все сигналы из SignalsList
        .sigtype которых входят в
        config.sigtypes_for_output_txt.
        """
        txt.write(f'// {self.name_for_comment}\n')
        for sigtype in config.sigtypes_for_m_output:
            txt.write(f'// {sigtype}\n')
            for signal in self.signals_list:
                if signal.sigtype == sigtype:
                    txt.write(
                        f'{signal.name}(.IVXX, .MBIN, .CAON, '
                        '.SCMX, .STYP, SYS_LNG.XLNG, .IDVX);\n'
                    )
            txt.write('\n')
        for sigtype in config.sigtypes_for_nm_output:
            txt.write(f'// {sigtype}\n')
            for signal in self.signals_list:
                if signal.sigtype == sigtype:
                    inv = 'TRUE' if signal.styp == 'inv' else '.INVR'
                    txt.write(
                        f'{signal.name}(_IO_{signal.address}, .CAON, .MBIN, '
                        f'{inv}, SYS_LNG.XLNG);\n'
                        f'_IO_{signal.address}.ValueBOOL'
                        f':=NOT {signal.name}.OXON;\n\n'
                        )
            txt.write('\n')

    # ALARMING
    def alarming_write_to_txt(self, txt):
        """
        Метод записывает в txt строки кода на ST.
        В коде участвуют все сигналы из SignalsList
        .sigtype которых входят в
        config.sigtypes_for_alarming_txt и при этом
        их атрибут .ff_out is None.
        """
        if self.contains_locations_with_warning():
            warning_part = f' OR {self.name}_XWRX_CNT > 0'
        else:
            warning_part = ''

        txt.write(f'// {self.name_for_comment}\n')
        for sigtype in config.sigtypes_for_alarming:
            txt.write(f'// {sigtype}\n')
            for signal in self.signals_list:
                if (
                        signal.sigtype == sigtype
                        and
                        signal.ff_out is None
                        and
                        signal.styp not in config.styp_except_for_alarming
                ):
                    txt.write(
                        f'{signal.name}.CAON:='
                        f'{signal.position.name}_XFRX_CNT > 0'
                        f'{warning_part};\n'
                    )
            txt.write('\n')

    # COUNTING
    def counting_write_to_txt(self, txt):

        self.upg_markers.sort()

        txt.write(f'// {self.name_for_comment}\n')

        cntrs_markers = config.cntrs_dict
        position = self.name

        signals_for_counting = SignalsList(
            signal for signal in self.signals_list
            if signal.location is not self.plc.exceptions_location
        )

        # СЛОВАРИ НАЛИЧИЯ СЧЕТЧИКОВ НА ПОЗИЦИИ

        # счетчики не инициирующих тушение сигналов
        cntrs_without_ff = {
            'Имитации':
                signals_for_counting
                .has_any_signal_with_sigtype_in(
                    config.sigtypes_for_imitations_in_counting
                ),
            'Ремонты':
                signals_for_counting
                .contains_signals_for_counting(),
            'Неисправности':
                signals_for_counting
                .has_any_no_ff_or_ffo_signal_with_sigtype_in(
                    config.sigtypes_for_faults_in_counting
                ),
            'Недостоверности':
                signals_for_counting
                .has_any_no_ff_or_ffo_signal_with_sigtype_in(
                    config.sigtypes_for_falsities_in_counting
                ),
            'Пожары':
                self
                .contains_locations_with_fire(),
            'Внимания':
                signals_for_counting
                .contains_no_ff_or_ffo_signals_with_warning()
        }

        # счетчики инициирующих тушение сигналов
        cntrs_with_ff = {
            'Неисправности':
                signals_for_counting
                .has_any_ff_or_ffo_signal_with_sigtype_in(
                    config.sigtypes_for_faults_in_counting
                ),
            'Недостоверности':
                signals_for_counting
                .has_any_ff_or_ffo_signal_with_sigtype_in(
                    config.sigtypes_for_falsities_in_counting
                ),
            'Внимания':
                signals_for_counting
                .contains_ff_or_ffo_signals_with_warning()
        }

        # ОБНУЛЕНИЕ СЧЕТЧИКОВ
        txt.write('// Обнуление счетчиков\n')

        # без тушения
        for cntr in cntrs_without_ff:
            if cntrs_without_ff[cntr]:
                counter = f'{position}_{cntrs_markers[cntr]}_CNT'
                self.counters_for_sum.append(counter)
                self.counters.append(counter)
                bool_counter = f'{position}_{cntrs_markers[cntr]}'
                self.bool_counters.add(bool_counter)
                txt.write(f'{counter}:=0;\n')

        # c тушением
        for upg_marker in self.upg_markers:
            for cntr in cntrs_with_ff:
                if cntrs_without_ff[cntr]:
                    counter = (
                        f'{position}_'
                        f'{cntrs_markers[cntr]}_'
                        f'{upg_marker}_CNT'
                    )
                    self.counters.append(counter)
                    bool_counter = (
                        f'{position}_'
                        f'{upg_marker}_'
                        f'{cntrs_markers[cntr]}'
                    )
                    self.bool_counters.add(bool_counter)
                    txt.write(f'{counter}:=0;\n')

        if len(self.upg_counters) > 0:
            txt.write(
                f'{self.name}_XRFD_CNT:=0;\n'
                f'{self.name}_XRFN_CNT:=0;\n'
            )

        for counter in self.upg_counters:
            txt.write(f'{counter}:=0;\n')

        # смежные системы
        for counter in self.xsy_counters:
            txt.write(f'{counter}:=0;\n')

        # ИМИТАЦИИ
        if cntrs_without_ff['Имитации']:

            txt.write('\n// Имитации')
            cntr_marker = cntrs_markers['Имитации']
            counter = f'{position}_{cntr_marker}_CNT'

            for sigtype in config.sigtypes_for_imitations_in_counting:
                txt.write(f'\n// {sigtype}\n')
                for signal in signals_for_counting:
                    if signal.sigtype == sigtype:
                        txt.write(
                            self.counter_one_signal_actuation(
                                signal,
                                counter,
                                cntr_marker,
                            )
                        )
                # txt.write('\n')

        # РЕМОНТЫ, ОТКЛЮЧЕНИЯ
        if cntrs_without_ff['Ремонты']:

            txt.write('\n// Ремонты, отключения')
            cntr_marker = cntrs_markers['Ремонты']
            counter = f'{position}_{cntr_marker}_CNT'

            for sigtype in config.sigtypes_for_repairs_in_counting:
                txt.write(f'\n// {sigtype}\n')
                for signal in signals_for_counting:
                    if signal.sigtype == sigtype:
                        txt.write(
                            self.counter_one_signal_actuation(
                                signal,
                                counter,
                                cntr_marker,
                            )
                        )
                # txt.write('\n')

        # СЧЕТЧИКИ ИП БЕЗ ТУШЕНИЯ
        # НЕИСПРАВНОСТИ (сигналы без тушения)
        if cntrs_without_ff['Неисправности']:

            txt.write('\n// Неисправности (сигналы без тушения)')
            cntr_marker = cntrs_markers['Неисправности']
            counter = f'{position}_{cntr_marker}_CNT'

            for sigtype in config.sigtypes_for_faults_in_counting:
                txt.write(f'\n// {sigtype}\n')
                for signal in signals_for_counting:
                    if (
                            signal.sigtype == sigtype
                            and
                            signal.ff_out is None
                            and
                            (signal.location is None
                             or
                             (isinstance(signal.location, Location)
                              and
                              signal.location.fire_fightings_cntrs is None))
                    ):
                        txt.write(
                            self.counter_one_signal_actuation(
                                signal,
                                counter,
                                cntr_marker,
                            )
                        )
                # txt.write('\n')

        # НЕДОСТОВЕРНОСТИ (сигналы без тушения)
        if cntrs_without_ff['Недостоверности']:

            txt.write('\n// Недостоверности (сигналы без тушения)')
            cntr_marker = cntrs_markers['Недостоверности']
            counter = f'{position}_{cntr_marker}_CNT'

            for sigtype in config.sigtypes_for_falsities_in_counting:
                txt.write(f'\n// {sigtype}\n')
                for signal in signals_for_counting:
                    if (
                            signal.sigtype == sigtype
                            and
                            signal.ff_out is None
                            and
                            (signal.location is None
                             or
                             (isinstance(signal.location, Location)
                              and
                              signal.location.fire_fightings_cntrs is None))
                    ):
                        txt.write(
                            self.counter_one_signal_actuation(
                                signal,
                                counter,
                                cntr_marker,
                            )
                        )
                # txt.write('\n')

        def write_indent(pos, location, locs_lst, file):
            def condition(loc):
                if (
                        int(loc.voting_logic[0]) == 2
                        and
                        int(loc.voting_logic[1]) > 2
                ):
                    return True

            if condition(location):
                ind = 0
                for j in range(len(locs_lst)):
                    if location == locs_lst[j]:
                        ind += j
                        break
                if (
                        pos == 'prev'
                        and
                        location != locs_lst[0]
                        and not condition(locs_lst[ind - 1])
                ):
                    file.write('\n')
                elif (
                        pos == 'post'
                        and
                        location != locs_lst[-1]
                        # and not condition(locs_lst[ind + 1])
                ):
                    file.write('\n')

        # СМЕЖНЫЕ СИСТЕМЫ
        if len(self.xsy_counters) > 0:

            txt.write('\n// Смежные системы\n')
            cntr_marker = cntrs_markers["Пожары"]

            iteration = 1
            for counter in self.xsy_counters:

                selected_locations = [
                    location for location in self.locations_list
                    if (
                            location.conterminal_systems_cntrs is not None
                            and
                            counter in location.conterminal_systems_cntrs
                    )
                ]

                for location in selected_locations:

                    write_indent('prev', location, selected_locations, txt)
                    self.__counter_with_condition_write_to_txt(
                        txt,
                        location,
                        counter,
                        cntr_marker,
                    )
                    write_indent('post', location, selected_locations, txt)

                if iteration != len(self.xsy_counters):
                    txt.write('\n')
                iteration += 1

        # ПОЖАРЫ (сигналы без тушения)
        if cntrs_without_ff['Пожары']:

            txt.write('\n// Пожары (сигналы без тушения)\n')
            cntr_marker = cntrs_markers['Пожары']
            counter = f'{position}_{cntr_marker}_CNT'

            selected_locations = [
                location for location in self.locations_list
                if location.fire_cntr
            ]

            for location in selected_locations:

                write_indent('prev', location, selected_locations, txt)
                self.__counter_with_condition_write_to_txt(
                        txt,
                        location,
                        counter,
                        cntr_marker,
                    )
                write_indent('post', location, selected_locations, txt)

        # ВНИМАНИЯ (сигналы без тушения)
        if cntrs_without_ff['Внимания']:

            txt.write('\n// Внимания (сигналы без тушения)\n')
            cntr_marker = cntrs_markers['Пожары']
            counter = f'{position}_{cntrs_markers["Внимания"]}_CNT'

            for location in self.locations_list:
                if (
                        location.warning_cntr
                        and
                        location.fire_fightings_cntrs is None
                ):
                    for signal in location.signals_list:
                        if signal.ff_out is None:
                            txt.write(
                                self.counter_one_signal_actuation(
                                    signal,
                                    counter,
                                    cntr_marker,
                                )
                            )

        # СЧЕТЧИКИ ИП С ТУШЕНИЕМ
        # НЕИСПРАВНОСТИ (сигналы с тушением)
        if cntrs_with_ff['Неисправности']:

            txt.write('\n// Неисправности (сигналы с тушением)')
            cntr_marker = cntrs_markers['Неисправности']

            iteration = 1
            for upg_marker in self.upg_markers:
                counter = f'{position}_{cntr_marker}_{upg_marker}_CNT'
                check_counter = (
                    f'{position}_{cntrs_markers["Пожары"]}_{upg_marker}_CNT'
                )

                for sigtype in config.sigtypes_for_faults_in_counting:
                    txt.write(f'\n// {sigtype}\n')
                    for signal in signals_for_counting:
                        if (
                                signal.sigtype == sigtype
                                and
                                ((
                                     signal.ff_out is not None
                                     and
                                     any(ff_out == upg_marker for ff_out
                                         in signal.ff_out)
                                )
                                or
                                (isinstance(signal.location, Location)
                                 and
                                 signal
                                 .location.fire_fightings_cntrs is not None
                                 and
                                 (check_counter in
                                  signal.location.fire_fightings_cntrs)))
                        ):
                            txt.write(
                                self.counter_one_signal_actuation(
                                    signal,
                                    counter,
                                    cntr_marker,
                                )
                            )
                    # txt.write('\n')
                if iteration != len(self.upg_markers):
                    txt.write('\n')
                iteration += 1

        # НЕДОСТОВЕРНОСТИ (сигналы с тушением)
        if cntrs_with_ff['Недостоверности']:

            txt.write('\n// Недостоверности (сигналы с тушением)')
            cntr_marker = cntrs_markers['Недостоверности']

            iteration = 1
            for upg_marker in self.upg_markers:
                counter = f'{position}_{cntr_marker}_{upg_marker}_CNT'
                check_counter = (
                    f'{position}_{cntrs_markers["Пожары"]}_{upg_marker}_CNT'
                )

                for sigtype in config.sigtypes_for_falsities_in_counting:
                    txt.write(f'\n// {sigtype}\n')
                    for signal in signals_for_counting:
                        if (
                                signal.sigtype == sigtype
                                and
                                ((
                                         signal.ff_out is not None
                                         and
                                         any(ff_out == upg_marker for ff_out
                                             in signal.ff_out)
                                 )
                                 or
                                 (isinstance(signal.location, Location)
                                  and
                                  signal
                                  .location.fire_fightings_cntrs is not None
                                  and
                                  check_counter in
                                  signal.location.fire_fightings_cntrs))
                        ):
                            txt.write(
                                self.counter_one_signal_actuation(
                                    signal,
                                    counter,
                                    cntr_marker,
                                )
                            )
                    # txt.write('\n')
                if iteration != len(self.upg_markers):
                    txt.write('\n')
                iteration += 1

        # ПОЖАРОТУШЕНИЯ (Пожары с тушением)
        if (
                self.signals_list
                .contains_signals_with_fire_fighting_for_counting()
        ):

            txt.write('\n// Пожаротушения (пожары с тушением)\n')
            cntr_marker = cntrs_markers['Пожары']

            iteration = 1
            for counter in self.upg_counters:

                selected_locations = [
                    location for location in self.locations_list
                    if (
                            location.fire_fightings_cntrs is not None
                            and
                            counter in location.fire_fightings_cntrs
                    )
                ]

                for location in selected_locations:

                    write_indent('prev', location, selected_locations, txt)
                    self.__counter_with_condition_write_to_txt(
                        txt,
                        location,
                        counter,
                        cntr_marker,
                    )
                    write_indent('post', location, selected_locations, txt)

                if iteration != len(self.upg_counters):
                    txt.write('\n')
                iteration += 1

        # ВНИМАНИЯ (сигналы c тушением)
        if cntrs_with_ff['Внимания']:

            txt.write('\n// Внимания (сигналы с тушением)\n')
            cntr_marker = cntrs_markers['Пожары']

            for upg_marker in self.upg_markers:
                counter = (
                    f'{position}_{cntrs_markers["Внимания"]}_{upg_marker}_CNT'
                )
                check_counter = (
                    f'{position}_{cntrs_markers["Пожары"]}_{upg_marker}_CNT'
                )
                for location in self.locations_list:
                    if (
                            location.warning_cntr
                            and
                            location.fire_fightings_cntrs is not None
                            and
                            check_counter in location.fire_fightings_cntrs
                    ):
                        for signal in location.signals_list:
                            txt.write(
                                self.counter_one_signal_actuation(
                                    signal,
                                    counter,
                                    cntr_marker,
                                )
                            )

        # СЧЕТЧИКИ РЕЖИМА
        for upg_marker in self.upg_markers:
            txt.write(
                '\n// Счетчик режима "Идет отсчет до начала тушения"\n'
                '{0}_XRFD_CNT:=Count({0}_{1}.XFDN, {0}_XRFD_CNT);\n\n'
                .format(position, upg_marker)
                +
                '// Счетчик режима "Идет тушение"\n'
                '{0}_XRFN_CNT:=Count({0}_{1}.OF1N, {0}_XRFN_CNT);\n'
                .format(position, upg_marker)
            )

        # ОБЩИЕ СЧЕТЧИКИ
        txt.write('\n// Общие счетчики\n')

        for upg_marker in self.upg_markers:
            txt.write(
                '{0}_XFRX_CNT:=Plus({0}_XFRX_{1}_CNT, {0}_XFRX_CNT);\n'
                '{0}_XWRX_CNT:=Plus({0}_XWRX_{1}_CNT, {0}_XWRX_CNT);\n'
                '{0}_FXXX_CNT:=Plus({0}_FXXX_{1}_CNT, {0}_FXXX_CNT);\n'
                '{0}_DVXX_CNT:=Plus({0}_DVXX_{1}_CNT, {0}_DVXX_CNT);\n\n'
                '{0}_{1}_XFRX:={0}_XFRX_{1}_CNT > 0;\n'
                '{0}_{1}_XWRX:={0}_XWRX_{1}_CNT > 0;\n'
                '{0}_{1}_FXXX:={0}_FXXX_{1}_CNT > 0 OR '
                '{0}_DVXX_{1}_CNT > 0;\n\n'
                .format(position, upg_marker)
            )
        """
        for i in range(len(self.xsy_counters)):
            index = i+1 if len(self.xsy_counters) > 1 else ''
            txt.write(
                '{0}_{1}{2}:={0}_{1}_CNT{2} > 0;\n'.format(
                    self.name,
                    cntrs_markers['Смежные системы'],
                    index,
                )
            )
        """
        for key in cntrs_markers:
            if key != 'Смежные системы':
                txt.write(
                    f'{position}_{cntrs_markers[key]}:='
                    f'{position}_{cntrs_markers[key]}_CNT > 0;\n'
                )

        txt.write('\n')

    # WEINTEK
    def weintek_write_to_txt(self, txt):

        import pandas as pd
        data = pd.DataFrame(
            None,
            columns=[
                'Name',
                'Address 1',
                'Address 2',
                'Address 3',
                'Address 4',
                'Equipment type',
                'Tag',
                'MBIN',
                'Status',
                'XVLX',
                'Blnk',
                'Blnk_RP / Blnk_Fr',
                'XRPX',
                'XCIM',
            ],
            index=range(len(self.signals_list))
        )

        signals_list_without_exc = [
            signal for signal in self.signals_list
            if signal.location != self.plc.exceptions_location
        ]

        di_iteration = 0
        di_cnt = 0
        for sigtype in config.sigtypes_di_for_weintek:
            for signal in signals_list_without_exc:
                if signal.sigtype == sigtype:
                    data['Name'][di_iteration] = signal.name
                    data['Tag'][di_iteration] = f'(* {signal.name} *)'
                    data['Equipment type'][di_iteration] = '// Извещатели'
                    data['Address 1'][di_iteration] = (
                        int(self.izv_addr)
                        +
                        di_iteration
                        +
                        di_cnt
                    )
                    data['Address 2'][di_iteration] = (
                            int(self.izv_addr)
                            +
                            di_iteration
                            +
                            di_cnt
                            +
                            1
                    )
                    data['Address 3'][di_iteration] = (
                            int(self.izv_addr)
                            +
                            di_iteration
                            +
                            di_cnt
                            +
                            2
                    )
                    data['Address 4'][di_iteration] = (
                            int(self.izv_addr)
                            +
                            di_iteration
                            +
                            di_cnt
                            +
                            3
                    )
                    di_iteration += 1
                    di_cnt += 3

        do_iteration = 0
        do_cnt = 0
        for sigtype in config.sigtypes_do_for_weintek:
            for signal in signals_list_without_exc:
                if signal.sigtype == sigtype:
                    num = do_iteration + di_iteration
                    data['Name'][num] = signal.name
                    data['Tag'][num] = f'(* {signal.name} *)'
                    data['Equipment type'][num] = '// Оповещатели'
                    data['Address 1'][num] = (
                        int(self.opv_addr)
                        +
                        do_iteration
                        +
                        do_cnt
                    )
                    data['Address 2'][num] = (
                            int(self.opv_addr)
                            +
                            do_iteration
                            +
                            do_cnt
                            +
                            1
                    )
                    data['Address 3'][num] = (
                            int(self.opv_addr)
                            +
                            do_iteration
                            +
                            do_cnt
                            +
                            2
                    )
                    do_iteration += 1
                    do_cnt += 2

        for i in range(len(data)):

            data['MBIN'][i] = \
                f'{data["Name"][i]}.MBIN:=' \
                f'_IO_IX{self.plc.reg}_0_{data["Address 1"][i]};'

            data['Status'][i] = \
                f'_IO_QX{self.plc.reg}_1_{data["Address 2"][i]}:=' \
                f'{data["Name"][i]}.Status;'

            data['Blnk'][i] = \
                f'_IO_QX{self.plc.coil}_1_{data["Address 1"][i]}:=' \
                f'{data["Name"][i]}.Blnk;'

            data['XRPX'][i] = \
                f'_IO_QX{self.plc.coil}_1_{data["Address 3"][i]}:=' \
                f'{data["Name"][i]}.XRPX;'

            if data['Equipment type'][i] == '// Извещатели':

                data['XCIM'][i] = \
                    f'_IO_QX{self.plc.coil}_1_{data["Address 4"][i]}:=' \
                    f'{data["Name"][i]}.XCIM;'

                data['XVLX'][i] = \
                    f'_IO_QX{self.plc.reg}_1_{data["Address 3"][i]}:=' \
                    f'{data["Name"][i]}.XVLX;'

                data['Blnk_RP / Blnk_Fr'][i] = \
                    f'_IO_QX{self.plc.coil}_1_{data["Address 2"][i]}:=' \
                    f'{data["Name"][i]}.Blnk_RP;'

            elif data['Equipment type'][i] == '// Оповещатели':

                data['Blnk_RP / Blnk_Fr'][i] = \
                    f'_IO_QX{self.plc.coil}_1_{data["Address 2"][i]}:=' \
                    f'{data["Name"][i]}.Blnk_Fr;'

        # ИЗВЕЩАТЕЛИ
        if '// Извещатели' in list(data['Equipment type']):
            txt.write('// Извещатели\n')
            for i in range(len(data)):
                if data['Equipment type'][i] == '// Извещатели':
                    txt.write(
                        f'{data["Tag"][i]}\n'
                        f'{data["MBIN"][i]}\n'
                        f'{data["Status"][i]}\n'
                        f'{data["XVLX"][i]}\n'
                        f'{data["Blnk"][i]}\n'
                        f'{data["Blnk_RP / Blnk_Fr"][i]}\n'
                        f'{data["XRPX"][i]}\n'
                        f'{data["XCIM"][i]}\n\n'
                    )

        # ОПОВЕЩАТЕЛИ
        if '// Оповещатели' in list(data['Equipment type']):
            txt.write('// Оповещатели\n')
            for i in range(len(data)):
                if data['Equipment type'][i] == '// Оповещатели':
                    txt.write(
                        f'{data["Tag"][i]}\n'
                        f'{data["MBIN"][i]}\n'
                        f'{data["Status"][i]}\n'
                        f'{data["Blnk"][i]}\n'
                        f'{data["Blnk_RP / Blnk_Fr"][i]}\n'
                        f'{data["XRPX"][i]}\n\n'
                    )

        # АНАЛОГИ
        if self.ai_addr is not None:
            ai_addr = int(self.ai_addr)
            txt.write('// Аналоги\n')
            for sigtype in config.sigtypes_analog_for_weintek:
                txt.write(f'// {sigtype}\n')
                selected_signals = [
                    signal for signal in self.signals_list
                    if signal.sigtype == sigtype
                ]
                for signal in selected_signals:
                    txt.write(
                        f'_IO_QX1_1_{ai_addr}:='
                        f'ANY_TO_DINT({signal.name}.XVLX);\n'
                    )
                    ai_addr += 1
                txt.write('\n')

        # ТУШЕНИЕ
        if self.tush_addr is not None:
            tush_addr = int(self.tush_addr)
            txt.write('// Тушение\n')
            txt.write(f'(* {self.name_for_comment} *)\n')
            for upg_marker in self.upg_markers:
                txt.write(
                    f'{self.name}_{upg_marker}.MBIN:='
                    f'_IO_IX{self.plc.reg}_0_{tush_addr};\n'
                )
                for i in range(len(config.weintek_upg_tails_reg)):
                    tail = config.weintek_upg_tails_reg[i]
                    txt.write(
                        f'_IO_QX{self.plc.reg}_1_{int(tush_addr)+1+i}:='
                        f'{self.name}_{upg_marker}.{tail};\n'
                    )
                for i in range(len(config.weintek_upg_tails_coils)):
                    tail = config.weintek_upg_tails_coils[i]
                    txt.write(
                        f'_IO_QX{self.plc.coil}_1_{int(tush_addr)+i}:='
                        f'{self.name}_{upg_marker}.{tail};\n'
                    )
                txt.write(
                    f'_IO_QX{self.plc.coil}_1_{int(tush_addr)+5}:='
                    f'{self.name}_{upg_marker}.XCPX AND '
                    f'{self.name}_{upg_marker}.XDOF;\n\n'
                )
                tush_addr += 6

        # ЗАДВИЖКИ
        if (
                self.mov_addr is not None
                and
                any(signal.sigtype in config.sigtypes_valves_for_weintek
                    for signal in signals_list_without_exc)
        ):
            txt.write('// Задвижки\n')
            addr = int(self.mov_addr)
            for sigtype in config.sigtypes_valves_for_weintek:
                txt.write(f'// {sigtype}\n')
                selected_signals = [
                    signal for signal in signals_list_without_exc
                    if signal.sigtype == sigtype
                ]
                for signal in selected_signals:
                    txt.write(f'(* {signal.name} *)\n')
                    for el in config.weintek_valves_tails_with_comments[0:5]:
                        txt.write(
                            '{0}{1}:=_IO_IX{2}_0_{3}; {4}\n'.format(
                                signal.name,
                                el[0],
                                self.plc.reg,
                                addr,
                                el[1],
                            )
                        )
                        addr += 1
                    for el in config.weintek_valves_tails_with_comments[5:13]:
                        txt.write(
                            '_IO_QX{0}_1_{1}:={2}{3}; {4}\n'.format(
                                self.plc.reg,
                                addr,
                                signal.name,
                                el[0],
                                el[1],
                            )
                        )
                        addr += 1
                    first_addr = addr - 13
                    for el in config.weintek_valves_tails_with_comments[13:]:
                        txt.write(
                            '_IO_QX{0}_1_{1}:={2}{3}; {4}\n'.format(
                                self.plc.coil,
                                first_addr,
                                signal.name,
                                el[0],
                                el[1],
                            )
                        )
                        first_addr += 1
                    txt.write('\n')
                    addr += 3
                txt.write('\n')

        # ПЕРЕДАЧА XSY
        if (
                self.xsy_addr is not None
                and
                any(signal.sigtype in config.sigtypes_xsy_for_weintek
                    for signal in self.signals_list)
        ):

            i = 0

            # DO_NM
            if any(signal.sigtype in config.sigtypes_xsy_for_weintek
                   for signal in self.signals_list):

                txt.write('// DO_NM\n')
                txt.write(f'(* {self.name_for_comment} *)\n')

                for signal in self.signals_list:
                    for location in self.locations_list:
                        if (
                                signal.styp == location.name
                                and
                                signal.sigtype
                                in config.sigtypes_xsy_for_weintek
                        ):
                            txt.write(
                                f'_IO_QX{self.plc.coil}_1_'
                                f'{int(self.xsy_addr) + i}:='
                                f'{signal.name}.OXON;\n'
                            )
                            i += 1
                txt.write('\n')

            # DI_NM
            if any(signal.sigtype in config.sigtypes_di_nm_for_weintek
                   for signal in self.signals_list):

                txt.write('// DI_NM\n')
                txt.write(f'(* {self.name_for_comment} *)\n')
                for signal in self.signals_list:
                    for location in self.locations_list:
                        if (
                                signal.styp == location.name
                                and
                                signal.sigtype
                                in config.sigtypes_di_nm_for_weintek
                        ):
                            txt.write(
                                f'_IO_QX{self.plc.coil}_1_'
                                f'{int(self.xsy_addr) + i}:='
                                f'{signal.name}.XVLX;\n'
                            )
                            i += 1
                txt.write('\n')

        # data.to_excel(
        #     fr'{self.plc.output_path}\weintek_table.xls',
        #     index=False,
        # )

    # TO_SAU
    def to_sau_write_to_txt(self, txt):
        if self.signals_list.contains_signals_for_to_sau():
            txt.write(
                f'// {self.name_for_comment}\n'
                '// Сигналы в смежные системы\n'
            )
            for signal in self.signals_list:
                for location in self.locations_list:
                    if signal.styp == location.name:
                        txt.write(
                            f'{signal.name}.CAON:='
                            f'{location.conterminal_systems_cntrs[0]} > 0;\n'
                        )
            txt.write('\n')


class Device:

    def __init__(
            self,
            plc,
            name,
            devtype,
            cabinet,
            input_index,
            output_index=None,
            m=None,
            s=None,
    ):

        if not isinstance(plc, PLC):
            raise ValueError(
                'Аргуметом plc при создании '
                'экземпляра Device'
                'может выступать только '
                'экземпляр/наследник класса PLC!'
            )

        self.signals_list = []
        self.__reset_addresses = []

        self.plc = plc
        self.name = name
        self.devtype = devtype
        self.cabinet = cabinet
        self.input_index = input_index
        self.output_index = output_index
        self.m = m
        self.s = s

    # ВЫЗОВ БЛОКОВ
    def call_mops_mups_write_to_txt(self, txt):

        if self.devtype == 'MOPS':
            args = ''
            for i in range(len(config.mops_args)-1):
                args += f'.{config.mops_args[i]}, '
            args += f'.{config.mops_args[-1]}'
            result = f'{self.name}({args});\n'
            txt.write(result)

        elif self.devtype == 'MUPS':
            args = ''
            for i in range(len(config.mups_args) - 1):
                args += f'.{config.mups_args[i]}, '
            args += f'.{config.mups_args[-1]}'
            result = f'{self.name}({args});\n'
            txt.write(result)

        elif self.devtype == 'MOPS3a':
            args = f'_IO_IX{self.input_index}_0_3, '
            for i in range(len(config.mops3a_args) - 1):
                args += f'{config.mops3a_args[i]}, '
            args += config.mops3a_args[-1]
            result = f'{self.name}({args});\n'
            txt.write(result)

    # ПЕРЕКЛАДЫВАНИЕ
    @staticmethod
    def __shift(device, devtype, args, cnt=0):

        if device.devtype == devtype:
            result = ''
            for arg in args:

                result += \
                    f'{device.name}.{arg}:=' \
                    f'_IO_IX{device.input_index}_0_{cnt};\n'
                cnt += 1

            result += '\n'
            return result

    def mops_shifting_write_to_txt(self, txt):
        if self.__shift(self, 'MOPS', config.mops_args) is not None:
            txt.write(self.__shift(self, 'MOPS', config.mops_args))

    def mups_shifting_write_to_txt(self, txt):
        if self.__shift(self, 'MUPS', config.mups_args, cnt=4) is not None:
            txt.write(self.__shift(self, 'MUPS', config.mups_args, cnt=4))

    # IVXX IDVX
    @staticmethod
    def __ivxx(device, devtype, args):

        if device.devtype == devtype:
            result = f'(* {device.name} *)\n'
            for i in range(len(args)):

                if isinstance(device.signals_list[i], Signal):
                    signal_name = device.signals_list[i].name
                    result += \
                        f'{signal_name}.IVXX:={device.name}.{args[i]}o;\n'

                elif device.signals_list[i] == '0':
                    result += f'// {args[i]} reserved\n'

            result += '\n'
            return result

    def mops_ivxx_write_to_txt(self, txt):
        if self.__ivxx(self, 'MOPS', config.mops_args) is not None:
            txt.write(self.__ivxx(self, 'MOPS', config.mops_args))

    def mups_ivxx_write_to_txt(self, txt):
        if self.__ivxx(self, 'MUPS', config.mups_args) is not None:
            txt.write(self.__ivxx(self, 'MUPS', config.mups_args))

    @staticmethod
    def __idvx(device, devtype, args):

        if device.devtype == devtype:
            result = f'(* {device.name} *)\n'
            for i in range(len(args)):

                if isinstance(device.signals_list[i], Signal):
                    signal_name = device.signals_list[i].name
                    result += \
                        f'{signal_name}.IDVX:={device.name}.DVXX;\n'

                elif device.signals_list[i] == '0':
                    result += f'// {args[i]} reserved\n'

            result += '\n'
            return result

    def mops_idvx_write_to_txt(self, txt):
        if self.__idvx(self, 'MOPS', config.mops_args) is not None:
            txt.write(self.__idvx(self, 'MOPS', config.mops_args))

    def mups_idvx_write_to_txt(self, txt):
        if self.__idvx(self, 'MUPS', config.mups_args) is not None:
            txt.write(self.__idvx(self, 'MUPS', config.mups_args))

    # OXON
    def mups_oxon_write_to_txt(self, txt):

        if self.devtype == 'MUPS':
            txt.write(
                f'(* {self.name} *)\n'
            )
            for i in range(len(config.mups_args)):

                if isinstance(self.signals_list[i], Signal):
                    signal_name = self.signals_list[i].name
                    txt.write(
                        f'_IO_QX{self.output_index}_1_{i}:='
                        f'{signal_name}.OXON;\n'
                    )

                elif self.signals_list[i] == '0':
                    txt.write(
                        f'// {config.mups_args[i]} reserved\n'
                    )

            txt.write('\n')

    # СБРОС МОСОВ
    def mops_reset_write_to_txt(self, txt):

        if self.devtype == 'MOPS':
            result = f'(* {self.name} *)\n'
            args = config.mops_args
            for i in range(len(args)):

                if isinstance(self.signals_list[i], Signal):
                    signal_name = self.signals_list[i].name
                    result += \
                        f'_IO_QX{self.output_index}_1_0.ValueDINT' \
                        f':={signal_name}.ORS3;\n'

                elif self.signals_list[i] == '0':
                    result += f'// {args[i]} reserved\n'

            result += '\n'
            txt.write(result)

    #  МОПСЫ 3а
    def __mops3a_has_any_m(self):
        if self.devtype == 'MOPS3a':
            flg = False
            for signal in self.signals_list:
                if signal.styp in config.styp_for_m_in_mops3a:
                    flg = True
                    break
            return flg

    @staticmethod
    def __three_addr(x):
        if (x * 3) % 90 == 0:
            return (x * 3) % 90 - 2 + 90
        else:
            return (x * 3) % 90 - 2

    def __m_name(self, addr, sm):
        return f'M{self.name[5:]}_{sm}_A{addr}'

    # м-имя для теста/сброса МОПСов 3а
    def __m_name_s_f_s(self, first, second):
        return f'M{self.name[5:]}_S_{first}_{second}'

    def mops3a_m_write_to_txt(self, txt):

        if self.__mops3a_has_any_m():

            txt.write(
                f'(* {self.name} *)\n'
                '//Ручные извещатели\n'
            )
            m_index_num = 0
            m_signals_lst = []

            for signal in self.signals_list:
                if signal.styp in config.styp_for_m_in_mops3a:
                    m_signals_lst.append(signal)

            m_signals_lst.sort(
                key=lambda sgnl: int(sgnl.address)
            )

            for signal in m_signals_lst:

                if len(self.m) > 1:
                    addr = int(signal.address)
                    if addr in range(1, 31):
                        m_index_num = 0
                    elif addr in range(31, 61):
                        m_index_num = 1
                    elif addr in range(61, 91):
                        m_index_num = 2
                    elif addr in range(91, 121):
                        m_index_num = 3
                    elif addr in range(121, 151):
                        m_index_num = 4

                addr = str(signal.address)
                if len(addr) == 1:
                    addr = '0' + addr

                three_addr = self.__three_addr(int(addr))

                m_name = self.__m_name(addr, 'M')
                self.plc.m_names.add(m_name)

                # Аргуметы
                arg1 = \
                    f'_IO_IX{self.input_index}_0_3'
                arg2 = \
                    f'_IO_IX{self.m[m_index_num]}_0_{three_addr}.ValueDINT'
                arg3 = \
                    f'{signal.name}.ORST'
                arg4 = \
                    '.CTST'
                arg5 = \
                    f'{config.address_bit[int(addr)]}'
                arg6 = \
                    f'.RST_CNT'
                arg7 = \
                    f'.TST_CNT'

                txt.write(
                    f'{m_name}('
                    f'{arg1}, '
                    f'{arg2}, '
                    f'{arg3}, '
                    f'{arg4}, '
                    f'{arg5}, '
                    f'{arg6}, '
                    f'{arg7});\n'
                )

            txt.write('\n')

    def __mops3a_has_any_s(self):
        if self.devtype == 'MOPS3a':
            flg = False
            for signal in self.signals_list:
                if signal.styp in config.styp_for_s_in_mops3a:
                    flg = True
                    break
            return flg

    def mops3a_s_write_to_txt(self, txt):

        if self.__mops3a_has_any_s():

            txt.write(
                f'(* {self.name} *)\n'
                '// Дымовые и тепловые извещатели\n'
            )
            s_signals_lst = []

            for signal in self.signals_list:
                if signal.styp in config.styp_for_s_in_mops3a:
                    s_signals_lst.append(signal)

            s_signals_lst.sort(
                key=lambda sgnl: int(sgnl.address)
            )

            from math import floor

            s_index_num = 0
            prev_addr = None
            prev_m_name = None

            iteration = 0
            for signal in s_signals_lst:
                iteration += 1

                if len(self.s) > 1:
                    addr = int(signal.address)
                    if addr in range(1, 31):
                        s_index_num = 0
                    elif addr in range(31, 61):
                        s_index_num = 1
                    elif addr in range(61, 91):
                        s_index_num = 2
                    elif addr in range(91, 121):
                        s_index_num = 3
                    elif addr in range(121, 151):
                        s_index_num = 4

                addr = str(signal.address)
                if len(addr) == 1:
                    addr = '0' + addr

                m_name = self.__m_name(addr, 'S')
                self.plc.m_names.add(m_name)

                three_addr = self.__three_addr(int(addr))

                if iteration == 1:

                    # Аргуметы
                    arg1 = \
                        f'_IO_IX{self.input_index}_0_3'
                    arg2 = \
                        f'_IO_IX{self.s[s_index_num]}_0_{three_addr}.ValueDINT'
                    arg3 = \
                        f'{signal.name}.ORST'
                    arg4 = \
                        '.CTST'
                    arg5 = \
                        f'{config.address_bit[int(addr)]}'
                    arg6 = \
                        '0'
                    arg7 = \
                        '0'

                    txt.write(
                        f'{m_name}('
                        f'{arg1}, '
                        f'{arg2}, '
                        f'{arg3}, '
                        f'{arg4}, '
                        f'{arg5}, '
                        f'{arg6}, '
                        f'{arg7});\n'
                    )

                elif (
                        floor((int(addr) - 1) / 16)
                        >
                        floor((int(prev_addr) - 1) / 16)
                ):

                    self.__reset_addresses.append(prev_addr)

                    # Аргуметы
                    arg1 = \
                        f'_IO_IX{self.input_index}_0_3'
                    arg2 = \
                        f'_IO_IX{self.s[s_index_num]}_0_{three_addr}' \
                        f'.ValueDINT'
                    arg3 = \
                        f'{signal.name}.ORST'
                    arg4 = \
                        '.CTST'
                    arg5 = \
                        f'{config.address_bit[int(addr)]}'
                    arg6 = \
                        '0'
                    arg7 = \
                        '0'

                    txt.write(
                        f'{m_name}('
                        f'{arg1}, '
                        f'{arg2}, '
                        f'{arg3}, '
                        f'{arg4}, '
                        f'{arg5}, '
                        f'{arg6}, '
                        f'{arg7});\n'
                    )

                else:

                    # Аргуметы
                    arg1 = \
                        f'_IO_IX{self.input_index}_0_3'
                    arg2 = \
                        f'_IO_IX{self.s[s_index_num]}_0_{three_addr}' \
                        f'.ValueDINT'
                    arg3 = \
                        f'{signal.name}.ORST'
                    arg4 = \
                        '.CTST'
                    arg5 = \
                        f'{config.address_bit[int(addr)]}'
                    arg6 = \
                        f'{prev_m_name}.RST_CNTo'
                    arg7 = \
                        f'{prev_m_name}.TST_CNTo'

                    txt.write(
                        f'{m_name}('
                        f'{arg1}, '
                        f'{arg2}, '
                        f'{arg3}, '
                        f'{arg4}, '
                        f'{arg5}, '
                        f'{arg6}, '
                        f'{arg7});\n'
                    )

                prev_addr = addr
                prev_m_name = m_name

            self.__reset_addresses.append(prev_addr)

            txt.write('\n')

    # ТЕСТ/СБРОС МОПСОВ 3А
    def mops3a_test_reset_write_to_txt(self, txt):

        if self.devtype == 'MOPS3a' and self.__reset_addresses is not None:

            first = 1
            second = 16
            cnt = 0

            txt.write(f'(* {self.name} *)\n')

            for addr in self.__reset_addresses:

                m_name = self.__m_name_s_f_s(first, second)

                # Аргуметы
                arg1 = \
                    f'_IO_IX{self.input_index}_0_{14+cnt}.ValueDINT'
                arg2 = \
                    f'_IO_IX{self.input_index}_0_{78+cnt}.ValueDINT'
                arg3 = \
                    f'{self.__m_name(addr, "S")}.RST_CNTo'
                arg4 = \
                    f'{self.__m_name(addr, "S")}.TST_CNTo'
                arg5 = \
                    '.FL'

                txt.write(
                    f'{m_name}('
                    f'{arg1}, '
                    f'{arg2}, '
                    f'{arg3}, '
                    f'{arg4}, '
                    f'{arg5});\n'
                )

                cnt += 1
                first += 16
                second += 16

            txt.write('\n')
            first = 1
            second = 16
            cnt = 0

            for _ in self.__reset_addresses:

                m_name = self.__m_name_s_f_s(first, second)

                var1 = f'_IO_QX{self.input_index}_1_{78+cnt}.ValueDINT'
                var2 = f'{m_name}.XTST'

                txt.write(f'{var1}:={var2};\n')

                var1 = f'_IO_QX{self.input_index}_1_{14 + cnt}.ValueDINT'
                var2 = f'{m_name}.XRST'

                txt.write(f'{var1}:={var2};\n')

                first += 16
                second += 16
                cnt += 1

            txt.write('\n')

    @staticmethod
    def __ivxx_xvlx_idvx_dvxx(device, arg1, arg2, styps_lst, ms):

        text = ''
        selected_signals_lst = []

        for signal in device.signals_list:
            if signal.styp in styps_lst:
                selected_signals_lst.append(signal)

        selected_signals_lst.sort(
            key=lambda sgnl: int(sgnl.address)
        )

        for signal in selected_signals_lst:

            addr = str(int(signal.address))
            if len(addr) == 1:
                addr = '0' + addr

            m_name = Device.__m_name(device, addr, ms)

            text += f'{signal.name}.{arg1}:={m_name}.{arg2};\n'

        text += '\n'
        return text

    def mops3a_m_ivxx_xvlx_write_to_txt(self, txt):
        if self.__mops3a_has_any_m():
            txt.write(
                f'(* {self.name} *)\n'
                '// Ручные извещатели\n'
            )
            txt.write(
                self.__ivxx_xvlx_idvx_dvxx(
                    self,
                    'IVXX',
                    'XVLX',
                    config.styp_for_m_in_mops3a,
                    'M'
                )
            )

    def mops3a_s_ivxx_xvlx_write_to_txt(self, txt):
        if self.__mops3a_has_any_s():
            txt.write(
                f'(* {self.name} *)\n'
                '// Дымовые и тепловые извещатели\n'
            )
            txt.write(
                self.__ivxx_xvlx_idvx_dvxx(
                    self,
                    'IVXX',
                    'XVLX',
                    config.styp_for_s_in_mops3a,
                    'S',
                )
            )

    def mops3a_m_idvx_dvxx_write_to_txt(self, txt):
        if self.__mops3a_has_any_m():
            txt.write(
                f'(* {self.name} *)\n'
                '// Ручные извещатели\n'
            )
            txt.write(
                self.__ivxx_xvlx_idvx_dvxx(
                    self,
                    'IDVX',
                    'DVXX',
                    config.styp_for_m_in_mops3a,
                    'M',
                )
            )

    def mops3a_s_idvx_dvxx_write_to_txt(self, txt):
        if self.__mops3a_has_any_s():
            txt.write(
                f'(* {self.name} *)\n'
                '// Дымовые и тепловые извещатели\n'
            )
            txt.write(
                self.__ivxx_xvlx_idvx_dvxx(
                    self,
                    'IDVX',
                    'DVXX',
                    config.styp_for_s_in_mops3a,
                    'S',
                )
            )


class PLC:

    def __init__(
            self,
            name,
            cabinet_category,
            reset_position,
            diag_addr=None,
            reg=None,
            coil=None,
    ):
        self.name = name
        self.cabinet_category = cabinet_category
        self.reset_position_for_comment = reset_position
        self.reset_position = Position.format_position_name(reset_position)

        self.diag_addr = diag_addr
        self.reg = reg
        self.coil = coil

        self.__signals_list = SignalsList()
        self.__locations_list = []
        self.__positions_list = []
        self.__devices_list = []
        # self.diag_position = Position(name='Diag_Position', plc=self)

        self.exceptions_location = None

        self.upg_counters = set()
        self.xsy_counters = set()
        self.other_counters = set()
        self.m_names = set()

        self.signals_list_filled = False
        self.ce_locations_filled = False
        self.devices_list_filled = False

        self.signals_reformed = False
        self.locations_reformed = False
        self.devices_reformed = False

        self.devices_diag_signals_created = False

        self.__counting_was_formed = False
        self.__mops_mups_was_formed = False

        self.output_path = None

    def change_output_path(self):
        self.output_path = str(input(
            'Введите путь для выходных файлов\n'
        ))

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$ ДОБАВЛЕНИЕ ЭКЗЕМПЛЯРОВ В СПИСКИ $$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def append_signal(self, obj):
        if isinstance(obj, Signal):
            self.__signals_list.append(obj)
        else:
            raise TypeError(
                'Попытка добавить в список сигналов контроллера'
                ' объект не являющийся экземпляром/наследником '
                'класса Signal.'
            )

    def append_location(self, obj):
        if isinstance(obj, Location):
            self.__locations_list.append(obj)
        else:
            raise TypeError(
                'Попытка добавить в список локаций контроллера'
                ' объект не являющийся экземпляром/наследником'
                ' класса Location.'
            )

    def append_position(self, obj):
        if isinstance(obj, Position):
            self.__positions_list.append(obj)
        else:
            raise TypeError(
                'Попытка добавить в список позиций контроллера'
                ' объект не являющийся экземпляром/наследником'
                ' класса Position.'
            )

    def append_device(self, obj):
        if isinstance(obj, Device):
            self.__devices_list.append(obj)
        else:
            raise TypeError(
                'Попытка добавить в список устройств контроллера'
                ' объект не являющийся экземпляром/наследником'
                ' класса Device.'
            )

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$ ОПЕРАЦИИ НАД ОБЪЕКТАМИ В СПИСКАХ $$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def sort_signals_except_for_diag_signals(self):

        sorted_signals = [
            signal for signal in self.__signals_list
            if signal.sigtype not in config.sigtypes_of_diagnostic_signals
        ]
        sorted_signals.sort(key=lambda signal: signal.name)

        not_sorted_signals = [
            signal for signal in self.__signals_list
            if signal.sigtype in config.sigtypes_of_diagnostic_signals
        ]

        self.__signals_list = SignalsList(sorted_signals + not_sorted_signals)

    def __fill_positions_signals_lists(self):
        """
        Заполнение signals_list экземпляров
        Position находящихся в self.__positions_list
        ссылками на экземпляры Signal.
        Запись ссылок на экземпляры Position в
        сооветствующие атрибуты экземпляров Signal.
        """
        for position in self.__positions_list:
            for signal in self.__signals_list:
                if signal.position == position.name:
                    position.signals_list.append(signal)
                    signal.position = position

    def __fill_locations_signals_lists_and_position(self):
        """
        Заполнение signals_list экземпляров
        Location находящихся в self.__locations_list
        ссылками на экземпляры Signal.
        Запись ссылок на экземпляры Location в
        сооветствующие атрибуты экземпляров Signal.
        """
        for location in self.__locations_list:
            for signal in self.__signals_list:
                if location.name == signal.location:
                    location.append_signal(signal)
                    """
                    Замена строковых значений
                    signal.location полученных
                    при чтении входных данных
                    ссылкой на соответствующие
                    экземпляры Location
                    """
                    signal.location = location
            if location != self.exceptions_location:
                location.position_check_and_set()

    def __fill_counters(self):
        """
        Для каждой позиции:
        Определение количесва счетчиков сигналов
        в смежные системы.
        Опредедение количества счетчиков для
        систем пожаротушений.
        Формирование имен для счетчиков.
        Запись в соответсвующие атрибуты у
        экземпляров Location.
        """
        for position in self.__positions_list:
            conterminal_systems = set()  # все смежные системы на позиции
            fire_fightings = set()  # все пожаротушения на позиции
            for location in position.locations_list:
                # Смежные системы
                if location.conterminal_systems_cntrs is not None:
                    cntrmnl_sstms_lst = location.conterminal_systems_cntrs
                    for conterminal_system in cntrmnl_sstms_lst:
                        conterminal_systems.add(conterminal_system)
                # Пожаротушения
                if location.fire_fightings_cntrs is not None:
                    fr_fghtngs_lst = location.fire_fightings_cntrs
                    for fire_fighting in fr_fghtngs_lst:
                        fire_fightings.add(fire_fighting)

            # словарь для смежных систем
            xsy_uniq_locations = {}
            # ключи - названия смежных систем, значения - "локации"
            for conterminal_system in conterminal_systems:
                xsy_uniq_locations[conterminal_system] = []
                for location in position.locations_list:
                    if location.conterminal_systems_cntrs is not None:
                        if (
                                conterminal_system
                                in
                                location.conterminal_systems_cntrs
                        ):
                            xsy_uniq_locations[conterminal_system].append(
                                location.name
                            )

            # удаляем неуникальные по "локациям" смежные системы
            lst_of_loc_lsts = []
            xsy_uniq_locations_for_iter = xsy_uniq_locations.copy()
            for conterminal_system in xsy_uniq_locations_for_iter:
                lst = xsy_uniq_locations[conterminal_system]
                if xsy_uniq_locations[conterminal_system] in lst_of_loc_lsts:
                    del xsy_uniq_locations[conterminal_system]
                lst_of_loc_lsts.append(lst)
            xsy_uniq_locations_for_iter.clear()
            lst_of_loc_lsts.clear()

            """
            Замена названий смежных систем из входных
            данных во временном словаре на названия
            счетчиков сигналов в эти смежные системы
            принятые в проекте для дальнейшего использования
            в коде на ST.
            """

            xsy_uniq_locations_for_iter = xsy_uniq_locations.copy()

            # Если счетчиков смежных систем больше одного
            num = 1  # в конце имени каджого добавляется порядковый номер
            if xsy_uniq_locations_for_iter == 1:
                num = ''

            xsy_uniq_locations.clear()
            for conterminal_system in xsy_uniq_locations_for_iter:
                counter = \
                    f'{position.name}_' \
                    f'{config.cntrs_dict["Смежные системы"]}_CNT' \
                    f'{num}'
                xsy_uniq_locations[counter] = \
                    xsy_uniq_locations_for_iter[conterminal_system]
                # добавление в атрибут позиции
                position.xsy_counters.append(counter)
                num += 1
            xsy_uniq_locations_for_iter.clear()

            """
            Заполнение атрибутов conterminal_systems_cntrs
            экземпляров Location необходимыми для формирования
            текста программ именами счетчиков сигналов в смежные
            системы.
            """

            for location in position.locations_list:
                # очистка от неактульных значений
                location.conterminal_systems_cntrs = None
                for conterminal_system in xsy_uniq_locations:
                    if (
                            location.name
                            in
                            xsy_uniq_locations[conterminal_system]
                    ):
                        if location.conterminal_systems_cntrs is None:
                            location.conterminal_systems_cntrs = []
                            location.conterminal_systems_cntrs.append(
                                conterminal_system
                            )
                        else:
                            location.conterminal_systems_cntrs.append(
                                conterminal_system
                            )

            # словарь для пожаротушений
            fire_fightings_locations = {}
            # ключи - названия пожаротушений, значения - "локации"
            for fire_fighting in fire_fightings:
                fire_fightings_locations[fire_fighting] = []
                for location in position.locations_list:
                    if location.fire_fightings_cntrs is not None:
                        if (
                                fire_fighting
                                in
                                location.fire_fightings_cntrs
                        ):
                            fire_fightings_locations[fire_fighting].append(
                                location.name
                            )

            """
            Замена названий пожаротушений из входных
            данных во временном словаре на названия
            счетчиков сигналов в эти пожаротушения
            принятые в проекте для дальнейшего
            использования в коде на ST.
            """

            fire_fightings_locations_for_iter = fire_fightings_locations.copy()
            fire_fightings_locations.clear()
            for fire_fighting in fire_fightings_locations_for_iter:
                fire_fightings_locations[
                    f'{position.name}_'
                    f'{config.cntrs_dict["Пожары"]}_'
                    f'{fire_fighting}_CNT'
                ] = fire_fightings_locations_for_iter[fire_fighting]

                # добавление в атрибуты экземпляра позиции
                position.upg_counters.append(
                    f'{position.name}_'
                    f'{config.cntrs_dict["Пожары"]}_'
                    f'{fire_fighting}_CNT'
                )

                # для использования в именах других счетчиков
                # в срабатывании которых будут участвовать
                # сигналы с тушением
                position.upg_markers.append(fire_fighting)

            fire_fightings_locations_for_iter.clear()

            """
            Заполнение атрибутов fire_fightings_cntrs
            экземпляров Location необходимыми для формирования
            текста программ именами счетчиков сигналов в
            пожаротушения.
            """

            for location in position.locations_list:
                # очистка от неактульных значений
                location.fire_fightings_cntrs = None
                for fire_fighting in fire_fightings_locations:
                    if (
                            location.name
                            in
                            fire_fightings_locations[fire_fighting]
                    ):
                        if location.fire_fightings_cntrs is None:
                            location.fire_fightings_cntrs = []
                            location.fire_fightings_cntrs.append(
                                fire_fighting
                            )
                        else:
                            location.fire_fightings_cntrs.append(
                                fire_fighting
                            )

    def __fill_devices_signals_lists(self):

        for device in self.__devices_list:

            if device.devtype == 'MOPS':
                for signal in self.__signals_list:
                    if signal.device == device.name:
                        addr = signal.address
                        if (
                                addr[0:2] != 'CH'
                                or
                                int(addr[2:]) > len(config.mops_args)
                                or
                                int(addr[2:]) < 1
                        ):
                            raise ValueError(
                                'Обнаружено некорректное значение'
                                'атрибута .address экземпляра Signal.\n'
                                f'Проверьте input.xlsx (сигнал {signal.name},'
                                ' см. значение в столбце Address).'
                            )
                        else:
                            device.signals_list[int(addr[2:])-1] = signal

            elif device.devtype == 'MUPS':
                for signal in self.__signals_list:
                    if signal.device == device.name:
                        addr = signal.address
                        if (
                                addr[0:2] != 'CH'
                                or
                                int(addr[2:]) > len(config.mups_args)
                                or
                                int(addr[2:]) < 1
                        ):
                            raise ValueError(
                                'Обнаружено некорректное значение'
                                'атрибута .address экземпляра Signal.\n'
                                f'Проверьте input.xlsx (сигнал {signal.name},'
                                ' см. значение в столбце Address).'
                            )
                        else:
                            device.signals_list[int(addr[2:])-1] = signal

            elif device.devtype == 'MOPS3a':
                for signal in self.__signals_list:
                    if signal.device == device.name:
                        device.signals_list.append(signal)

    def __create_devices_diag_signals(self):

        d = {
            'MOPS3a': 'Mops3A',
            'MOPS': 'Mops3',
            'MUPS': 'Mups3',
        }
        for device in self.__devices_list:

            signal = Signal(
                name=device.name,
                plc=self,
                sigtype=d[device.devtype],
                position=device.cabinet,
            )

            for position in self.__positions_list:
                if position.name == signal.position:
                    signal.position = position
                    position.signals_list.append(signal)

            self.append_signal(signal)

    def input_data_reformation(self):
        """
        Обработка данных полученных при выполнении
        функции read() из модуля read_input.
        "Взведение" флагов, указывающих на то,
        какие именно операции по обработке данных
        были выполнены.
        """
        print('\n\tПреобразование входных данных...\n')

        if self.signals_list_filled:
            self.__fill_positions_signals_lists()
            self.signals_reformed = True
            # отсортируем позиции

            not_diag_positions = [
                position for position in self.__positions_list
                if not position.is_diag()
            ]

            diag_positions = [
                position for position in self.__positions_list
                if position.is_diag()
            ]

            not_diag_positions.sort(
                key=lambda position: position.name_for_comment
            )
            self.__positions_list = not_diag_positions + diag_positions

            if self.ce_locations_filled:
                self.__fill_locations_signals_lists_and_position()
                self.__fill_counters()
                self.locations_reformed = True

            if self.devices_list_filled:
                self.__fill_devices_signals_lists()
                self.devices_reformed = True
                self.__create_devices_diag_signals()
                self.devices_diag_signals_created = True

        """
        for position in self.__positions_list:
            if position.is_diag():
                print(position.name_for_comment)
                for signal in position.signals_list:
                    print(signal.name)
        """

        print(
            'Атрибуты экземпляров сигналов заполнены по словарю, '
            'экземпляры сигналов и позиций соотнесены: '
            f'{self.signals_reformed}'
        )
        print(
            'Экземпляры сигналов, локаций и позиций соотнесены, '
            f'созданы имена счетчиков: {self.locations_reformed}'
        )
        print(
            'Экземпляры сигналов и устройств соотнесены: '
            f'{self.devices_reformed}'
        )
        print(
            f'Экземпляры сигналов диагностики '
            f'устройств созданы: {self.devices_diag_signals_created}'
        )

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$ ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ $$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    @staticmethod
    def __counter_one_signal_actuation_inv(
            signal,
            counter,
            cntr_marker,
    ):
        if signal.styp != 'inv':
            return (
                f'{counter}:=Count({signal.name}.{cntr_marker}, {counter});\n'
            )
        elif signal.styp == 'inv':
            return (
                f'{counter}:='
                f'Count((NOT {signal.name}.{cntr_marker}), {counter});\n'
            )

    def __contains_devtype_in_devices_list(self, devtype):
        return (
            any(device.devtype == devtype for device in self.__devices_list)
        )

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$ ПРОВЕРКА ГОТОВНОСТИ К ФОРМИРОВАНИЮ ПРОГРАММ $$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    # INPUT
    def ready_for_input(self):
        return (
            self.__signals_list.contains_signals_for_input()
            and
            self.signals_reformed
        )

    # OUTPUT
    def ready_for_output(self):
        return (
            self.__signals_list.contains_signals_for_output()
            and
            self.signals_reformed
        )

    # ALARMING
    def ready_for_alarming(self):
        return (
            self.ready_for_counting()
            and
            self.__signals_list.contains_signals_for_alarming()
        )

    # COUNTING
    def ready_for_counting(self):
        return (
            self.__signals_list.contains_signals_for_counting()
            and
            self.locations_reformed
            and
            self.__signals_list.contains_diagnostic_signals()
            and
            self.devices_diag_signals_created
        )

    # MOPS_MUPS
    def ready_for_mops_mups(self):
        return self.devices_reformed

    # RESET_MOPS3A
    def ready_for_reset_mops3a(self):
        return (
                self.devices_reformed
                and
                self.__contains_devtype_in_devices_list('MOPS3a')
        )

    # OXON
    def ready_for_oxon(self):
        return self.devices_reformed

    # WEINTEK
    def ready_for_weintek(self):
        return (
                self.signals_list_filled
                and
                self.signals_reformed
                and
                any(position.izv_addr is not None
                    and
                    position.opv_addr is not None
                    and
                    len(position.signals_list) != 0
                    for position in self.__positions_list)
                and
                self.devices_diag_signals_created
                and
                self.__signals_list.contains_diagnostic_signals()
        )

    # TO_SAU
    def ready_for_to_sau(self):
        return self.__signals_list.contains_signals_for_to_sau()

    # DIAG
    def ready_for_diag(self):
        return self.__signals_list.contains_signals_for_diag()

    # DATATABLE
    def ready_for_datatable(self):
        return self.__counting_was_formed and self.__mops_mups_was_formed

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$ ФОРМИРОВАНИЕ ТЕКСТОВ ПРОГРАММ $$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    # INPUT
    def establishing_input_txt(self):
        if self.ready_for_input():
            txt = open(fr'{self.output_path}\Input.txt', 'w')
            for position in self.__positions_list:
                if position.signals_list.contains_signals_for_input():
                    position.input_write_to_txt(txt)
            txt.close()
            return True

    # OUTPUT
    def establishing_output_txt(self):
        if self.ready_for_input():
            txt = open(fr'{self.output_path}\Output.txt', 'w')
            for position in self.__positions_list:
                if position.signals_list.contains_signals_for_output():
                    position.output_write_to_txt(txt)
            txt.close()
            return True

    # ALARMING
    def establishing_alarming_txt(self):
        if self.ready_for_alarming():
            txt = open(fr'{self.output_path}\Alarming.txt', 'w')
            for position in self.__positions_list:
                if position.signals_list.contains_signals_for_alarming():
                    position.alarming_write_to_txt(txt)
            txt.close()
            return True

    # COUNTING
    def establishing_counting_txt(self):
        if self.ready_for_counting():
            txt = open(fr'{self.output_path}\Counting.txt', 'w')
            for position in self.__positions_list:
                if position.signals_list.contains_signals_for_counting():
                    position.counting_write_to_txt(txt)
            # Обнуление общих счетчиков
            cab_faults_cntr = (
                f'{self.reset_position}_CAB_'
                f'{config.cntrs_dict["Неисправности"]}_CNT'
            )
            cab_falsities_cntr = (
                f'{self.reset_position}_CAB_'
                f'{config.cntrs_dict["Недостоверности"]}_CNT'
            )
            txt.write(
                f'{cab_faults_cntr}:=0;\n'
                f'{cab_falsities_cntr}:=0;\n\n'
            )
            for key in config.cntrs_dict:
                if key != 'Смежные системы':
                    cntr = (
                        f'{self.reset_position}_{config.cntrs_dict[key]}_CNT'
                    )
                    txt.write(
                        f'{cntr}:=0;\n'
                    )

            # Неисправности КСПА
            falsities_cntr_marker = config.cntrs_dict["Недостоверности"]
            faults_cntr_marker = config.cntrs_dict["Неисправности"]

            txt.write('\n// Неисправности КСПА\n')
            faults_cab_counter = (
                f'{self.reset_position}_CAB_{faults_cntr_marker}_CNT'
            )

            dct = {
                'Mops3': config.cntrs_dict["Недостоверности"],
                'Mups3': config.cntrs_dict["Недостоверности"],
                'Mops3A': config.cntrs_dict["Недостоверности"],
                'DIAG_DI': 'XVLX',
                'DIAG_Mod': config.cntrs_dict["Неисправности"],
            }

            for sigtype in config.sigtypes_for_kspa_faults_in_counting:
                txt.write(f'// {sigtype}\n')
                for signal in self.__signals_list:
                    if signal.sigtype == sigtype:
                        txt.write(
                            self.__counter_one_signal_actuation_inv(
                                signal,
                                faults_cab_counter,
                                dct[sigtype],
                            )
                        )
                txt.write('\n')

            txt.write('// Недостоверности КСПА\n')
            falsities_cab_counter = (
                f'{self.reset_position}_CAB_{falsities_cntr_marker}_CNT'
            )
            for sigtype in config.sigtypes_for_kspa_falsities_in_counting:
                txt.write(f'// {sigtype}\n')
                for signal in self.__signals_list:
                    if (
                            signal.sigtype == sigtype
                            and
                            signal.sigtype != 'DIAG_DI'
                    ):
                        txt.write(
                            self.__counter_one_signal_actuation_inv(
                                signal,
                                falsities_cab_counter,
                                falsities_cntr_marker,
                            )
                        )
                    elif signal.sigtype == 'DIAG_DI':
                        txt.write(
                            Position.counter_one_signal_actuation(
                                signal,
                                falsities_cab_counter,
                                falsities_cntr_marker,
                            )
                        )
                txt.write('\n')

            # булы
            txt.write(
                f'{self.reset_position}_CAB_{faults_cntr_marker}:='
                f'{self.reset_position}_CAB_{faults_cntr_marker}_CNT > 0;\n'
                f'{self.reset_position}_CAB_{falsities_cntr_marker}:='
                f'{self.reset_position}_CAB_{falsities_cntr_marker}_CNT > 0;\n'
                '\n'
            )

            def sum_of_cntrs(
                    reset_position,
                    cntr_marker,
                    txt_file,
                    one_more_cntr='',
            ):
                counter = f'{reset_position}_{cntr_marker}_CNT'
                strng = f'{counter}:={counter}'
                for pos in self.__positions_list:
                    for counter in pos.counters_for_sum:
                        if cntr_marker in counter:
                            strng += f'+{counter}'
                if one_more_cntr != '':
                    strng += f'+{one_more_cntr}'
                strng += ';\n'
                txt_file.write(f'{strng}')

            # Сложение счетчиков пожаров
            sum_of_cntrs(
                self.reset_position,
                config.cntrs_dict['Пожары'],
                txt,
            )

            # Сложение счетчиков неисправностей
            sum_of_cntrs(
                self.reset_position,
                config.cntrs_dict['Неисправности'],
                txt,
                cab_faults_cntr,
            )

            # Сложение счетчиков вниманий
            sum_of_cntrs(
                self.reset_position,
                config.cntrs_dict['Внимания'],
                txt,
            )

            # Сложение счетчиков ремонтов
            sum_of_cntrs(
                self.reset_position,
                config.cntrs_dict['Ремонты'],
                txt,
            )

            sum_of_cntrs(
                self.reset_position,
                config.cntrs_dict['Имитации'],
                txt,
            )

            sum_of_cntrs(
                self.reset_position,
                config.cntrs_dict['Недостоверности'],
                txt,
                cab_falsities_cntr,
            )

            txt.write('\n')

            for key in config.cntrs_dict:
                if key != 'Смежные системы':
                    txt.write(
                        f'{self.reset_position}_{config.cntrs_dict[key]}:='
                        f'{self.reset_position}_{config.cntrs_dict[key]}_'
                        f'CNT > 0;\n'
                    )

            txt.close()
            self.__counting_was_formed = True
            return True

    # MOPS_MUPS
    def establishing_mops_mups_txt(self):
        if self.ready_for_mops_mups():
            txt = open(fr'{self.output_path}\MOPS_MUPS.txt', 'w')

            # $$$$$$$$$$$$$$$$$$$ ВЫЗОВ БЛОКОВ $$$$$$$$$$$$$$$$$$
            txt.write('// Вызов блоков\n')
            for device in self.__devices_list:
                device.call_mops_mups_write_to_txt(txt)

            # $$$$$$$$$$$$ ПЕРЕКЛАДЫВАНИЕ МОПС/МУПС $$$$$$$$$$$$$
            txt.write(
                '\n(* Ниже принимаем данные с канала modbus RTU *)\n'
                '(* Перекладываем входные данные с МОПС/МУПС на'
                ' входы ФБ для\nдиагностики связи и привязки'
                ' к конкретному устройству *)\n'
                '// Перекладываем данные из каналов IO'
                ' Tecon во входные переменные ФБ Mups 3/Mops 3\n\n'
            )
            # МОПСЫ
            for device in self.__devices_list:
                device.mops_shifting_write_to_txt(txt)
            # МУПСЫ
            for device in self.__devices_list:
                device.mups_shifting_write_to_txt(txt)

            # $$$$$$$$$$$$$$$$$$$$$$ IVXX $$$$$$$$$$$$$$$$$$$$$$$
            txt.write(
                '//Перекладываем данные с выходов ФБ МОПС/'
                'МУПС во входные переменные ФБ извещателя\n\n'
            )
            # МОПСЫ
            for device in self.__devices_list:
                device.mops_ivxx_write_to_txt(txt)
            # МУПСЫ
            for device in self.__devices_list:
                device.mups_ivxx_write_to_txt(txt)

            # $$$$$$$$$$$$$$$$$$$$$$ IDVX $$$$$$$$$$$$$$$$$$$$$$$
            txt.write(
                '// Формируем сигнал Недостоверность шле'
                'йфа по исчезновению связи с МОПС/МУПС\n\n'
            )
            # МОПСЫ
            for device in self.__devices_list:
                device.mops_idvx_write_to_txt(txt)
            # МУПСЫ
            for device in self.__devices_list:
                device.mups_idvx_write_to_txt(txt)

            # $$$$$$$$$$$$$$$$$$ СБРОС МОПСОВ $$$$$$$$$$$$$$$$$$$
            txt.write('// Сброс мопсов\n')
            for device in self.__devices_list:
                device.mops_reset_write_to_txt(txt)

            #  МОПСЫ 3а
            if self.__contains_devtype_in_devices_list('MOPS3a'):
                for device in self.__devices_list:
                    device.mops3a_m_write_to_txt(txt)
                    device.mops3a_s_write_to_txt(txt)

                txt.write('// Тест и сброс извещателей\n')
                for device in self.__devices_list:
                    device.mops3a_test_reset_write_to_txt(txt)

                txt.write(
                    '// Перекладываем данные с выходов МОПС3А'
                    ' в входные переменные ФБ извещателя\n\n'
                )
                for device in self.__devices_list:
                    device.mops3a_m_ivxx_xvlx_write_to_txt(txt)
                    device.mops3a_s_ivxx_xvlx_write_to_txt(txt)

                txt.write(
                    '//Формируем сигнал Недостоверность шлейфа '
                    'по исчезновению связи с МОПС3А\n\n'
                )
                for device in self.__devices_list:
                    device.mops3a_m_idvx_dvxx_write_to_txt(txt)
                    device.mops3a_s_idvx_dvxx_write_to_txt(txt)

            txt.close()
            self.__mops_mups_was_formed = True
            return True

    # Reset_MOPS3a
    def establishing_reset_mops3a_txt(self):
        if self.ready_for_reset_mops3a():
            txt = open(fr'{self.output_path}\Reset_MOPS3a.txt', 'w')
            txt.write(
                '// Сброс\n'
                f'{self.reset_position}_COOF(.COOF, .CSOF, .CPOF, .CWOF);\n'
                f'{self.reset_position}_CORS(.CORS, .CSRS, .CPRS, .CWRS);\n\n'
                '// Сброс МОПС3А\n'
                f'IF {self.reset_position}_CORS.XORS THEN\n'
            )
            for device in self.__devices_list:
                if device.devtype == 'MOPS3a':
                    txt.write(
                        f'_IO_QX{device.input_index}_1_8.ValueDINT:=1;\n'
                    )
            txt.write('ELSE\n')
            for device in self.__devices_list:
                if device.devtype == 'MOPS3a':
                    txt.write(
                        f'_IO_QX{device.input_index}_1_8.ValueDINT:=0;\n'
                    )
            txt.write(
                'END_IF;\n\n'
            )
            txt.close()
            return True

    # OXON
    def establishing_oxon_txt(self):
        if self.ready_for_oxon():
            txt = open(fr'{self.output_path}\Oxon.txt', 'w')
            for device in self.__devices_list:
                device.mups_oxon_write_to_txt(txt)
            txt.close()
            return True

    # WEINTEK
    def establishing_weintek_txt(self):
        if self.ready_for_weintek():
            txt = open(fr'{self.output_path}\Weintek.txt', 'w')
            for position in self.__positions_list:
                if (
                        position.izv_addr is not None
                        and
                        position.opv_addr is not None
                        and
                        len(position.signals_list) != 0
                ):
                    txt.write(f'// {position.name_for_comment}\n')
                    position.weintek_write_to_txt(txt)

            if self.diag_addr != '':
                txt.write('// Диагностика\n')
                n = 0

                diag_positions = [
                    position for position in self.__positions_list
                    if position.is_diag()
                ]

                for sigtype in config.sigtypes_diag_for_weintek:
                    if sigtype == 'DIAG_DI':
                        txt.write(f'// {sigtype}\n')
                        for position in diag_positions:
                            txt.write(f'// {position.name_for_comment}\n')
                            for signal in position.signals_list:
                                if signal.sigtype == sigtype:

                                    txt.write(
                                        '_IO_QX{0}_1_{2}:={1}.XVLX;\n'
                                        '_IO_QX{0}_1_{3}:={1}.DVXX;\n'.format(
                                            self.coil,
                                            signal.name,
                                            int(self.diag_addr)+1+n,
                                            int(self.diag_addr)+2+n,
                                        )
                                    )
                                    n += 2

                            txt.write('\n')

                    elif sigtype == 'DIAG_Mod':
                        txt.write(f'// {sigtype}\n')
                        for position in diag_positions:
                            txt.write(f'// {position.name_for_comment}\n')
                            for signal in position.signals_list:
                                if signal.sigtype == sigtype:

                                    txt.write(
                                        '_IO_QX{0}_1_{2}:={1}.FXXX;\n'.format(
                                            self.coil,
                                            signal.name,
                                            int(self.diag_addr) + 1 + n,
                                        )
                                    )
                                    n += 1

                            txt.write('\n')

                    elif sigtype in ['Mops3', 'Mups3', 'Mops3A']:
                        txt.write(f'// {sigtype}\n')
                        for position in diag_positions:
                            txt.write(f'// {position.name_for_comment}\n')
                            for signal in position.signals_list:
                                if signal.sigtype == sigtype:

                                    txt.write(
                                        '_IO_QX{0}_1_{2}:={1}.DVXX;\n'.format(
                                            self.coil,
                                            signal.name,
                                            int(self.diag_addr) + 1 + n,
                                        )
                                    )
                                    n += 1

                            txt.write('\n')

            txt.close()
            return True

    # TO_SAU
    def establishing_to_sau_txt(self):
        if self.ready_for_to_sau():
            txt = open(fr'{self.output_path}\To_SAU.txt', 'w')
            for position in self.__positions_list:
                position.to_sau_write_to_txt(txt)
            txt.close()
            return True

    # DIAG
    def establishing_diag_txt(self):
        if self.ready_for_diag():

            txt = open(fr'{self.output_path}\Diag.txt', 'w')

            for position in self.__positions_list:
                if position.is_diag():
                    txt.write(
                        f'// {position.name_for_comment}\n'
                    )
                    diag_di = [
                        signal for signal in position.signals_list
                        if signal.sigtype in config.sigtypes_di_for_diag
                    ]

                    diag_modules = [
                        signal for signal in position.signals_list
                        if signal.sigtype in config.sigtypes_modules_for_types
                    ]

                    for signal in diag_di:
                        txt.write(
                            f'{signal.name}(_IO_{signal.address}, '
                            f'SYS_LNG.XLNG);\n'
                        )

                    if len(diag_di) != 0:
                        txt.write('\n')

                    for signal in diag_modules:
                        txt.write(
                            f'{signal.name}(_IO_{signal.address}.Status);\n'
                        )

                    if len(diag_modules) != 0:
                        txt.write('\n')

            txt.close()
            return True

    # DATATABLE
    def __datatable(self, category):

        for position in self.__positions_list:
            for upg_marker in position.upg_markers:
                bool_counter = \
                    f'{position.name}_' \
                    f'{upg_marker}_' \
                    f'{config.cntrs_dict["Пожары"]}'
                position.bool_counters.add(bool_counter)

        cors_coof = ['CORS', 'COOF']

        data_len = 1

        data_len += len(self.__signals_list)
        data_len += len(self.m_names)
        data_len += len(cors_coof) * len(self.__positions_list)

        for position in self.__positions_list:
            data_len += len(position.upg_counters)
            data_len += len(position.counters)
            data_len += len(position.bool_counters)

        import pandas as pd
        data = pd.DataFrame(
            None,
            columns=[
                'Марка',
                'Наименование',
                'Описание',
                'Тип Объекта',
                'Пер.архив.',
                'Подпись',
                'Контроллер',
                'Ресурс №',
                'Группа событий',
                'KKS',
                'Шаблон',
                'Классификатор',
            ],
            index=range(data_len)
        )

        for i in range(len(data)):
            data['Контроллер'][i] = \
                self.name
            data['Ресурс №'][i] = \
                'Resource1'

        filled = 0
        for i in range(len(self.__signals_list)):
            signal = self.__signals_list[i]
            data['Марка'][i] = \
                signal.name
            data['Тип Объекта'][i] = \
                signal.sigtype
            data['Группа событий'][i] = \
                signal.position.name_for_comment
            data['KKS'][i] = \
                signal.name[1:].replace('_', '-') \
                if signal.name[0] == 'P' \
                else signal.name.replace('_', '-')
            data['Шаблон'][i] = \
                'FB_' + signal.sigtype
            filled += 1

        def cnt(counters, pos):
            nonlocal filled
            for j in range(len(counters)):
                cntr = counters[j]
                data['Марка'][j+filled] = \
                    cntr
                data['Тип Объекта'][j+filled] = \
                    'DINT'
                data['Группа событий'][j+filled] = \
                    pos
                data['Шаблон'][j+filled] = \
                    'простой'
                data['Классификатор'][j+filled] = \
                    'CNT'
            filled += len(counters)

        for position in self.__positions_list:
            cnt(position.counters, position.name_for_comment)
            cnt(position.upg_counters, position.name_for_comment)
            cnt(position.xsy_counters, position.name_for_comment)

        for position in self.__positions_list:
            iteration = 0
            for bool_counter in position.bool_counters:
                data['Марка'][iteration + filled] = \
                    f'{bool_counter}'
                data['Тип Объекта'][iteration + filled] = \
                    'BOOL'
                data['Группа событий'][iteration + filled] = \
                    position.name_for_comment
                data['Шаблон'][iteration + filled] = \
                    'простой'
                data['Классификатор'][iteration + filled] = \
                    'CNT'
                iteration += 1
            filled += len(position.bool_counters)

        m_names = list(self.m_names)
        for i in range(len(m_names)):
            m_name = m_names[i]
            data['Марка'][i+filled] = \
                m_name
            data['Тип Объекта'][i+filled] = \
                'Mops3A'
            data['Группа событий'][i+filled] = \
                self.reset_position_for_comment
            data['Шаблон'][i+filled] = \
                'Mops3A'
        filled += len(self.m_names)

        for position in self.__positions_list:
            iteration = 0
            for corscoof in cors_coof:
                data['Марка'][iteration+filled] = \
                    f'{position.name}_{corscoof}'
                data['Тип Объекта'][iteration + filled] = \
                    corscoof
                data['Группа событий'][iteration + filled] = \
                    position.name_for_comment
                data['Шаблон'][iteration + filled] = \
                    'FB_' + corscoof
                data['Классификатор'][iteration + filled] = \
                    corscoof
                iteration += 1
            filled += len(cors_coof)

        if category == 2:
            data.to_excel(
                fr'{self.output_path}\datatable_cat2.xls',
                index=False,
                header=False,
            )
        else:
            data.to_excel(
                fr'{self.output_path}\datatable.xls',
                index=False,
                header=False,
            )

    # DATATABLE
    def establishing_datatable_to_xlsx(self):
        if self.ready_for_datatable():
            if self.cabinet_category == '2':
                self.__datatable(1)
                self.__datatable(2)
            else:
                self.__datatable(1)
            return True
