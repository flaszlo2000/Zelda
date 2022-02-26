## TODO

### usual)
- clean code and weekly refactors

### p1) (doing)
- refactor player.py and create abstractions for entities:
    - [x] entities/player.py can be drawn with NormalTile
    - [] use new entities/player.py for the character
- because player.py has confusing statloading, get together the settings.py
    - [x] mvc models for settings
    - [x] game_essentails/data/loaders/data_loader.py to be able to load different kind of files as well
    - [x] game_essentails/level_handling/resource_loader.py to load datas dynamically 
    - [] setup every setting file into settings folder

- make sound disabled 

### p2)
- trial ee listener
- reconstruct folder and file structure:
    - [x] level_handler folder:
        - [] data_loader into this folder, with image_provider
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

3. save and load system
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
