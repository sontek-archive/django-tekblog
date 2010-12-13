try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='django-tekblog',
    version=__import__('tekblog').__version__,
    description='A django blog engine',
    long_description='',
    author='John Anderson',
    author_email='sontek@gmail.com',
    url='http://github.com/sontek/django-tekblog',
    download_url='http://github.com/sontek/django-tekblog',
    license='BSD',
    packages=['tekblog'],
    classifiers=[
            'Framework :: Django',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
    ],
)
