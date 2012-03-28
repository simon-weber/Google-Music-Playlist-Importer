from distutils.core import setup

setup(
    name='Google-Music-Playlist-Importer',
    version='2012.03.28',
    author='Simon Weber',
    author_email='simon@simonmweber.com',
    url='https://github.com/simon-weber/Google-Music-Playlist-Importer',
    packages=[],
    scripts=['gm_playlist_importer.py'],
    license='GPLv3',
    description='A Python script to import local playlists to Google Music.',
    long_description="""\
A local list of song metadata will be matched against already-uploaded songs in Google Music. This is most useful for people who keep their music library organized.
""",
    install_requires = [
        "gmusicapi == 2012.03.27",
        "chardet"],
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio",
        ]
)
