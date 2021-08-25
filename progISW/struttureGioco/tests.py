from django.test import TestCase
import unittest
from account.models import Account
from struttureGioco.models import Inventario, Boss, Personaggio, Equipaggiamento
from struttureGioco.funzioni import combattiBoss, modificaEquip, sceltaDrop
from django.core.exceptions import EmptyResultSet


# Create your tests here.
class StruttureGiocoTest(TestCase):

	def setUp(self):
		self.boss = Boss(nome="Bossss", luogo="Milano Marittima", abilitato=True, vita=120, vitalita=2, forza=120)
		self.boss.save()
		self.account = Account.objects.create_user(playerID='Riccardo', password='Fallito234')
		self.p = Personaggio(nome=self.account.playerID)
		self.p.save()
		self.account.personaggio = self.p
		self.account.save()
		self.equipaggiamento1 = Equipaggiamento(nome="Lama Lama Lama", tipo='P')
		self.equipaggiamento2 = Equipaggiamento(nome="Col Tel Lo", tipo='S')


		self.equipaggiamento1.save()
		self.equipaggiamento2.save()

		self.account.personaggio.zaino.add(self.equipaggiamento1)
		self.account.personaggio.save()

	def test_personaggioExists(self):
		self.assertEqual(len(Personaggio.objects.filter(nome=self.account.playerID)), 1)

	def test_accountHasPersonaggio(self):
		self.assertEqual(Account.objects.get(playerID=self.account.playerID).personaggio, self.p)

	def test_personaggioHasOneEquip(self):
		self.assertEqual(len(Account.objects.get(playerID=self.account.playerID).personaggio.zaino.all()), 1)

	def test_bossExists(self):
		self.assertEqual(len(Boss.objects.filter(nome=self.boss.nome)), 1)

	def test_bossHasEquip(self):
		self.equipaggiamento1.boss = self.boss
		self.equipaggiamento1.save()
		self.assertEqual(Equipaggiamento.objects.get(nome=self.equipaggiamento1.nome).boss.nome, self.boss.nome)

	def test_combattimento_boss_winner(self):
		self.assertFalse(combattiBoss(user=self.account, boss=self.boss))

	def test_combattimento_player_winner(self):
		self.p.vita = 400
		self.p.forza = 450
		self.p.save()
		self.assertTrue(combattiBoss(user=self.account, boss=self.boss))

	def test_modifica_equip_item_not_in_zaino(self):
		with self.assertRaisesMessage(ValueError, "Equipaggiamento non presente all'interno dello zaino"):
			modificaEquip(self.account, self.equipaggiamento2.id)

	def test_modifica_equip_item_not_in_db(self):
		self.assertRaises(Equipaggiamento.DoesNotExist, modificaEquip, user=self.account, itemID=40)

	def test_drop_appartente_a_boss(self):
		self.equipaggiamento1.boss = self.boss
		self.equipaggiamento2.boss = self.boss

		self.equipaggiamento1.save()
		self.equipaggiamento2.save()

		drop = sceltaDrop(self.boss)

		self.assertIn(drop, Equipaggiamento.objects.filter(boss=self.boss))

	def test_drop_non_appartente_a_boss(self):
		self.equipaggiamento1.boss = self.boss
		self.equipaggiamento2.boss = self.boss

		self.equipaggiamento1.save()
		self.equipaggiamento2.save()

		self.equipaggiamento3 = Equipaggiamento(nome="Pug Na Le", tipo='S')
		self.equipaggiamento3.save()

		self.assertNotIn(self.equipaggiamento3, Equipaggiamento.objects.filter(boss=self.boss))

	def test_drop_no_items(self):
		self.boss1 = Boss(nome="prova", luogo="milano", abilitato=True)
		self.boss1.save()

		self.assertRaises(EmptyResultSet, sceltaDrop, boss=self.boss1)


if __name__ == "__main__":
	unittest.main()
