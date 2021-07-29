# media_pipe_ros2
<!-- ABOUT THE PROJECT -->
## About The Project
ROS2 package that utilizes the MediaPipe library.
https://mediapipe.dev/

Functionalities:
- [ ] Face Detection
- [x] Face Mesh
- [ ] Iris
- [x] Hands
- [x] Pose
- [x] Holistic
- [ ] Selfie Segmentation
- [ ] Hair Segmentation
- [ ] Object Detection
- [ ] Box Tracking
- [ ] Instant Motion Tracking
- [ ] Objectron
- [ ] KNIFT
- [ ] AutoFlip
- [ ] MediaSequence
- [ ] YouTube 8M
<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
* Python3
* OpenCV
    ```sh
  pip install opencv-python
  ```
* Media Pipe
  ```sh
  python3 -m venv mp_env && source mp_env/bin/activate
  ```
  ```sh
  pip install mediapipe
  ```
### Installation
1. Clone this repository into your ROS2 workspace/src directory.
 ```
  git clone https://github.com/dmartinelli1997/media_pipe_ros2
  ``` 
2. Run colcon_build from your ROS2 workspace directory.
<!-- USAGE EXAMPLES -->
## Usage
From another bash:
  ```sh
  source ros2_workspace/install/setup.bash
  ros2 run media_ṕipe_ros2 hands_detector
  ```
<!-- CONTACT -->
## Contact

Dieisson Martinelli - dmartinelli1997@gmail.com
