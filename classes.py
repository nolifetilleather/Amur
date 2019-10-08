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

    def any_signal_sigtype_in(self, sigtypes_list):
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
        return self.any_signal_sigtype_in(config.sigtypes_for_input_txt)

    def contains_signals_for_output_txt(self):
        return self.any_signal_sigtype_in(config.sigtypes_for_output_txt)

    def contains_signals_for_alarming_txt(self):
        return self.any_signal_sigtype_in(config.sigtypes_for_alarming_txt)

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$ ПРОВЕРКА НАЛИЧИЯ СИГНАЛОВ ДЛЯ COUNTING $$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def contains_signals_for_counting_txt(self):
        return self.any_signal_sigtype_in(config.sigtypes_for_counting_txt)

    def contains_signals_with_ff_out_for_counting_txt(self):
        flg = False
        for signal in self:
            if (
                    isinstance(signal, Signal)
                    and
                    signal.ff_out is not None
                    and
                    signal.sigtype in config.sigtypes_for_counting_txt
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
                    signal.sigtype in config.sigtypes_for_counting_txt
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
                    signal.sigtype in config.sigtypes_for_counting_txt
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
                    signal.sigtype in config.sigtypes_for_counting_txt
            ):
                flg = True
                break
        return flg

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$ ПРОВЕРКА НАЛИЧИЯ СИГНАЛОВ ДЛЯ DIAG_ST $$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def contains_signals_for_diag_st_txt(self):
        return self.any_signal_sigtype_in(config.sigtypes_for_diag_st_txt)


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
        к "локации" принадлежат к одной позиции,
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
    pass

