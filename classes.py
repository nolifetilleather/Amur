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
                        (signal.location.fire_fightings_cntrs is not None
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
                        signal.location.fire_fightings_cntrs is None
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
        return any(
            isinstance(signal, Signal)
            and
            signal.ff_out is not None
            and
            signal.sigtype in config.sigtypes_for_counting
            for signal in self
        )

    def contains_signals_without_ff_out_for_counting(self):
        return any(
            isinstance(signal, Signal)
            and
            signal.ff_out is None
            and
            signal.sigtype in config.sigtypes_for_counting
            for signal in self
        )

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
                    signal.location.fire_fightings_cntrs is not None
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
                    signal.location.fire_fightings_cntrs is None
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
                         signal.location.fire_fightings_cntrs is not None)
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
                         signal.location.fire_fightings_cntrs is None)
                ):
                    flg = True
                    break
        return flg

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$ ПРОВЕРКА НАЛИЧИЯ СИГНАЛОВ ДЛЯ DIAG_ST $$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def contains_signals_for_diag_st(self):
        return self.has_any_signal_with_sigtype_in(
            config.sigtypes_for_diag_st
        )


class Location:

    def __init__(
            self,
            name,
            warning_cntr=None,
            fire_cntr=None,
            fire_fightings_cntrs=None,
            conterminal_systems_cntrs=None,
            voting_logic=None,
    ):

        self.signals_list = SignalsList()  # для ссылок на объекты сигналов
        self.position = None  # см метод position_check_and_set

        self.name = name
        self.warning_cntr = warning_cntr
        self.fire_cntr = fire_cntr
        self.fire_fightings_cntrs = fire_fightings_cntrs
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
        self.name_for_comment = name
        self.name = self.format_position_name(name)

        self.izv_addr = izv_addr
        self.opv_addr = opv_addr
        self.tush_addr = tush_addr

        self.signals_list = SignalsList()
        self.locations_list = []
        self.upg_counters = []
        self.upg_markers = []
        self.xsy_counters = []
        self.counters = []
        self.bool_counters = set()

    @staticmethod
    def format_position_name(name):
        frmt_name = name.replace(' ', '').replace('-', '_')
        if not frmt_name[0].isalpha():
            frmt_name = 'P' + frmt_name
        return frmt_name

    def contains_locations_with_warning(self):
        """
        Возвращет True если в списке locations_list
        есть экземпляр Location атрибут .warning_cntr
        которого == True.
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

    def input_write_to_txt(self, txt):
        """
        Метод записывает в txt строки кода на ST.
        В коде участвуют все сигналы из self.signals_list
        .sigtype которых входят в
        config.sigtypes_for_input_txt.
        """
        # for signal in self.signals_list:
        #    print(f'{signal.name} {signal.sigtype}')
        txt.write(f'// {self.name_for_comment}\n')
        for sigtype in config.sigtypes_for_input:
            txt.write(f'// {sigtype}\n')
            for signal in self.signals_list:
                if signal.sigtype == sigtype:
                    txt.write(
                        f'{signal.name}(.IVXX, .MBIN, '
                        f'{signal.plc.reset_position}_CORS.XORS, '
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
                if signal.sigtype == sigtype:
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

            txt.write('\n// Имитации')

            cntr_marker = cntrs_markers['Имитации']
            counter = f'{position}_{cntr_marker}_CNT'

            for sigtype in config.sigtypes_for_imitations_in_counting:
                txt.write(f'\n// {sigtype}\n')
                for signal in self.signals_list:
                    if signal.sigtype == sigtype:
                        txt.write(
                            self.__counter_one_signal_actuation(
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
                for signal in self.signals_list:
                    if signal.sigtype == sigtype:
                        txt.write(
                            self.__counter_one_signal_actuation(
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
                              signal.location.fire_fightings_cntrs is None))
                    ):
                        txt.write(
                            self.__counter_one_signal_actuation(
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
                              signal.location.fire_fightings_cntrs is None))
                    ):
                        txt.write(
                            self.__counter_one_signal_actuation(
                                signal,
                                counter,
                                cntr_marker,
                            )
                        )
                # txt.write('\n')

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

        # СЧЕТЧИКИ ИП С ТУШЕНИЕМ
        # НЕИСПРАВНОСТИ (сигналы с тушением)
        if cntrs_with_ff['Неисправности']:

            txt.write('\n// Неисправности (сигналы с тушением)')

            iteration = 1

            cntr_marker = cntrs_markers['Неисправности']
            for upg_marker in self.upg_markers:
                counter = f'{position}_{cntr_marker}_{upg_marker}_CNT'

                for sigtype in config.sigtypes_for_faults_in_counting:
                    txt.write(f'\n// {sigtype}\n')
                    for signal in self.signals_list:
                        if (
                                signal.sigtype == sigtype
                                and
                                (signal.ff_out is not None
                                 or
                                 (isinstance(signal.location, Location)
                                  and
                                  signal
                                  .location.fire_fightings_cntrs is not None))
                        ):
                            txt.write(
                                self.__counter_one_signal_actuation(
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

            iteration = 1

            cntr_marker = cntrs_markers['Недостоверности']
            for upg_marker in self.upg_markers:
                counter = f'{position}_{cntr_marker}_{upg_marker}_CNT'

                for sigtype in config.sigtypes_for_falsities_in_counting:
                    txt.write(f'\n// {sigtype}\n')
                    for signal in self.signals_list:
                        if (
                                signal.sigtype == sigtype
                                and
                                (signal.ff_out is not None
                                 or
                                 (isinstance(signal.location, Location)
                                  and
                                  signal
                                  .location.fire_fightings_cntrs is not None))
                        ):
                            txt.write(
                                self.__counter_one_signal_actuation(
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

        # ВНИМАНИЯ (сигналы c тушением)
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

        # СЧЕТЧИКИ РЕЖИМА
        if len(self.upg_counters) != 0:
            txt.write(

                '\n// Счетчик режима "Идет отсчет до начала тушения"\n'
                '{0}XRFD_CNT:=Count({0}UPG.XFDN, {0}XRFD_CNT);\n\n'
                .format(position)
                +
                '// Счетчик режима "Идет тушение"\n'
                '{0}XRFN_CNT:=Count({0}UPG.OF1N, {0}XRFN_CNT);\n'
                .format(position)
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
        return f'M{self.name[5:]}_{sm}_A{addr}'

    # м-имя для теста/сброса МОПСов 3а
    def __m_name_s_f_s(self, first, second):
        return f'M{self.name[5:]}_S_{first}_{second}'

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
                    f'{self.__m_name(addr, "S")}.RST_CNTo'
                    # f'M{self.name[5:]}_S_A{addr}.RST_CNTo'
                arg4 = \
                    f'{self.__m_name(addr, "S")}.TST_CNTo'
                    # f'M{self.name[5:]}_S_A{addr}.TST_CNTo'
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
        self.reset_position_for_comment = reset_position
        self.reset_position = Position.format_position_name(reset_position)

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

    def change_output_path(self):
        self.output_path = str(input(
            'Введите путь для выходных файлов\n'
        ))

    # def print_signals(self):
    #    for signal in self.__signals_list:
    #        print(f'{signal.name} {signal.sigtype}')

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$ ЗАПОЛНЕНИЕ СПИСКОВ $$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

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

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$ ОПЕРАЦИИ НАД ОБЪЕКТАМИ В СПИСКАХ $$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

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
                    location.signals_list.append(signal)
                    """
                    Заменим строковое значение атрибута
                    location объекта сигнала полученное
                    при чтении входныъ данных ссылкой на
                    соответствующий объект "локации".
                    """
                    signal.location = location
            """
            Проверка допустимости значений в signals_list
            экземпляра Location.
            Установка установка необходимых ссылок
            в атрибутах экзмпляра Location и соответствующего
            экземпляра Position на основе заполненного
            signals_list.
            """
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

        diag_device_position = Position(name='Diag_Devices_Position', plc=self)
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
                position=diag_device_position,
            )
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

            if self.ce_locations_filled:
                self.__fill_locations_signals_lists_and_position()
                self.__fill_counters()
                self.locations_reformed = True

            if self.devices_list_filled:
                self.__fill_devices_signals_lists()
                self.devices_reformed = True
                self.__create_devices_diag_signals()
                self.devices_diag_signals_created = True

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
        print()

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$ ПРОВЕРКА ГОТОВНОСТИ К ФОРМИРОВАНИЮ ПРОГРАММ $$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def ready_for_counting(self):
        return (
            self.__signals_list.contains_signals_for_counting()
            and
            self.locations_reformed
        )

    def ready_for_alarming(self):
        return (
            self.ready_for_counting()
            and
            self.__signals_list.contains_signals_for_alarming()
        )

    def ready_for_output(self):
        return (
            self.__signals_list.contains_signals_for_output()
            and
            self.signals_reformed
        )

    def ready_for_input(self):
        return (
            self.__signals_list.contains_signals_for_input()
            and
            self.signals_reformed
        )

    def ready_for_mops_mups(self):
        return self.devices_reformed

    def ready_for_datatable(self):
        return self.__counting_was_formed and self.__mops_mups_was_formed

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
        )

    def ready_for_diag_st(self):
        return self.__signals_list.contains_signals_for_diag_st()

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$ ФОРМИРОВАНИЕ ТЕКСТОВ ПРОГРАММ $$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    # OUTPUT
    def establishing_output_txt(self):
        if self.ready_for_input():
            txt = open(fr'{self.output_path}\Output.txt', 'w')
            for position in self.__positions_list:
                if position.signals_list.contains_signals_for_output():
                    position.output_write_to_txt(txt)
            txt.close()
            return True

    # INPUT
    def establishing_input_txt(self):
        if self.ready_for_input():
            txt = open(fr'{self.output_path}\Input.txt', 'w')
            for position in self.__positions_list:
                if position.signals_list.contains_signals_for_input():
                    position.input_write_to_txt(txt)
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
            txt.close()
            self.__counting_was_formed = True
            return True

    # MOPS_MUPS
    def contains_devtype_in_devices_list(self, devtype):
        return(
            any(device.devtype == devtype for device in self.__devices_list)
        )

    def establishing_mops_mups_txt(self):
        if self.ready_for_mops_mups():
            txt = open(fr'{self.output_path}\MOPS_MUPS.txt', 'w')

            # $$$$$$$$$$$$$$$$$$$ ВЫЗОВ БЛОКОВ $$$$$$$$$$$$$$$$$$
            txt.write('// Вызов блоков\n')
            for device in self.__devices_list:
                txt.write(device.call_for_mops_mups_text())

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
                if device.mops_shifting_text() is not None:
                    txt.write(device.mops_shifting_text())
            # МУПСЫ
            for device in self.__devices_list:
                if device.mups_shifting_text() is not None:
                    txt.write(device.mups_shifting_text())

            # $$$$$$$$$$$$$$$$$$$$$$ IVXX $$$$$$$$$$$$$$$$$$$$$$$
            txt.write(
                '//Перекладываем данные с выходов ФБ МОПС/'
                'МУПС во входные переменные ФБ извещателя\n\n'
            )
            # МОПСЫ
            for device in self.__devices_list:
                if device.mops_ivxx_text() is not None:
                    txt.write(device.mops_ivxx_text())
            # МУПСЫ
            for device in self.__devices_list:
                if device.mups_ivxx_text() is not None:
                    txt.write(device.mups_ivxx_text())

            # $$$$$$$$$$$$$$$$$$$$$$ IDVX $$$$$$$$$$$$$$$$$$$$$$$
            txt.write(
                '// Формируем сигнал Недостоверность шле'
                'йфа по исчезновению связи с МОПС/МУПС\n\n'
            )
            # МОПСЫ
            for device in self.__devices_list:
                if device.mops_idvx_text() is not None:
                    txt.write(device.mops_idvx_text())
            # МУПСЫ
            for device in self.__devices_list:
                if device.mups_idvx_text() is not None:
                    txt.write(device.mups_idvx_text())

            # $$$$$$$$$$$$$$$$$$ СБРОС МОПСОВ $$$$$$$$$$$$$$$$$$$
            txt.write('// Сброс мопсов\n')
            for device in self.__devices_list:
                if device.mops_reset_text() is not None:
                    txt.write(device.mops_reset_text())

            #  МОПСЫ 3а
            if self.contains_devtype_in_devices_list('MOPS3a'):
                for device in self.__devices_list:
                    if device.mops3a_m_text() is not None:
                        txt.write(device.mops3a_m_text())
                    if device.mops3a_s_text() is not None:
                        txt.write(device.mops3a_s_text())

                txt.write('// Тест и сброс извещателей\n')
                for device in self.__devices_list:
                    if device.mops3a_test_reset_text() is not None:
                        txt.write(device.mops3a_test_reset_text())

                txt.write(
                    '// Перекладываем данные с выходов МОПС3А'
                    ' в входные переменные ФБ извещателя\n\n'
                )
                for device in self.__devices_list:
                    if device.mops3a_m_ivxx_xvlx_text() is not None:
                        txt.write(device.mops3a_m_ivxx_xvlx_text())
                    if device.mops3a_s_idvx_dvxx_text() is not None:
                        txt.write(device.mops3a_s_ivxx_xvlx_text())

                txt.write(
                    '//Формируем сигнал Недостоверность шлейфа '
                    'по исчезновению связи с МОПС3А\n\n'
                )
                for device in self.__devices_list:
                    if device.mops3a_m_idvx_dvxx_text() is not None:
                        txt.write(device.mops3a_m_idvx_dvxx_text())
                    if device.mops3a_s_idvx_dvxx_text() is not None:
                        txt.write(device.mops3a_s_idvx_dvxx_text())
            txt.close()
            self.__mops_mups_was_formed = True
            return True

    # Reset_MOPS3a
    def establishing_reset_mops3a_txt(self):
        if (
            self.ready_for_mops_mups()
            and
            self.contains_devtype_in_devices_list('MOPS3a')
        ):
            txt = open(fr'{self.output_path}\Reset_MOPS.txt', 'w')
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
        if self.ready_for_mops_mups():
            txt = open(fr'{self.output_path}\Oxon.txt', 'w')
            for device in self.__devices_list:
                if device.mups_oxon_text() is not None:
                    txt.write(device.mups_oxon_text())
            txt.close()
            return True

    # DIAG_ST
    def establishing_diag_st_txt(self):
        if self.ready_for_diag_st():
            txt = open(fr'{self.output_path}\Diag_ST.txt', 'w')
            import re

            def select_by_type_and_sort_by_address(types_lst, sgnls_lst):
                lst = \
                    list(filter(lambda sgnl:
                                sgnl.sigtype
                                in
                                types_lst,
                                sgnls_lst))
                lst.sort(
                    key=lambda sgnl: int(re.findall(r'\d+', sgnl.address)[-1])
                )
                return lst

            for position in self.__positions_list:
                if position.signals_list.contains_signals_for_diag_st():
                    txt.write(f'// {position.name_for_comment}\n')

                diag_st_di = select_by_type_and_sort_by_address(
                    config.sigtypes_di_for_diag_st, position.signals_list
                )

                diag_st_modules = select_by_type_and_sort_by_address(
                    config.sigtypes_modules_for_types, position.signals_list
                )

                for signal in diag_st_di:
                    txt.write(
                        f'{signal.name}(_IO_{signal.address}, SYS_LNG.XLNG);\n'
                    )

                if len(diag_st_di) != 0:
                    txt.write('\n')

                for signal in diag_st_modules:
                    txt.write(
                        f'{signal.name}(_IO_{signal.address}.Status);\n'
                    )

                if len(diag_st_modules) != 0:
                    txt.write('\n')

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
                    txt.write('\n')

            if self.diag_addr != '':
                txt.write('// Диагностика\n')
                n = 0
                for sigtype in config.sigtypes_diag_for_weintek:
                    for signal in self.__signals_list:
                        if signal.sigtype == sigtype:
                            if sigtype == 'DIAG_DI':
                                txt.write(
                                    '_IO_QX{0}_1_{2}: = {1}.XVLX;\n'
                                    '_IO_QX{0}_1_{3}: = {1}.DVXX;\n'.format(
                                        self.coil,
                                        signal.name,
                                        int(self.diag_addr)+1+n,
                                        int(self.diag_addr)+2+n,
                                    )
                                )
                                n += 2
                            elif sigtype == 'DIAG_Mod':
                                txt.write(
                                    '_IO_QX{0}_1_{2}: = {1}.FXXX;\n'.format(
                                        self.coil,
                                        signal.name,
                                        int(self.diag_addr) + 1 + n,
                                    )
                                )
                                n += 1
                            elif sigtype in ['Mops3', 'Mups3', 'Mops3a']:
                                txt.write(
                                    '_IO_QX{0}_1_{2}: = {1}.DVXX;\n'.format(
                                        self.coil,
                                        signal.name,
                                        int(self.diag_addr) + 1 + n,
                                    )
                                )
                                n += 1
                    txt.write('\n')
            txt.close()
            return True

    def __datatable(self, category):

        for position in self.__positions_list:
            if len(position.upg_counters) != 0:
                bool_counter = \
                    f'{position.name}UPG_{config.cntrs_dict["Пожары"]}'
                position.bool_counters.add(bool_counter)
            if len(position.xsy_counters) != 0:
                bool_counter = \
                    f'{position.name}{config.cntrs_dict["Смежные системы"]}'
                position.bool_counters.add(bool_counter)
            for counter in position.counters:
                for cntr_type in config.cntrs_dict:
                    cntr_marker = config.cntrs_dict[cntr_type]
                    if cntr_marker in counter and 'UPG' not in counter:
                        bool_counter = \
                            f'{position.name}{cntr_marker}'
                        position.bool_counters.add(bool_counter)
                    elif cntr_marker in counter and 'UPG' in counter:
                        bool_counter = \
                            f'{position.name}UPG_{cntr_marker}'
                        position.bool_counters.add(bool_counter)

        cors_coof = ['CORS', 'COOF']

        data_len = 0

        data_len += len(self.__signals_list)
        data_len += len(self.m_names)
        data_len += len(cors_coof)*len(self.__positions_list)

        for position in self.__positions_list:
            data_len += len(position.upg_counters)
            data_len += len(position.xsy_counters)
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
                signal.sigtype \
                if category != 2 \
                else signal.signal_type_cat2
            data['Группа событий'][i] = \
                signal.position.name_for_comment
            data['KKS'][i] = \
                signal.name[1:].replace('_', '-') \
                if signal.name[1] == 'P' \
                else signal.name.replace('_', '-')
            data['Шаблон'][i] = \
                'FB_' + signal.sigtype \
                if category != 2 \
                else signal.signal_type_cat2
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
                'MOPS3a'
            data['Группа событий'][i+filled] = \
                self.reset_position_for_comment
            data['Шаблон'][i+filled] = \
                'MOPS3a'
        filled += len(self.m_names)

        for position in self.__positions_list:
            iteration = 0
            for corscoof in cors_coof:
                data['Марка'][iteration+filled] = \
                    f'{position.name}{corscoof}'
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

    def establishing_datatable_to_xlsx(self):
        if self.ready_for_datatable():
            if self.cabinet_category == '2':
                self.__datatable(1)
                self.__datatable(2)
            else:
                self.__datatable(1)
