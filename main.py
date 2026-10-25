import os
import sys

# Paksa biar ga error mixer di Pydroid
try:
    import pygame
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.init()
    pygame.mixer.init()
except:
    pass

# Baru jalanin game.py yang sefolder
if os.path.exists("game.py"):
    exec(open("game.py").read())
else:
    print("game.py tidak ditemukan sefolder!")
