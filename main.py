# -*- coding: utf-8 -*-
import game
import traceback
import pygame

if __name__ == "__main__":
    try:
        game.game()
    except SystemExit:
        pass
    except:
        traceback.print_ext()
        pygame.quit()
        input()

