import math
import imageDetect

CNT = 0


def getDegree(key1, key2, key3):
    x = math.atan((key1[0] - key2[0]) / (key1[1] - key2[1])) - \
        math.atan((key3[0] - key2[0]) / (key3[1] - key2[1]))
    return x*180/math.pi


def setting(exCode):
    global d_LIMIT, s_LIMIT, LIMIT, CNT
    arr = imageDetect.main(exCode)
    d_LIMIT = arr[11][0]-arr[13][0]
    s_LIMIT = getDegree(arr[11], arr[18], arr[13])  # 상체-무릎 각도 limit
    LIMIT = abs(getDegree(arr[11], arr[13], arr[15]))

    print("카운트를 시작합니다. 5회 반복해주세요.")

# 런지 무릎 각도 (ㄱㄴ)


def lunge_knee_angle(keypoint, i):
    # keypoint[11] : 왼쪽골반, keypoint[13] : 왼쪽무릎, keypoint[15] : 왼쪽발목
    # +i (1) = 오른쪽
    angle = getDegree(keypoint[11+i], keypoint[13+i], keypoint[15+i])

    print("------------------")
    print("1. lunge_knee_angle")
    print("LIMIT")
    print(LIMIT)
    print(angle)
    if angle >= LIMIT:
        print("checkpoint #1 OK")
        return True
    else:
        print("앞 무릎을 조금 더 굽혀주세요.")
        return False

# 상체 기울기 체크


def lunge_straight(keypoint, i):
    # keypoint[11] : 왼쪽골반, keypoint[18] : 척수중, keypoint[13] : 왼쪽 무릎
    value = 10  # testing 후 적당한 값 찾아야함
    angle = getDegree(keypoint[11+i], keypoint[18], keypoint[13+i])

    print("------------------")
    print("2. lunge_straight")
    print("s_LIMIT")
    print(s_LIMIT)
    print(angle)
    if s_LIMIT-value <= angle <= s_LIMIT+value:
        print("checkpoint #2 OK")
        return True
    elif angle < s_LIMIT-value:
        print("조금 더 허리를 세워주세요.")
        return False
    elif angle > s_LIMIT+value:
        print("조금 더 허리를 구부려주세요.")
        return False


# 무릎 발끝 위치 비교
def lunge_tiptoe(keypoint, i):
    # keypoint[11][0] : 왼쪽 골반 y좌표, keypoint[13][0] : 왼쪽 무릎 y좌표
    # +i (1) = 오른쪽
    hip_knee = keypoint[11+i][0]-keypoint[13+i][0]
    value = 30
    print("===================================================")
    print("3. lunge_down")
    print("d_LIMIT")
    print(d_LIMIT)
    print(hip_knee)
    if(hip_knee > d_LIMIT + value):
        print("앞 무릎이 발 앞으로 나오지 않도록 하세요.")
        return False
    elif(d_LIMIT - value <= hip_knee <= d_LIMIT + value):
        print("checkpoint #3 OK")
        return True
    else:
        print("앞 무릎을 앞으로 조금 더 굽히세요.")
        return False


def postureCorrection(keypoint):
    global flag_lr
    flag_lr = True

    if flag_lr:
        if lunge_knee_angle(keypoint, 0) and lunge_straight(keypoint, 0) and lunge_tiptoe(keypoint, 0):
            flag_lr = False
            print("반대쪽 무릎으로 동일한 하게 진행해주세요.")
            return False
    else:
        if lunge_knee_angle(keypoint, 1) and lunge_straight(keypoint, 1) and lunge_tiptoe(keypoint, 1):
            return True
