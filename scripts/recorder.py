#!/usr/bin/env python


## ADD AIMS HEADER ##





## Imports
import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
import os
import numpy as np

from sensor_msgs.msg import Image





class RECORDER():

    def __init__(self, pub_color, pub_depth):
        """Initialize

            Setup Publishers as class variables.
        """

        # Setup Variables
        self.pub_color = pub_color  
        self.pub_depth = pub_depth

        # Tools
        self.bridge = CvBridge()

        # System Parameters
        param_savefolder = rospy.get_param("/save_folder")
        self.param_saveimages = rospy.get_param("/save_images")

        # Setup Working Directory
        path_package = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.path_ws = os.path.join(path_package, str(param_savefolder))

        try:
            os.makedirs(self.path_ws, True)
        except OSError:
            if not os.path.isdir(self.path_ws):
                raise
        os.chmod(self.path_ws, 0777)




    def runner_color(self, data):
        """ Runner for Callback to Color Topic
            
            Variables
            data: Input frame as ROS Image message type
        """

        runner_source = "color", 
        pub_object  = self.pub_color

        ### - This section identical for both runners - ###
        try:
            # Convert Image to CV2 Frame
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")

            # Frame MetaData
            frame_seq = data.header.seq
            frame_stamp = data.header.stamp
            frame_name = str(frame_stamp) + "_color.tiff"

            # Save frame
            if self.param_saveimages:
                frame_path = os.path.join(self.path_ws, frame_name)
                cv2.imwrite(frame_path, cv_image)


            ## Publish frame to ROS Topic
            # Add Text
            cv2.putText(cv_image,
                'FrameName: ' + str(frame_name),
                org = (20, 20),
                fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                fontScale = 0.7,
                color = (0,0,0),
                thickness = 2,
                lineType = cv2.LINE_AA,
                bottomLeftOrigin = False)
            cv2.putText(cv_image,
                'Frame SeqID: ' + str(frame_seq),
                org = (20, 40),
                fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                fontScale = 0.7,
                color = (0,0,0),
                thickness = 2,
                lineType = cv2.LINE_AA,
                bottomLeftOrigin = False)

        # Publish Image
            msg_img = self.bridge.cv2_to_imgmsg(cv_image, 'bgr8')
            pub_object.publish(msg_img)

        except rospy.ROSInterruptException:
            exit()
        except KeyboardInterrupt:
            exit()
        except CvBridgeError as e:
            print(e)



    def runner_depth(self, data):
        """ Runner for Callback Function to Depth Topic

            Variables
            data: Input frame as ROS Image message type
        """

        runner_source = "depth", 
        pub_object  = self.pub_depth


        ### - This section identical for both runners - ###
        try:
            # Convert Image to CV2 Frame
            cv_image = self.bridge.imgmsg_to_cv2(data, desired_encoding='passthrough')
            depth_array = np.array(cv_image, dtype=np.float32)

            # Frame MetaData
            frame_seq = data.header.seq
            frame_stamp = data.header.stamp
            frame_name = str(frame_stamp) + "_depth.tiff"

            # Save frame
            if self.param_saveimages:
                frame_path = os.path.join(self.path_ws, frame_name)
                cv2.imwrite(frame_path, depth_array)

        # Publish Image
            msg_img = self.bridge.cv2_to_imgmsg(cv_image, encoding="passthrough")
            pub_object.publish(msg_img)

        except rospy.ROSInterruptException:
            exit()
        except KeyboardInterrupt:
            exit()
        except CvBridgeError as e:
            print(e)






## Main
def main():

    
    # Setup ROS Node
    rospy.init_node("gesture_recorder", anonymous=False)
    rospy.loginfo("Launched Node: gesture_recorder")


    # Setup ROS Publishers
    pub_color = rospy.Publisher("/gesture_recorder/color", Image, queue_size=15)
    pub_depth = rospy.Publisher("/gesture_recorder/depth", Image, queue_size=15)


    # Setup Class
    recorder = RECORDER(pub_color, pub_depth)


    # Setup ROS Subscribers
    sub_color = rospy.Subscriber("/color/image_raw", Image, recorder.runner_color)
    sub_depth = rospy.Subscriber("/aligned_depth_to_color/image_raw", Image, recorder.runner_depth)


    # Auto-Run until launch file is shutdown
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()