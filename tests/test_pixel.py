from seneca.tooling import *
from decimal import Decimal
from unittest import TestCase, main
import seneca, os

path = os.path.abspath('../contracts')
wallet = '324ee2e3544a8853a3c5a0ef0946b929aa488cbe7e7ee31a0fef9585ce398502'

class TestPixel(TestCase):
	def setUp(self):
		default_driver.r.flushdb()
		for contract in ['tau', 'pixel']:
			with open('{}/{}.sen.py'.format(path, contract)) as f:
				default_driver.publish_code_str(fullname=contract, author='stu', code_str=f.read())

		self.pixel = ContractWrapper(contract_name='pixel', driver=default_driver, default_sender='stu')
		self.tau = ContractWrapper(contract_name='tau', driver=default_driver, default_sender='stu')

	def test_coor_str(self):
		res = self.pixel.coor_str(x=1, y=0)
		self.assertEqual(res['output'], '1,0')

	def test_buy_pixel(self):
		res = self.pixel.buy_pixel(x=0, y=0, r=255, g=255, b=0, new_price=1000)
		self.assertEqual(res['status'], 'success')
		self.assertTrue(default_driver.r.exists('tau:balances:stu'))
		self.assertTrue(default_driver.r.exists('pixel:colors:0,0'))

	def test_buy_pixel(self):
		self.pixel.buy_pixel(x=0, y=0, r=255, g=255, b=0, new_price=1000)
		self.tau.add_to_custodial(to='pixel', amount=100000, sender=wallet)
		self.pixel.buy_pixel(x=0, y=0, r=255, g=255, b=0, new_price=10000, sender=wallet)

		davis_custodial = self.tau.get_custodial(owner=wallet, spender='pixel')['output']
		davis_balance = self.tau.get_balance(account=wallet)['output']

		self.assertEqual(davis_custodial, Decimal('100000') - Decimal('1000'))
		self.assertEqual(davis_balance, Decimal('900000'))

	def test_bad_buy_pixel(self):
		self.pixel.buy_pixel(x=0, y=0, r=255, g=255, b=0, new_price=1000000000)
		with self.assertRaises(AssertionError):
			self.pixel.buy_pixel(x=0, y=0, r=255, g=255, b=0, new_price=10000, sender=wallet)

	def test_buy_out_of_bounds_pixel(self):
		with self.assertRaises(AssertionError):
			self.pixel.buy_pixel(x=999, y=999, r=255, g=255, b=0, new_price=1000000000)

	def test_buy_out_of_bounds_pixel_negative(self):
		with self.assertRaises(AssertionError):
			self.pixel.buy_pixel(x=-999, y=-999, r=255, g=255, b=0, new_price=1000000000)

	def test_price_pixel(self):
		self.pixel.buy_pixel(x=0, y=0, r=255, g=255, b=0, new_price=1000)
		self.pixel.price_pixel(x=0, y=0, new_price=1234)

		self.assertEqual(self.pixel.price_of_pixel(x=0, y=0)['output'], Decimal('1234'))

	def test_price_pixel_not_owned_fails(self):
		with self.assertRaises(AssertionError):
			self.pixel.price_pixel(x=0, y=0, new_price=1234)

if __name__ == "__main__":
	main()
