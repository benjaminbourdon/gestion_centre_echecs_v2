class MenuView():
    def ask_choice(self, choicies):
        print("Que voulez-vous faire ?")
        for index, choice in enumerate(choicies):
            print(index, choice[0])
        return input("Tapez le numéro de l'action souhaitée : ").strip()