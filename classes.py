import config


class Signal:

    def __init__(
            self,
            name,
            plc,
            sigtype=None,
            position=None,
            location=None,
            ff_out=None,
            device=None,
            address=None,
            styp=None,
    ):

        if not isinstance(plc, PLC):
            raise ValueError(
                'Аргуметом plc при создании '
                'экземпляра Signal'
                'может выступать только '
                'экземпляр/наследник класса PLC!'
            )

        self.name = name.replace('-', '_').replace(' ', '')
        if not self.name[0].isalpha():
            self.name = 'P' + self.name

        self.plc = plc
        self.sigtype = sigtype
        self.position = position
        self.location = location
        self.ff_out = ff_out
        self.device = device
        self.address = address
        self.styp = styp


class SignalsList(list):

    def has_any_signal_with_sigtype_in(self, sigtypes_list):
        flg = False
        for signal in self:
            if isinstance(signal, Signal):
                if signal.sigtype in sigtypes_list:
                    flg = True
                    break
        return flg

    # $$$$$$$$$$$$$$ ПРОВЕРКА НАЛИЧИЯ СИГНАЛОВ $$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$            ДЛЯ            $$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$   INPUT, OUTPUT, ALARMING $$$$$$$$$$$$$$$$$$$

    def contains_signals_for_input(self):
        return self.has_any_signal_with_sigtype_in(config.sigtypes_for_input)

    def contains_signals_for_output(self):
        return self.has_any_signal_with_sigtype_in(config.sigtypes_for_output)

    def contains_signals_for_alarming(self):
        flg = False
        for signal in self:
            if isinstance(signal, Signal):
                if (
                        signal.sigtype in config.sigtypes_for_alarming
                        and
                        signal.ff_out is None
                ):
                    flg = True
                    break
        return flg

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$ ПРОВЕРКА НАЛИЧИЯ СИГНАЛОВ ДЛЯ COUNTING $$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def has_any_ff_or_ffo_signal_with_sigtype_in(self, sigtypes_list):
        flg = False
        for signal in self:
            if (
                    isinstance(signal, Signal)
                    and
                    isinstance(signal.location, Location)
            ):
                if (
                        signal.sigtype in sigtypes_list
                        and
                        (signal.location.fire_fighting_cntrs is not None
                         or
                         signal.ff_out is not None)
                ):
                    flg = True
                    break
        return flg

    def has_any_no_ff_or_ffo_signal_with_sigtype_in(self, sigtypes_list):
        flg = False
        for signal in self:
            if (
                    isinstance(signal, Signal)
                    and
                    isinstance(signal.location, Location)
            ):
                if (
                        signal.sigtype in sigtypes_list
                        and
                        signal.location.fire_fighting_cntrs is None
                        and
                        signal.ff_out is None
                ):
                    flg = True
                    break
        return flg

    def contains_signals_for_counting(self):
        return self.has_any_signal_with_sigtype_in(
            config.sigtypes_for_counting
        )

    def contains_signals_with_ff_out_for_counting(self):
        flg = False
        for signal in self:
            if (
                    isinstance(signal, Signal)
                    and
                    signal.ff_out is not None
                    and
                    signal.sigtype in config.sigtypes_for_counting
            ):
                flg = True
                break
        return flg

    def contains_signals_without_ff_out_for_counting(self):
        flg = False
        for signal in self:
            if (
                    isinstance(signal, Signal)
                    and
                    signal.ff_out is None
                    and
                    signal.sigtype in config.sigtypes_for_counting
            ):
                flg = True
                break
        return flg

    def contains_signals_with_fire_fighting_for_counting(self):
        flg = False
        for signal in self:
            if (
                    (
                            isinstance(signal, Signal)
                            and
                            isinstance(signal.location, Location)
                    )
                    and
                    signal.location.fire_fighting_cntrs is not None
                    and
                    signal.sigtype in config.sigtypes_for_counting
            ):
                flg = True
                break
        return flg

    def contains_signals_without_fire_fighting_for_counting(self):
        flg = False
        for signal in self:
            if (
                    (
                            isinstance(signal, Signal)
                            and
                            isinstance(signal.location, Location)
                    )
                    and
                    signal.location.fire_fighting_cntrs is None
                    and
                    signal.sigtype in config.sigtypes_for_counting
            ):
                flg = True
                break
        return flg

    def contains_ff_or_ffo_signals_with_warning(self):
        flg = False
        for signal in self:
            if (
                    isinstance(signal, Signal)
                    and
                    isinstance(signal.location, Location)
            ):
                if (
                        signal.location.warning_cntr
                        and
                        (signal.ff_out is not None
                         or
                         signal.location.fire_fighting_cntrs is not None)
                ):
                    flg = True
                    break
        return flg

    def contains_no_ff_or_ffo_signals_with_warning(self):
        flg = False
        for signal in self:
            if (
                    isinstance(signal, Signal)
                    and
                    isinstance(signal.location, Location)
            ):
                if (
                        signal.location.warning_cntr
                        and
                        (signal.ff_out is None
                         and
                         signal.location.fire_fighting_cntrs is None)
                ):
                    flg = True
                    break
        return flg

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$ ПРОВЕРКА НАЛИЧИЯ СИГНАЛОВ ДЛЯ DIAG_ST $$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def contains_signals_for_diag_st(self):
        return self.has_any_signal_with_sigtype_in(config.sigtypes_for_diag_st)


class Location:

    def __init__(
            self,
            name,
            warning_cntr=None,
            fire_cntr=None,
            fire_fighting_cntrs=None,
            conterminal_systems_cntrs=None,
            voting_logic=None,
    ):

        self.signals_list = SignalsList()  # для ссылок на объекты сигналов
        self.position = None  # см метод position_check_and_set

        self.name = name
        self.warning_cntr = warning_cntr
        self.fire_cntr = fire_cntr
        self.fire_fighting_cntrs = fire_fighting_cntrs
        self.conterminal_systems_cntrs = conterminal_systems_cntrs
        self.voting_logic = voting_logic

    def position_check_and_set(self):
        """
        Метод проверяет, что все сигналы относящиеся
        к локации принадлежат к одной позиции,
        бросает ошибку, если это не так.
        Устанавливает значение для атрибута position.
        """
        positions_set = set()
        for signal in self.signals_list:
            positions_set.add(signal.position)
        if len(positions_set) != 1:
            print(
                f'Список позиций сигналов '
                f'"локации" {self.name}:\n'
            )
            for position in positions_set:
                print(position.name)
            print()
            raise ValueError(
                f'В локации {self.name} обнаружены '
                'сигналы с разными позициями,\n'
                'исправьте входные данные.'
            )
        else:
            self.position = list(positions_set)[0]
            self.position.locations_list.append(self)


class Position:

    def __init__(
            self,
            plc,
            name,
            izv_addr=None,
            opv_addr=None,
            tush_addr=None,
    ):

        if not isinstance(plc, PLC):
            raise ValueError(
                'Аргуметом plc при создании '
                'экземпляра Position'
                'может выступать только '
                'экземпляр/наследник класса PLC!'
            )

        self.plc = plc
        self.name = name.replace(' ', '').replace('-', '_')
        if not self.name[0].isalpha():
            self.name = 'P' + self.name

        self.izv_addr = izv_addr
        self.opv_addr = opv_addr
        self.tush_addr = tush_addr

        self.name_for_comment = name

        self.signals_list = SignalsList()
        self.locations_list = []
        self.upg_counters = []
        self.upg_markers = []
        self.xsy_counters = []
        self.counters = []
        self.bool_counters = set()

    def contains_locations_with_warning(self):
        """
        Возвращет True если в списке locations_list
        есть экземпляр Location атрибут .warning_cntr
        которого == True.
        Если такого экземпляра нет - возвращает False.
        """
        flg = False
        for location in self.locations_list:
            if location.warning_cntr:
                flg = True
                break
        return flg

    def contains_locations_with_warning_and_fire_fighting(self):
        """
        Возвращет True если в списке locations_list
        есть экземпляр Location атрибут .warning_cntr
        которого True, а атрибут .fire_fightings_cntrs
        is not None.
        Если такого экземпляра нет - возвращает False.
        """
        flg = False
        for location in self.locations_list:
            if (
                    location.warning_cntr
                    and
                    location.fire_fightings_cntrs is not None
            ):
                flg = True
                break
        return flg

    def contains_locations_with_warning_without_fire_fighting(self):
        """
        Возвращет True если в списке locations_list
        есть экземпляр Location атрибут .warning_cntr
        которого is True, а атрибут .fire_fightings_cntrs
        is None.
        Если такого экземпляра нет - возвращает False.
        """
        flg = False
        for location in self.locations_list:
            if (
                    location.warning_cntr
                    and
                    location.fire_fightings_cntrs is None
            ):
                flg = True
                break
        return flg

    def contains_locations_with_fire(self):
        """
        Возвращет True если в списке locations_list
        есть экземпляр Location атрибут .fire_cntr
        которого == True.
        Если такого экземпляра нет - возвращает False.
        """
        flg = False
        for location in self.locations_list:
            if location.fire_cntr:
                flg = True
                break
        return flg

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$ ЗАПИСЬ ST КОДА В ФАЙЛЫ $$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def input_write_to_txt(self, txt):
        """
        Метод записывает в txt строки кода на ST.
        В коде участвуют все сигналы из self.signals_list
        .sigtype которых входят в
        config.sigtypes_for_input_txt.
        """
        txt.write(f'// {self.name_for_comment}\n')
        for sigtype in config.sigtypes_for_input:
            txt.write(f'// {sigtype}\n')
            for signal in self.signals_list:
                if signal.sigtype == 'sigtype':
                    txt.write(
                        f'{signal.name}(.IVXX, .MBIN, '
                        f'{signal.plc.reset_position}CORS.XORS, '
                        f'.IDVX, .IFXX, SYS_LNG.XLNG, {signal.styp});\n'
                    )
            txt.write('\n')

    def output_write_to_txt(self, txt):
        """
        Метод записывает в txt строки кода на ST.
        В коде участвуют все сигналы из SignalsList
        .sigtype которых входят в
        config.sigtypes_for_output_txt.
        """
        txt.write(f'// {self.name_for_comment}\n')
        for sigtype in config.sigtypes_for_output:
            txt.write(f'// {sigtype}\n')
            for signal in self.signals_list:
                if signal.sigtype == 'sigtype':
                    txt.write(
                        f'{signal.name}(.IVXX, .MBIN, .CAON, '
                        '.SCMX, .STYP, SYS_LNG.XLNG, .IDVX);\n'
                    )
            txt.write('\n')

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

        for sigtype in config.sigtypes_for_alarming:
            txt.write(f'// {sigtype}\n')
            for signal in self.signals_list:
                if (
                        signal.sigtype == 'sigtype'
                        and
                        signal.ff_out is None
                ):
                    txt.write(
                        f'{signal.name}.CAON:='
                        f'{signal.position.name}XFRX_CNT > 0'
                        f'{warning_part};\n'
                    )
            txt.write('\n')

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$ COUNTING $$$$$$$$$$$$$$$$$$$$$$$$$$$$

    @staticmethod
    def __counter_one_signal_actuation(
            signal,
            counter,
            cntr_marker,
    ):
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
                        Position.__counter_one_signal_actuation(
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

    def counting_write_to_txt(self, txt):

        txt.write(f'// {self.name_for_comment}\n')

        cntrs_markers = config.cntrs_dict
        position = self.name

        # СЛОВАРИ НАЛИЧИЯ СЧЕТЧИКОВ НА ПОЗИЦИИ

        # счетчики не инициирующих тушение сигналов
        cntrs_without_ff = {
            'Имитации':
                self.signals_list
                .has_any_signal_with_sigtype_in(
                    config.sigtypes_for_imitations_in_counting
                ),
            'Ремонты':
                self.signals_list
                .contains_signals_for_counting(),
            'Неисправности':
                self.signals_list
                .has_any_no_ff_or_ffo_signal_with_sigtype_in(
                    config.sigtypes_for_faults_in_counting
                ),
            'Недостоверности':
                self.signals_list
                .has_any_no_ff_or_ffo_signal_with_sigtype_in(
                    config.sigtypes_for_falsities_in_counting
                ),
            'Пожары':
                self
                .contains_locations_with_fire(),
            'Внимания':
                self.signals_list
                .contains_no_ff_or_ffo_signals_with_warning()
        }

        # счетчики инициирующих тушение сигналов
        cntrs_with_ff = {
            'Неисправности':
                self.signals_list
                .has_any_ff_or_ffo_signal_with_sigtype_in(
                    config.sigtypes_for_faults_in_counting
                ),
            'Недостоверности':
                self.signals_list
                .has_any_ff_or_ffo_signal_with_sigtype_in(
                    config.sigtypes_for_falsities_in_counting
                ),
            'Внимания':
                self.signals_list
                .contains_ff_or_ffo_signals_with_warning()
        }

        # ОБНУЛЕНИЕ СЧЕТЧИКОВ
        txt.write('// Обнуление счетчиков\n')

        # без тушения
        for cntr in cntrs_without_ff:
            if cntrs_without_ff[cntr]:
                counter = f'{position}_{cntrs_markers[cntr]}_CNT'
                self.counters.append(counter)
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
                    txt.write(f'{counter}:=0;\n')

        for counter in self.upg_counters:
            txt.write(f'{counter}:=0;\n')

        # смежные системы
        for counter in self.xsy_counters:
            txt.write(f'{counter}:=0;\n')

        # ИМИТАЦИИ
        if cntrs_without_ff['Имитации']:

            txt.write('\n// Имитации\n')

            cntr_marker = cntrs_markers['Имитации']
            counter = f'{position}_{cntr_marker}_CNT'

            for sigtype in config.sigtypes_for_imitations_in_counting:
                txt.write(f'// {sigtype}\n')
                for signal in self.signals_list:
                    if signal.sigtype == sigtype:
                        txt.write(
                            self.__counter_one_signal_actuation(
                                signal,
                                counter,
                                cntr_marker,
                            )
                        )
                txt.write('\n')

        # РЕМОНТЫ, ОТКЛЮЧЕНИЯ
        if cntrs_without_ff['Ремонты']:

            txt.write('\n// Ремонты, отключения\n')

            cntr_marker = cntrs_markers['Ремонты']
            counter = f'{position}_{cntr_marker}_CNT'

            for sigtype in config.sigtypes_for_repairs_in_counting:
                txt.write(f'// {sigtype}\n')
                for signal in self.signals_list:
                    if signal.sigtype == sigtype:
                        txt.write(
                            self.__counter_one_signal_actuation(
                                signal,
                                counter,
                                cntr_marker,
                            )
                        )
                txt.write('\n')

        # СЧЕТЧИКИ ИП БЕЗ ТУШЕНИЯ
        # НЕИСПРАВНОСТИ (сигналы без тушения)
        if cntrs_without_ff['Неисправности']:

            txt.write('\n// Неисправности (сигналы без тушения)\n')

            cntr_marker = cntrs_markers['Неисправности']
            counter = f'{position}_{cntr_marker}_CNT'

            for sigtype in config.sigtypes_for_faults_in_counting:
                txt.write(f'// {sigtype}\n')
                for signal in self.signals_list:
                    if (
                            signal.sigtype == sigtype
                            and
                            signal.ff_out is None
                            and
                            (signal.location is None
                             or
                             (isinstance(signal.location, Location)
                              and
                              signal.location.fire_fighting_cntrs is None))
                    ):
                        txt.write(
                            self.__counter_one_signal_actuation(
                                signal,
                                counter,
                                cntr_marker,
                            )
                        )
                txt.write('\n')

        # НЕДОСТОВЕРНОСТИ (сигналы без тушения)
        if cntrs_without_ff['Недостоверности']:

            txt.write('\n// Недостоверности (сигналы без тушения)\n')

            cntr_marker = cntrs_markers['Недостоверности']
            counter = f'{position}_{cntr_marker}_CNT'

            for sigtype in config.sigtypes_for_falsities_in_counting:
                txt.write(f'// {sigtype}\n')
                for signal in self.signals_list:
                    if (
                            signal.sigtype == sigtype
                            and
                            signal.ff_out is None
                            and
                            (signal.location is None
                             or
                             (isinstance(signal.location, Location)
                              and
                              signal.location.fire_fighting_cntrs is None))
                    ):
                        txt.write(
                            self.__counter_one_signal_actuation(
                                signal,
                                counter,
                                cntr_marker,
                            )
                        )
                txt.write('\n')

        # СМЕЖНЫЕ СИСТЕМЫ
        if len(self.xsy_counters) > 0:

            txt.write('\n// Смежные системы\n')

            cntr_marker = cntrs_markers["Пожары"]

            iteration = 1
            for counter in self.xsy_counters:
                for location in self.locations_list:
                    if (
                            location.conterminal_systems_cntrs is not None
                            and
                            counter in location.conterminal_systems_cntrs
                    ):
                        self.__counter_with_condition_write_to_txt(
                            txt,
                            location,
                            counter,
                            cntr_marker,
                        )
                if iteration != len(self.xsy_counters):
                    txt.write('\n')
                iteration += 1

        # ПОЖАРЫ (сигналы без тушения)
        if cntrs_without_ff['Пожары']:

            txt.write('\n// Пожары (сигналы без тушения)\n')

            cntr_marker = cntrs_markers['Пожары']
            counter = f'{position}_{cntr_marker}_CNT'

            for location in self.locations_list:
                if location.fire_cntr:
                    self.__counter_with_condition_write_to_txt(
                            txt,
                            location,
                            counter,
                            cntr_marker,
                        )

        # ВНИМАНИЯ (сигналы без тушения)
        if cntrs_without_ff['Внимания']:

            txt.write('\n// Внимания (сигналы без тушения)\n')

            cntr_marker = cntrs_markers['Внимания']
            counter = f'{position}_{cntr_marker}_CNT'

            for location in self.locations_list:
                if (
                        location.warning_cntr
                        and
                        location.fire_fightings_cntrs is None
                ):
                    for signal in location.signals_list:
                        if signal.ff_out is None:
                            txt.write(
                                self.__counter_one_signal_actuation(
                                    signal,
                                    counter,
                                    cntr_marker,
                                )
                            )
                txt.write('\n')

        # СЧЕТЧИКИ ИП С ТУШЕНИЕМ
        # НЕИСПРАВНОСТИ (сигналы с тушением)
        if cntrs_with_ff['Неисправности']:

            txt.write('\n// Неисправности (сигналы с тушением)\n')

            iteration = 1

            cntr_marker = cntrs_markers['Неисправности']
            for upg_marker in self.upg_markers:
                counter = f'{position}_{cntr_marker}_{upg_marker}_CNT'

                for sigtype in config.sigtypes_for_faults_in_counting:
                    txt.write(f'// {sigtype}\n')
                    for signal in self.signals_list:
                        if (
                                signal.sigtype == sigtype
                                and
                                (signal.ff_out is not None
                                 or
                                 (isinstance(signal.location, Location)
                                  and
                                  signal
                                  .location.fire_fighting_cntrs is not None))
                        ):
                            txt.write(
                                self.__counter_one_signal_actuation(
                                    signal,
                                    counter,
                                    cntr_marker,
                                )
                            )
                    txt.write('\n')
                if iteration != len(self.upg_markers):
                    txt.write('\n')
                iteration += 1

        # НЕДОСТОВЕРНОСТИ (сигналы с тушением)
        if cntrs_with_ff['Недостоверности']:

            txt.write('\n// Недостоверности (сигналы с тушением)\n')

            iteration = 1

            cntr_marker = cntrs_markers['Недостоверности']
            for upg_marker in self.upg_markers:
                counter = f'{position}_{cntr_marker}_{upg_marker}_CNT'

                for sigtype in config.sigtypes_for_falsities_in_counting:
                    txt.write(f'// {sigtype}\n')
                    for signal in self.signals_list:
                        if (
                                signal.sigtype == sigtype
                                and
                                (signal.ff_out is not None
                                 or
                                 (isinstance(signal.location, Location)
                                  and
                                  signal
                                  .location.fire_fighting_cntrs is not None))
                        ):
                            txt.write(
                                self.__counter_one_signal_actuation(
                                    signal,
                                    counter,
                                    cntr_marker,
                                )
                            )
                    txt.write('\n')
                if iteration != len(self.upg_markers):
                    txt.write('\n')
                iteration += 1

        # ПОЖАРОТУШЕНИЯ (Пожары с тушением)
        if (
                self.signals_list
                .contains_signals_with_fire_fighting_for_counting()
        ):

            txt.write('\n// Пожаротушения (пожары с тушением)\n')

            iteration = 1

            cntr_marker = cntrs_markers['Пожары']
            for counter in self.upg_counters:

                for location in self.locations_list:
                    if (
                            location.fire_fightings_cntrs is not None
                            and
                            counter in location.fire_fightings_cntrs
                    ):
                        self.__counter_with_condition_write_to_txt(
                            txt,
                            location,
                            counter,
                            cntr_marker,
                        )
                if iteration != len(self.upg_counters):
                    txt.write('\n')
                iteration += 1

        # ВНИМАНИЯ (сигналы без тушения)
        if cntrs_without_ff['Внимания']:

            txt.write('\n// Внимания (сигналы с тушением)\n')

            cntr_marker = cntrs_markers['Внимания']
            for upg_marker in self.upg_markers:
                counter = f'{position}_{cntr_marker}_{upg_marker}_CNT'

                for location in self.locations_list:
                    if (
                            location.warning_cntr
                            and
                            location.fire_fightings_cntrs is not None
                    ):
                        for signal in location.signals_list:
                            txt.write(
                                self.__counter_one_signal_actuation(
                                    signal,
                                    counter,
                                    cntr_marker,
                                )
                            )
                txt.write('\n')

        # СЧЕТЧИКИ РЕЖИМА
        if len(self.upg_counters) != 0:
            txt.write(

                '\n// Счетчик режима "Идет отсчет до начала тушения"\n'
                '{0}XRFD_CNT:=Count({0}UPG.XFDN, {0}XRFD_CNT);\n\n'
                .format(position),

                '// Счетчик режима "Идет тушение"\n'
                '{0}XRFN_CNT:=Count({0}UPG.OF1N, {0}XRFN_CNT);\n'
                .format(position),

            )

        # ОБЩИЕ СЧЕТЧИКИ
        txt.write('\n//Общие счетчики\n')

        for upg_marker in self.upg_markers:
            txt.write(
                '{0}XFRX_CNT:=Plus({0}XFRX_{1}_CNT, {0}XFRX_CNT);\n'
                '{0}XWRX_CNT:=Plus({0}XWRX_{1}_CNT, {0}XWRX_CNT);\n'
                '{0}FXXX_CNT:=Plus({0}FXXX_{1}_CNT, {0}FXXX_CNT);\n'
                '{0}DVXX_CNT:=Plus({0}DVXX_{1}_CNT, {0}DVXX_CNT);\n\n'
                '{0}UPG_XFRX:={0}XFRX_{1}_CNT > 0;\n'
                '{0}UPG_XWRX:={0}XWRX_{1}_CNT > 0;\n'
                '{0}UPG_FXXX:={0}FXXX_{1}_CNT > 0 OR {0}DVXX_{1}_CNT > 0;\n\n'
                .format(position, upg_marker)
            )

        txt.write(
            '{0}XFRX:={0}XFRX_CNT > 0;\n'
            '{0}XWRX:={0}XWRX_CNT > 0;\n'
            '{0}FXXX:={0}FXXX_CNT > 0;\n'
            '{0}DVXX:={0}DVXX_CNT > 0;\n'
            '{0}XCIM:={0}XCIM_CNT > 0;\n'
            '{0}XRPX:={0}XRPX_CNT > 0;\n'
            .format(position)
        )

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

        di_iteration = 0
        di_cnt = 0
        for sigtype in config.sigtypes_di_for_weintek:
            for signal in self.signals_list:
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
            for signal in self.signals_list:
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
                f'_IO_QX{self.plc.reg}_1_{data["Address 1"][i]}:=' \
                f'{data["Name"][i]}.Status;'

            data['Blnk'][i] = \
                f'_IO_QX{self.plc.reg}_1_{data["Address 1"][i]}:=' \
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
                    f'{data["Name"][i]}.XVLX'

                data['Blnk_RP / Blnk_Fr'][i] = \
                    f'_IO_QX{self.plc.coil}_1_{data["Address 2"][i]}:=' \
                    f'{data["Name"][i]}.Blnk_RP;'

            elif data['Equipment type'][i] == '// Оповещатели':

                data['Blnk_RP / Blnk_Fr'][i] = \
                    f'_IO_QX{self.plc.coil}_1_{data["Address 2"][i]}:=' \
                    f'{data["Name"][i]}.Blnk_Fr;'

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

        if self.tush_addr is not None:
            txt.write('// Тушение\n')
            txt.write(f'(* {self.name_for_comment} *)\n')
            txt.write(
                f'{self.name}_UPG.MBIN:='
                f'_IO_IX{self.plc.reg}_0_{self.tush_addr};\n'
            )
            for i in range(len(config.weintek_upg_tails_reg)):
                tail = config.weintek_upg_tails_reg[i]
                txt.write(
                    f'_IO_QX{self.plc.reg}_1_{int(self.tush_addr)+2+i}:='
                    f'{self.name}_UPG.{tail};\n'
                )
            for i in range(len(config.weintek_upg_tails_coils)):
                tail = config.weintek_upg_tails_coils[i]
                txt.write(
                    f'_IO_QX{self.plc.coil}_1_{int(self.tush_addr)+2+i}:='
                    f'{self.name}_UPG.{tail};\n'
                )
            txt.write(
                f'_IO_QX{self.plc.coil}_1_{int(self.tush_addr)+7}:='
                f'{self.name}_UPG.XCPX AND '
                f'{self.name}_UPG.XDOF;\n'
            )

        data.to_excel(
            fr'{self.plc.output_path}\weintek_table.xls',
            index=False,
        )


class Device:

    def __init__(
            self,
            plc,
            name,
            devtype,
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
        self.input_index = input_index
        self.output_index = output_index
        self.m = m
        self.s = s

    # ВЫЗОВ БЛОКОВ
    def call_for_mops_mups_text(self):

        if self.devtype == 'MOPS':
            args = ''
            for i in range(len(config.mops_args)-1):
                args += f'.{config.mops_args[i]}, '
            args += f'.{config.mops_args[-1]}'
            text = f'{self.name}({args});\n'
            return text

        elif self.devtype == 'MUPS':
            args = ''
            for i in range(len(config.mups_args) - 1):
                args += f'.{config.mups_args[i]}, '
            args += f'.{config.mups_args[-1]}'
            text = f'{self.name}({args});\n'
            return text

        elif self.devtype == 'MOPS3a':
            args = f'_IO_IX{self.input_index}_0_3, '
            for i in range(len(config.mops3a_args) - 1):
                args += f'{config.mops3a_args[i]}, '
            args += config.mops3a_args[-1]
            text = f'{self.name}({args});\n'
            return text

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

    def mops_shifting_text(self):
        return self.__shift(self, 'MOPS', config.mops_args)

    def mups_shifting_text(self):
        return self.__shift(self, 'MUPS', config.mups_args, cnt=4)

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

    def mops_ivxx_text(self):
        return self.__ivxx(self, 'MOPS', config.mops_args)

    def mups_ivxx_text(self):
        return self.__ivxx(self, 'MUPS', config.mups_args)

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

    def mops_idvx_text(self):
        return self.__idvx(self, 'MOPS', config.mops_args)

    def mups_idvx_text(self):
        return self.__idvx(self, 'MUPS', config.mups_args)

    # OXON
    def mups_oxon_text(self):

        if self.devtype == 'MUPS':
            text = f'(* {self.name} *)\n'
            for i in range(len(config.mups_args)):

                if isinstance(self.signals_list[i], Signal):
                    signal_name = self.signals_list[i].name
                    text += \
                        f'_IO_QX{self.output_index}_1_{i}:=' \
                        f'{signal_name}.OXON;\n'

                elif self.signals_list[i] == '0':
                    text += f'// {config.mups_args[i]} reserved\n'

            text += '\n'
            return text

    # СБРОС МОСОВ
    def mops_reset_text(self):

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
            return result

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
        return f'M{self.name[4:]}_{sm}_A{addr}'

    def __m_name_s_f_s(self, first, second):
        return f'M{self.name[4:]}_S_{first}_{second}'

    def mops3a_m_text(self):

        if self.__mops3a_has_any_m():

            text = f'(* {self.name} *)\n'
            text += '//Ручные извещатели\n'
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

                text += \
                    f'{m_name}(' \
                    f'{arg1}, ' \
                    f'{arg2}, ' \
                    f'{arg3}, ' \
                    f'{arg4}, ' \
                    f'{arg5}, ' \
                    f'{arg6}, ' \
                    f'{arg7});\n'

            text += '\n'
            return text

    def __mops3a_has_any_s(self):
        if self.devtype == 'MOPS3a':
            flg = False
            for signal in self.signals_list:
                if signal.styp in config.styp_for_s_in_mops3a:
                    flg = True
                    break
            return flg

    def mops3a_s_text(self):

        if self.__mops3a_has_any_s():

            text = f'(* {self.name} *)\n'
            s_signals_lst = []

            for signal in self.signals_list:
                if signal.styp in config.styp_for_s_in_mops3a:
                    s_signals_lst.append(signal)

            s_signals_lst.sort(
                key=lambda sgnl: int(sgnl.address)
            )

            from math import floor

            text += '// Дымовые и тепловые извещатели\n'
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

                m_name = self.__m_name(addr, 'M')
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

                    text += \
                        f'{m_name}(' \
                        f'{arg1}, ' \
                        f'{arg2}, ' \
                        f'{arg3}, ' \
                        f'{arg4}, ' \
                        f'{arg5}, ' \
                        f'{arg6}, ' \
                        f'{arg7});\n'

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

                    text += \
                        f'{m_name}(' \
                        f'{arg1}, ' \
                        f'{arg2}, ' \
                        f'{arg3}, ' \
                        f'{arg4}, ' \
                        f'{arg5}, ' \
                        f'{arg6}, ' \
                        f'{arg7});\n'

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

                    text += \
                        f'{m_name}(' \
                        f'{arg1}, ' \
                        f'{arg2}, ' \
                        f'{arg3}, ' \
                        f'{arg4}, ' \
                        f'{arg5}, ' \
                        f'{arg6}, ' \
                        f'{arg7});\n'

                prev_addr = addr
                prev_m_name = m_name

            self.__reset_addresses.append(prev_addr)

            text += '\n'
            return text

    # ТЕСТ/СБРОС МОПСОВ 3А
    def mops3a_test_reset_text(self):

        if self.devtype == 'MOPS3a' and len(self.__reset_addresses) != 0:

            text = ''
            first = 1
            second = 16
            cnt = 0

            for addr in self.__reset_addresses:

                m_name = self.__m_name_s_f_s(first, second)

                # Аргуметы
                arg1 = \
                    f'_IO_IX{self.input_index}_0_{14+cnt}.ValueDINT'
                arg2 = \
                    f'_IO_IX{self.input_index}_0_{78+cnt}.ValueDINT'
                arg3 = \
                    f'M{self.name[4:]}_S_A{addr}.RST_CNTo'
                arg4 = \
                    f'M{self.name[4:]}_S_A{addr}.TST_CNTo'
                arg5 = \
                    '.FL'

                text += \
                    f'{m_name}(' \
                    f'{arg1}, ' \
                    f'{arg2}, ' \
                    f'{arg3}, ' \
                    f'{arg4}, ' \
                    f'{arg5});\n'

                cnt += 1
                first += 16
                second += 16

            text += '\n'
            first = 1
            second = 16
            cnt = 0

            for _ in self.__reset_addresses:

                m_name = self.__m_name_s_f_s(first, second)

                var1 = f'_IO_QX{self.input_index}_1_{78+cnt}.ValueDINT'
                var2 = f'{m_name}.XTST'

                text += f'{var1}:={var2};\n'

                var1 = f'_IO_QX{self.input_index}_1_{14 + cnt}.ValueDINT'
                var2 = f'{m_name}.XRST'

                text += f'{var1}:={var2};\n'

                first += 16
                second += 16
                cnt += 1

            text += '\n'
            return text

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

    def mops3a_m_ivxx_xvlx_text(self):
        if self.__mops3a_has_any_m():
            text = f'(* {self.name} *)\n'
            text += '// Ручные извещатели\n'
            text += self.__ivxx_xvlx_idvx_dvxx(
                self,
                'IVXX',
                'XVLX',
                config.styp_for_m_in_mops3a,
                'M'
            )
            return text

    def mops3a_s_ivxx_xvlx_text(self):
        if self.__mops3a_has_any_s():
            text = f'(* {self.name} *)\n'
            text += '// Дымовые и тепловые извещатели\n'
            text += self.__ivxx_xvlx_idvx_dvxx(
                self,
                'IVXX',
                'XVLX',
                config.styp_for_s_in_mops3a,
                'S'
            )
            return text

    def mops3a_m_idvx_dvxx_text(self):
        if self.__mops3a_has_any_m():
            text = f'(* {self.name} *)\n'
            text += '// Ручные извещатели\n'
            text += self.__ivxx_xvlx_idvx_dvxx(
                self,
                'IDVX',
                'DVXX',
                config.styp_for_m_in_mops3a,
                'M'
            )
            return text

    def mops3a_s_idvx_dvxx_text(self):
        if self.__mops3a_has_any_s():
            text = f'(* {self.name} *)\n'
            text += '// Дымовые и тепловые извещатели\n'
            text += self.__ivxx_xvlx_idvx_dvxx(
                self,
                'IDVX',
                'DVXX',
                config.styp_for_s_in_mops3a,
                'S',
            )
            return text


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
        self.reset_position = reset_position

        self.diag_addr = diag_addr
        self.reg = reg
        self.coil = coil

        self.__signals_list = SignalsList()
        self.__locations_list = []
        self.__positions_list = []
        self.__devices_list = []

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
