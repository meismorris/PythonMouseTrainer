import math
import random
import time
import pygame 
pygame.init()

WIDTH,HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH,HEIGHT)) # Takes width and height to create a display based on that resolution

pygame.display.set_caption("Mouse Clicker!") # Sets the name of the application

TARGET_INCREMENT = 150 # Time it takes to spawn another target
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30

BG_COLOR = (0,25,40)
LIVES = 3
TOP_BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("arial", 24)

class Target: 
    # Set max size, growth rate, and color
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"
    
    def __init__(self,x,y): # Create taget with its sizes, position and whether to grow or not
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True
        
    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE: # IF the size reaches max size, stop growing
            self.grow = False
            
        if self.grow: # IF self.grow is true, continues to grow by 0.2
            self.size += self.GROWTH_RATE
            
        else: # If it has been set false from the first statement, start subtracting
            self.size  -= self.GROWTH_RATE
    
    def draw(self,win): #Creating the target using 4 circles with different colors. 
        pygame.draw.circle(win,self.COLOR, (self.x,self.y), self.size)
        pygame.draw.circle(win,self.SECOND_COLOR, (self.x,self.y), self.size * 0.8)
        pygame.draw.circle(win,self.COLOR, (self.x,self.y), self.size * 0.6)
        pygame.draw.circle(win,self.SECOND_COLOR, (self.x,self.y), self.size * 0.4)
        
    def collide(self, x, y):
       dis = math.sqrt((x - self.x)**2 + (y - self.y)**2) # Check radius of circle, and position of mouse 
       return dis <= self.size
        
    

def draw(win,targets): # Draw Function, updates screen upon creating target
    win.fill(BG_COLOR) 
    
    for target in targets:
        target.draw(win)
    
def format_time(secs): # Format and display timer

    mili = math.floor(int(secs* 1000 % 1000) / 100)
    seconds = int(round(secs % 60,1))
    minutes = int(secs // 60)
    
    return f"{minutes:02d}:{seconds:02d}.{mili}"

def draw_top_bar(win,elasped_time, targets_pressed, misses):
    pygame.draw.rect(win, "grey", (0,0,WIDTH, TOP_BAR_HEIGHT )) # Draw bar, 0,0 is top left
    
    #Create Labels for each info
    time_label = LABEL_FONT.render(f"Time: {format_time(elasped_time)}", 1, "black")
    speed = round(targets_pressed / elasped_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")
    
    win.blit(time_label,(5,5))
    win.blit(speed_label,(200,5))
    win.blit(hits_label,(450,5))
    win.blit(lives_label,(650,5))
    
def end_screen(win, elasped_time, targets_pressed,clicks): # Display End Screeen
    win.fill(BG_COLOR)
    
    if targets_pressed == 0:
        accuracy = 0
    accuracy = round(targets_pressed / clicks * 100, 1)
    time_label = LABEL_FONT.render(f"Time: {format_time(elasped_time)}", 1, "white")
    speed = round(targets_pressed / elasped_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")
    
    win.blit(time_label, (get_middle(time_label),100))
    win.blit(speed_label, (get_middle(speed_label),200))
    win.blit(hits_label, (get_middle(hits_label),300))
    win.blit(accuracy_label, (get_middle(accuracy_label),400))
    
    pygame.display.update()
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()
            
def get_middle(surface): # gets the middle for object
    return WIDTH / 2 - surface.get_width()/2    

# Runs the program. 
def main():
    run = True
    targets = [] # Targets
    clock = pygame.time.Clock() # Sets fps for the game
    
    targets_pressed = 0
    clicks = 0
    misses = 0 
    start_time = time.time()
    
    pygame.time.set_timer(TARGET_EVENT,TARGET_INCREMENT) # Triggers target_event, every target_increment
    
    while run: # Pygame doesn't have an option to quit the program if you press "x"
        clock.tick(60) # sets game to 60 fps
        click = False # Using this to check if mouse has click/collided with target
        mouse_pos = pygame.mouse.get_pos() # gives xy of mouse as a tuple
        elasped_time = time.time() - start_time # Time passed once game started
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # We would need to find the "Quit" event in the event types, and breaks if it matches
                run = False
                break
            
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING) # Ensures that target stays in display
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT , HEIGHT - TARGET_PADDING)
                target = Target(x,y)
                targets.append(target)
            
            if event.type == pygame.MOUSEBUTTONDOWN: #Check if mouse button clicks on target
                click = True
                clicks += 1
             
        for target in targets: 
            target.update() 
            
            if target.size <= 0: # Removes rargets from list to reduce lag
                targets.remove(target) 
                misses += 1 #Bc we let the value hit 0, we missed the target
            
            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1
                
        if misses >= LIVES: 
            end_screen(WIN,elasped_time,targets_pressed, clicks) # this ends the game as well when you run out of lives
                
                
        draw(WIN, targets)
        draw_top_bar(WIN, elasped_time,targets_pressed, misses)
        pygame.display.update()
            
    pygame.quit()
        
        
        
if __name__ == "__main__":
    main()