''':module: ytmusicscripts
:author: Willow Ciesialka
:date: 2023-04-19
'''

from ytmusicapi import YTMusic

__version__ = "1.0.0"
__author__ = "Willow Ciesialka"

# Sign-in procedure
print("Signing in...", end=' ', flush=True)
print('\033[92mDONE!', end='\033[0m\n')
ytmusic = YTMusic("oauth.json")
