
from ParaView.simple import *

import sys, time
# Path to Leap Motion Python Library
leapPath = "LeapDeveloperKit/LeapSDK/lib"
sys.path.append(leapPath)
print leapPath + " has been appended to library. Enjoy Leap Motion"

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

# ParaView object/data to interact with
c = Cone(Radius=1)

# Show the object/data to demonstrate
Show(c)
camera = GetActiveCamera()

# Don't show the slice for demonstrative purposes
sl = Slice(c)

#
x,y,z = (0,1,2)


class SampleListener(Leap.Listener):

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"


    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        
        # Check that there are 2 and only hands and that each have at least 2 fingers shown
        # This allows user to close hands to stop scaling. Therefore user has ability to zoom further
        if len(frame.hands) == 2 and len(frame.hands[0].fingers) >= 2 and len(frame.hands[1].fingers) >= 2:
            # Zoom based on the scaling from frames
            cam.Zoom(frame.scale_factor(controller.frame(2)))
        Render()
        
        #Data recording
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

            # Get the hand's sphere Radius=1 and palm position
            print "Hand sphere Radius=1: %f mm, palm position: %s" % (
                  hand.sphere_radius, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            print "Hand pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG)


        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""



def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    while True:
        time.sleep(1.0)
    
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()

main()