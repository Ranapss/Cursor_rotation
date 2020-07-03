from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding
from math import atan2, degrees
from array import *
from numpy import angle
import random
from psychopy.hardware import joystick
from time import sleep
import serial.tools.list_ports
import serial

_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)


psychopyVersion = '3.0.6'
expName = 'Force_Rotate'
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: 
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data' + os.sep + '%s_%s' % (expInfo['participant'], expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\Rana\\Documents\\My stuff\\sanghoon\\rana_lastrun.py',                                                              #change to new location
    savePickle=True, saveWideText=True,
    dataFileName=filename)
    
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp





#joystick.backend = 'pyglet'

joystick.backend = 'testmonitor'                                                                                         # must match window type 


#win = visual.Window((800.0, 800.0), allowGUI=False, winType=joystick.backend)

#win = visual.Window((800.0, 800.0), allowGUI=False, winType=joystick.backend, screen = 2)                                             # main

#win = visual.Window((800.0, 800.0), allowGUI=False, winType="pyglet")s

#win2 = visual.Window(size=(800, 800), monitor='testMonitor')

win = visual.Window(size=(800, 800), monitor=joystick.backend)

nJoysticks=joystick.getNumJoysticks()
if nJoysticks>0:
    joy = joystick.Joystick(0)
    print('found ',joy.getName(),' with:')

else:
    print("You don't have a joystick connected!?")


smooth = 3                                                                                              #smoothing array averages this many inputs 
xaxisMultiplier = -1                                                                                    #depending on the controler x or y may need different signs 
yaxisMultiplier = -1

sets = [1,2,1]                                                                                         #the different sets of trials, total trials are sets * targets
angles = [0,-60,0]                                                                                       # angle distortion for each set, sets and angles must be the same size, positive is clockwise rotation        -60
distort = [False, True, False]                                                                       # true or false to use the visual distortion, 
force = False                                                                                         # change to true to use force sensors

# used if changing the radius/ alter the cursor position with the aspect ratio
size = 1
xaspect = win.size[1]/win.size[0] * size
yaspect = 1*size

# global variables used throughout 
xx = 0 # x point
yy = 0 # y point


xx2 = 0
yy2 = 0

score = 0

ang = 0 # angle of the cursor position
r = 0 # radius (distance) of the cursor
lastx = 0
lasty = 0
speed = 0
lastt = 0
lastr = 0
count = 0
same = 0
lastp = 0

# arrays used in force sensor calculations 
axes = [1,2,3,4,5,6]
counter = 0
x = 0
bias = [8255, 8245, 8253, 8061, 8369, 8154]                                                              # sensor values when no forces applied
sensitivity = [32.590,32.590,33.700,1635.000,1629.500,1633.500]                                             #returned by sensor after writing b'p'
fixed = [0,1,2,3,4,5]                                                                                      #array of size six used for the sensor force calculations

# arrays that will be used for smoothing, if the smooth function is used 
xx0 = array('f',[])
yy0 = array('f',[])
for n in range(0,smooth):
    xx0.append(0)
    yy0.append(0)

# arrays to record data for the experiment                                                    You can add more arrays here to record different data 
radius_array = array('f', [])
rawx_array = array('f',[])
rawy_array = array('f',[])
joyx_array = array('f', [])
joyy_array = array('f', [])
polarx_array = array('f',[])
polary_array = array('f',[])
angle_array = array('f', [])
torquex_array = array('f',[])
torquey_array = array("f",[])
visdx_array = array('f',[])
visdy_array = array('f',[])
smoothx_array = array('f',[])
smoothy_array = array('f',[])

# timers used 
exp_clock = core.Clock()
trial_clock = core.CountdownTimer()
#hold_clock = core.CountdownTimer()

# functions 
def getAngle(c): 
    ang = degrees(atan2(c[1], -c[0]) - atan2(0.5,0))
    return ang + 360 if ang < 0 else ang

def getPoint():
    global xx, yy, xx2, yy2
    
    xx = xaxisMultiplier*joy.getX()
    yy = yaxisMultiplier*joy.getY()
    
    xx2 = xaxisMultiplier*joy.getX()
    yy2 = yaxisMultiplier*joy.getY()
    
    joyx_array.append(xx)
    joyy_array.append(yy)
    rawx_array.append(xx/xaxisMultiplier)
    rawy_array.append(yy/yaxisMultiplier)

def smooth(smoothing = smooth):
    global xx, yy, xx0, yy0
    xx0.insert( 0, xx )
    yy0.insert( 0, yy )
    xx0.pop()
    yy0.pop()
    xx = sum(xx0)/smoothing
    yy = sum(yy0)/smoothing

def angleDist(rotangle = 0):
    global r, xx, yy
    getPoint()
    r = sqrt( xx**2 + yy**2 )
    theta = atan2(yy,xx)
    theta = theta - rotangle*(2*pi)/360
    
    xx = r*cos( theta )
    yy = r*sin( theta )
    polarx_array.append(xx)
    polary_array.append(yy)

def set_target(target,rad = 0.91):
    ypos = rad*sin((90-target)/360*2*pi)
    xpos = rad*cos((90-target)/360*2*pi)
    return xpos,ypos

def draw_cursor():
    getPoint()
    cursor.setPos((xx,yy))
    cursor0.setPos((xx,yy))

def forcepts():
    global xx, yy, xx2, yy2, ser, fixed
    ser.write(b'R')
    #print(rl.readline())
    #ser.write(b's')

    reading = ser.read(27)
    if len(reading) != 27 or str(reading)[-3:-1] != '\\n':
        reading = ser.readline()
    for x in range(6):
        axes[x]=int(reading[1+(x*4):(1+(x*4))+4],16)
        fixed[x] = round((axes[x]-bias[x])/sensitivity[x],3)
    xx = fixed[3] * -1                                                                            # using tourque x, change the number to change senitivity but not the sign 
    yy = fixed[4] * 1                                                                           # using tourque y change the number to change sensitivity 
    
    xx2 = fixed[3] * -0.75                                                                           # using tourque x
    yy2 = fixed[4] * 0.75
    
    
    joyx_array.append(xx)
    joyy_array.append(yy)
    torquex_array.append(fixed[3])
    torquey_array.append(fixed[4])

def angleDist_force(rotangle = 0):
    global r, xx, yy
    forcepts()
    r = sqrt( xx**2 + yy**2 )
    theta = atan2(yy,xx)
    theta = theta - rotangle*(2*pi)/360
    
    xx = r*cos( theta )
    yy = r*sin( theta )
    polarx_array.append(xx)
    polary_array.append(yy)

def init_sensor():
    global ser
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p)
    if len(ports) != 0:
        ser = serial.Serial('COM3', 921600,timeout=1,write_timeout=1)                                                                 #
    else:
        print('force sensor not connected')

def vis_distort_joy(rotangle = 0):
    global r, xx, yy, lastx, lasty,lastt, lastr, count, same, lastp
    getPoint()
    speed = sqrt((lastx - xx)**2 + (lasty - yy)**2)
    lastx = xx
    lasty = yy
    
    r = sqrt( xx**2 + yy**2 )
    
    
    rspeed = r - lastr
    rspeed *= 1
    lastr = r
    
    theta1 = atan2(yy,xx)
    
    if count == 0:
        lastp = theta1
    theta = lastp - 0.9*speed -(lastt-theta1)                                                       # change the number to change how much the velocity affects the distortion. 

    lastt = theta1
    xx = r*cos( theta ) 
    
    yy = r*sin( theta )
    lastp = atan2(yy,xx)

    
    visdx_array.append(xx)
    visdy_array.append(yy)

def vis_distort_force(rotangle = 0):
    global r, xx, yy, lastx, lasty,lastt, lastr, count, same, lastp
    forcepts()
    speed = sqrt((lastx - xx)**2 + (lasty - yy)**2)
    lastx = xx
    lasty = yy
    
    r = sqrt( xx**2 + yy**2 )
    
    
    rspeed = r - lastr
    rspeed *= 1
    lastr = r
    
    theta1 = atan2(yy,xx)
    
    if count == 0:
        lastp = theta1
    theta = lastp - 0.9*speed - (lastt-theta1)                                                        # change the number to change how much the velocity affects the distortion

    lastt = theta1
    xx = r*cos( theta ) 
    
    yy = r*sin( theta )
    lastp = atan2(yy,xx)
    
    visdx_array.append(xx)
    visdy_array.append(yy)

def draw_cursor2_joy():
    getPoint()
    test.setPos((xx2,yy2))

def draw_cursor2_force():
    forcepts()
    test.setPos((xx2,yy2))

def get_score():

    score = getAngle((xpos,ypos))-ang
    if abs(score) > 180:
        360-score
    score = round((360 - score)/100,0)
    return score

def add_data():
    thisExp.addData('Force', force)
    thisExp.addData('distortion',distort[spot])
    thisExp.addData('rotation',angles[spot])
    thisExp.addData('radius', radius_array[:])
    thisExp.addData('angle',angle_array[:])
    thisExp.addData('joyx',joyx_array[:])
    thisExp.addData('joyy',joyy_array[:])
    thisExp.addData('polarx',polarx_array[:])
    thisExp.addData('polary',polary_array[:])
    thisExp.addData('Vis_distx_raw',visdx_array[:])
    thisExp.addData('vis_disty_raw',visdy_array[:])
    thisExp.addData('smoothx',smoothx_array[:])
    thisExp.addData('smoothy',smoothy_array[:])
    thisExp.addData('torquex',torquex_array[:])
    thisExp.addData('torquey',torquey_array[:])
    thisExp.addData('rawx',rawx_array[:])
    thisExp.addData('rawy',rawy_array[:])
    thisExp.nextEntry()

# Text stimuli
time = visual.TextStim(win,text='.', pos=(-0.5,-0.95))
time.size= 0.08
msg = visual.TextStim(win, text=' ', pos=(0, -.45))
score_msg = visual.TextStim(win, text = ' ', pos = (-0.5,.95))


# circle stimuli, targets, cursor, boundry, center 
# change the value of radius to change the size
cursor = visual.Circle(win, radius= .03,fillColor = 'red', units=None)
cursor0 = visual.Circle(win, radius= .03,fillColor = 'black',edges = 1, units=None,lineColor = 'black')                                   #circle within the cursor incase a more precice overlap is needed
center = visual.Circle(win,radius =.07, units = None, fillColor=None, lineColor='white')
boundry = visual.Circle(win,radius = .9, units = None, fillColor = None, lineColor = "green")

endpt = visual.Circle(win, radius = 0.05, fillColor = 'blue', units = None,opacity = 0)
targetC = visual.Circle(win, radius = 0.04, fillColor = 'green', units = None)
targetC.opacity = 0

test = visual.Circle(win, radius= .03,fillColor = 'green', units=None)                                                                   #second cursor to test different controls 

line = visual.ShapeStim(win,lineColor='red',closeShape=False,vertices=np.empty((0, 2)))
line.vertices = np.array([(0,0)])
# Sound stimuli 
highA = sound.Sound('A', octave=3, sampleRate=44100, secs=0.8, stereo=True)
#highA.setVolume(0.8)
tick = sound.Sound(800, secs=0.01, sampleRate=44100, stereo=True)
tock = sound.Sound('600', secs=0.01, sampleRate=44100, stereo=True)


init_sensor()                                                                                                                                      #initialize sensors, if none are pluged in it will skip it
q = False                                                                                                                      #used in the experiment to return to 1 to 1 controls by pressing q
complete = 0                                                                                                                     # keep track of completed trials 
accurate = [0,0,0]                                                                                                                # calculate accuracy for 3 sets

msg.text = 'press s to start'
msg.draw()
win.flip()

#event.waitKeys(keyList = ['s'])                                         conmment 388-390 if you're having issues
while not event.getKeys(keyList = ['s']):
    event.clearEvents()
    #print('clear')

msg.text = ' '
win.flip() 

for spot in range(len(sets)):
    set = sets[spot]

    for x in range(set):
        targets = [0,45,90,135,180,225,270,315]
        target = None
        t = 0
        err = False
        hit = False
        out = False
        added = False
        count = 0
        liner = 0
        
        while len(targets) != 0:
            
            if not distort[spot]:
                if force:
                    angleDist_force(angles[spot])
                else:
                    angleDist(angles[spot])
            if distort[spot]:
                if force:
                    draw_cursor2_force()
                    vis_distort_force(angles[spot])
                else:
                    draw_cursor2_joy()
                    vis_distort_joy(angles[spot])
                    
            
            
            r = sqrt( xx**2 + yy**2 )

            if r < 0.6:
                xx = xx * (r+0.4)
                yy = yy * (r+0.4)
            else:
                xx = xx 
                yy = yy 
            
            if (hit or err) and r<= 0.2 and distort[spot]:
                xx = xx * .1
                yy = yy * .1

            if event.getKeys(['q']):
                q = True
                msg.text = ' Q is pressed, press W to return to experiment controls'
                event.clearEvents('keyboard')
            elif event.getKeys(['w']):
                q = False
                msg.text = ' '
                event.clearEvents('keyboard')
            if q:
                #print('q')
                draw_cursor()
            
            smooth()
            smoothx_array.append(xx)
            smoothy_array.append(yy)
            
            ang = getAngle([xx,yy])
            r = sqrt( xx**2 + yy**2 )                              # neccessray if smoothing is used 
            lastr = r
            radius_array.append(r)
            angle_array.append(ang)
            #if abs(ang-lang) > 100:
            #    err = True
            cursor.setPos((xx,yy))
            cursor0.setPos((xx,yy))
            
            if targetC.opacity != 0 and target != None:                                # distort[spot] and 
                
                if abs(liner- lastr)>0.1:
                    liner = lastr
                    line.vertices = np.append(line.vertices, np.array([(xx,yy)]), axis=0)
                    
            #test.draw()                                               # test cursor to see joystick input without any rotation/distortion
            
            cursor.draw()
            cursor0.draw()
            
            
            if center.overlaps(cursor0):
                center.lineColor = "red"
                count = 0
                #center.opacity = 1
            elif msg.text != 'return to center' and not err:
                center.lineColor = 'darkblue'
                #center.opacity = 0
            
            
            
            if target == None and center.overlaps(cursor0):
                line.vertices = np.array([(0,0)])
                if err or out:
                    core.wait(0.2)                                                                    #if there is an error, the program will pause for 0.2 seconds to give the participant time to read
                
                if hit and not out and not err:
                    hit = False
                    complete += 1
                    targetC.opacity = 0
                    targets.remove(remove)
                    thisExp.addData('Force', force)
                    thisExp.addData('distortion',distort[spot])
                    thisExp.addData('rotation',angles[spot])
                    thisExp.addData('radius', radius_array[:])
                    thisExp.addData('angle',angle_array[:])
                    thisExp.addData('joyx',joyx_array[:])
                    thisExp.addData('joyy',joyy_array[:])
                    thisExp.addData('polarx',polarx_array[:])
                    thisExp.addData('polary',polary_array[:])
                    thisExp.addData('Vis_distx_raw',visdx_array[:])
                    thisExp.addData('vis_disty_raw',visdy_array[:])
                    thisExp.addData('smoothx',smoothx_array[:])
                    thisExp.addData('smoothy',smoothy_array[:])
                    thisExp.addData('torquex',torquex_array[:])
                    thisExp.addData('torquey',torquey_array[:])
                    thisExp.addData('rawx',rawx_array[:])
                    thisExp.addData('rawy',rawy_array[:])
                    thisExp.nextEntry()
                if len(targets) == 0:
                    break
                #hold_clock.reset()
                #hold_clock.add(1)
                
                out = False
                err = False
                added = False
                deleted = False
                
                target = random.choice(targets)
                thisExp.addData('target', target)
                xpos,ypos = set_target(target)                                              # set_target() has an arg for the radius size if you need to change the radius of targets 
                targetC.setPos((xpos,ypos))
                thisExp.addData('xpos',xpos)
                thisExp.addData('ypos',ypos)
                targetC.fillColor = 'green'
#                targetC.opacity = 1
                endpt.opacity = 0
                msg.text = ' '
                trial_clock.reset()
                trial_clock.add(3)
                t = trial_clock.getTime()

            if not center.overlaps(cursor) and targetC.opacity != 1:
                trial_clock.reset()
                trial_clock.add(2)
                t = trial_clock.getTime()
            if t - trial_clock.getTime() > 1 and center.overlaps(cursor) and target != None:
                targetC.opacity =1
                endpt.opacity = 0
                trial_clock.reset()
                trial_clock.add(2)
                t = trial_clock.getTime()
                if not deleted:
                    del radius_array[:]
                    del rawx_array[:]
                    del rawy_array[:]
                    del joyx_array[:]
                    del joyy_array[:]
                    del polarx_array[:]
                    del polary_array[:]
                    del angle_array[:]
                    del torquex_array[:]
                    del torquey_array[:]
                    del visdx_array[:]
                    del visdy_array[:]
                    del smoothx_array[:]
                    del smoothy_array[:]
                    deleted = True
            
            if t - trial_clock.getTime() < 0.1 and not center.overlaps(cursor) and target != None and targetC.opacity != 0:                  # change the number to change how fast you have to move for a too soon error 
                err = True 
                target = None
                targetC.opacity = 0
                score -= 2
                msg.text = 'Moved too soon, restarting trial. Return to center'
                line.vertices = np.array([(0,0)])
            if t - trial_clock.getTime() > 0.5 and center.overlaps(cursor0) and target != None and targetC.opacity != 0:                    # change the number to change how long you can sit in the center before a too slow error
                err = True
                msg.text = 'Moved too slow, restarting trial. Return to center'
                target = None
                targetC.opacity = 0
                center.opacity = 1
                score -= 2
                line.vertices = np.array([(0,0)])
            if t - trial_clock.getTime() > 0.9 and (center.overlaps(cursor0) or hit == False) and target != None and targetC.opacity != 0:
                err = True
                msg.text = 'Took too long, restarting trial. Return to center'
                target = None
                targetC.opacity = 0
                center.opacity = 1
                score -= 2
                line.vertices = np.array([(0,0)])
                
            if complete % 160 == 0 and complete != 0:
                time.text = 'trials completed {}'.format(complete)
            else:
                time.text = ' '
            time.draw()

            if target != None and r > 0.9 and targetC.opacity == 1:                                                            # set the cursor hit condition
                
                count = 0
                endpt.setPos((xx,yy))
                score += get_score()
                endpt.opacity = 1
                msg.text = 'return to center'
                center.opacity = 1
                if targetC.overlaps(endpt):
                    accurate[spot] += 1
                remove = target
                target = None
                hit = True
                line.vertices = np.append(line.vertices, np.array([(xx,yy)]), axis=0)
            if r> 1.05:                                                                            # set the out of bounds limit
                out = True
                target = None
                targetC.opacity = 0
                score -= 2
                msg.text = 'out of bounds, restarting trial'
            score_msg.text = 'current score = {}'.format(score)
            #if distort[spot]:
            line.draw()
            endpt.draw()
            targetC.draw()
            center.draw()
            msg.draw()
            boundry.draw()
            #score_msg.draw()
            if not center.overlaps(cursor0):
                count += 1
            win.flip()
end = []
for x in range(len(accurate)):
    end.append(round(100*(accurate[x]/(sets[x]*8)),1))

end.append(round(100*(sum(accurate)/complete),1))
win.flip()

score_msg.setPos((0,0))
#score_msg.text = str('Final Score = {} Accuracy set 1 = {}%\nAccruacy set 2 = {}%\nAccuracy set 3 = {}%\nTotal accuracy = {}%'.format(score,
#    round(100*(accurate[0]/(sets[0]*8)),1),round(100*(accurate[1]/(sets[1]*8)),1),round(100*(accurate[2]/(sets[2]*8)),1),round(100*(sum(accurate)/complete),1)))
score_msg.text='Accuracy = {}'.format(end)
score_msg.draw()
win.flip()

core.wait(4)
print('score = ',score)
print('accuracy =', end)
print(accurate)
win.close()
print('Experiment finshed, and closed properly')
core.quit()
