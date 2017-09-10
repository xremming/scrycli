from distutils.core import setup

from scrycli import __version__


setup(
    name="scrycli",
    packages=["scrycli"],
    version=__version__,
    description="CLI to Scryfall",
    author="Maximilian Remming",
    author_email="maxremming@gmail.com",
    url="https://github.com/PolarPayne/scrycli",
    download_url="https://github.com/PolarPayne/scrycli/archive/{}.tar.gz".format(__version__),
    license="MIT",
    install_requires=[
        "requests==2.18.4"
    ],
    entry_points={
          'console_scripts': [
              'scrycli = scrycli.__main__:main'
          ]
      },
    keywords=["mtg", "tcg", "api", "scryfall"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ]
)
