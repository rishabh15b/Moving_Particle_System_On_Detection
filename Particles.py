import cv2
import pygame ,sys, random
import numpy as np
import HandDetectorModule as htm   # It includes all the function for hand, finger detection
import autopy # This helps to get the size of the of the screen on which user is working


class Particle:
    def __init__(self):
        self.particles = []

    def moveParticle(self):  # Move particles
        if self.particles:
            self.deleteParticle()
            for particle in self.particles:
                particle[0][1] += (particle[2][0] * 2)
                particle[1] -= 0.2
                particle[0][0] += (particle[2][1] * 2)
                pygame.draw.circle(screen, ((color_1, color_2, color_3)), particle[0], int(particle[1]))

    def addParticle(self):  # Add new particles
        pos_x = pygame.mouse.get_pos()[0]  # x_pos
        pos_y = pygame.mouse.get_pos()[1]  # y_pos
        radius = 10
        direction_x = random.randint(-5, 5)
        direction_y = random.randint(-5, 5)
        particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
        self.particles.append(particle_circle)

    def deleteParticle(self):  # Delete particles after some time
        particleCopy = [particle for particle in self.particles if particle[1] > -2]
        self.particles = particleCopy


####################################      MOUSE POiNTER          ###############################
width, height = 1000, 500    # width = screen width to show the application  && height = screen height to show the application
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
detector = htm.handDetector(detectionCon=0.7)
wS, hS = autopy.screen.size()   # wS = user's screen width  && hS = user's screen height

####################################      PARTICLE FORMATION          ################################
pygame.init()
screen = pygame.display.set_mode((1000, 600))
# Background
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (1000, 600)).convert_alpha()
clock = pygame.time.Clock()

particle_1 = Particle()
# Events Construction
Particle_Event = pygame.USEREVENT + 1  # As this is to be called many times
pygame.time.set_timer(Particle_Event, 40)

color_1 = random.randint(0, 255)
color_2 = random.randint(0, 255)
color_3 = random.randint(0, 255)


while True:
    ###################### TO SHOW THE DIFFERENT COLOR PARTICLES AT SAME TIME #######################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == Particle_Event:
            if 0 < color_1 < 255:
                color_1 += 1
            elif color_1 >= 255:
                color_1 -= 255
            elif color_1 <= 0:
                color_1 += 5
            particle_1.addParticle()

    ###################### TO TRACK THE HAND THEN INDEX FINGER TO MOVE THE MOUSE CURSOR #######################
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img)
        if len(lmlist) != 0:
            x1, y1 = lmlist[8][1:]
            x2, y2 = lmlist[12][1:]

            fingers = detector.fingersUp()
            #print(fingers)

            if fingers[1] == 1 and fingers[2] == 0:
                x3 = np.interp(x1, (0, width), (0, wS))
                y3 = np.interp(y1, (0, height), (0, hS))

                autopy.mouse.move(wS - x3, y3)
    ############### TO SHOW THE IMAGE FROM THE CAMERA FEED ######################
        cv2.imshow("Image", img)
        cv2.waitKey(1)

    ##############  TO SHOW THE PARTICLES ON THE SCREEN #########################
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))
        particle_1.moveParticle()
        pygame.display.update()
        clock.tick(60)
        cv2.imshow("Image", img)
        cv2.waitKey(1)