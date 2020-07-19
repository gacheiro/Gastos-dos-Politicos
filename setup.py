from setuptools import setup, find_packages

import gastos_politicos

setup(
    name="Gastos-dos-Politicos",
    version=gastos_politicos.__version__,
    description="Gastos dos políticos brasileiros.",
    author="Thiago J. Barbalho",
    license='GNU General Public License v3',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Flask>=1.1.2",
        "Flask-SQLAlchemy>=2.4.3",
        "Flask-WTF>=0.4.13",
        "pytest>=5.4.3",
        "python-dotenv>=0.13.0",
        "requests>=2.24.0",
    ],
)
