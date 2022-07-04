from user.models import User


# 유저 더미데이터
def gen_master(apps, schema_editor):
    # 슈퍼 유저 생성
    User.objects.create_superuser(
        email='admin@email.com',
        nickname='admin',
        password='password'
    )

    # # 일반 유저 생성
    # for id in range(2, 5):
    #     email = f'user{id}@email.com'
    #     nickname = f'user{id}'
    #     password = 'password'
    #
    #     User.objects.create_user(
    #         email=email,
    #         nickname=nickname,
    #         password=password
    #     )