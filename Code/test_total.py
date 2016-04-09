
from ParaView.simple import *

import sys, time
# Path to Leap Motion Python Library
leapPath = "LeapDeveloperKit/LeapSDK/lib"
sys.path.append(leapPath)
print leapPath + " has been appended to library. Enjoy Leap Motion"

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

# ParaView object/data to interact with
# Will use this data file for demonstration
reader = ExodusIIReader(FileName="../Examples/ParaViewTutorialData/disk_out_ref.ex2")

Show(reader)
dp1 = GetDisplayProperties(reader)
# Wireframe to see within the object
dp1.Representation = 'Wireframe'
thresholdFilter = Threshold(reader)
Show(thresholdFilter)
# Show the slice for slicing action
sl = Slice(reader)
Show(sl)
cam = GetActiveCamera()
cam.SetPosition(1,1,1)
x,y,z = (0,1,2)

# # Turn slicing on/off
# def sliceRender(sliceOn):
#     # Already on (True)
#     if sliceOn: 
#         return False
#     else:
#         return True

# # Show new slice if slicing is on
# def slice(frame,oldNormal,on):
#     if on:
#         # ParaView slice normal
#         normal = [ 
#             frame.hands[0].palm_normal[x], 
#             frame.hands[0].palm_normal[y],
#             frame.hands[0].palm_normal[z] 
#             ]
#         return normal
#     else:
#         return oldNormal
         

class SampleListener(Leap.Listener):

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        
        # ParaView parameters
        normal1 = [ 
            frame.hands[0].palm_normal[x], 
            frame.hands[0].palm_normal[y], 
            frame.hands[0].palm_normal[z] 
            ]
        
        # ParaView slice: if only 1 hand and not a fist
        if len(frame.hands) == 1 and len(frame.hands[0].fingers) > 0:
            sl.SliceType.Normal = normal1

        # ParaView zoom: if 2 hands with each at least 2 fingers
        elif len(frame.hands) == 2 and len(frame.hands[0].fingers) >= 2 and len(frame.hands[1].fingers) >= 2:
            cam.Zoom( frame.scale_factor(controller.frame(2)) )

        # ParaView rotate: only attempt if there are 2 hands (at least one must have less than 2 fingers)
        if len(frame.hands) == 2:
            # Check for which hand has at least 2 fingers and use that one
            if len(frame.hands[0].fingers) < 2 and len(frame.hands[1].fingers) > 2 :
                rotHand = frame.hands[1]
                rollAngle = rotHand.palm_normal.roll * Leap.RAD_TO_DEG
                azimAngle = rotHand.palm_normal.yaw * Leap.RAD_TO_DEG
                cam.SetRoll( rollAngle )                
            elif len(frame.hands[1].fingers) < 2 and len(frame.hands[0].fingers) > 2 :
                rotHand = frame.hands[0] 
                rollAngle = rotHand.palm_normal.roll * Leap.RAD_TO_DEG
                azimAngle = rotHand.palm_normal.yaw * Leap.RAD_TO_DEG
                cam.SetRoll( rollAngle )
            #else:
            #cam.SetRoll(0)
        
        Render()

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        if not frame.hands.is_empty:
            # Get the first hand
            hand = frame.hands[0]

            # Check if the hand has any fingers
            fingers = hand.fingers
            if not fingers.is_empty:
                # Calculate the hand's average finger tip position
                avg_pos = Leap.Vector()
                for finger in fingers:
                    avg_pos += finger.tip_position
                avg_pos /= len(fingers)
                print "Hand has %d fingers, average finger tip position: %s" % (
                      len(fingers), avg_pos)

            # Get the hand's sphere radius and palm position
            print "Hand sphere radius: %f mm, palm position: %s" % (
                  hand.sphere_radius, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            print "Hand pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG)

            # Gestures
            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                    circle = CircleGesture(gesture)

                    # Determine clock direction using the angle between the pointable and the circle normal
                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4:
                        clockwiseness = "clockwise"
                    else:
                        clockwiseness = "counterclockwise"

                    # Calculate the angle swept since the last frame
                    swept_angle = 0
                    if circle.state != Leap.Gesture.STATE_START:
                        previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                        swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                    print "Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                            gesture.id, self.state_string(gesture.state),
                            circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    print "Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                            gesture.id, self.state_string(gesture.state),
                            swipe.position, swipe.direction, swipe.speed)

                if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                    keytap = KeyTapGesture(gesture)
                    print "Key Tap id: %d, %s, position: %s, direction: %s" % (
                            gesture.id, self.state_string(gesture.state),
                            keytap.position, keytap.direction )

                if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                    screentap = ScreenTapGesture(gesture)
                    print "Screen Tap id: %d, %s, position: %s, direction: %s" % (
                            gesture.id, self.state_string(gesture.state),
                            screentap.position, screentap.direction )

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    while True:
        time.sleep(1.0)
#     print 1
    
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()

main()