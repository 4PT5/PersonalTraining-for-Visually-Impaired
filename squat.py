import math
import imageDetect


def getDegree(key1, key2, key3):
    x = math.atan((key1[0] - key2[0]) / (key1[1] - key2[1])) - \
        math.atan((key3[0] - key2[0]) / (key3[1] - key2[1]))
    return x*180/math.pi


def setting():
    global d_LIMIT, s_LIMIT, LIMIT
    arr = imageDetect.main()
    d_LIMIT = ((arr[11][0]-arr[13][0])+(arr[12][0]-arr[14][0]))/2
    s_LIMIT = getDegree(arr[17], arr[18], arr[19])
    LIMIT = abs(getDegree(arr[12], arr[14], arr[16]) +
                getDegree(arr[11], arr[13], arr[15]))/2


def squat_down(keypoint):
    # keypoint[11][0] : 왼쪽 골반 y좌표, keypoint[13][0] : 왼쪽 무릎 y좌표
    # keypoint[12][0] : 오른쪽 골반 y좌표, keypoint[14][0] : 오른쪽 무릎 y좌표
    hip_knee_l = keypoint[11][0]-keypoint[13][0]
    hip_knee_r = keypoint[12][0]-keypoint[14][0]
    hip_knee = (hip_knee_l+hip_knee_r)/2
    #MAX_LIMIT = 50
    #MIN_LIMIT = -60
    value = 30
    print("===================================================")
    print("1. squat_down")
    print("d_LIMIT")
    print(d_LIMIT)
    print(hip_knee)
    if(hip_knee > d_LIMIT + value):
        print("조금 일어나세요.")
        return False
    elif(d_LIMIT - value <= hip_knee <= d_LIMIT + value):
        print("checkpoint #2 OK")
        return True
    else:
        print("조금 더 앉으세요")
        return False


def squat_straight(keypoint):
    # keypoint[17] : 척수상, keypoint[18] : 척수중, keypoint[19] : 척추하
    #MIN_LIMIT = -10
    #MAX_LIMIT = 10
    value = 10
    angle = getDegree(keypoint[17], keypoint[18], keypoint[19])

    print("------------------")
    print("2. squat_straight")
    print("s_LIMIT")
    print(s_LIMIT)
    print(angle)
    if s_LIMIT-value <= angle <= s_LIMIT+value:
        print("OK")
        return True

    elif angle < s_LIMIT-value:
        print("조금 더 허리를 세워주세요.")
        return False

    elif angle > s_LIMIT+value:
        print("조금 더 허리를 구부려주세요.")
        return False


def squat_knee_angle(keypoint):
    # keypoint[12] : 오른쪽골반, keypoint[14] : 오른쪽무릎, keypoint[16] : 오른쪽발목
    # keypoint[11] : 왼쪽골반, keypoint[13] : 왼쪽무릎, keypoint[15] : 왼쪽발목
    #LIMIT = 75
    right_angle = getDegree(keypoint[12], keypoint[14], keypoint[16])
    left_angle = getDegree(keypoint[11], keypoint[13], keypoint[15])
    angle = abs((right_angle + left_angle) / 2)

    print("------------------")
    print("3. squat_knee_angle")
    print("LIMIT")
    print(LIMIT)
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
