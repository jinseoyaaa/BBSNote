"""
forms.py에서는 필수 항목인지 선택 항목인지를 정의할 수 있음
예를 들어, class Meta 위에 있는 email = forms.EmailField(label="이메일")을 주석 처리하면 이메일은 선택 항목이 됨
"""



# Django의 forms 모듈을 가져옴
from django import forms
# Django의 인증 시스템에서 제공하는 UserCreationForm을 가져옴
from django.contrib.auth.forms import UserCreationForm
# Django의 인증 시스템에서 제공하는 User 모델을 가져옴
from django.contrib.auth.models import User


# UserCreationForm을 상속받는 UserForm 클래스 정의 
class UserForm(UserCreationForm):
    # 이메일 필드 추가, 이메일 필드의 이름은 '이메일'로 지정
    email = forms.EmailField(label="이메일")

    # Meta 클래스 정의
    class Meta:
        # 속성을 User로 설정
        model = User
        # fields 속성을 ('username','email')로 설정, 사용자의 username과 email 필드만 사용
        fields = ("username","email")
