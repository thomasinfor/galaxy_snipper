# initialize
## import
from vpython import *
from math import *
#import random
## scene
def zeroScene():
    scene.autoscale = False
    scene.center = vector(0, 0, 0)
    scene.forward = vector(0, 0, -1)
    scene.range = 10
    scene.width = 1000
    scene.weight = 800
zeroScene()
## variables
charge = 0
K = 3 # ratio of speed
playerAngle = (pi/2, pi/2)
aimAngle = (0, pi/2)
t = 0; dt = 1/240 #240fps owo
## vpython objects
planet = []; bullet = []; target = []
planet.append(sphere(pos=vector(0, 0, 0), texture=textures.earth))
color.miku = vector(0, 0.784, 0.686)

planet.append(sphere(pos=vector(5, 4, 3), color=color.miku))
planet.append(sphere(pos=vector(5, -4, 2), color=color.miku))
planet.append(sphere(pos=vector(-2, 5, -5), color=color.miku))
planet.append(sphere(pos=vector(-5, -3, 3), color=color.miku))
planet.append(sphere(pos=vector(-3, -2, -3), color=color.miku))

player = cone(color=color.red, pos=vector(0, 1, 0), radius=0.1, length=0.5, axis=vector(0, 1, 0))
aim = arrow(color=color.blue, pos=vector(0, 1.3, 0), axis=vector(0.3, 0, 0))

predict = sphere(
    pos=aim.pos,
    radius=0.1,
    make_trail=True,
    color=vector(0, 1, 1), 
    trail_type='points', 
    interval=10, 
    retain=100,
    opacity = 0,
    v=vector(0, 0, 0)
)

def updatePos():
    global player, aim, aimAngle, playerAngle, charge
    player.pos = vector(
        cos(playerAngle[1])*sin(playerAngle[0]),
        sin(playerAngle[1]),
        cos(playerAngle[1])*cos(playerAngle[0])
    )
    v = vector(
        cos(aimAngle[1])*sin(aimAngle[0]),
        sin(aimAngle[1]),
        cos(aimAngle[1])*cos(aimAngle[0])
    )
    aim.axis = vector(
		########################## 待補!!
	)
    player.axis = player.pos*0.5
    aim.pos = player.pos*1.3
    predict.pos = aim.pos
    predict.clear_trail()
    predict.v = norm(aim.axis)*K*charge
    for _ in range(int(1/dt)):
        for p in planet:
            d = p.pos-predict.pos
            if mag(d) >= 0.9:
                predict.v += K*10/mag2(d)*dt*norm(d) #GMm/d^2
            else:
                return
        predict.pos += predict.v*dt

updatePos()
# keyboard control
def keydownControl(evt):
    global charge, charging, scene, playerAngle, aimAngle
    aimAction = {
        'w':(0, 1),  #箭頭向上
        's':(0, -1), #向下
        'a':(1, 0),  #向左
        'd':(-1, 0)  #向右
    }
    playerAction = {
        'o':(0, 1),  #玩家向北
        'l':(0, -1), #玩家向南
        'k':(1, 0),  #向西
        ';':(-1, 0)  #向東
    }
    s = evt.key
    if s == ' ': #charge
        if mag(aim.axis) > 0.2:
            aim.axis -= (10**-3)*aim.axis/mag2(aim.axis) #charging effect
        if charge < 3:
            charge += 0.1
            updatePos()
    elif s == 'q': #zeroing angle of vision
        zeroScene()
    else:
        if s in aimAction: #change aiming angle
            dAlpha = aimAction[s][0]*pi/60; dBeta = aimAction[s][1]*pi/60
            aimAngle = (aimAngle[0] + dAlpha, aimAngle[1] + dBeta)
        if s in playerAction: #change player angle
            dAlpha = playerAction[s][0]*pi/60; dBeta = playerAction[s][1]*pi/60
            playerAngle = (playerAngle[0] + dAlpha, playerAngle[1] + dBeta)
        updatePos()
scene.bind('keydown', keydownControl)
def keyupControl(evt):
    global aim, charge
    if evt.key == ' ' and charge > 0:
        bullet.append(sphere(
            radius=0.05, 
            pos=aim.pos, 
            v=norm(aim.axis)*charge*K, 
            color=vector(1, 0.68, 0.9), 
            make_trail=True, 
            trail_type='points', 
            interval=25, 
            retain=25, 
            inGround = None
        ))
        aim.axis = norm(aim.axis)*0.3
        charge = 0.5
        updatePos()
scene.bind('keyup', keyupControl)

# main
while t<200:
    rate(1/dt)
    # gravity effect
    for b in bullet:
        if b.inGround == None:
            for p in planet:
                d = p.pos-b.pos
                if mag(d) >= 0.9:
                    b.v += K*10/mag2(d)*dt*norm(d) #GMm/d^2
                else:
                    b.inGround = p
                    break
            b.pos += b.v*dt
        elif b.visible:
            p = b.inGround
            d = p.pos-b.pos
            if mag(d) >= 0.8:
                b.v = norm(d)*0.01
                b.pos += b.v*dt
            else:
                b.clear_trail()
                b.visible = False
    bullet = list(filter(lambda b:b.visible, bullet))
print('Time is up!')
