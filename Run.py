import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import sqlite3
import datetime

class AutonomousSurveillanceRobot:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('autonomous_surveillance_robot')

        # Initialize ROS publishers and subscribers
        self.image_subscriber = rospy.Subscriber('/camera/image_raw', Image, self.on_image_received)
        self.map_publisher = rospy.Publisher('/map', Image, queue_size=10)
        self.object_positions_publisher = rospy.Publisher('/object_positions', String, queue_size=10)

        # Initialize SLAM algorithm
        self.slam = cv2.ORB_SLAM3_create()

        # Initialize OpenCV bridge for converting images
        self.cv_bridge = CvBridge()

        # Initialize SQLite3 database
        self.conn = None
        self.c = None
        self.connect_to_database()
        self.create_surveillance_table()

    def connect_to_database(self):
        try:
            self.conn = sqlite3.connect('surveillance_data.db')
            self.c = self.conn.cursor()
        except sqlite3.Error as e:
            rospy.logerr("Error connecting to the database: %s", str(e))
            rospy.signal_shutdown("Database connection error")

    def create_surveillance_table(self):
        try:
            self.c.execute('''CREATE TABLE IF NOT EXISTS surveillance_data (
                timestamp DATETIME PRIMARY KEY,
                object_class TEXT,
                x_position FLOAT,
                y_position FLOAT,
                z_position FLOAT
            )''')
            self.conn.commit()
        except sqlite3.Error as e:
            rospy.logerr("Error creating the surveillance table: %s", str(e))
            rospy.signal_shutdown("Database table creation error")

    def on_image_received(self, image_message):
        try:
            # Convert ROS image message to OpenCV image
            image = self.cv_bridge.imgmsg_to_cv2(image_message, desired_encoding="bgr8")

            # Run SLAM algorithm
            self.slam.processFrame(image)

            # Run object detection algorithm
            object_detections = self.detect_objects(image)

            # Publish the map as an image
            map_image_msg = self.cv_bridge.cv2_to_imgmsg(self.slam.getFrame(), encoding="bgr8")
            self.map_publisher.publish(map_image_msg)

            # Publish object positions
            object_positions_msg = ', '.join([f"{detection[0]}, {detection[1]}, {detection[2]}, {detection[3]}" for detection in object_detections])
            self.object_positions_publisher.publish(object_positions_msg)

            # Save the surveillance data to the database
            self.save_surveillance_data(object_detections)

        except CvBridgeError as e:
            rospy.logerr("Error converting image message: %s", str(e))

    def detect_objects(self, image):
        # Implement object detection logic here
        # Replace this with your actual object detection code
        # Example:
        object_detections = []

        # Your object detection code goes here

        return object_detections

    def save_surveillance_data(self, object_detections):
        timestamp = datetime.datetime.now()
        for detection in object_detections:
            try:
                self.c.execute('''INSERT INTO surveillance_data (timestamp, object_class, x_position, y_position, z_position)
                                VALUES (?, ?, ?, ?, ?)''',
                                (timestamp, detection[5], detection[0], detection[1], detection[2]))
                self.conn.commit()
            except sqlite3.Error as e:
                rospy.logerr("Error saving surveillance data: %s", str(e))

if __name__ == '__main__':
    robot = AutonomousSurveillanceRobot()
    rospy.spin()
