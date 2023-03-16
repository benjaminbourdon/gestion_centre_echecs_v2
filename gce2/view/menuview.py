from gce2.utils import _is_str, _is_int


class MenuView:
    def __init__(self) -> None:
        self.msg_error = None

    def print_menu_choicies(self, choicies, msg_intro=None):
        print()
        if self.msg_error is not None:
            print(self.msg_error)
            self.msg_error = None
        if msg_intro is not None and _is_str(msg_intro):
            print(msg_intro)
        for index, choice in enumerate(choicies):
            print(index, choice[0])

    def ask_choice(self, choicies, msg_intro=None, msg_action=None):
        while True:
            self.print_menu_choicies(choicies, msg_intro=msg_intro)

            answer = input(msg_action).strip()
            print()

            if _is_int(answer) and int(answer) < len(choicies):
                return choicies[int(answer)][1]
            else:
                self.msg_error = "Vous devez indiquer un numéro valide. Ré-essayer."

    def ask_menu_choicies(self, choicies):
        msg_intro = "Que voulez-vous faire ?"
        msg_action = "Tapez ici le numéro souhaité : "
        return self.ask_choice(choicies, msg_intro=msg_intro, msg_action=msg_action)
