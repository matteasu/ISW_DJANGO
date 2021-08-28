from django.test import TestCase, Client
import unittest
from django.urls import reverse
from account.models import Account
from struttureGioco.models import Inventario, Boss, Personaggio, Equipaggiamento
from struttureGioco.funzioni import combattiBoss, modificaEquip, sceltaDrop
from django.core.exceptions import EmptyResultSet


# Create your tests here.
class StruttureGiocoTest(TestCase):

	def setUp(self):
		self.boss = Boss(nome = "Bossss", luogo = "Milano Marittima", abilitato = True, vita = 120, vitalita = 2,
		                 forza = 120)
		self.boss.save()
		self.account = Account.objects.create_user(playerID = 'Nino Nino', password = 'Paramedico234')
		self.p = Personaggio(nome = self.account.playerID)
		self.p.save()
		self.account.personaggio = self.p
		self.account.save()
		
		self.admin = Account.objects.create_superuser(playerID = "dev", password = "dev23456789")
		
		self.equipaggiamento1 = Equipaggiamento(nome = "Lama Lama Lama", tipo = 'P')
		self.equipaggiamento2 = Equipaggiamento(nome = "Col Tel Lo", tipo = 'S')
		self.equipaggiamento3 = Equipaggiamento(nome = "pugnale", tipo = 'S', vitalita = 4, forza = 5)
		self.client = Client()
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

	def test_bossExists(self):
		self.assertEqual(len(Boss.objects.filter(nome = self.boss.nome)), 1)

	def test_bossHasEquip(self):
		self.equipaggiamento1.boss = self.boss
		self.equipaggiamento1.save()
		self.assertEqual(Equipaggiamento.objects.get(nome = self.equipaggiamento1.nome).boss.nome, self.boss.nome)

	def test_combattimento_boss_winner(self):
		self.assertFalse(combattiBoss(user = self.account, boss = self.boss))

	def test_combattimento_player_winner(self):
		self.p.vita = 400
		self.p.forza = 450
		self.p.save()
		self.assertTrue(combattiBoss(user = self.account, boss = self.boss))

	def test_modifica_equip_item_not_in_zaino(self):
		with self.assertRaisesMessage(ValueError, "Equipaggiamento non presente all'interno dello zaino"):
			modificaEquip(self.account, self.equipaggiamento2.id)

	def test_modifica_equip_item_not_in_db(self):
		self.assertRaises(Equipaggiamento.DoesNotExist, modificaEquip, user = self.account, itemID = 40)

	def test_drop_appartente_a_boss(self):
		self.equipaggiamento1.boss = self.boss
		self.equipaggiamento2.boss = self.boss

		self.equipaggiamento1.save()
		self.equipaggiamento2.save()

		drop = sceltaDrop(self.boss)

		self.assertIn(drop, Equipaggiamento.objects.filter(boss = self.boss))
		#test view
		self.client.login(playerID = self.account.playerID, password = 'Paramedico234')
		response = self.client.get(reverse('dettaglioBoss', args = [self.boss.luogo]))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, drop.nome)

	def test_drop_non_appartente_a_boss(self):
		self.equipaggiamento1.boss = self.boss
		self.equipaggiamento2.boss = self.boss

		self.equipaggiamento1.save()
		self.equipaggiamento2.save()

		drop = sceltaDrop(self.boss)

		self.assertNotIn(self.equipaggiamento3, Equipaggiamento.objects.filter(boss = self.boss))
		#test view
		self.client.login(playerID = self.account.playerID, password = 'Paramedico234')
		response = self.client.get(reverse('dettaglioBoss', args = [self.boss.luogo]))
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, self.equipaggiamento3.nome)

	def test_drop_no_items(self):
		self.boss1 = Boss(nome = "prova", luogo = "milano", abilitato = True)
		self.boss1.save()
		
		#test view
		self.client.login(playerID = self.account.playerID, password = "Paramedico234")
		response = self.client.get(reverse('dettaglioBoss', args = [self.boss1.luogo]))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "NESSUN DROP. QUALCHE ADMIN NON HA FATTO IL PROPRIO DOVERE...")
		
		self.assertRaises(EmptyResultSet, sceltaDrop, boss = self.boss1)

	def test_modifica_equip_utente(self):
		expectedVitalita = self.equipaggiamento3.vitalita + self.account.personaggio.vitalita
		expectedForza = self.equipaggiamento3.forza + self.account.personaggio.forza
		self.account.personaggio.zaino.add(self.equipaggiamento3)
		self.account.personaggio.save()
		modificaEquip(self.account, self.equipaggiamento3.id)
		self.account.personaggio.save()
		self.assertEqual(self.account.personaggio.vitalita, expectedVitalita)
		self.assertEqual(self.account.personaggio.forza, expectedForza)
		self.assertIn(self.equipaggiamento3, self.account.personaggio.zaino.all())
		
		#test view
		self.client.login(playerID = self.account.playerID, password = 'Paramedico234')
		response = self.client.get(reverse('inventario'))
		self.assertEqual(response.status_code, 200)
		if self.equipaggiamento3.tipo == "P":
			self.assertContains(response, "PRIMARIA - " + self.equipaggiamento3.nome)
		elif self.equipaggiamento3.tipo == "S":
			self.assertContains(response, "SECONDARIA - " + self.equipaggiamento3.nome)
		else:
			self.assertContains(response, "ARMATURA - " + self.equipaggiamento3.nome)


	def test_modifica_boss(self):
		expectedVita = 30
		expectedAbilitato = True
		expectedNome = "Billie Bossa Nova"
		self.boss.vita = 30
		self.boss.abilitato = True
		self.boss.nome = "Billie Bossa Nova"
		self.boss.save()
		self.assertEqual(Boss.objects.get(nome = self.boss.nome).nome, expectedNome)
		self.assertEqual(Boss.objects.get(nome = self.boss.nome).vita, expectedVita)
		self.assertEqual(Boss.objects.get(nome = self.boss.nome).abilitato, expectedAbilitato)
		
		#test view
		self.client.login(playerID = self.account.playerID, password = "Paramedico234")
		response = self.client.get(reverse('dettaglioBoss', args = [self.boss.luogo]))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "VITA " + str(self.boss.vita * self.boss.vitalita))
		self.assertContains(response, self.boss.nome)

	def test_aggiunta_boss(self):
		nuovoBoss = Boss(nome = "Nuovo Boss", luogo = "Postiano", abilitato = True, vita = 120, vitalita = 2)
		nuovoBoss.save()

		expectedNome = "Nuovo Boss"
		expectedLuogo = "Postiano"
		expectedAbilitato = True
		expectedVita = 120
		expectedVitalita = 2

		self.assertEqual(Boss.objects.get(nome = nuovoBoss.nome).nome, expectedNome)
		self.assertEqual(Boss.objects.get(nome = nuovoBoss.nome).luogo, expectedLuogo)
		self.assertEqual(Boss.objects.get(nome = nuovoBoss.nome).abilitato, expectedAbilitato)
		self.assertEqual(Boss.objects.get(nome = nuovoBoss.nome).vita, expectedVita)
		self.assertEqual(Boss.objects.get(nome = nuovoBoss.nome).vitalita, expectedVitalita)
		#test view
		self.client.login(playerID = self.account.playerID, password = "Paramedico234")
		response = self.client.get(reverse('luoghi'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Postiano")

	def test_modifica_equip(self):
		self.equipaggiamento1.forza = 500
		self.equipaggiamento1.intelligenza = 30
		self.equipaggiamento1.save()

		expectedForza = 500
		expectedIntelligenza = 30

		self.assertEqual(Equipaggiamento.objects.get(pk = self.equipaggiamento1.id).forza, expectedForza)
		self.assertEqual(Equipaggiamento.objects.get(pk = self.equipaggiamento1.id).intelligenza, expectedIntelligenza)
		#test view
		self.client.login(playerID = self.admin.playerID, password = "dev23456789")
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "FRZ 500")
		self.assertContains(response, "INT 30")

	def test_battaglia(self):
		self.account.personaggio.vita = 400
		self.account.personaggio.forza = 450
		self.account.personaggio.save()

		self.equipaggiamento3.boss = self.boss
		self.equipaggiamento3.save()
		item = sceltaDrop(self.boss)

		if combattiBoss(self.account, self.boss):
			self.account.personaggio.zaino.add(item)
			self.account.personaggio.save()
			self.assertIn(item, self.account.personaggio.zaino.all())
		else:
			self.assertNotIn(item, self.account.personaggio.zaino.all())

	def test_aggiunta_equip(self):
		eq = Equipaggiamento(nome = "arma cattiva", tipo = 'P', vitalita = 4, forza = 5)
		eq.save()
		expectedNome = "arma cattiva"
		expectedTipo = "P"
		expectedVitalita = 4
		expectedForza = 5
		self.assertEqual(Equipaggiamento.objects.get(nome = eq.nome).nome, expectedNome)
		self.assertEqual(Equipaggiamento.objects.get(nome = eq.nome).tipo, expectedTipo)
		self.assertEqual(Equipaggiamento.objects.get(nome = eq.nome).vitalita, expectedVitalita)
		self.assertEqual(Equipaggiamento.objects.get(nome = eq.nome).forza, expectedForza)
		#test view
		self.client.login(playerID = self.admin.playerID, password = "dev23456789")
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, eq.nome)

	def test_personaggio_has_no_equip(self):
		accountTest = Account.objects.create_user(playerID = 'NinoSenzaEquip', password = 'Paramedico234')
		personaggio = Personaggio(nome = accountTest.playerID)
		personaggio.save()
		accountTest.personaggio = personaggio
		accountTest.save()
		self.client.login(playerID = accountTest.playerID, password = "Paramedico234")
		response = self.client.get(reverse('inventario'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Inventario Vuoto")


if __name__ == "__main__":
	unittest.main()
