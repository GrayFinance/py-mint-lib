from setuptools import setup

with open("./requirements.txt", 'r') as file:
    requires_depend = file.read().split()

setup(
    name='mintlib',
    py_modules=['mintlib'],
    install_requires=requires_depend
)
