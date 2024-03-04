import sys
import pygame
import random, math

W = 1000
H = 1000

dt = 0.0005

class Point:
    def __init__(self,x,y,vx,vy,r,c):
        self.xy = (x,y)
        self.vx = vx
        self.vy = vy
        self.r = r
        self.color = c
    
    def draw(self):
        pygame.draw.circle(window, self.color, self.xy, self.r)
    
    def move(self):
        x,y = self.xy
        self.xy = (x+self.vx*dt,y+self.vy*dt)

    def temp_color(self, min_v, max_v):
        
        n = max_v - min_v
        #print(min_v, max_v, n)
        v = (self.vx**2 + self.vy**2)**(1/2)
        r = ((v)/max_v)*255
        b = 255 - r
        self.color = (r,0,b)

    def force(self,x2,y2,r2):
        x1,y1 = self.xy
        r1 = self.r
        r = ((x1-x2)**2 + (y1-y2)**2)**(1/2)
        ax = 0
        ay = 0
        if r < (r1+r2):
            ax += 1000000*(x1-x2)/r**3
            ay += 1000000*(y1-y2)/r**3

            #print(ax, ax*dt, ay, ay*dt)

        if (x1>W-self.r):
            ax += -100000/(W - x1)**2
        if (x1<self.r):
            ax += 100000/x1**2
        if (y1>H-self.r):
            ay += -100000/(H - y1)**2
            if x1 < 10:
                ay *= 1.1
            else: ay *= 0.2
        if (y1<self.r):
            ay += 100000/y1**2

        ay += 10



        self.vx += ax*dt
        self.vy += ay*dt    
            
        

pygame.init()
#clock = pygame.time.Clock()

window = pygame.display.set_mode((W, H))

ps = []
"""
for i in range(200):
    v,u = (random.random(),random.random())
    dx = v * math.cos(-u*2*3.14)
    dy = v * math.sin(-u*2*3.14)
    p = Point(W/2+dx*W/2,H/2+dy*H/2, 0, 0, 10, (255,0,0))
    ps.append(p)
"""
k = 2
for i in range(4):
    v,u = (random.random(),random.random())
    dx = 10*v * math.cos(-u*2*3.14)
    dy = 10*v * math.sin(-u*2*3.14)
    p = Point(W/(2*k)+i%k*W/k,H/(2*k)+i//k*H/k, dx, dy, 10, (255,0,0))
    #print(i%k*W/k, i//k*H/k)
    ps.append(p)
t = 0
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    window.fill((0,0,0))
    
    max_v = 0
    min_v = 1000000
    mask = []
    for p in ps:
        x,y = p.xy
        r = p.r
        mask.append((x,y,r))
    
    for p in ps:
        for m in mask:
            x1,y1 = p.xy
            x2,y2,r2 = m

            if (x1 != x2) and (y1 != y2):
                p.force(x2,y2,r2)


    for p in ps:
        v = (p.vx**2 + p.vy**2)**(1/2)
        
        if max_v < v:
            max_v = v
        
        if min_v > v:
            min_v = v
            
    for p in ps:    
        p.move()
        

    t += 1
    if t >= 1/(dt*60):
        t = 0
        for p in ps:
            p.temp_color(min_v, max_v)
            p.draw() 
            
        pygame.display.flip()
