from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm

from .models import MyUser, Year


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label='비밀번호(8자리 이상)', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호(확인)', widget=forms.PasswordInput)
    year_admission = forms.ModelChoiceField(queryset=Year.objects.all(), to_field_name="year", label='입학년도(전입년도)')

    class Meta:
        model = MyUser
        fields = ('email', 'name', 'user_code', 'year_admission')
        labels = {
            'email': '이메일 (로그인 시 아이디로 사용)',
            'name': '이름',
            'user_code': '학번(교사는 0으로 입력)',
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['year_admission'].label_from_instance = lambda obj: "%s" % obj.year

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 서로 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'name', 'user_code', 'year_admission')
        labels = {
            'email': '이메일',
            'name': '이름',
            'user_code': '학번',
            'year_admission': '입학년도'
        }

    def clean_password(self):
        return self.initial["password"]