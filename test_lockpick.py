import pygame
import sys
from lockpick_game import LockpickMinigame

def run_test():
    pygame.init()
    # Set up a standard 800x600 window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Lockpick Minigame Test")
    
    print("Launching Lockpick Minigame...")
    print("Controls:")
    print(" - LEFT/RIGHT arrows to move the pick")
    print(" - Hold UP arrow to raise the active pin")
    print(" - Tap SPACEBAR when the pin is centered on the Red Shear Line to lock it!")
    print(" - ESC to exit early")
    
    # Initialize and run the minigame directly
    game = LockpickMinigame(screen)
    result = game.run()
    
    # Print the result of the game when it exits
    if result:
        print("\n🎉 SUCCESS! You picked the lock!")
    else:
        print("\n❌ FAILED! You gave up or broke your pick.")
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_test()