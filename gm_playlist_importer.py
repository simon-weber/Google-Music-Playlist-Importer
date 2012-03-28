#!/home/simon/programming/python/Google-Music-Playlist-Importer/test/bin/python

"""Python script to import local playlists to Google Music."""


import re
import sys
import codecs
from getpass import getpass

import chardet
import gmusicapi.gmtools.tools as gm_tools
from gmusicapi.api import Api


def init(max_attempts=3):
    """Makes an instance of the api and attempts to login with it.
    Returns the api after at most max_attempts.
    
    :param max_attempts:
    """

    api = Api()
    
    logged_in = False
    attempts = 0

    print "Log in to Google Music."

    while not logged_in and attempts < max_attempts:
        email = raw_input("Email: ")
        password = getpass()

        logged_in = api.login(email, password)
        attempts += 1

    return api


def guess_encoding(filename):
    """Returns a tuple of (guessed encoding, confidence).
    
    :param filename:
    """

    res = chardet.detect(open(filename).read())
    return (res['encoding'], res['confidence'])


def main():
    
    if not len(sys.argv) == 2:
        print "usage:", sys.argv[0], "<playlist file>"
        sys.exit(0)

    #The three md_ lists define the format of the playlist and how matching should be done against the library.
    #They must all have the same number of elements.

    #Where this pattern matches, a query will be formed from the captures.
    #My example matches against a playlist file with lines like:
    # /home/simon/music/library/The Cat Empire/Live on Earth/The Car Song.mp3
    #Make sure it won't match lines that don't contain song info!
    md_pattern = r"^/home/simon/music/library/(.*)/(.*)/(.*)\..*$"

    #Identify what metadata each capture represents.
    #These need to be valid fields in the GM json - see protocol_info in the api repo.
    md_cap_types = ('artist', 'album', 'title')

    #The lower-better priority of the capture types above.
    #In this example, I order title first, then artist, then album.
    md_cap_pr = (2,3,1)


    #Build queries from the playlist.
    playlist_fname = sys.argv[1]
    pl_encoding, confidence = guess_encoding(playlist_fname)

    queries = None
    with codecs.open(playlist_fname, encoding=pl_encoding, mode='r') as f:
        queries = gm_tools.build_queries_from(f,
                                     re.compile(md_pattern), 
                                     md_cap_types, 
                                     md_cap_pr, 
                                     pl_encoding)

    api = init()

    if not api.is_authenticated():
        print "Failed to log in."
        sys.exit(0)
    
    print "Loading library from Google Music..."
    library = api.get_all_songs()

    print "Matching songs..."

    matcher = gm_tools.SongMatcher(library)
    
    matched_songs = matcher.match(queries)

    res = raw_input("Output matches to file or terminal? (f/t): ")

    if res == "t":
        print matcher.build_log()
    elif res == "f":
        res = raw_input("Filename to write to: ")
        with open(res, mode='w') as f:
            f.write(matcher.build_log())
        print "File written."
        


    go = raw_input("Create playlist from these matches? (y/n): ")
    if go == "y":
        name = raw_input("playlist name: ")
        p_id = api.create_playlist(name)['id']

        print "Made playlist", name

        
        res = api.add_songs_to_playlist(p_id, 
                                map(gm_tools.filter_song_md, matched_songs))
        print "Added songs."

if __name__ == '__main__':
    main()
