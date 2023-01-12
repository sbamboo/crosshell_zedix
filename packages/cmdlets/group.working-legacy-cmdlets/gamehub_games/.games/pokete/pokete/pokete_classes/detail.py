"""Contains classes needed for the detail-view of a Pokete"""

import scrap_engine as se
import pokete_classes.game_map as gm
from pokete_general_use_fns import liner
from .hotkeys import Action, get_action
from .pokestats import PokeStatsInfoBox
from .loops import std_loop
from .event import _ev
from .ui_elements import StdFrame2, ChooseBox
from .color import Color
from .tss import tss


class Informer:
    """Supplies methods for Deck and Detail"""

    @staticmethod
    def add(poke, figure, _map, _x, _y, in_deck=True):
        """Adds a Pokete's info to the deck
        ARGS:
            poke: Poke object
            figure: Figure object
            _map: se.Map object the information is added to
            _x: X-coordinate the info is added to
            _y: Y-coordinate
            in_deck: bool whether or not the info is added to the deck"""
        poke.text_name.add(_map, _x + 12, _y + 0)
        if poke.identifier != "__fallback__":
            for obj, __x, __y in zip([poke.ico, poke.text_lvl, poke.text_hp,
                                      poke.tril, poke.trir, poke.hp_bar,
                                      poke.text_xp],
                                     [0, 12, 12, 18, 27, 19, 12],
                                     [0, 1, 2, 2, 2, 2, 3]):
                obj.add(_map, _x + __x, _y + __y)
            if in_deck and figure.pokes.index(poke) < 6:
                poke.pball_small.add(_map, round(_map.width / 2) - 1
                                           if figure.pokes.index(poke) % 2 == 0
                                           else _map.width - 2, _y)
            for eff in poke.effects:
                eff.add_label()

    @staticmethod
    def remove(poke):
        """Removes a Pokete from the deck
        ARGS:
            poke: Poke object that should be removed"""
        for obj in [poke.ico, poke.text_name, poke.text_lvl, poke.text_hp,
                    poke.tril, poke.trir, poke.hp_bar, poke.text_xp,
                    poke.pball_small]:
            obj.remove()
        for eff in poke.effects:
            eff.cleanup()


class Detail(Informer):
    """Shows details about a Pokete
    ARGS:
        height: Height of the map
        width: Width of the map"""

    def __init__(self, height, width):
        self.map = gm.GameMap(height, width, name="detail")
        self.name_label = se.Text("Details", esccode=Color.thicc)
        self.name_attacks = se.Text("Attacks", esccode=Color.thicc)
        self.frame = StdFrame2(17, self.map.width, state="float")
        self.attack_defense = se.Text("Attack:   Defense:", state="float")
        self.world_actions_label = se.Text("Abilities:", state="float")
        self.type_label = se.Text("Type:", state="float")
        self.initiative_label = se.Text("Initiative:", state="float")
        self.exit_label = se.Text(f"{Action.DECK.mapping}: Exit", state="float")
        self.nature_label = se.Text(
            f"{Action.NATURE_INFO.mapping}: Nature", state="float"
        )
        self.stats_label = se.Text(
            f"{Action.STATS_INFO.mapping}: Statistics", state="float"
        )
        self.ability_label = se.Text(
            f"{Action.ABILITIES_INFO.mapping}: Use ability", state="float"
        )
        self.line_sep1 = se.Square("-", self.map.width - 2, 1, state="float")
        self.line_sep2 = se.Square("-", self.map.width - 2, 1, state="float")
        self.line_middle = se.Square("|", 1, 10, state="float")
        # adding
        self.name_label.add(self.map, 2, 0)
        self.name_attacks.add(self.map, 2, 6)
        self.attack_defense.add(self.map, 13, 5)
        self.world_actions_label.add(self.map, 24, 4)
        self.type_label.add(self.map, 36, 5)
        self.initiative_label.add(self.map, 49, 5)
        self.exit_label.add(self.map, 0, self.map.height - 1)
        self.nature_label.add(self.map, 9, self.map.height - 1)
        self.stats_label.add(self.map, 20, self.map.height - 1)
        self.ability_label.add(self.map, 35, self.map.height - 1)
        self.line_sep1.add(self.map, 1, 6)
        self.line_sep2.add(self.map, 1, 11)
        self.frame.add(self.map, 0, 0)
        self.line_middle.add(self.map, round(self.map.width / 2), 7)
        self.poke = None
        self.overview = None

    def resize_view(self):
        """Manages recursive view resizing"""
        self.exit_label.remove()
        self.nature_label.remove()
        abb_added = self.ability_label.added
        self.ability_label.remove()
        self.stats_label.remove()
        self.line_sep1.remove()
        self.line_sep2.remove()
        self.frame.remove()
        self.line_middle.remove()
        self.poke.desc.remove()
        for atc in self.poke.attack_obs:
            for label in [
                atc.label_name, atc.label_factor,
                atc.label_type, atc.label_ap, atc.label_desc
            ]:
                label.remove()
        self.map.resize(tss.height - 1, tss.width, background=" ")
        self.overview.resize_view()
        self.line_sep1.resize(self.map.width - 2, 1)
        self.line_sep2.resize(self.map.width - 2, 1)
        self.frame.resize(17, self.map.width)
        self.poke.desc.rechar(liner(self.poke.inf["desc"], tss.width - 34))
        self.line_sep1.add(self.map, 1, 6)
        self.line_sep2.add(self.map, 1, 11)
        self.frame.add(self.map, 0, 0)
        self.exit_label.add(self.map, 0, self.map.height - 1)
        self.nature_label.add(self.map, 9, self.map.height - 1)
        self.stats_label.add(self.map, 20, self.map.height - 1)
        if abb_added:
            self.ability_label.add(self.map, 35, self.map.height - 1)
        self.poke.desc.add(self.map, self.poke.desc.x, self.poke.desc.y)
        self.add_attack_labels()
        self.line_middle.add(self.map, round(self.map.width / 2), 7)

    def add_attack_labels(self):
        """Adds the atatck labels to map"""
        for atc, _x, _y in zip(
            self.poke.attack_obs,
            [
                1, round(self.map.width / 2) + 1,
                1, round(self.map.width / 2) + 1
            ],
            [7, 7, 12, 12]
        ):
            atc.temp_i = 0
            atc.temp_j = -30
            atc.label_desc.rechar(atc.desc[:int(self.map.width / 2 - 1)])
            atc.label_ap.rechar(f"AP:{atc.ap}/{atc.max_ap}")
            for label, __x, __y in zip([atc.label_name, atc.label_factor,
                                        atc.label_type,
                                        atc.label_ap, atc.label_desc],
                                       [0, 0, 11, 0, 0],
                                       [0, 1, 1, 2, 3]):
                label.add(self.map, _x + __x, _y + __y)

    def __call__(self, poke, abb=True, overview=None):
        """Shows details
        ARGS:
            poke: Poke object whose details are given
            abb: Bool whether or not the ability option is shown"""
        self.poke = poke
        self.overview = overview
        ret_action = None
        self.add(self.poke, None, self.map, 1, 1, False)
        abb_obs = [i for i in self.poke.attack_obs
                   if i.world_action != ""]
        if abb_obs != [] and abb:
            self.world_actions_label.rechar("Abilities:"
                                            + " ".join([i.name
                                                        for i in abb_obs]))
            self.ability_label.add(self.map, 35, self.map.height - 1)
        else:
            self.world_actions_label.rechar("")
            self.ability_label.remove()
        self.attack_defense.rechar(f"Attack:{self.poke.atc}\
{(4 - len(str(self.poke.atc))) * ' '}Defense:{self.poke.defense}")
        self.initiative_label.rechar(f"Initiative:{self.poke.initiative}")
        for obj, _x, _y in zip([self.poke.desc, self.poke.text_type], [34, 41], [2, 5]):
            obj.add(self.map, _x, _y)
        self.add_attack_labels()
        if (tss.height - 1, tss.width) != (self.map.height, self.map.width):
            self.resize_view()
        self.map.show(init=True)
        while True:
            action = get_action()
            if action.triggers(Action.DECK, Action.CANCEL):
                self.remove(self.poke)
                for obj in [self.poke.desc, self.poke.text_type]:
                    obj.remove()
                for atc in self.poke.attack_obs:
                    for obj in [atc.label_name, atc.label_factor, atc.label_ap,
                                atc.label_desc, atc.label_type]:
                        obj.remove()
                    del atc.temp_i, atc.temp_j
                return ret_action
            if action.triggers(Action.NATURE_INFO):
                poke.nature.info(self.map, self)
            elif action.triggers(Action.STATS_INFO):
                PokeStatsInfoBox(poke.poke_stats, self)(self.map)
            elif action.triggers(Action.ABILITIES_INFO):
                if abb_obs != [] and abb:
                    with ChooseBox(
                        len(abb_obs) + 2, 25, name="Abilities",
                        c_obs=[
                            se.Text(i.name)
                            for i in abb_obs
                        ],
                        overview=self
                    ).center_add(self.map)\
                            as box:
                        while True:
                            action = get_action()
                            if action.triggers(Action.UP, Action.DOWN):
                                box.input(action)
                                self.map.show()
                            elif action.triggers(Action.ACCEPT):
                                ret_action = abb_obs[box.index.index].world_action
                                _ev.set(Action.CANCEL.mapping)
                                break
                            elif action.triggers(Action.CANCEL):
                                break
                            std_loop(False, box=box)
            std_loop(False, box=self)
            # This section generates the Text effect for attack labels
            for atc in self.poke.attack_obs:
                if len(atc.desc) > int((self.map.width - 3) / 2 - 1):
                    if atc.temp_j == 5:
                        atc.temp_i += 1
                        atc.temp_j = 0
                        if atc.temp_i == len(atc.desc)\
                                          - int(self.map.width / 2 - 1)\
                                          + 10:
                            atc.temp_i = 0
                            atc.temp_j = -30
                        atc.label_desc.rechar(atc.desc[atc.temp_i:
                                                       int(self.map.width
                                                           / 2 - 1)
                                                       + atc.temp_i])
                    else:
                        atc.temp_j += 1
            self.map.show()


detail = None

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
