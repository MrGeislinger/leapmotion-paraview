
from paraview.simple import *

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
Render()
#Show(sl)


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
        x,y,z = (0,1,2)
        normal = frame.hands[0].palm_normal
        position = frame.hands[0].stabilized_palm_position

        print "Normal:", normal[0] , normal[1], normal[2]
        print frame.hands[0].palm_normal.roll * Leap.RAD_TO_DEG

        # ParaView Manipulation: camera is turned based on user's (first hand)
        if not frame.hands.is_empty:
            # Use the roll of hand for 2D rotation (rotate about vector point out from screen, like a doorknob)
            rollAngle = frame.hands[0].palm_normal.roll * Leap.RAD_TO_DEG
            camera.SetRoll( rollAngle * 2 )
            # Orignally to rotate about another axis, but difficult for user interaction
            #azimAngle = frame.hands[0].palm_normal.yaw * Leap.RAD_TO_DEG
            #camera.Yaw( azimAngle )
        # No hand was detected so set camera back to original state
        # Line could be deleted to retain rotation after hand is removed
        else:
            camera.SetRoll(0)

        # Render the change now
        Render()

        print "hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        if not frame.hands.is_empty:
            # Get the first hand
            hand = frame.hands[0]

            # Check if the hand has any fingers

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

                    print "Circle id: %d, %s, progress: %f, Radius=1: %f, angle: %f degrees, %s" % (
                            gesture.id, self.state_string(gesture.state),
                            circle.progress, circleradius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

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

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()

main()
