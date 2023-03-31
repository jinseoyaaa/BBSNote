# django.apps에서 AppConfig 클래스를 가져옴
from django.apps import AppConfig


# CommonConfig라는 클래스를 정의하고 AppConfig 클래스를 상속받음
class CommonConfig(AppConfig):
    # default_auto_field 속성을 'django.db.models.BigAutoField'로 설정
    default_auto_field = "django.db.models.BigAutoField"
    # name 속성을 'common'으로 앱 이름 지정
    name = "common"
    