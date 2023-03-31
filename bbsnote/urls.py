# django.urls 모듈에서 path 함수를 가져옴, 이 함수는 URL 패턴을 정의하는 데 사용
from django.urls import path
# 현재 디렉토리의 views 모듈을 가져움
from . import views


# 앱의 이름을 'bbsnote'로 설정, 이 이름은 URL 패턴의 네임스페이스로 사용
app_name = 'bbsnote'

# URL 패턴 목록을 정의, 각 패턴은 path 함수를 사용하여 정의
urlpatterns = [
    # 첫번째 URL 패턴, 이 패턴은 빈 문자열과 일치
    # 일치할 경우 views.index 뷰 함수 호출
    path('', views.index, name='index'),
    # 두번째 URL 패턴, 이 패턴은 정수형 변수인 board_id와 일치
    # 일치할 경우 views.detail 뷰 함수 호출
    path('<int:board_id>/', views.detail, name='detail'),
    # 세번째 URL 패턴, 이 패턴은 'comment/create/' 문자열 다음에 정수형 변수인 board_id와 일치
    # 일치할 경우 views.comment_create 뷰 함수 호출
    path('comment/create/<int:board_id>/', views.comment_create, name='comment_create'),
    path('board/create/', views.board_create, name='board_create'),
    path('board/modify/<int:board_id>/', views.board_modify, name='board_modify'),
    path('board/delete/<int:board_id>', views.board_delete, name='board_delete'),
    path('comment/modify/<int:comment_id>/', views.comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
]
