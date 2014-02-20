from distutils.core import setup

setup(
    name='django-classy-mail',
    version='0.1.0',
    author='Alex Lovell-Troy',
    author_email='alex@lovelltroy.org',
    description='Class-Based Email for Django built with Mixins',
    packages=['classy_mail', 'classy_mail.mixins', 'classy_mail.migrations'],
    url='https://github.com/alexlovelltroy/django-classy-mail',
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    install_requires=[
        "Django >= 1.5",
        "markdown >= 2.4",
        "BeautifulSoup >= 3.2",
        "South >= 0.8",
        "PyYAML >= 3.10",
    ],
)
