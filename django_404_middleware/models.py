from django.db.models import Model, TextField, BooleanField
from django_404_middleware.match import match

class Ignorable404Url(Model):

	class Meta:
		verbose_name = 'Ignorable 404 URL'

	pattern = TextField(help_text='URLs matching this pattern are ignored.')
	exact = BooleanField(
		verbose_name='The full URL must match', blank=False, default=True
	)
	is_re = BooleanField(
		verbose_name='Is regular expression', blank=False, default=False
	)
	case_sensitive = BooleanField(
		verbose_name='Is case sensitive', blank=False, default=False
	)

	def matches(self, path):
		return bool(match(
			self.pattern, path, self.exact, self.is_re, self.case_sensitive
		))

	def __str__(self):
		return self.pattern

class Ignorable404Referer(Model):

	class Meta:
		verbose_name = 'Ignorable 404 Referer'

	pattern = TextField(help_text='Referers matching this pattern are ignored.')
	exact = BooleanField(
		verbose_name='The full referer must match', blank=False, default=True
	)
	is_re = BooleanField(
		verbose_name='Is regular expression', blank=False, default=False
	)
	case_sensitive = BooleanField(
		verbose_name='Is case sensitive', blank=False, default=False
	)

	def matches(self, path):
		return bool(match(
			self.pattern, path, self.exact, self.is_re, self.case_sensitive
		))

	def __str__(self):
		return self.pattern