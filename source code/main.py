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
    file_manager = FileManager("score_history.txt", None)
    game = Game(state, screen)
    keybind_manager = KeyBindManager(screen, state, game, file_manager)

    screen.keymanager = keybind_manager
    game.keyBindManager = keybind_manager
    file_manager.keyBindManager = keybind_manager

    done()

if __name__ == "__main__":
    main()
