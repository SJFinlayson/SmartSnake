import pygame
import random
import os
import time
import neat
import visualize
import pickle
pygame.font.init() #init font


WIN_WIDTH = 800
WIN_HEIGHT = 800
STAT_FONT = pygame.font.SysFont("leelawadee", 50)
END_FONT = pygame.font.SysFont("leelawadee", 70)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Slither snake")

snakeHead_img = pygame.image.load(os.path.join("imgs","SnakeHead.png")).convert_alpha()
snakeBody_img = pygame.image.load(os.path.join("imgs","SnakeBody.png")).convert_alpha()
food_img = pygame.image.load(os.path.join("imgs","Foood.png")).convert_alpha()
bg_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha())

gen = 0
vision = [0] * 24 #Set up vision array

class Snake:
    #Class representing the snake
    headIMG = snakeHead_img
    bodyIMG = snakeBody_img
    length = 2
    x = [200]
    y = [200]
    direction = 0

    updateCountMax = 2
    updateCount = 0
    #Variables for each snake
    
    def __init__(self, x, y, length):  #Initialise the snake/variables
        self.hImg = self.headIMG
        self.bImg = self.bodyIMG
        self.vel = 20
        self.tick_count = 0
        self.length = length
        for i in range(0, 2000):
            self.x.append(00)
            self.y.append(00)
        self.x[0] = x
        self.x[1] = x
        #self.x[2] = x
        #self.x[3] = x
        self.y[0] = y
        self.y[1] = 1 * -45
        #self.y[2] = 2 * -45
        #self.y[3] = 3 * -45
        #print(str(self.x[0]) + "," + str(self.y[0]))

        
    def move(self):
        #count update frames
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
            
            for i in range(self.length-1,0,-1): #Move snake tail forwards with the head
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
                
            #To make the snake move
            if self.direction == 0:
                self.x[0] = self.x[0] + self.vel
            if self.direction == 1:
                self.x[0] = self.x[0] - self.vel
            if self.direction == 2:
                self.y[0] = self.y[0] + self.vel
            if self.direction == 3:
                self.y[0] = self.y[0] - self.vel

            self.updateCount = 0

    #methods to change direction
    def moveRight(self): 
        self.direction = 0
    def moveLeft(self):
        self.direction = 1
    def moveDown(self):
        self.direction = 2
    def moveUp(self):
        self.direction = 3

    #Draw snake to screen
    def draw(self, win):
        for i in range(0, self.length):
            if i == 0:
                win.blit(self.hImg, (self.x[i],self.y[i]))
            else:
                win.blit(self.bImg, (self.x[i],self.y[i]))
    
def sight(snake, apple): #Function to determine the snakes sight & variables
    #Look up
    tempVals = directionLook(snake, apple, 0, -20)
    vision[0] = tempVals[0]
    vision[1] = tempVals[1]
    vision[2] = tempVals[2]
    #Look up/right
    tempVals = directionLook(snake, apple, 20, -20)
    vision[3] = tempVals[0]
    vision[4] = tempVals[1]
    vision[5] = tempVals[2]
    #Look right
    tempVals = directionLook(snake, apple, 20, 0)
    vision[6] = tempVals[0]
    vision[7] = tempVals[1]
    vision[8] = tempVals[2]
    #Look down/right
    tempVals = directionLook(snake, apple, 20, 20)
    vision[9] = tempVals[0]
    vision[10] = tempVals[1]
    vision[11] = tempVals[2]
    #Look down
    tempVals = directionLook(snake, apple, 0, 20)
    vision[12] = tempVals[0]
    vision[13] = tempVals[1]
    vision[14] = tempVals[2]
    #Look down/left
    tempVals = directionLook(snake, apple, -20, 20)
    vision[15] = tempVals[0]
    vision[16] = tempVals[1]
    vision[17] = tempVals[2]
    #Look left
    tempVals = directionLook(snake, apple, -20, 0)
    vision[18] = tempVals[0]
    vision[19] = tempVals[1]
    vision[20] = tempVals[2]
    #Look up/left
    tempVals = directionLook(snake, apple, -20, -20)
    vision[21] = tempVals[0]
    vision[22] = tempVals[1]
    vision[23] = tempVals[2]
    
def directionLook(snake, apple, dirX, dirY): #Function to fill in sight for a direction
    directionSight = [0] * 3
    #print(directionSight)
    position = [snake.x[0], snake.y[0]]
    foundFood = False
    foundTail = False
    distance = 0
    
    position[0] = position[0] + dirX
    position[1] = position[1] + dirY
    distance += 1
    
    while not (position[0] < 0 or position[1] < 0 or position[0] >= 800 or position[1] >= 800 ):
        if not foundFood and position[0] == apple.x and position[1] == apple.y :
            directionSight[0] = 1
            foundFood = True  #Check if food is in a direction
        
        for i in range(2, snake.length):
            if not foundTail and Game.collide(position[0], position[1], snake.x[i], snake.y[i]):
                directionSight[1] = 1/distance
                foundTail = True #Check if tail is in a direction
                
        position[0] = position[0] + dirX
        position[1] = position[1] + dirY
        distance += 1
    
    directionSight[2] = (1/distance)
    
    return directionSight #Return sight in a specific direction
    
    
class Food(): #Class and variables for apple
    x = 0
    y = 0
    foodIMG = food_img
    
    def __init__(self, x, y): #Initialise
        self.x = x
        self.y = y
        self.img = self.foodIMG
    
    def draw (self, win): #Draw food
        win.blit(self.img, (self.x, self.y))
        
        
class Game: #Required to handle collision with food and snake tail
    def collide( x1, y1, x2, y2):
        if x1 >= x2 and x1 <= x2 + 20:
            if y1 >= y2 and y1 <= y2 + 20:
                return True
        return False

def draw_window(win, snakes, apple, score, gen): #Drawing the screen
    if gen == 0:
        gen = 1 #Passing first generation
    win.blit(bg_img,(0,0)) #Draw/clear background


    for snake in snakes:
        snake.draw(win) #Draw each snake
            

    apple.draw(win) #Draw the apple
    
    #score
    #score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    #win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))
    
    # generations
    score_label = STAT_FONT.render("Gens: " + str(gen-1),1,(255,255,255))
    win.blit(score_label, (10, 10))

    # alive
    score_label = STAT_FONT.render("Alive: " + str(len(snakes)),1,(255,255,255))
    win.blit(score_label, (10, 50))

    pygame.display.update() #Update the display

def eval_genomes(genomes, config): #Genome evaluation function
    global WIN, gen
    win = WIN
    #print("Win is " + str(win))
    gen +=1
    
    nets = []
    snakes = []
    ge = []
    for genome_id, genome in genomes: #Initialise a generation/snake
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        snakes.append(Snake(200, 200, 2))
        ge.append(genome)
        
    apple = Food(220,200) #First food
    score = 0
    
    clock = pygame.time.Clock()
    
    run = True
    while run and len(snakes) > 0:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break #A quit function
                
        for x, snake in enumerate(snakes): #Funtion in which the neural network will acertain outputs 
            ge[x].fitness += 0.1
            snake.move()
            
            sight(snake, apple)
            #Give net, snake head location and vision
            #print(vision)
            output = nets[snakes.index(snake)].activate((snake.x[0], snake.y[0], vision[0], vision[1], vision[2], vision[3], vision[4], vision[5], vision[6], vision[7], vision[8], vision[9], vision[10], vision[11], vision[12], vision[13], vision[14], vision[15], vision[16], vision[17], vision[18], vision[19], vision[20], vision[21], vision[22], vision[23]))
            #outputs correspond to movement directions
            if output[0] > 0.5:
                snake.moveRight()
            elif output[1] > 0.5:
                snake.moveLeft()
            elif output[2] > 0.5:
                snake.moveDown()
            elif output[3] > 0.5:
                snake.moveUp()

        
    
        for snake in snakes:
            snake.move() #Move the snake
            if Game.collide(apple.x, apple.y, snake.x[0], snake.y[0]):
                apple.x = random.randrange(20, 760)
                apple.y = random.randrange(20, 760)
                score += 1
                for genome in ge:
                    genome.fitness += 8
                snake.length = snake.length + 1 #Check if colliding with apple, and increase fitness/score if so
                
            for i in range(3, snake.length):   
                if Game.collide(snake.x[0], snake.y[0], snake.x[i], snake.y[i]):
                    #print("You lose! Collision: ")
                    ge[snakes.index(snake)].fitness -= 3
                    nets.pop(snakes.index(snake))
                    ge.pop(snakes.index(snake))
                    snakes.pop(snakes.index(snake)) #If collide with tail kill snake
        
        for snake in snakes:
            if snake.y[0] <= 0 or snake.y[0] >= 800 or snake.x[0] <= 0 or snake.x[0] >= 800:
                ge[snakes.index(snake)].fitness -= 5
                nets.pop(snakes.index(snake))
                ge.pop(snakes.index(snake))
                snakes.pop(snakes.index(snake)) #If collide with wall kill snake
            
        draw_window(WIN, snakes, apple, score, gen) #Call the drawing of the window
            
        
def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play snake.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 100 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)





