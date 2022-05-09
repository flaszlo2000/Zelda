## TODO
graphics_src is needed in the players.json

### usual)
- clean code, mypy

### p1) (doing)
- player reconstruct (and throw out old player.py)

### p2)
- trial ee listener
- enemies


### p3)
- fix animations  
- fix (or redo) fighting "system"
- keybindings for ui elements:
    - on menu
    - shortcuts (quicksave):
        - [x] exit
        - [] save
        - [] load
- full game save

### p4)
- sound
- additional ais

#

### additional content
0. interactable objects:
    - simple
    - placeable
    - milk (ee)
    - teapot (ee)
1. settings tab:
    - ee mode!
2. map editor:
    - load layers and enable to edit them one by one
    - be able to create/load/save different maps

3. save and load system (atm we have the basis of this)
4. achievments
5. multiplayer:
    - local (hotseat/lan ?)  
    - connected with a server
    - chat (ee!)

6. procedural generation
7. resprites
8. dungeons
9. bosses ?
10. mvc ?
11. modding api

## NOTE
life is good

## DONE
- refactor player.py and create abstractions for entities:
    - [x] entities/player.py can be drawn with NormalTile
    - [x] use new entities/player.py for the character
- because player.py has confusing statloading, get together the settings.py
    - [x] mvc models for settings
    - [x] game_essentails/data/loaders/data_loader.py to be able to load different kind of files as well
    - [x] game_essentails/level_handling/resource_loader.py to load datas dynamically 
    - [x] setup every setting file into settings folder

- make sound disabled (saved in db)
- player pos can be saved and loaded

- reconstruct folder and file structure:
    - [x] level_handler folder:
        - [x] data_loader into this folder, with image_provider
