import math

def getDegree(key1, key2, key3):
    x = math.atan((key1[1] - key2[1]) / (key1[0] - key2[0])) - math.atan((key3[1] - key2[1]) / (key3[0] - key2[0]))
    return x*180/math.pi

def squat_straight(keypoint):
    # keypoint[17] : 척수상, keypoint[18] : 척수중, keypoint[19] : 척추하
    MIN_LIMIT = 175
    MAX_LIMIT = 185
    angle = getDegree(keypoint[17], keypoint[18], keypoint[19])

    print("2. squat_straight")
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
    LIMIT = 90
    right_angle = getDegree(keypoint[12], keypoint[14], keypoint[16])
    left_angle = getDegree(keypoint[11], keypoint[13], keypoint[15])
    angle = (right_angle + left_angle) / 2

    print("3. squat_knee_angle")
    if angle <= LIMIT:
        print("OK")
        return True
    else:
        print("무릎이 발보다 더 나와있습니다.")
        return False


