from setuptools import setup

setup(
    name='stock-bot',
    version='0.1.0',    
    description='Discord bot for monitoring stock positions',
    url='https://github.com/ericqian1/stock-bot.git',
    author='Eric Qian',
    author_email='tianze1995@yahoo.com',
    license='MIT',
    packages=['discord.py', 'yfinance'],
    install_requires=[],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
    ],
)
