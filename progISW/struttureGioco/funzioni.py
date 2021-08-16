
def aggiungiStatistiche(user, equipaggiamento):
    user.personaggio.vitalita += equipaggiamento.vitalita
    user.personaggio.destrezza += equipaggiamento.destrezza
    user.personaggio.forza += equipaggiamento.forza
    user.personaggio.intelligenza += equipaggiamento.intelligenza
    user.personaggio.tempra += equipaggiamento.tempra

def rimuoviStatistiche (user, equipaggiamento):
    user.personaggio.vitalita -= equipaggiamento.vitalita
    user.personaggio.destrezza -= equipaggiamento.destrezza
    user.personaggio.forza -= equipaggiamento.forza
    user.personaggio.intelligenza -= equipaggiamento.intelligenza
    user.personaggio.tempra -= equipaggiamento.tempra