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
    download_url="https://github.com/PolarPayne/scrycli/archive/{}.tar.gz".format(VERSION),
    license="MIT",
    entry_points={
          'console_scripts': [
              'scrycli = scrycli.__main__:main'
          ]
      },
    keywords=["mtg", "tcg", "api", "scryfall"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.6",
    ]
)
