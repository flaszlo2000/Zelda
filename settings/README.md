### if you want to add a new file with existing data loader
1. add the filename without the extension to the game_essentails/data/models/__init__.py 's HANDLER_MAP
    - for this you will need a data representation class (inherited from GameData), this will be only a dataclass model

### if you want to add a new type of file:
1. add the file extension to the game_essentails/data/loaders/__init__.py 's DATA_LOADERS
    - with this you will need a DataLoader, you can easily create yours in the same folder's data_loader.py, the only abstract method is the **loadData**

#### NOTE
.md files shouldn't be considered as a file to parse as configuration to be able to place readmes and logs for instance as that type