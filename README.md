# Django 404 Middleware
Django's
[BrokenLinkEmailsMiddleware](https://docs.djangoproject.com/en/2.1/howto/error-reporting/#errors)
can email you about broken links on your site:

```
Broken link on mysite.com
=========================
Referrer: https://www.google.com
Requested URL: /nonexistent
User agent: Mozilla/5.0 (...)
IP address: 1.2.3.4
```

The problem is, these emails often contain false positives. To tell Django to
ignore particular broken links, you need to change the setting
`IGNORABLE_404_URLS`. This quickly becomes tedious.

This library is a drop-in replacement for `BrokenLinkEmailsMiddleware`. It sends
the same emails, but is configured via the database (and Django's Admin
interface) instead of a setting. This makes it much easier to mark URLs as
ignorable.

When a broken URL is encountered, this library adds a link to the bottom of the
404 email:

```
Broken link on mysite.com
=========================
...

To ignore this link, visit mysite.com/admin/...
```

Clicking on the link opens Django's Admin interface with a pre-filled form for
ignoring the 404:

![Add](Screenshot.png?raw=true "Optional Title")

Just click _Save_ no never be notified of this particular false positive again.

## Installation

Install this library via:

    pip install django-404-middleware

Add it to the `INSTALLED_APPS` in your Django settings file:

```
INSTALLED_APPS = [
    ...,
    'django_404_middleware'
]
```

Also add it to your `MIDDLEWARE` setting. Typically, you would already have an
entry `django.middleware.common.BrokenLinkEmailsMiddleware`. Replace it by the
following:

```
MIDDLEWARE = [
    ...,
    'django_404_middleware.BrokenLinkEmailsDbMiddleware',
    ...
]
```

(Note that if you are using Django < 2, the setting is called
`MIDDLEWARE_CLASSES`, not `MIDDLEWARE`.)

The same caveat as for Django's built-in 404 middleware applies:
`BrokenLinkEmailsDbMiddleware` must appear before other middleware that
intercepts 404 errors. Put it towards the top of your `MIDDLEWARE` setting.

Finally, apply migrations to initialise the database:

    python manage.py migrate

## Caveats

The current implementation is not optimized for performance in any way.