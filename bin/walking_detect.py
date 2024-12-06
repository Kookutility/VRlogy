import time
import numpy as np

class InPlaceWalkingDetector:
    def __init__(self):
        self.left_ankle_heights = []
        self.right_ankle_heights = []
        self.left_knee_angles = []
        self.right_knee_angles = []
        self.time_stamps = []
        self.window_size = 30  # 분석할 프레임 수
        self.crossing_threshold = 0.02  # 교차 판단 임계값
        self.walking_threshold = 1.5    # 걷기 감지 임계값
        self.amplitude_threshold = 0.05 # 진폭 임계값
        self.knee_angle_threshold = 10  # 무릎 각도 변화 임계값 (도 단위)
        self.in_place_walking_detected = False
        self.frame_interval = 1 / 30    # FPS 30 가정

    def calculate_knee_angle(self, hip, knee, ankle):
        # 각도 계산
        thigh = hip - knee
        calf = ankle - knee
        cos_theta = np.dot(thigh, calf) / (np.linalg.norm(thigh) * np.linalg.norm(calf) + 1e-8)
        angle = np.arccos(np.clip(cos_theta, -1.0, 1.0))
        return np.degrees(angle)

    def detect_in_place_walking(self, pose3d):
        if pose3d is None or len(pose3d) < 29:
            return False

        # 주요 관절 좌표 추출
        left_ankle = pose3d[5]     # 왼쪽 발목
        right_ankle = pose3d[0]    # 오른쪽 발목
        left_knee = pose3d[4]      # 왼쪽 무릎
        right_knee = pose3d[1]     # 오른쪽 무릎
        left_hip = pose3d[3]       # 왼쪽 엉덩이
        right_hip = pose3d[2]      # 오른쪽 엉덩이
        left_shoulder = pose3d[12] # 왼쪽 어깨
        right_shoulder = pose3d[13]# 오른쪽 어깨

        # 신장 추정
        torso_length_left = np.linalg.norm(left_shoulder - left_hip)
        torso_length_right = np.linalg.norm(right_shoulder - right_hip)
        estimated_height = (torso_length_left + torso_length_right)

        if estimated_height == 0:
            return False

        # 발목 높이를 신장으로 정규화
        left_ankle_height = left_ankle[1] / estimated_height
        right_ankle_height = right_ankle[1] / estimated_height

        # 무릎 각도 계산
        left_knee_angle = self.calculate_knee_angle(left_hip, left_knee, left_ankle)
        right_knee_angle = self.calculate_knee_angle(right_hip, right_knee, right_ankle)

        # 데이터 저장
        self.left_ankle_heights.append(left_ankle_height)
        self.right_ankle_heights.append(right_ankle_height)
        self.left_knee_angles.append(left_knee_angle)
        self.right_knee_angles.append(right_knee_angle)

        # 히스토리 초과 시 제거
        if len(self.left_ankle_heights) > self.window_size:
            self.left_ankle_heights.pop(0)
            self.right_ankle_heights.pop(0)
            self.left_knee_angles.pop(0)
            self.right_knee_angles.pop(0)

        # 데이터가 충분하지 않으면 False 반환
        if len(self.left_ankle_heights) < self.window_size:
            return False

        # 발목 높이 변화의 진폭 계산
        left_amplitude = max(self.left_ankle_heights) - min(self.left_ankle_heights)
        right_amplitude = max(self.right_ankle_heights) - min(self.right_ankle_heights)
        average_amplitude = (left_amplitude + right_amplitude) / 2

        # 무릎 각도 변화 계산
        left_knee_angle_change = max(self.left_knee_angles) - min(self.left_knee_angles)
        right_knee_angle_change = max(self.right_knee_angles) - min(self.right_knee_angles)
        average_knee_angle_change = (left_knee_angle_change + right_knee_angle_change) / 2

        # 발목 높이 차이 계산 및 부호 변화 검출
        ankle_height_diffs = np.array(self.left_ankle_heights) - np.array(self.right_ankle_heights)
        zero_crossings = np.where(np.diff(np.sign(ankle_height_diffs)))[0]

        # 히스토리의 총 시간 계산
        time_diff = self.frame_interval * (self.window_size - 1)  # 초 단위

        # 교차 빈도 계산
        crossing_rate = len(zero_crossings) / time_diff if time_diff > 0 else 0

        # 걷기 감지 조건 적용
        if (crossing_rate >= self.walking_threshold and
            average_amplitude >= self.amplitude_threshold and
            average_knee_angle_change >= self.knee_angle_threshold):
            self.in_place_walking_detected = True
        else:
            self.in_place_walking_detected = False

        # 결과 출력 (옵션)
        print(f"Crossing Rate: {crossing_rate:.2f} Hz")
        print(f"Average Amplitude: {average_amplitude:.4f}")
        print(f"Average Knee Angle Change: {average_knee_angle_change:.2f} degrees")
        print(f"In-Place Walking Detected: {self.in_place_walking_detected}\n")

        return self.in_place_walking_detected
