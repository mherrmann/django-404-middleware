from unittest import TestCase
from .match import match

class MatchTest(TestCase):
	def test_exact(self):
		self.assertTrue(match('/nonexistent', '/nonexistent'))
		self.assertFalse(match('/nonexistent', '/other-pattern'))
	def test_regex(self):
		self.assertTrue(match('/[0-9]+', '/1234', is_re=True))
		self.assertFalse(match('/[0-9]+', '/abc', is_re=True))
	def test_inexact(self):
		self.assertTrue(match('substr', '/some/substr/in/path', exact=False))
		self.assertFalse(match('substr', '/some/substr/in/path'))
	def test_case_sensitive(self):
		self.assertTrue(match('/foo', '/Foo'))
		self.assertFalse(match('/foo', '/Foo', case_sensitive=True))
	def test_inexact_regex(self):
		self.assertFalse(match('[0-9]', '/hi/3/there', is_re=True))
		self.assertTrue(match('[0-9]', '/hi/3/there', is_re=True, exact=False))