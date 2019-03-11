import re

def match(pattern, path, exact=True, is_re=False, case_sensitive=False):
	"""
	The main motivation for keeping this function in a separate Python module,
	and not eg. as a method of Ignorable404Url, is so we can test it without any
	dependencies on Django (and in particular without having to initialize
	Django's settings just for a simple unit test).
	"""
	regex = pattern if is_re else re.escape(pattern)
	if exact:
		regex = '^%s/?$' % regex
	flags = 0 if case_sensitive else re.I
	return re.search(regex, path, flags)