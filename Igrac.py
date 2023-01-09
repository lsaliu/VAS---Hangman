import time as t
import random as r
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
from spade import quit_spade


rijeci = ["ABLE", "ABOUT", "ABOVE", "ACID", "ACQUIRE", "ACROSS", "ACT", "ADOPT", "ADVICE", "AGAINST", "AGE", "AGENCY", "AGENDA", "AGENT", "AGO", "AGREE", "AHEAD", "AID", "AIDE", "AIM", "AIR", "ALIVE", "ALLY", "ALSO", "EAGER", "EAR", "EARLY", "EARN", "EARNINGS", "EARTH", "EASE", "EAST", "EASY", "EAT", "ECONOMY", "EDGE", "EDITION", "EDITOR", "EDUCATE", "EDUCATION", "EDUCATOR", "EFFECT", "EFFECTIVE", "EFFICIENT", "EFFORT", "EGG", "EIGHT", "EITHER", "ELDERLY", "ELECT", "ELECTION", "ELEMENTARY", "ELIMINATE", "ELITE", "ELSE", "ELSEWHERE", "EMBRACE", "EMPHASIS", "EMPTY", "ENABLE", "ENCOURAGE", "END", "ENGINE", "INFLUENCE", "INFORM", "INFORMATION", "INNER", "INNOCENT", "INQUIRY", "INSTEAD", "INSTITUTION", "INTENSE", "INTERPRET", "INTERVIEW", "INTO", "INTRODUCE", "INVEST", "INVITE", "INVOLVE", "INVOLVED", "INVOLVEMENT",
          "IRAQI", "IRISH", "IRON", "ISLAMIC", "ISLAND", "ISRAELI", "ISSUE", "IT", "ITALIAN", "ITEM", "ITS", "OBJECT", "OBJECTIVE", "OBLIGATION", "OBSERVATION", "OBSERVE", "OBSERVER", "OBTAIN", "OBVIOUS", "OBVIOUSLY", "OCCASION", "OCCASIONALLY", "OCCUPATION", "OCCUPY", "OCCUR", "OCEAN", "ODD", "ODDS", "OF", "OFF", "OFFENSE", "OFFENSIVE", "OFFER", "OFFICE", "OFFICER", "OFFICIAL", "OFTEN", "OH", "OIL", "OK", "OKAY", "OLD", "OLYMPIC", "ON", "ONCE", "ONE", "ONGOING", "ONION", "ONLINE", "ONLY", "ONTO", "OPEN", "OPENING", "OPERATE", "OPERATING", "OPERATION", "OPERATOR", "OPINION", "OPPONENT", "OPPORTUNITY", "OPPOSE", "OPPOSITE", "OPPOSITION", "OPTION", "OR", "ORANGE", "ORDER", "ORDINARY", "ORIGIN", "OTHER", "OUGHT", "OUR", "OURSELVES", "OUT", "OUTCOME", "OUTSIDE", "OVEN", "OVER", "OVERALL", "OVERCOME", "OVERLOOK", "OWE", "OWN", "OWNER", "ZEAXANTHIN", "ZIGZAGGERS", "ZIGZAGGERY", "ZIGZAGGING", "ZINCIFYING", "ZOMBIFYING", "ZOOMORPHIC", "ZYGOBRANCH", "ZYGODACTYL", "ZYGOMORPHY", "ZYGOMYCETE", "ZYGOPHYTES"]

abeceda = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
pojavljivanje_prvog_slova = ["AI", "AOEIUMBH", "AEOIUYHBCK", "AEOIUYSBF", "SEAOIUYH", "EAIOUSY", "EIAOUS",
                             "EIAOU", "EIAOU", "EIOAU", "EIOAD", "EIOAF", "IEOA", "IEO", "IEA", "IEH", "IER", "IEA", "IEA", "IE"]
pogodeno_prvo = False
duljina_rijeci = 0
trazena_rijec = ""


def optimalna_slova(prosljedena_rijec):
    global abeceda

    uredena_rijec = prosljedena_rijec.replace(" ", "")
    lista_rijeci = []
    slicne_rijeci = []
    potencijalna_slova = []

    for rijec in rijeci:
        if (len(rijec) == len(uredena_rijec)):
            lista_rijeci.append(rijec)
    
    index = 0

    for rijec in lista_rijeci:
        slicna = True

        for index in range(len(uredena_rijec)):
            if rijec[index] == uredena_rijec[index]:
                slicna &= True
            elif uredena_rijec[index] == "_":
                slicna &= True
            else:
                slicna &= False
                break

        if slicna == True:
            slicne_rijeci.append(rijec)

    for rijec in slicne_rijeci:
        for slovo in rijec:
            if slovo not in abeceda:
                rijec.replace(slovo, "")
            else:
                potencijalna_slova.append(slovo)

    pojavljivanje = 0
    slovo_za_vratiti = ""

    for slovo in potencijalna_slova:
        if potencijalna_slova.count(slovo) > pojavljivanje:
            pojavljivanje = potencijalna_slova.count(slovo)
            slovo_za_vratiti = slovo

    return slovo_za_vratiti


class Igrac(Agent):

    class Pokretanje(FSMBehaviour):
        async def on_start(self):
            print("Početak ponašanja igrača\n")

        async def on_end(self):
            print("Kraj ponašanja igrača\n")
            await self.agent.stop()

    class Povezivanje(State):
        async def run(self):

            msg = Message(to="hangman@localhost", body="",
                          metadata={"performative": "Request"})
            await self.send(msg)

            self.set_next_state("CekamIgru")

    class CekamIgru(State):
        async def run(self):

            global duljina_rijeci, trazena_rijec

            print("Čekam riječ\n")
            msg = await self.receive(timeout=30)

            if (msg.metadata['performative'] == 'Inform'):
                print("Riječ primljena\n")
                duljina_rijeci = int(msg.body)
                for i in range(duljina_rijeci):
                    trazena_rijec += "_ "
                self.set_next_state("Igraj")

            else:
                self.set_next_state("CekamIgru")

    class Igraj(State):
        async def run(self):

            global pogodeno_prvo, abeceda
            slovo = ""

            print("\nRiječ: " + trazena_rijec + "\n")

            if pogodeno_prvo == False:
                slovo = pojavljivanje_prvog_slova[duljina_rijeci-1][0]
                pojavljivanje_prvog_slova[duljina_rijeci-1] = pojavljivanje_prvog_slova[duljina_rijeci-1].replace(
                    slovo, "")
                abeceda = abeceda.replace(slovo, "")

                if (len(pojavljivanje_prvog_slova[duljina_rijeci-1]) <= 3):
                    pogodeno_prvo = True

            else:
         
                slovo = optimalna_slova(trazena_rijec)
                abeceda = abeceda.replace(slovo, "")

            print("Predlažem slovo " + slovo + "\n")
            msg = Message(to="hangman@localhost", body=slovo,
                          metadata={"performative": "Propose"})
            await self.send(msg)
            self.set_next_state("CekamOdgovor")

    class CekamOdgovor(State):
        async def run(self):

            global pogodeno_prvo, trazena_rijec
            msg = await self.receive(timeout=30)

            if msg.metadata['performative'] == 'Inform':

                if "Promašaj" in msg.body:
                    trazena_rijec = msg.body.split(",")[1]
                    self.set_next_state("Igraj")

                elif "Pogodak" in msg.body:
                    trazena_rijec = msg.body.split(",")[1]
                    self.set_next_state("Igraj")

                elif "Pogodak prvog" in msg.body:
                    trazena_rijec = msg.body.split(",")[1]
                    pogodeno_prvo = True
                    self.set_next_state("Igraj")

            elif msg.metadata['performative'] == 'Failure':
                self.set_next_state("Kraj")

            elif msg.metadata['performative'] == 'Confirm':
                self.set_next_state("Kraj")

            else:
                self.set_next_state("CekamOdgovor")

    class Kraj(State):
        async def run(self):
            print("Igra gotova\n")

    async def setup(self):

        fsm = self.Pokretanje()

        fsm.add_state(name="Povezivanje",
                      state=self.Povezivanje(), initial=True)
        fsm.add_state(name="CekamIgru", state=self.CekamIgru())
        fsm.add_state(name="Igraj", state=self.Igraj())
        fsm.add_state(name="CekamOdgovor", state=self.CekamOdgovor())
        fsm.add_state(name="Kraj", state=self.Kraj())

        fsm.add_transition(source="Povezivanje", dest="CekamIgru")
        fsm.add_transition(source="CekamIgru", dest="CekamIgru")
        fsm.add_transition(source="CekamIgru", dest="Igraj")
        fsm.add_transition(source="Igraj", dest="CekamOdgovor")
        fsm.add_transition(source="CekamOdgovor", dest="Igraj")
        fsm.add_transition(source="CekamOdgovor", dest="Kraj")

        self.add_behaviour(fsm)


if __name__ == '__main__':

    igrac = Igrac("igrac@localhost", "igrac")

    igrac_obj = igrac.start()
    igrac_obj.result()

    while igrac.is_alive():
        try:
            t.sleep(1)
        except KeyboardInterrupt:
            print("\nGasim!\n")
            break

    igrac.stop()

    quit_spade()
