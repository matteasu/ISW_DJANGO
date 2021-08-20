import random

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

def combattiBoss(user, boss):
    win = False

    # Str - attacco
    # Dex - chance critico dex% di fare X2 danno
    # Int - chance diminuzione difesa nemica
    # Tem - dininuzione attacco nemico (resistenza)

    vitapg = user.personaggio.vita * user.personaggio.vitalita
    vitaboss = boss.vita * boss.vitalita

    print(vitaboss, vitapg, user.personaggio.nome)

    while vitapg > 0 and vitaboss > 0:
        # Turno PG
        atk = user.personaggio.forza

        if user.personaggio.destrezza >= 100:
            atk *= 2
        elif random.randint(1, 100) <= user.personaggio.destrezza:
            atk *= 2

        if user.personaggio.intelligenza >= 100:
            danni = atk
        elif random.randint(1, 100) <= user.personaggio.intelligenza:
            danni = atk
        else:
            danni = atk - boss.tempra

        if danni <= 0:
            danni = 50

        vitaboss -= danni

        #Turno Boss
        atk = boss.forza

        if boss.destrezza >= 100:
            atk *= 2
        elif random.randint(1, 100) <= boss.destrezza:
            atk *= 2

        if boss.intelligenza >= 100:
            danni = atk
        elif random.randint(1, 100) <= boss.intelligenza:
            danni = atk
        else:
            danni = atk - user.personaggio.tempra

        if danni <= 0:
            danni = 5

        vitapg -= danni

    if vitapg > vitaboss:
        win = True
    else:
        win = False

    print(vitaboss, vitapg)

    return win