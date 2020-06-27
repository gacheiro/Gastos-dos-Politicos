from setuptools import setup, find_packages

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
    name='Gastos-Politicos',
    version='0.1',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
)
