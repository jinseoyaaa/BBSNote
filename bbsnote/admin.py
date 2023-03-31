# 장고의 기본 관리자 페이지 모듈
from django.contrib import admin
# 현재 디렉토리의 models.py 파일에서 Board, Comment 모델 가져오기
from .models import Board, Comment


# BoardAdmin 클래스 정의, 이 클래스는 admin.ModelAdmin을 상속
# 관리자 페이지에서 Board 모델을 어떻게 표시할지 정의
class BoardAdmin(admin.ModelAdmin):
    # 관리자 페이지에서 검색 가능한 필드를 정의, 제목(subject)과 내용(content) 검색 가능
    search_fields = ['subject', 'content']
    
# 관리자 페이지에 Board 모델 등록, 이 모델은 위의 클래스에 정의된 방식으로 표시
admin.site.register(Board, BoardAdmin)
admin.site.register(Comment)
