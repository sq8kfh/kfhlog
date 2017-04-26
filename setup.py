import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'psycopg2',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'bcrypt',
    'hamtools',
    'docutils',
    'pyramid_rpc',
    'python-dateutil',
    'redis',
    'hamutils',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
]

setup(
    name='kfhlog',
    version='0.0.0',
    description='Amateur radio logging program',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Pyramid',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Communications :: Ham Radio',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python',
    ],
    author='SQ8KFH',
    author_email='sq8kfh@gmail.com',
    url='https://github.com/sq8kfh/kfhlog',
    keywords='web pyramid pylons ham',
    packages=find_packages(),
    python_requires='>=3.4',
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = kfhlog:main',
        ],
        'console_scripts': [
            'initialize_kfhlog_db = kfhlog.scripts.initializedb:main',
            'load_country_files = kfhlog.scripts.loadcountryfiles:main',
        ],
    },
)
