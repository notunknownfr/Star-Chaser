from screen import ScreenClass


class GameState:
    def __init__(self, screen: ScreenClass, state="idle"):
        self.currentState=state
        self.screen=screen


    def change_state(self, new_state):
        if self.currentState==new_state:
            pass

        elif self.currentState=="running":
            if new_state=="pause":
                self.currentState=new_state
                self.screen.keymanager.function_caller()

            else:    
                pass
        
        elif self.currentState=="changeKeyBind":
            if new_state=="back":
                self.currentState="back"
                self.screen.keymanager.function_caller()

        else:
            self.currentState = new_state
            self.screen.keymanager.function_caller()