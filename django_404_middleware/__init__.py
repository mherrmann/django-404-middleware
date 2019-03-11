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
				subject = self._get_email_subject(domain, referer)
				message = self._get_email_message(request, path, referer)
				mail_managers(subject, message, fail_silently=True)
		return response

	def _get_email_subject(self, domain, referer):
		result = 'Broken '
		if self.is_internal_request(domain, referer):
			result += 'INTERNAL '
		result += 'link on ' + domain
		return result

	def _get_email_message(self, request, path, referer):
		user_agent = force_text(
			request.META.get('HTTP_USER_AGENT', '<none>'), errors='replace'
		)
		ip = request.META.get('REMOTE_ADDR', '<none>')
		result = 'Referrer: %s\n' % referer
		result += 'Requested URL: %s\n' % path
		result += 'User agent: %s\n' % user_agent
		result += 'IP address: %s' % ip

		admin_url = reverse('admin:django_404_middleware_ignorable404url_add')+\
				   '?' + urlencode({'pattern': path})
		result += '\n\nTo ignore this link, visit %s.' % \
				   request.build_absolute_uri(admin_url)
		return result

	def is_ignorable_request(self, request, uri, domain, referer):
		if super().is_ignorable_request(request, uri, domain, referer):
			return True
		# If we import this at module level, we get exception
		# AppRegistryNotReady when starting Django. So import it late, here:
		from .models import Ignorable404Url
		return any(i.matches(uri) for i in Ignorable404Url.objects.all())