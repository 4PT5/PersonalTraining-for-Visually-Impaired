import speech_recognition as sr

# microphone에서 auido source를 생성합니다
while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # 구글 웹 음성 API로 인식하기 (하루에 제한 50회)
    try:
        result = r.recognize_google(audio, language='ko')
        print("Google Speech Recognition thinks you said : " + result)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        continue
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))
        continue

    # 결과
    if result == '일번' or result == '1번':
        print('1번 페이지로 이동합니다.')
        break
    elif result == '이번' or result == '2번':
        print('2번 페이지로 이동합니다.')
        break
    elif result == '삼번' or result == '3번':
        print('3번 페이지로 이동합니다.')
        break
    else:
        print('다시 말하세요.')
