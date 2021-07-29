import rclpy
import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
from rclpy.node import Node
from media_pipe_ros2_msg.msg import  MediaPipeHumanFaceMeshList                            
from mediapipe.python.solutions.pose import PoseLandmark

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
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

class FaceMeshPublisher(Node):

    def __init__(self):
        super().__init__('mediapipe_face_mesh_publisher')
        self.publisher_ = self.create_publisher(MediaPipeHumanFaceMeshList, '/mediapipe/human_face_mesh_list', 10)
        

    def getimage_callback(self):
        mediapipehumanfacemeshlist = MediaPipeHumanFaceMeshList() 
        
        drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        with mp_face_mesh.FaceMesh(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
            while cap.isOpened():

                success, image = cap.read()
                if not success:
                    print("Sem camera.")
                            
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)                
                image.flags.writeable = False
                results = face_mesh.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                imageHeight, imageWidth, _ = image.shape

                    # Draw the pose annotation on the image.
                image.flags.writeable = True                
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                teste = []
                if results.multi_face_landmarks:
                    index_face_mesh = 0
                    
                    while index_face_mesh <= 467:
                        print(index_face_mesh )
                        teste.append(results.multi_face_landmarks[0].landmark[index_face_mesh]) 
                        mediapipehumanfacemeshlist.human_face_mesh_list[index_face_mesh].x = results.multi_face_landmarks[0].landmark[index_face_mesh].x
                        mediapipehumanfacemeshlist.human_face_mesh_list[index_face_mesh].y = results.multi_face_landmarks[0].landmark[index_face_mesh].y
                        mediapipehumanfacemeshlist.human_face_mesh_list[index_face_mesh].z = results.multi_face_landmarks[0].landmark[index_face_mesh].z
                        index_face_mesh = index_face_mesh +1
                        
                
                    landmark_subset = landmark_pb2.NormalizedLandmarkList(landmark = teste)
                    mp_drawing.draw_landmarks(
                            image=image,
                            landmark_list=landmark_subset,
                            connections=mp_face_mesh.FACE_CONNECTIONS,
                            landmark_drawing_spec=drawing_spec,
                            connection_drawing_spec=drawing_spec) 
                        
                    mediapipehumanfacemeshlist.num_humans = 1
                    self.publisher_.publish(mediapipehumanfacemeshlist)
                else: # responsavel por mandar 0 nos topicos quando corpo nao esta na tela
                    index_face_mesh = 0
                    while index_face_mesh <= 467:                          
                                                                                          
                        mediapipehumanfacemeshlist.human_face_mesh_list[index_face_mesh].x = 0.0
                        mediapipehumanfacemeshlist.human_face_mesh_list[index_face_mesh].y = 0.0
                        mediapipehumanfacemeshlist.human_face_mesh_list[index_face_mesh].z = 0.0
                        index_face_mesh = index_face_mesh +1

                
                    mediapipehumanfacemeshlist.num_humans = 1
                    self.publisher_.publish(mediapipehumanfacemeshlist)

                cv2.imshow('MediaPipe Face Mesh', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break        

def main(args=None):
    rclpy.init(args=args)

    face_mesh_publisher = FaceMeshPublisher()
    face_mesh_publisher.getimage_callback()    
    
    cap.release()
    
    rclpy.spin(face_mesh_publisher)

    face_mesh_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()