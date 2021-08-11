import math


def getDegree(key1, key2, key3):
    x = math.atan((key1[0] - key2[0]) / (key1[1] - key2[1])) - \
        math.atan((key3[0] - key2[0]) / (key3[1] - key2[1]))
    return x*180/math.pi


def squat_down(keypoint):
    # keypoint[11][0] : 왼쪽 골반 y좌표, keypoint[13][0] : 왼쪽 무릎 y좌표
    # keypoint[12][0] : 오른쪽 골반 y좌표, keypoint[14][0] : 오른쪽 무릎 y좌표
    hip_knee_l = keypoint[11][0]-keypoint[13][0]
    hip_knee_r = keypoint[12][0]-keypoint[14][0]
    hip_knee = (hip_knee_l+hip_knee_r)/2
    MAX_LIMIT = 50
    MIN_LIMIT = -60
    print("===================================================")
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


def squat_straight(keypoint):
    # keypoint[17] : 척수상, keypoint[18] : 척수중, keypoint[19] : 척추하
    MIN_LIMIT = -10
    MAX_LIMIT = 10
    angle = getDegree(keypoint[17], keypoint[18], keypoint[19])

    print("------------------")
    print("2. squat_straight")
    print(angle)
    if MIN_LIMIT <= angle <= MAX_LIMIT:
        print("OK")
        return True

    elif angle < MIN_LIMIT:
        print("조금 더 허리를 세워주세요.")
        return False

    elif angle > MAX_LIMIT:
        print("조금 더 허리를 구부려주세요.")
        return False


def squat_knee_angle(keypoint):
    # keypoint[12] : 오른쪽골반, keypoint[14] : 오른쪽무릎, keypoint[16] : 오른쪽발목
    # keypoint[11] : 왼쪽골반, keypoint[13] : 왼쪽무릎, keypoint[15] : 왼쪽발목
    LIMIT = 75
    right_angle = getDegree(keypoint[12], keypoint[14], keypoint[16])
    left_angle = getDegree(keypoint[11], keypoint[13], keypoint[15])
    angle = abs((right_angle + left_angle) / 2)

    print("------------------")
    print("3. squat_knee_angle")
    print(angle)
    if angle >= LIMIT:
        print("OK")
        return True
    else:
        print("무릎이 발보다 더 나와있습니다.")
        return False


def main(keypoint):
    if(squat_down(keypoint) and squat_straight(keypoint) and squat_knee_angle(keypoint)):
        return True
    else:
        return False
