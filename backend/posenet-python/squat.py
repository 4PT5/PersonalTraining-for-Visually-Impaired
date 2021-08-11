def squat_down(keypoint):
    # keypoint[11][0] : 왼쪽 골반 y좌표, keypoint[13][0] : 왼쪽 무릎 y좌표
    # keypoint[12][0] : 오른쪽 골반 y좌표, keypoint[14][0] : 오른쪽 무릎 y좌표
    hip_knee_l = keypoint[11][0]-keypoint[13][0]
    hip_knee_r = keypoint[12][0]-keypoint[14][0]
    hip_knee = (hip_knee_l+hip_knee_r)/2
    MAX_LIMIT = 50
    MIN_LIMIT = -60
    print("1. squat_down")
    print(hip_knee)
    if(hip_knee > MAX_LIMIT):
        print("조금 일어나세요.")
        return False
    elif(MIN_LIMIT <= hip_knee <= MAX_LIMIT):
        print("checkpoint #2 OK")
        return True
    else:
        print("조금 더 앉으세요")
        return False


def main(keypoint):
    if(squat_down(keypoint) and squat_straight(keypoint) and squat_knee_angle(keypoint)):
        return True
    else:
        return False
