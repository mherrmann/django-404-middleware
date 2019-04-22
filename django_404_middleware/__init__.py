from django.conf import settings
from django.core.mail import mail_managers
from django.middleware.common import BrokenLinkEmailsMiddleware
from django.utils.encoding import force_text
from urllib.parse import urlencode

try:
	from django.urls import reverse
except ImportError:
	# Django < 2:
	from django.core.urlresolvers import reverse

class BrokenLinkEmailsDbMiddleware(BrokenLinkEmailsMiddleware):

	def process_response(self, request, response):
		"""
		Send broken link emails for relevant 404 NOT FOUND responses.
		"""
		if response.status_code == 404 and not settings.DEBUG:
			domain = request.get_host()
			path = request.get_full_path()
			referer = force_text(
				request.META.get('HTTP_REFERER', ''), errors='replace'
			)
			if not self.is_ignorable_request(request, path, domain, referer):
				_notify_managers_of_broken_link(request, path, domain, referer)
		return response

	def is_ignorable_request(self, request, uri, domain, referer):
		if super().is_ignorable_request(request, uri, domain, referer):
			return True
		Ignorable404Url, Ignorable404Referer = _import_models()
		if any(i.matches(referer) for i in Ignorable404Referer.objects.all()):
			return True
		return any(i.matches(uri) for i in Ignorable404Url.objects.all())

def _notify_managers_of_broken_link(request, path, domain, referer):
	subject = _get_email_subject(domain, referer)
	message = _get_email_message(request, path, referer)
	mail_managers(subject, message, fail_silently=True)

def _get_email_subject(domain, referer):
	result = 'Broken '
	if BrokenLinkEmailsMiddleware.is_internal_request(None, domain, referer):
		result += 'INTERNAL '
	result += 'link on ' + domain
	return result

def _get_email_message(request, path, referer):
	user_agent = force_text(
		request.META.get('HTTP_USER_AGENT', '<none>'), errors='replace'
	)
	ip = request.META.get('REMOTE_ADDR', '<none>')
	result = 'Referrer: %s\n' % referer
	result += 'Requested URL: %s\n' % path
	result += 'User agent: %s\n' % user_agent
	result += 'IP address: %s' % ip

	Ignorable404Url, Ignorable404Referer = _import_models()
	result += '\n\nTo ignore this link, visit %s.' % \
			  _get_admin_add_url(request, Ignorable404Url, pattern=path)
	result += '\n\nTo ignore all links from this referer, visit %s.' % \
			  _get_admin_add_url(request, Ignorable404Referer, pattern=referer)
	return result

def _get_admin_add_url(request, model, **defaults):
	return request.build_absolute_uri(
		reverse('admin:%s_%s_add' % (__name__, model.__name__.lower()))
		+ '?' + urlencode(defaults)
	)

def _import_models():
	# If we import the models at module level, we get exception
	# AppRegistryNotReady when starting Django. So import them late, here:
	from .models import Ignorable404Url, Ignorable404Referer
	return Ignorable404Url, Ignorable404Referer