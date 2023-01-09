import time as t
import random as r
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
from spade import quit_spade

rijeci = ["ABLE", "ABOUT", "ABOVE", "ACID", "ACQUIRE", "ACROSS", "ACT", "ADOPT", "ADVICE", "AGAINST", "AGE", "AGENCY", "AGENDA", "AGENT", "AGO", "AGREE", "AHEAD", "AID", "AIDE", "AIM", "AIR", "ALIVE", "ALLY", "ALSO", "EAGER", "EAR", "EARLY", "EARN", "EARNINGS", "EARTH", "EASE", "EAST", "EASY", "EAT", "ECONOMY", "EDGE", "EDITION", "EDITOR", "EDUCATE", "EDUCATION", "EDUCATOR", "EFFECT", "EFFECTIVE", "EFFICIENT", "EFFORT", "EGG", "EIGHT", "EITHER", "ELDERLY", "ELECT", "ELECTION", "ELEMENTARY", "ELIMINATE", "ELITE", "ELSE", "ELSEWHERE", "EMBRACE", "EMPHASIS", "EMPTY", "ENABLE", "ENCOURAGE", "END", "ENGINE", "INFLUENCE", "INFORM", "INFORMATION", "INNER", "INNOCENT", "INQUIRY", "INSTEAD", "INSTITUTION", "INTENSE", "INTERPRET", "INTERVIEW", "INTO", "INTRODUCE", "INVEST", "INVITE", "INVOLVE", "INVOLVED", "INVOLVEMENT",
          "IRAQI", "IRISH", "IRON", "ISLAMIC", "ISLAND", "ISRAELI", "ISSUE", "IT", "ITALIAN", "ITEM", "ITS", "OBJECT", "OBJECTIVE", "OBLIGATION", "OBSERVATION", "OBSERVE", "OBSERVER", "OBTAIN", "OBVIOUS", "OBVIOUSLY", "OCCASION", "OCCASIONALLY", "OCCUPATION", "OCCUPY", "OCCUR", "OCEAN", "ODD", "ODDS", "OF", "OFF", "OFFENSE", "OFFENSIVE", "OFFER", "OFFICE", "OFFICER", "OFFICIAL", "OFTEN", "OH", "OIL", "OK", "OKAY", "OLD", "OLYMPIC", "ON", "ONCE", "ONE", "ONGOING", "ONION", "ONLINE", "ONLY", "ONTO", "OPEN", "OPENING", "OPERATE", "OPERATING", "OPERATION", "OPERATOR", "OPINION", "OPPONENT", "OPPORTUNITY", "OPPOSE", "OPPOSITE", "OPPOSITION", "OPTION", "OR", "ORANGE", "ORDER", "ORDINARY", "ORIGIN", "OTHER", "OUGHT", "OUR", "OURSELVES", "OUT", "OUTCOME", "OUTSIDE", "OVEN", "OVER", "OVERALL", "OVERCOME", "OVERLOOK", "OWE", "OWN", "OWNER", "ZEAXANTHIN", "ZIGZAGGERS", "ZIGZAGGERY", "ZIGZAGGING", "ZINCIFYING", "ZOMBIFYING", "ZOOMORPHIC", "ZYGOBRANCH", "ZYGODACTYL", "ZYGOMORPHY", "ZYGOMYCETE", "ZYGOPHYTES"]

odabrana_rijec = ""
odabrana_slova = []
broj_pogresaka = 0
pobjedio = 0
skrivena_rijec = ""


def nacrtaj_vjesalo():
    global broj_pogresaka

    if (broj_pogresaka == 1):
        print("    +-------+      ")
        print("    |       |      ")
        print("    |       O      ")
        print("    |              ")
        print("    |              ")
        print("    |              ")
        print("    |              ")
        print("    |              ")
        print("____________       \n")

    elif (broj_pogresaka == 2):
        print("    +-------+      ")
        print("    |       |      ")
        print("    |       O      ")
        print("    |       |      ")
        print("    |              ")
        print("    |              ")
        print("    |              ")
        print("    |              ")
        print("____________       \n")

    elif (broj_pogresaka == 3):
        print("    +-------+      ")
        print("    |       |      ")
        print("    |       O      ")
        print("    |      /|      ")
        print("    |              ")
        print("    |              ")
        print("    |              ")
        print("    |              ")
        print("____________       \n")

    elif (broj_pogresaka == 4):
        print("    +-------+      ")
        print("    |       |      ")
        print("    |       O      ")
        print("    |      /|\      ")
        print("    |              ")
        print("    |              ")
        print("    |              ")
        print("    |              ")
        print("____________       \n")

    elif (broj_pogresaka == 5):
        print("    +-------+      ")
        print("    |       |      ")
        print("    |       O      ")
        print("    |      /|\     ")
        print("    |      /       ")
        print("    |              ")
        print("    |              ")
        print("    |              ")
        print("____________       \n")

    elif (broj_pogresaka == 6):
        print("    +-------+      ")
        print("    |       |      ")
        print("    |       O      ")
        print("    |      /|\     ")
        print("    |      / \     ")
        print("    |              ")
        print("    |              ")
        print("    |              ")
        print("____________       \n")

    else:
        print("    +-------+      ")
        print("    |       |      ")
        print("    |              ")
        print("    |              ")
        print("    |              ")
        print("    |              ")
        print("    |              ")
        print("    |              ")
        print("____________       \n")


class Hangman(Agent):

    class Pokretanje(FSMBehaviour):
        async def on_start(self):
            print("Pocetak\n")

        async def on_end(self):
            print("Kraj\n")
            await self.agent.stop()

    class Povezivanje(State):
        async def run(self):

            print("Čekam igrača\n")
            msg = await self.receive(timeout=30)

            if (msg.metadata['performative'] == 'Request'):
                print("Započinjem igru!\n")
                self.set_next_state("Generiranje")

            else:
                print("Igrač se nije povezao!\n")
                self.set_next_state("Povezivanje")

    class Generiranje(State):
        async def run(self):
            global odabrana_rijec, skrivena_rijec

            odabrana_rijec = rijeci[r.randint(0, len(rijeci))]
            tijelo_poruke = len(odabrana_rijec)
            msg = Message(to="igrac@localhost", body=str(tijelo_poruke),
                          metadata={"performative": "Inform"})
            await self.send(msg)

            for i in range(len(odabrana_rijec)):
                    skrivena_rijec += "_ "

            print("\nOdabrana riječ je: " + odabrana_rijec + "\n")
            nacrtaj_vjesalo()

            self.set_next_state("Provjera")

    class Provjera(State):
        async def run(self):
            global odabrana_rijec, broj_pogresaka, odabrana_slova, pobjedio, skrivena_rijec
            tijelo_poruke = ""

            print("Provjeravam slovo\n")
            msg = await self.receive(timeout=30)

            if (msg.metadata['performative'] == 'Propose'):

                poslano_slovo = msg.body.upper()
                print("Odabrano slovo je " + poslano_slovo + "\n")
                odabrana_slova.append(poslano_slovo)

                if poslano_slovo in odabrana_rijec:
                    print("Bravo, pogodio si\n")
                    
                    index = 0
                    skrivena_rijec = skrivena_rijec.replace(" ","")
                    temp = skrivena_rijec
                    skrivena_rijec = ""

                    for index in range(len(odabrana_rijec)):
                        if temp[index] == "_" and odabrana_rijec[index]==poslano_slovo:
                            skrivena_rijec += poslano_slovo

                        elif temp[index]=="_" and odabrana_rijec[index]!=poslano_slovo:
                            skrivena_rijec +="_ "
                        
                        else:
                            skrivena_rijec += temp[index]


                    tijelo_poruke = "Pogodak ,"+ skrivena_rijec
                    
                    if poslano_slovo == odabrana_rijec[0]:
                        tijelo_poruke = "Pogodak prvog ,"+ skrivena_rijec

                    if not "_" in skrivena_rijec: 
                        pobjedio = 1

                else:
                    print("Slovo nije u rijeci\n")
                    tijelo_poruke = "Promašaj ," + skrivena_rijec
                    broj_pogresaka += 1

                nacrtaj_vjesalo()

                if broj_pogresaka == 6:

                    msg = Message(to="igrac@localhost", body="Gubitak",
                                  metadata={"performative": "Failure"})
                    await self.send(msg)
                    self.set_next_state("Kraj")

                elif pobjedio == 0:
                    print("Pogađaš dalje\n")
                    pokusaji = 6 - broj_pogresaka
                    print("Imaš još " + str(pokusaji) + " pokušaja\n")

                    msg = Message(to="igrac@localhost", body=tijelo_poruke, metadata={"performative": "Inform"})
                    await self.send(msg)
                    self.set_next_state("Provjera")

                else:
                    msg = Message(to="igrac@localhost", body="Pobjeda",
                                  metadata={"performative": "Confirm"})
                    await self.send(msg)
                    self.set_next_state("Kraj")

            else:
                self.set_next_state("Provjera")

    class Kraj(State):
        async def run(self):
            global pobjedio
            if pobjedio == 0:
                print("Izgubio si\n")
            else:
                print("Pobjedio si\n")

    async def setup(self):

        fsm = self.Pokretanje()

        fsm.add_state(name="Povezivanje",
                      state=self.Povezivanje(), initial=True)
        fsm.add_state(name="Generiranje", state=self.Generiranje())
        fsm.add_state(name="Provjera", state=self.Provjera())
        fsm.add_state(name="Kraj", state=self.Kraj())

        fsm.add_transition(source="Povezivanje", dest="Povezivanje")
        fsm.add_transition(source="Povezivanje", dest="Generiranje")
        fsm.add_transition(source="Generiranje", dest="Provjera")
        fsm.add_transition(source="Provjera", dest="Provjera")
        fsm.add_transition(source="Provjera", dest="Kraj")

        self.add_behaviour(fsm)


if __name__ == '__main__':

    hangman = Hangman("hangman@localhost", "hangman")

    hangman_obj = hangman.start()
    hangman_obj.result()

    while hangman.is_alive():
        try:
            t.sleep(1)
        except KeyboardInterrupt:
            print("\nGasim!\n")
            break

    hangman.stop()

    quit_spade()
