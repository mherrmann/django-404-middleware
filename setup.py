"""An alternative to Django's BrokenLinkEmailsMiddleware

See:
https://github.com/mherrmann/django-404-middleware
"""

from setuptools import setup, find_packages

description = "An alternative to Django's BrokenLinkEmailsMiddleware"
url = 'https://github.com/mherrmann/django-404-middleware'
setup(
    name='django-404-middleware',
    version='0.0.1',
    description=description,
    long_description=description + '\n\nHome page: ' + url,
    author='Michael Herrmann',
    author_email='michael+removethisifyouarehuman@herrmann.io',
    url=url,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
    
        'License :: OSI Approved :: MIT License',
    
        'Operating System :: OS Independent',
    
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Framework :: Django',

        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    license='MIT',
    keywords='Django 404 Middleware Email',
    platforms=['MacOS', 'Windows', 'Debian', 'Fedora', 'CentOS', 'Arch'],
    test_suite='django_404_middleware.tests'
)