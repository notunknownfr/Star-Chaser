from screen import ScreenClass
from state_machine import GameState
from score_manager import FileManager
from settings import KeyBindManager
from game import Game
from turtle import done

def main():
    
    screen = ScreenClass()
    screen.imageSetup()
    screen.StartScreenSetup()

    state = GameState(screen)
    #Initialize file manager with None for keybindmanager first
    file_manager = FileManager("score_history.txt", None)
    
    game = Game(state, screen)
    
    #Initialize KeyBindManager
    keybind_manager = KeyBindManager(screen, state, game, file_manager)
    keybind_manager.setup_keybinds()

    file_manager.keybindmanager = keybind_manager
    game.keyBindManager = keybind_manager
    screen.keymanager = keybind_manager

    done()

if __name__ == "__main__":
    main()
