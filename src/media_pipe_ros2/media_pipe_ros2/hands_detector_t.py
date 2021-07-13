import cv2
import mediapipe as mp
import time
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
	
with mp_hands.Hands(
  static_image_mode=False, 
  min_detection_confidence=0.7, 
  min_tracking_confidence=0.7, 
  max_num_hands=2) as hands:

  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Sem camera.")
      continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    image.flags.writeable = False
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    imageHeight, imageWidth, _ = image.shape
    if results.multi_hand_landmarks != None:
      for hand_landmarks, handedness in zip(results.multi_hand_landmarks,results.multi_handedness):
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)        
        for point in mp_hands.HandLandmark:
          normalizedLandmark = hand_landmarks.landmark[point]
          
          print(handedness.classification[0].label)# direita ou esquerda
          print(handedness.classification[0].score)# probabilidade de ser a mao correta
          print(point) # nome/ qual ponto
          print(normalizedLandmark) # posiçao do ponto
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
