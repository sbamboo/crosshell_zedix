"""Contains the LearnAttack class"""

import random
import scrap_engine as se
import pokete_data as p_data
from pokete_general_use_fns import liner
from .hotkeys import Action, get_action
from .loops import std_loop, easy_exit_loop
from .input import ask_bool, ask_ok
from .ui_elements import ChooseBox, Box
from . import detail
from .attack import Attack


class AttackInfo(Box):
    """Gives information about a certain attack
    ARGS:
        attack: The attack's name
        _map: se.Map this should be shown on"""

    def __init__(self, attack, _map, overview):
        atc = Attack(attack)
        desc_label = se.Text(liner(atc.desc, 40))
        super().__init__(
            5 + len(desc_label.text.split("\n")),
            sorted(
                len(i) for i in
                desc_label.text.split("\n")
                + [
                    atc.label_type.text,
                    atc.label_factor.text
                ]
            )[-1] + 4, atc.name, f"{Action.CANCEL.mapping}:close",
            overview=overview)
        self.map = _map
        self.add_ob(atc.label_type, 2, 1)
        self.add_ob(atc.label_factor, 2, 2)
        self.add_ob(se.Text(f"AP:{atc.max_ap}"), 2, 3)
        self.add_ob(desc_label, 2, 4)

    def __enter__(self):
        """Enter dunder for context management"""
        self.center_add(self.map)
        self.map.show()
        return self


class LearnAttack:
    """Lets a Pokete learn a new attack
    ARGS:
        poke: The Poke that should learn an attack
        _map: The se.Map this should happen on"""

    def __init__(self, poke, _map, overview):
        self.map = _map
        self.poke = poke
        self.box = ChooseBox(
            6, 25, name="Attacks",
            info=f"{Action.DECK.mapping}:Details, {Action.INFO.mapping}:Info",
            overview=overview
        )

    @staticmethod
    def get_attack(poke):
        """Gets a learnable attack for a given pokete
        ARGS:
            poke: The pokete
        RETURNS:
            The attacks name, None if none is found"""
        attacks = p_data.attacks
        pool = [i for i, atc in attacks.items()
                if all(j in [i.name for i in poke.types]
                       for j in atc["types"])
                and atc["is_generic"]]
        full_pool = [i for i in poke.inf["attacks"] +
                     poke.inf["pool"] + pool
                     if i not in poke.attacks
                     and attacks[i]["min_lvl"] <= poke.lvl()]
        if len(full_pool) == 0:
            return None
        return random.choice(full_pool)

    def __call__(self, attack=None):
        """Starts the learning process
        ARGS:
            attack: The attack's name that should be learned, if None a fitting
                    attack will be chosen randomly
        RETURNS:
            bool: Whether or not the attack was learned"""
        attacks = p_data.attacks
        if attack is None:
            if (new_attack := self.get_attack(self.poke)) is None:
                return False
        else:
            new_attack = attack
        if ask_bool(
            self.map,
            f"{self.poke.name} wants to learn "
            f"{attacks[new_attack]['name']}!",
            self.map
        ):
            if len(self.poke.attacks) < 4:
                self.poke.attacks.append(new_attack)
                self.poke.attack_obs.append(Attack(new_attack,
                                                  len(self.poke.attacks)))
            else:
                self.box.add_c_obs([se.Text(f"{i + 1}: {j.name}", state="float")
                                    for i, j in enumerate(self.poke.attack_obs)])
                with self.box.center_add(self.map):
                    while True:
                        action = get_action()
                        if action.triggers(Action.UP, Action.DOWN):
                            self.box.input(action)
                            self.map.show()
                        elif action.triggers(Action.ACCEPT):
                            i = self.box.index.index
                            self.poke.attacks[i] = new_attack
                            self.poke.attack_obs[i] = Attack(new_attack, i + 1)
                            ask_ok(
                                self.map,
                                f"{self.poke.name} learned "
                                f"{attacks[new_attack]['name']}!",
                                self.box
                            )
                            break
                        elif action.triggers(Action.DECK):
                            detail.detail(self.poke, False, overview=self.box)
                            self.map.show(init=True)
                        elif action.triggers(Action.INFO):
                            with AttackInfo(
                                new_attack, self.map, self.box
                            ) as box:
                                easy_exit_loop(box=box)
                        elif action.triggers(Action.CANCEL):
                            return False
                        std_loop(box=self.box)
                self.box.remove_c_obs()
            return True
        return False
