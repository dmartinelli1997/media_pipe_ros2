import rclpy
import cv2
import mediapipe as mp
from rclpy.node import Node
from media_pipe_ros2_msg.msg import HandPoint,MediaPipeHumanHand,MediaPipeHumanHandList
                            

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

class HandsPublisher(Node):

    def __init__(self):
        super().__init__('mediapipe_publisher')
        self.publisher_ = self.create_publisher(MediaPipeHumanHandList, '/mediapipe/human_hand_list', 10)
        

    def getimage_callback(self):
        mediapipehumanlist = MediaPipeHumanHandList() 
        mediapipehuman = MediaPipeHumanHand()
        points = HandPoint()

        with mp_hands.Hands(
                static_image_mode=False,
                min_detection_confidence=0.7, 
                min_tracking_confidence=0.7, 
                max_num_hands=2) as hands:
            while cap.isOpened():

                success, image = cap.read()
                if not success:
                    print("Sem camera.")
                            
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)                
                image.flags.writeable = False
                results = hands.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                imageHeight, imageWidth, _ = image.shape
                
                if results.multi_hand_landmarks != None:
                    hand_number_screen = 0 # index de controle de quantas maos aparecem na tela                  
                    #esse for passa pela quantidades de mão na tela setada como maximo 2 no momento
                    for hand_landmarks, handedness in zip(results.multi_hand_landmarks,results.multi_handedness):
                                            
                        if handedness.classification[0].label == "Right":
                            mp_drawing.draw_landmarks(
                            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                            index_point = 0
                            
                            for point in mp_hands.HandLandmark:                                
                                normalizedLandmark = hand_landmarks.landmark[point]                                                                
                                mediapipehuman.right_hand_key_points[index_point].name = str(point) 
                                mediapipehuman.right_hand_key_points[index_point].x = normalizedLandmark.x
                                mediapipehuman.right_hand_key_points[index_point].y = normalizedLandmark.y
                                mediapipehuman.right_hand_key_points[index_point].z = normalizedLandmark.z                                
                                if hand_number_screen == 0:
                                    mediapipehuman.left_hand_key_points[index_point].name = str(point) 
                                    mediapipehuman.left_hand_key_points[index_point].x = 0.0
                                    mediapipehuman.left_hand_key_points[index_point].y = 0.0
                                    mediapipehuman.left_hand_key_points[index_point].z = 0.0
                                index_point = index_point +1
                            hand_number_screen = hand_number_screen +1

                        elif handedness.classification[0].label == "Left":
                            mp_drawing.draw_landmarks(
                            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                            index_point = 0
                            
                            for point in mp_hands.HandLandmark:
                                
                                normalizedLandmark = hand_landmarks.landmark[point]  
                                points.name = str(point)                            
                                mediapipehuman.left_hand_key_points[index_point].name = str(point) 
                                mediapipehuman.left_hand_key_points[index_point].x = normalizedLandmark.x
                                mediapipehuman.left_hand_key_points[index_point].y = normalizedLandmark.y 
                                mediapipehuman.left_hand_key_points[index_point].z = normalizedLandmark.z
                                
                                if hand_number_screen == 0:
                                    mediapipehuman.right_hand_key_points[index_point].name = str(point) 
                                    mediapipehuman.right_hand_key_points[index_point].x = 0.0
                                    mediapipehuman.right_hand_key_points[index_point].y = 0.0
                                    mediapipehuman.right_hand_key_points[index_point].z = 0.0
                                index_point = index_point +1
                            hand_number_screen = hand_number_screen +1

                    mediapipehumanlist.human_hand_list.right_hand_key_points = mediapipehuman.right_hand_key_points
                    mediapipehumanlist.human_hand_list.left_hand_key_points = mediapipehuman.left_hand_key_points
                    mediapipehumanlist.num_humans = 1
                    self.publisher_.publish(mediapipehumanlist)
                else: # responsavel por mandar 0 nos topicos quando as duas maos nao estao na tela
                    index_point = 0
                    for point in mp_hands.HandLandmark:                          
                                                                                          
                        mediapipehuman.right_hand_key_points[index_point].name = str(point) 
                        mediapipehuman.right_hand_key_points[index_point].x = 0.0
                        mediapipehuman.right_hand_key_points[index_point].y = 0.0
                        mediapipehuman.right_hand_key_points[index_point].z = 0.0 
                        mediapipehuman.left_hand_key_points[index_point].name = str(point) 
                        mediapipehuman.left_hand_key_points[index_point].x = 0.0
                        mediapipehuman.left_hand_key_points[index_point].y = 0.0
                        mediapipehuman.left_hand_key_points[index_point].z = 0.0
                        index_point = index_point + 1 

                    mediapipehumanlist.human_hand_list.right_hand_key_points = mediapipehuman.right_hand_key_points
                    mediapipehumanlist.human_hand_list.left_hand_key_points = mediapipehuman.left_hand_key_points
                    mediapipehumanlist.num_humans = 1
                    self.publisher_.publish(mediapipehumanlist)

                cv2.imshow('MediaPipe Hands', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break        

def main(args=None):
    rclpy.init(args=args)

    hands_publisher = HandsPublisher()
    hands_publisher.getimage_callback()
    
    
    cap.release()
    
    rclpy.spin(hands_publisher)

    hands_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()