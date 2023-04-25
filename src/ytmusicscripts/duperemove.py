#!/usr/bin/env python3
''':module: duperemove
This module is responsible for the duperemove feature.
It will scan your "liked music" playlist and remove all duplicates.

:author: Willow Ciesialka
:date: 2023-04-19
'''

from ytmusicscripts import ytmusic
from typing import List, Tuple, Dict


def _string_compare(str_1: str, str_2: str) -> float:
    '''Compare two strings of indeterminant length and
    return the similarity score between them.
    @TODO Use a different similarity score algorithm.

    :param str_1: First string to compare.
    :type str_1: str
    :param str_2: Second string to compare.
    :type str_2: str
    :return: The similarity score between them.
    :rtype: float
    '''
    if str_1 == str_2:
        return 1.0

    # Make sure str_1 is always the shorter string
    # (if they are different lengths)
    if len(str_1) > len(str_2):
        str_1, str_2 = str_2, str_1

    min_length: int = len(str_1)
    max_length: int = len(str_2)

    matches = 0
    for i, char in enumerate(str_1):
        if char == str_1[i]:
            matches += 1
    return matches / max_length

def _compare_tracks(track_1: Tuple[str, str, str],
                    track_2: Tuple[str, str, str]) -> float:
    '''Compare two tracks and return their similarity score.

    :param track_1: First track to compare.
    :type track_1: Tuple[str, str, str]
    :param track_2: Second track to compare.
    :type track_2: Tuple[str, str, str]
    :return: Similarity score. If the artists are different, this will be zero.
    :rtype: float
    '''
    title_1: str = track_1[0].casefold()
    artist_1: str = track_1[1].casefold()
    title_2: str = track_2[0].casefold()
    artist_2: str = track_2[1].casefold()

    if _string_compare(artist_1, artist_2) < 0.9:
        return 0
    return _string_compare(title_1, title_2)


def _find_duplicates(tracks: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
    '''Find duplicates in a list of tracks.

    :param tracks: List of tracks to find duplicates in.
    :type tracks: List[Tuple[str, str, str]]
    :return: List of duplicates.
    :rtype: List[Tuple[str, str, str]]
    '''
    cleared: List[Tuple[str, str, str]] = []
    dupes: List[Tuple[str, str, str]] = []
    for track in tracks:
        duplicate: bool = False
        for check in cleared:
            similarity: float = _compare_tracks(track, check)
            if similarity >= 0.9:
                dupes.append(track)
                duplicate = True
                print('\033[31mDupe found: \033[91m', track, '\033[0mconflicts with\033[92m', check, end='\033[0m\n')
            elif similarity >= 0.75:
                print("\033[33mPossible dupe found: \033[93m", track, '\033[0mmay conflict with\033[92m', check, f"\033[93m({similarity*100:.1f}%)", end='\033[0m\n')
        if not duplicate:
            cleared.append(track)
    return dupes


def main():
    # Generate list of tracks
    print("Getting liked tracks...", end=' ', flush=True)
    playlist: Dict = ytmusic.get_playlist('LM', limit=None)
    tracks: List[Tuple[str, str, str]] = [
        (
            track.get('title'),
            track.get('artists')[0].get('name'),
            track.get('videoId')
        ) for track in playlist.get('tracks')]
    print('\033[92mDONE!', end='\033[0m\n')

    # Find duplicates
    print("Finding duplicates...")
    dupes: List[Tuple[str, str, str]] = _find_duplicates(tracks)
    print('\033[92mDONE!', end='\033[0m\n')

    # Rate and remove from playlist
    print("Unliking Duplicates...", end=' ', flush=True)
    for dupe in dupes:
        ytmusic.rate_song(dupe[2], rating='INDIFFERENT')
    print('\033[92mDONE!', end='\033[0m\n')
    print('\033[92mProcess Complete!',
          '\033[0m(Changes may take a while to reflect)', end='\033[0m\n')


if __name__ == "__main__":
    main()
