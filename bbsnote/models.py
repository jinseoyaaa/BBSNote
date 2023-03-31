"""
models.py에서는 null/not null을 정해줌
예를 들어, Board 클래스의 subject는 not null로 설정되어 있음
즉, subject에는 null 값이 들어가면 안됨
만약 not null로 설정되어 있지만 null을 허용하고싶다면 괄호 안에 null=True를 넣어주면 됨
만약 not null로 설정되어 있지만 빈 값을 허용하고싶다면 괄호 안에 blank=True를 넣어주면 됨
not null로 설정되어있는 필드에 null 값을 넣게 되면 오류가 남
이러한 오류 방지를 위해 blank=True 옵션을 주면 값을 입력하지 않더라도 자동으로 빈 값으로 채워줌
"""



# django.db 모듈에서 models를 가져옴
from django.db import models
from django.contrib.auth.models import User


# models.Model을 상속하는 새로운 클래스 Board를 정의, 데이터베이스 테이블을 나타냄
class Board(models.Model):
    # Board 클래스의 속성으로 문자열 필드 subject를 정의, 최대 길이 200자인 필드
    subject = models.CharField(max_length=200)
    # Board 클래스의 속성으로 텍스트 필드 content를 정의
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Board 클래스의 속성으로 날짜/시간 필드 create_date를 정의 
    # 객체가 처음 생성될 때 자동으로 현재 날짜/시간으로 설정
    create_date = models.DateTimeField(auto_now_add=True)
    # Board 클래스의 속성으로 날짜/시간 필드인 update_date를 정의
    # 객체가 저장될 때마다 자동으로 현재 날짜/시간으로 갱신
    update_date = models.DateTimeField(auto_now=True)

    # 객체가 문자열로 표현될 때 호출
    # 예를 들어, 객체를 출력할 때
    def __str__(self):
        # [id] subject 형식의 문자열 반환
        # 여기서 id와 subject는 각각 객체의 id와 subject의 속성값
        return f'[{self.id}] {self.subject}'

# models.Model을 상속하는 새로운 클래스인 Comment를 정의, 이 클래스는 데이터베이스 테이블   
class Comment(models.Model):
    # 외래키 필드인 board를 정의, 이 필드는 Board 모델과 관계있음
    # on_delete 옵션은 Board 객체가 삭제될 때 관련된 Comment 객체도 함께 삭제되도록 지정
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    # Comment 클래스의 속성으로 텍스트 필드 content를 정의
    content = models.TextField()
    # ForeignKey로 User 모델과 연결
    # on_delete=models.CASCADE는 User 객체가 삭제될 때 이 객체도 함께 삭제됨을 의미함
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 객체가 처음 생성될 때 자동으로 현재 날짜/시간으로 설정
    create_date = models.DateTimeField(auto_now_add=True)
    # 객체가 저장될 때마다 자동으로 현재 날짜/시간으로 갱신
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return f'[{self.board.id}] {self.content}'
    