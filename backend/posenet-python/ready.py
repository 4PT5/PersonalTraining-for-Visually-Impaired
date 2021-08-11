def isReady(keypoint):
    # keypoint[15][0]: 왼쪽 발목 y좌표, keypoint[1][0]: 왼쪽 눈 y좌표
    height = keypoint[15][0]-keypoint[1][0]
    MAX_LIMIT = 550
    MIN_LIMIT = 450
    if MIN_LIMIT <= height <= MAX_LIMIT:
        print("ready: ok")
        return True
    elif height > MAX_LIMIT:
        print("ready: 뒤로 가주세요")
        return False
    elif height < MIN_LIMIT:
        print("ready: 앞으로 가주세요")
        return False


def isSide(keypoint):
    # keypoint[11][1]: 왼쪽 골반 x좌표, keypoint[12][1]: 오른쪽 골반 x좌표
    pelvis = abs(keypoint[11][1] - keypoint[12][1])
    limit = 20
    if pelvis <= limit:
        print("side: 측면")
        return True
    else:
        print("side: 정면")
        return False