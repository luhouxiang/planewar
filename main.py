# -*- coding: utf-8 -*-

import pygame
import game
import traceback

if __name__ == "__main__":
    try:
        game.Game.start()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()


