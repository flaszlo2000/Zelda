from scripts.observer import KeySubject

# Custom Event constants for extend the options of pygame.constants
# NOTE: use 10_xxx prefix to avoid id confusion
SAVE: int = 10_001
LOAD: int = 10_002
LOAD_REQ: int = 10_003 # request to send out a specific saved value
MAIN_SOUND_TOGGLE: int = 10_004

key_broadcast_subject = KeySubject()
