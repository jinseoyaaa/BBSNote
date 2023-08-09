"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# django.contrib 모듈에서 admin 모듈을 가져옴, Django의 관리자 인터페이스
from django.contrib import admin
# django.urls 모듈에서 path, include 함수를 가져옴, URL 패턴을 정의
from django.urls import path, include
# bbsnote 앱의 views 모듈을 가져옴
from bbsnote import views


# URL 패턴 목록 정의
urlpatterns = [
    # 이 패턴은 'admin/' 문자열과 일치
    # 일치할 경우 Django의 관리자 인터페이스 호출
    path("admin/", admin.site.urls),
    # 이 패턴은 'bbsnote/' 문자열과 일치
    # 일치할 경우 'bbsnote.urls' 모듈에 정의된 URL 패턴 목록이 포함
    path("bbsnote/", include("bbsnote.urls")),
    path("common/", include("common.urls")),
    # 이 패턴은 빈 문자열과 일치
    # 일치할 경우 views.index 뷰 함수 호출
    path("", views.index, name='index'),
    path("insta/", include('insta.urls')),
]
