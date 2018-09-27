# -*- coding: utf-8 -*-
import pygame
import mygame
import traceback

if __name__ == "__main__":
    try:
        mygame.MyGame.start()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()


