import rclpy
import cv2
import mediapipe as mp
from rclpy.node import Node
from media_pipe_ros2_msg.msg import  MediaPipeHumanPoseList                            
from mediapipe.python.solutions.pose import PoseLandmark

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
NAME_POSE = [
    (PoseLandmark.NOSE), (PoseLandmark.LEFT_EYE_INNER),
    (PoseLandmark.LEFT_EYE), (PoseLandmark.LEFT_EYE_OUTER),
    (PoseLandmark.RIGHT_EYE_INNER), ( PoseLandmark.RIGHT_EYE),
    (PoseLandmark.RIGHT_EYE_OUTER), ( PoseLandmark.LEFT_EAR),
    (PoseLandmark.RIGHT_EAR), ( PoseLandmark.MOUTH_LEFT),
    (PoseLandmark.MOUTH_RIGHT), ( PoseLandmark.LEFT_SHOULDER),
    (PoseLandmark.RIGHT_SHOULDER), ( PoseLandmark.LEFT_ELBOW),
    (PoseLandmark.RIGHT_ELBOW), ( PoseLandmark.LEFT_WRIST),
    (PoseLandmark.RIGHT_WRIST), ( PoseLandmark.LEFT_PINKY),
    (PoseLandmark.RIGHT_PINKY), ( PoseLandmark.LEFT_INDEX),
    (PoseLandmark.RIGHT_INDEX), ( PoseLandmark.LEFT_THUMB),
    (PoseLandmark.RIGHT_THUMB), ( PoseLandmark.LEFT_HIP),
    (PoseLandmark.RIGHT_HIP), ( PoseLandmark.LEFT_KNEE),
    (PoseLandmark.RIGHT_KNEE), ( PoseLandmark.LEFT_ANKLE),
    (PoseLandmark.RIGHT_ANKLE), ( PoseLandmark.LEFT_HEEL),
    (PoseLandmark.RIGHT_HEEL), ( PoseLandmark.LEFT_FOOT_INDEX),
    (PoseLandmark.RIGHT_FOOT_INDEX)
]
cap = cv2.VideoCapture(0)

class PosePublisher(Node):

    def __init__(self):
        super().__init__('mediapipe_pose_publisher')
        self.publisher_ = self.create_publisher(MediaPipeHumanPoseList, '/mediapipe/human_pose_list', 10)
        

    def getimage_callback(self):
        mediapipehumanposelist = MediaPipeHumanPoseList() 
        

        with mp_pose.Pose(
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5) as pose:
            while cap.isOpened():

                success, image = cap.read()
                if not success:
                    print("Sem camera.")
                            
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)                
                image.flags.writeable = False
                results = pose.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                imageHeight, imageWidth, _ = image.shape

                    # Draw the pose annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
  
                
                if results.pose_landmarks != None:
                    index_pose = 0
                    for pose_landmarks in (results.pose_landmarks.landmark):
                        print(index_pose)
                        mediapipehumanposelist.human_pose_list[index_pose].name = str(NAME_POSE[index_pose])
                        mediapipehumanposelist.human_pose_list[index_pose].x = pose_landmarks.x
                        mediapipehumanposelist.human_pose_list[index_pose].y = pose_landmarks.y
                        mediapipehumanposelist.human_pose_list[index_pose].visibility = pose_landmarks.visibility
                        index_pose = index_pose +1

                    mediapipehumanposelist.num_humans = 1
                    self.publisher_.publish(mediapipehumanposelist)
                else: # responsavel por mandar 0 nos topicos quando corpo nao esta na tela
                    index_pose = 0
                    for point in mp_pose.PoseLandmark:                          
                                                                                          
                        mediapipehumanposelist.human_pose_list[index_pose].name = str(NAME_POSE[index_pose])
                        mediapipehumanposelist.human_pose_list[index_pose].x = 0.0
                        mediapipehumanposelist.human_pose_list[index_pose].y = 0.0
                        mediapipehumanposelist.human_pose_list[index_pose].visibility = 0.0
                        index_pose = index_pose +1

                
                    mediapipehumanposelist.num_humans = 1
                    self.publisher_.publish(mediapipehumanposelist)

                cv2.imshow('MediaPipe Pose', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break        

def main(args=None):
    rclpy.init(args=args)

    pose_publisher = PosePublisher()
    pose_publisher.getimage_callback()    
    
    cap.release()
    
    rclpy.spin(pose_publisher)

    pose_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()