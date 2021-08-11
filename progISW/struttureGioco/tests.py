from django.test import TestCase
import unittest
from account.models import Account
from struttureGioco.models import Inventario, Boss, Personaggio, Equipaggiamento

# Create your tests here.
class StruttureGiocoTest(TestCase):

    def setUp(self):
        self.account = Account.objects.create_user(playerID='Riccardo', password='Fallito234')
        self.p = Personaggio(nome = self.account.playerID)
        self.p.save()
        self.account.personaggio = self.p
        self.account.save()
        self.equipaggiamento1 = Equipaggiamento(nome = "Lama Lama Lama", tipo = 'P')
        self.equipaggiamento2 = Equipaggiamento(nome = "Col Tel Lo", tipo = 'S')
        self.equipaggiamento3 = Equipaggiamento(nome = "Giacchetto", tipo = 'A')
        self.equipaggiamento1.save()
        self.equipaggiamento2.save()
        self.equipaggiamento3.save()
        self.account.personaggio.zaino.add(self.equipaggiamento1)
        self.account.personaggio.save()



    def test_personaggioExists(self):
        self.assertEqual(len(Personaggio.objects.filter(nome = self.account.playerID)), 1)


    def test_accountHasPersonaggio(self):
        self.assertEqual(Account.objects.get(playerID = self.account.playerID).personaggio, self.p)


    def test_personaggioHasOneEquip(self):
        self.assertEqual(len(Account.objects.get(playerID = self.account.playerID).personaggio.zaino.all()), 1)



if __name__ == "__main__":
	unittest.main()