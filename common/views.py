# render와 redirect 함수를 가져옴
from django.shortcuts import render, redirect
# authenticate 함수는 사용자 인증 처리 담당
# login 함수는 로그인 처리 담당
from django.contrib.auth import authenticate, login
# 현재 디렉토리의 forms.py 파일에서 UserForm 클래스를 가져옴
from .forms import UserForm


# 회원가입 페이지를 표시하고 회원가입 처리를 담당하는 함수 정의 
def signup(request):
    # 요청 메소드가 POST인 경우 시작
    if request.method == "POST":
        # UserForm 클래스의 인스턴스 생성, 폼 데이터는 request.POST에서 가져옴
        form = UserForm(request.POST)
        # 데이터가 유효한 경우의 시작
        if form.is_valid():
            # 데이터베이스에 저장
            form.save()
            # 사용자 이름을 가져옴
            username = form.cleaned_data.get('username')
            # 비밀번호를 가져옴
            raw_password = form.cleaned_data.get('password1')
            # 사용자 인증 처리
            user = authenticate(username=username, password=raw_password)
            # 로그인 처리
            login(request, user)
            # index URL로 리다이렉트하는 HTTP 응답 반환
            return redirect('index')
    # POST가 아닌 경우
    else:
        # UserForm 클래스의 인스턴스 생성
        form = UserForm()
    # request를 받고, 렌더링할 템플릿 파일의 경로를 받음
    # UserForm 객체를 signup 템플릿에 전달하여 HTML로 렌더링
    return render(request, 'common/signup.html', {'form':form}) 
         