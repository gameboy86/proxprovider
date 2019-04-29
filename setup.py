from setuptools import setup, find_packages

setup(
    name='proxprovider',
    version='0.1',
    description='Manage many proxy providers from one place',
    url='https://github.com/gameboy86/proxprovider',
    author='Maciej Gębarski',
    author_email='mgebarski@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
