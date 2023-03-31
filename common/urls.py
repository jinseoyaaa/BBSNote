# django.contrib.auth 패키지에서 views 모듈을 가져옴
from django.contrib.auth import views as auth_views
# URL 패턴을 구별하는 데 사용되는 path 함수
from django.urls import path
# 현재 디렉토리의 views.py 파일에서 뷰 함수를 가져옴
from . import views


# URL 패턴의 그룹 이름을 common으로 지정
app_name = 'common'

# URL 패턴 목록 정의
urlpatterns = [
    # /login/ URL로 요청이 들어오면 로그인 페이지 표시, 로그인 처리를 담당하는 페이지 호출
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    # /logout/ URL로 요청이 들어오면 로그아웃 처리를 담당하는 페이지 호출
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    # /signup/ URL로 요청이 들어오면 views의 signup 클래스 호출
    path('signup/', views.signup, name='signup'),
]
