from setuptools import setup, find_packages

requires = [
    "Flask",
    "Flask-SQLAlchemy",
    "Flask-WTF",
    "pytest",
    "python-dotenv",
    "requests",
]


setup(
    name="Gastos-dos-Politicos",
    version="0.1",
    description="Gastos dos políticos brasileiros.",
    author="Thiago J. Barbalho",
    license='GNU General Public License v3',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
)
