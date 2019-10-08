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
    ):
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

    def contains_signals_for_input_txt(self):
        return self.has_any_signal_with_sigtype_in(config.sigtypes_for_input)

    def contains_signals_for_output_txt(self):
        return self.has_any_signal_with_sigtype_in(config.sigtypes_for_output)

    def contains_signals_for_alarming_txt(self):
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

    def contains_signals_for_counting_txt(self):
        return self.has_any_signal_with_sigtype_in(
            config.sigtypes_for_counting
        )

    def contains_signals_with_ff_out_for_counting_txt(self):
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

    def contains_signals_without_ff_out_for_counting_txt(self):
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

    def contains_signals_with_fire_fighting_for_counting_txt(self):
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

    def contains_signals_without_fire_fighting_for_counting_txt(self):
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

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$ ПРОВЕРКА НАЛИЧИЯ СИГНАЛОВ ДЛЯ DIAG_ST $$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def contains_signals_for_diag_st_txt(self):
        return self.has_any_signal_with_sigtype_in(config.sigtypes_for_diag_st)


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
        self.plc = plc
        self.name = name.replace(' ', '').replace('-', '_')
        if not self.name[0].isalpha():
            self.name = 'P' + self.name

        self.izv_addr = izv_addr
        self.opv_addr = opv_addr
        self.tush_addr = tush_addr

        self.name_for_comment = f"{self.name[1:-1].replace('_', '-')}"

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

    def contains_locations_with_warning_and_without_fire_fighting(self):
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
                        f'{signal.name}(.IVXX, .MBIN, .CAON, '
                        '.SCMX, .STYP, SYS_LNG.XLNG, .IDVX);\n'
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
                        f'{signal.name}(.IVXX, .MBIN, '
                        f'{signal.plc.reset_position}CORS.XORS, '
                        '.IDVX, SYS_LNG.XLNG);\n'
                    )
            txt.write('\n')

    def alarming_write_to_txt(self, txt, warning_part):
        """
        Метод записывает в txt строки кода на ST.
        В коде участвуют все сигналы из SignalsList
        .sigtype которых входят в
        config.sigtypes_for_alarming_txt и при этом
        их атрибут .ff_out is None.
        """
        for sigtype in config.sigtypes_for_alarming:
            txt.write(f'// {sigtype}\n')
            for signal in self.signals_list:
                if (
                        signal.sigtype == 'sigtype'
                        and
                        signal.ff_out is not None
                ):
                    txt.write(
                        f'{signal.name}.CAON:='
                        f'{signal.position.name}XFRX_CNT > 0'
                        f'{warning_part};\n'
                    )
            txt.write('\n')
