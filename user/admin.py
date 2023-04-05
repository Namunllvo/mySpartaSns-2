from django.contrib import admin    # 장고에서 admin툴을 사용하겠다
from .models import UserModel   # 생성한 모델 가져오기

# Register your models here.
admin.site.register(UserModel) # 이 코드가 나의 UserModel을 Admin에 추가 해 줍니다