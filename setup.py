from setuptools import setup

requires = [
    'Flask',
    'Flask-SQLAlchemy',
    'gunicorn',
    'psycopg2-binary',
    'pytest',
    'python-dotenv',
    'requests',
]


setup(
    name='vcvaipagar',
    version='0.1',
    long_description=__doc__,
    packages=['app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
)
