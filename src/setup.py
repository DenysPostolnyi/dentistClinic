from setuptools import setup

with open('../requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='dentistClinic',
    version='1.0',
    description='Application for dentist clinic',
    # packages=find_packages(where='models', exclude='tests'),
    packages=['models'],
    author='Denys Postolnyi',
    author_email='poostlden44@gmail.com',
    include_package_data=True,
    # zip_safe=False,
    install_requires=requirements
)

