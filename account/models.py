from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


# 사용자 정보 관리 클래스
class UserManager(BaseUserManager):

    def create_user(self, email, name, year_admission, user_code, password=None, **extra_fields):

        if not email:
            raise ValueError('이메일은 필수 요소입니다.')

        if not password:
            raise ValueError('패스워드는 필수 요소입니다.')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            year_admission=year_admission,
            user_code=user_code,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):

        if not email:
            raise ValueError('이메일은 필수 요소입니다.')

        if not password:
            raise ValueError('패스워드는 필수 요소입니다.')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.is_student = False
        user.is_teacher = False
        user.is_coordinator = False
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.is_active = True

        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=30, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_coordinator = models.BooleanField(default=False)

    year_admission = models.IntegerField(null=True)
    user_code = models.IntegerField(null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email


class Year(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.IntegerField()

    objects = models.Manager()

    def __int__(self):
        return self.year
