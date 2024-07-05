import time
import numpy as np

class InPlaceWalkingDetector:
    def __init__(self):
        self.left_ankle_positions = []
        self.right_ankle_positions = []
        self.max_history = 10  # 기록할 프레임 수를 줄여 더 빠르게 인식
        self.position_threshold = 0.05  # 위치 변화 임계값
        self.height_threshold = 1.0  # 높이 변화 임계값
        self.min_height_threshold = 0.1  # 최소 높이 변화 임계값
        self.horizontal_movement_threshold = 0.6  # 수평 이동 임계값
        self.last_in_place_walk_time = 0  # 마지막으로 제자리 걸음이 감지된 시간
        self.in_place_walking_detected = False  # 제자리 걸음이 감지되었는지 여부

    def detect_in_place_walking(self, pose3d):
        if pose3d is None or len(pose3d) < 6:
            return False

        ankle_left = pose3d[0]
        ankle_right = pose3d[5]

        # 상체만 감지되는 상황에서는 ankle 좌표가 추정된 값일 가능성이 높음
        if self.is_upper_body_only(pose3d):
            self.in_place_walking_detected = False  # 상체만 감지된 경우 감지 상태 리셋
            return False

        if not self.is_valid_ankle_position(ankle_left) or not self.is_valid_ankle_position(ankle_right):
            self.in_place_walking_detected = False  # 유효하지 않은 발목 위치일 경우 감지 상태 리셋
            return False

        self.left_ankle_positions.append(ankle_left)
        self.right_ankle_positions.append(ankle_right)

        if len(self.left_ankle_positions) > self.max_history:
            self.left_ankle_positions.pop(0)
            self.right_ankle_positions.pop(0)

        if len(self.left_ankle_positions) < self.max_history:
            return False

        left_ankle_movement = np.linalg.norm(np.max(self.left_ankle_positions, axis=0) - np.min(self.left_ankle_positions, axis=0))
        right_ankle_movement = np.linalg.norm(np.max(self.right_ankle_positions, axis=0) - np.min(self.right_ankle_positions, axis=0))

        left_ankle_height_movement = np.max(self.left_ankle_positions, axis=0)[1] - np.min(self.left_ankle_positions, axis=0)[1]
        right_ankle_height_movement = np.max(self.right_ankle_positions, axis=0)[1] - np.min(self.right_ankle_positions, axis=0)[1]

        left_ankle_horizontal_movement = np.linalg.norm(
            np.max(self.left_ankle_positions, axis=0)[:2] - np.min(self.left_ankle_positions, axis=0)[:2]
        )
        right_ankle_horizontal_movement = np.linalg.norm(
            np.max(self.right_ankle_positions, axis=0)[:2] - np.min(self.right_ankle_positions, axis=0)[:2]
        )

        height_movement = (left_ankle_height_movement + right_ankle_height_movement) / 2
        horizontal_movement = (left_ankle_horizontal_movement + right_ankle_horizontal_movement) / 2

        is_in_place_walking = horizontal_movement < self.horizontal_movement_threshold and self.min_height_threshold < height_movement < self.height_threshold

        self.in_place_walking_detected = is_in_place_walking
        return is_in_place_walking

    def is_upper_body_only(self, pose3d):
        # 상체만 감지되는 상황인지 확인하는 로직 (예: 발목의 Y좌표가 기준보다 높음)
        upper_body_threshold = -0.5  # 이 값을 조정하여 상체/하체의 기준을 설정
        return all(joint[1] > upper_body_threshold for joint in pose3d)

    def is_valid_ankle_position(self, ankle):
        # 발목 위치가 유효한지 확인하는 로직 추가 (예: 임계값 범위 내에 있는지 확인)
        # 여기서는 단순히 모든 값이 0이 아닌 경우를 유효한 값으로 간주
        return not np.all(ankle == 0)
