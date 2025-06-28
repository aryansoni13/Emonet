import cv2
import mediapipe as mp
import numpy as np
import time
import os
from collections import deque
from datetime import datetime

class EmotionAvatar:
    def __init__(self):
        # Mediapipe setup
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False, 
            max_num_faces=1, 
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.drawing_utils = mp.solutions.drawing_utils
        self.LIPS = self.mp_face_mesh.FACEMESH_LIPS
        self.LEFT_IRIS = [468, 469, 470, 471]
        self.RIGHT_IRIS = [473, 474, 475, 476]
        
        # Enhanced emotion settings
        self.emotions = {
            "happy": {"emoji": "😊", "color": (0, 255, 0), "description": "Joyful and cheerful"},
            "sad": {"emoji": "😢", "color": (255, 0, 0), "description": "Down and melancholic"},
            "angry": {"emoji": "😠", "color": (0, 0, 255), "description": "Frustrated and upset"},
            "surprise": {"emoji": "😲", "color": (0, 255, 255), "description": "Shocked and amazed"},
            "neutral": {"emoji": "😐", "color": (255, 255, 255), "description": "Calm and composed"},
            "fear": {"emoji": "😨", "color": (255, 140, 0), "description": "Scared and anxious"},
            "disgust": {"emoji": "🤢", "color": (138, 43, 226), "description": "Repulsed and disturbed"}
        }
        
        # Tracking variables
        self.emotion_history = deque(maxlen=30)
        self.current_emotion = "neutral"
        self.emotion_confidence = 0.0
        self.fps_history = deque(maxlen=10)
        self.avg_fps = 0
        self.show_debug = False
        self.avatar_style = "mesh"
        
        # Create screenshots directory
        os.makedirs("screenshots", exist_ok=True)

    def distance(self, p1, p2):
        return np.linalg.norm(np.array([p1.x, p1.y]) - np.array([p2.x, p2.y]))

    def get_emotion_features(self, landmarks):
        """Extract enhanced emotion features"""
        top_lip = landmarks[13]
        bottom_lip = landmarks[14]
        left_mouth = landmarks[61]
        right_mouth = landmarks[291]
        left_eye_top = landmarks[159]
        left_eye_bottom = landmarks[145]
        right_eye_top = landmarks[386]
        right_eye_bottom = landmarks[374]
        left_eyebrow = landmarks[70]
        right_eyebrow = landmarks[300]
        
        face_width = self.distance(landmarks[234], landmarks[454])
        
        features = {
            'mouth_open': self.distance(top_lip, bottom_lip) / face_width,
            'mouth_stretch': self.distance(left_mouth, right_mouth) / face_width,
            'eye_open': (self.distance(left_eye_top, left_eye_bottom) + 
                        self.distance(right_eye_top, right_eye_bottom)) / (2 * face_width),
            'eyebrow_height': (self.distance(left_eyebrow, left_eye_top) + 
                              self.distance(right_eyebrow, right_eye_top)) / (2 * face_width)
        }
        
        # Sadness detection
        eye_top_avg = (left_eye_top.y + right_eye_top.y) / 2
        eye_bottom_avg = (left_eye_bottom.y + right_eye_bottom.y) / 2
        iris_avg = landmarks[468].y
        eye_center_y = (eye_top_avg + eye_bottom_avg) / 2
        features['sad_offset'] = iris_avg - eye_center_y
        
        return features

    def get_emotion(self, landmarks):
        """Enhanced emotion detection with confidence"""
        features = self.get_emotion_features(landmarks)
        
        emotion_scores = {emotion: 0.0 for emotion in self.emotions.keys()}
        
        # Emotion detection rules
        if features['mouth_stretch'] > 0.40 and features['mouth_open'] < 0.06:
            emotion_scores['happy'] = min(1.0, features['mouth_stretch'] * 2)
        
        if features['mouth_open'] >= 0.12:
            emotion_scores['surprise'] = min(1.0, features['mouth_open'] * 8)
        
        if 0.06 < features['mouth_open'] < 0.12 and features['eyebrow_height'] > 0.05:
            emotion_scores['fear'] = min(1.0, features['mouth_open'] * 10)
        
        if features['sad_offset'] > 0.01 and features['eye_open'] < 0.04:
            emotion_scores['sad'] = min(1.0, abs(features['sad_offset']) * 50)
        
        if features['mouth_open'] < 0.03 and features['mouth_stretch'] < 0.38:
            emotion_scores['disgust'] = 0.8
        
        if features['eye_open'] > 0.096 and features['mouth_open'] < 0.06:
            emotion_scores['angry'] = 0.7
        
        emotion_scores['neutral'] = 0.5
        
        detected_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = emotion_scores[detected_emotion]
        
        if self.show_debug:
            print(f"[DEBUG] Features: {features}")
            print(f"[DEBUG] Detected: {detected_emotion} (confidence: {confidence:.2f})")
        
        return detected_emotion, confidence

    def draw_avatar(self, frame, landmarks, emotion, h, w):
        """Draw avatar with different styles"""
        avatar_canvas = np.zeros_like(frame)
        color = self.emotions[emotion]["color"]
        
        if self.avatar_style == "mesh":
            self.drawing_utils.draw_landmarks(
                avatar_canvas, landmarks,
                self.mp_face_mesh.FACEMESH_TESSELATION, None,
                self.drawing_utils.DrawingSpec(color=color, thickness=1, circle_radius=1)
            )
        elif self.avatar_style == "points":
            for landmark in landmarks.landmark:
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(avatar_canvas, (cx, cy), 2, color, -1)
        else:  # minimal
            self.drawing_utils.draw_landmarks(
                avatar_canvas, landmarks,
                self.mp_face_mesh.FACEMESH_CONTOURS, None,
                self.drawing_utils.DrawingSpec(color=color, thickness=2, circle_radius=2)
            )
        
        # Draw lips and eyes
        self.drawing_utils.draw_landmarks(
            avatar_canvas, landmarks, self.LIPS, None,
            self.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
        )
        
        # Draw iris
        for idx in self.LEFT_IRIS + self.RIGHT_IRIS:
            pt = landmarks.landmark[idx]
            cx, cy = int(pt.x * w), int(pt.y * h)
            cv2.circle(avatar_canvas, (cx, cy), 3, (0, 255, 255), -1)
        
        return avatar_canvas

    def draw_ui(self, frame, emotion, fps):
        """Draw enhanced UI elements"""
        label = f"{emotion.upper()} {self.emotions[emotion]['emoji']}"
        description = self.emotions[emotion]['description']
        
        # Background for text
        cv2.rectangle(frame, (5, 5), (400, 120), (0, 0, 0), -1)
        cv2.rectangle(frame, (5, 5), (400, 120), self.emotions[emotion]["color"], 2)
        
        cv2.putText(frame, label, (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 
                    1.2, self.emotions[emotion]["color"], 3)
        cv2.putText(frame, description, (15, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, (200, 200, 200), 2)
        cv2.putText(frame, f"FPS: {int(fps)}", (15, 85), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, (100, 255, 100), 2)
        cv2.putText(frame, f"Confidence: {self.emotion_confidence:.2f}", (15, 105), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 100), 2)
        
        # Controls info
        controls_text = "ESC: Quit | S: Screenshot | D: Debug | A: Avatar Style"
        cv2.putText(frame, controls_text, (10, frame.shape[0] - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)

    def take_screenshot(self, frame, avatar_frame):
        """Take a screenshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/emotion_avatar_{timestamp}.jpg"
        combined = np.hstack([frame, avatar_frame])
        cv2.imwrite(filename, combined)
        print(f"Screenshot saved: {filename}")

    def run(self):
        """Main application loop"""
        print("🎭 Real-Time Emotion Avatar")
        print("Controls: ESC=Quit, S=Screenshot, D=Debug, A=Avatar Style")
        print()
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Error: Could not open webcam")
            return
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        prev_time = time.time()
        avatar_styles = ["mesh", "points", "minimal"]
        style_index = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Error: Could not read frame")
                    break

                frame = cv2.flip(frame, 1)
                h, w, _ = frame.shape
                
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.face_mesh.process(rgb)
                
                avatar_canvas = np.zeros_like(frame)
                emotion = "neutral"
                confidence = 0.0

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        emotion, confidence = self.get_emotion(face_landmarks.landmark)
                        avatar_canvas = self.draw_avatar(frame, face_landmarks, emotion, h, w)
                
                # Update tracking
                self.current_emotion = emotion
                self.emotion_confidence = confidence
                self.emotion_history.append(emotion)
                
                # Calculate FPS
                curr_time = time.time()
                fps = 1 / (curr_time - prev_time) if prev_time else 0
                prev_time = curr_time
                
                self.fps_history.append(fps)
                self.avg_fps = sum(self.fps_history) / len(self.fps_history)
                
                # Draw UI
                self.draw_ui(frame, emotion, self.avg_fps)
                self.draw_ui(avatar_canvas, emotion, self.avg_fps)
                
                # Display windows
                cv2.imshow("Webcam Feed", cv2.resize(frame, (640, 480)))
                cv2.imshow("Emotion Avatar", cv2.resize(avatar_canvas, (640, 480)))

                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                    break
                elif key == ord('s'):  # Screenshot
                    self.take_screenshot(frame, avatar_canvas)
                elif key == ord('d'):  # Toggle debug
                    self.show_debug = not self.show_debug
                    print(f"Debug mode: {'ON' if self.show_debug else 'OFF'}")
                elif key == ord('a'):  # Cycle avatar style
                    style_index = (style_index + 1) % len(avatar_styles)
                    self.avatar_style = avatar_styles[style_index]
                    print(f"Avatar style: {self.avatar_style}")

        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("👋 Goodbye!")

if __name__ == "__main__":
    avatar = EmotionAvatar()
    avatar.run()
