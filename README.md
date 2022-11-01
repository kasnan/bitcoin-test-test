# bitcoin-test-test

실습 파일 
# python version = 3.6.1
학교 와이파이로 실행되지 않는다.
mtu 설정을 조금만 바꾸면 바로 접속이 가능하다. 단, 코빗 거래소는 제외한다.

## python dll linker 에러
### pyinstaller로 실행 파일 생성할 때 에러가 발생하는 경우
-p 옵션을 추가하고 아래의 경로를 지정해 준다.
C:\Users\kasna\AppData\Local\Programs\Python\Python36

추가로 -F 옵션으로 쓸데없는 파일의 생성을 막는다.

e.g. pyinstaller -F -p C:\Users\kasna\AppData\Local\Programs\Python\Python36 portfolio.py
