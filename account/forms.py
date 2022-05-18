from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User


# class Registerforms(forms.Form):
#     error_css_class = 'text-danger'
#     required_css_class = 'required'
#     First_name = forms.CharField(label=mark_safe('نام'), max_length=70, required=True, widget=forms.TextInput(attrs={'class': "e-field-inner"}))
#     Last_name = forms.CharField(label=mark_safe('<br />نام خانوادگی'), max_length=70, required=True, widget=forms.TextInput(attrs={'class': "e-field-inner"}))
#     User_name = forms.CharField(label=mark_safe('<br />نام کاربری'), max_length=70, required=True, widget=forms.TextInput(attrs={'class': "e-field-inner"}))
#     Email = forms.EmailField(label=mark_safe('<br />ایمیل'), max_length=121, required=True, widget=forms.EmailInput(attrs={'class': "e-field-inner"}))
#     Password = forms.CharField(label=mark_safe('<br />رمز عبور'), max_length=70, required=True, widget=forms.PasswordInput(attrs={'class': "e-field-inner"}))
#     re_Password = forms.CharField(label=mark_safe('<br />تکرار رمز عبور'), max_length=70, required=True, widget=forms.PasswordInput(attrs={'class': "e-field-inner"}))
#
#     def Passcheck(self):
#         data = self.cleaned_data
#         password = self.cleaned_data.get("Password")
#         confirm_password = self.cleaned_data.get("re_Password")
#
#         if password != confirm_password:
#             raise forms.ValidationError("لطفا از یکسان بودن رمز عبور خود اطمینان حاصل فرمایید")
#         return data
class RegisterForm(forms.Form):

    error_css_class = 'text-danger'
    required_css_class = 'required'
    First_name = forms.CharField(required=True, label="نام ", widget=forms.TextInput(attrs={"class": "e-field-inner",
                                                                                            "placeholder": "نام خود را نظر را وارد کنید"}))

    Last_name = forms.CharField(required=True, label="نام خانوادگی ", widget=forms.TextInput(attrs={"class": "e-field-inner",
                                                                                                    "placeholder": "نام خانوداگی خود ار نظر را وارد کنید"}))

    User_name = forms.CharField(required=True, label="نام کاربری ", widget=forms.TextInput(attrs={"class": "e-field-inner",
                                                                                                  "placeholder": "نام کاربری مورد نظر را وارد کنید"}))

    Email = forms.EmailField(required=True, label=" ایمیل", widget=forms.EmailInput(attrs={"class": "e-field-inner",
                                                                                           "placeholder": "ایمیل خود را وارد کنید", "id": "khas"}))

    Password = forms.CharField(required=True, label=" رمز", widget=forms.PasswordInput(attrs={"class": "e-field-inner",
                                                                                              "placeholder": "رمز عبور"}))

    re_Password = forms.CharField(required=True, label="تکرار رمز", widget=forms.PasswordInput(attrs={"class": "e-field-inner",
                                                                                                      "placeholder": "تکرار رمز عبور"}))

    # def clean(self):
    #     data = self.cleaned_data
    #     password = self.cleaned_data.get("Password")
    #     password2 = self.cleaned_data.get("re_Password")
    #     user = self.cleaned_data.get('User_name')
    #     nemoone = User.objects.filter(username=user)
    #     if len(nemoone):
    #         raise forms.ValidationError('in user name ghablan sabt shode !!!')
    #
    #     if password != password2:
    #         raise forms.ValidationError("پسورد ها یکی نیست")
    #     return data
    def clean_User_name(self):
        username = self.cleaned_data.get("User_name")
        user = User.objects.filter(username=username)
        if len(user):
            raise forms.ValidationError(f" {username} از قبل وجود دارد ")
        return username

    def clean_Email(self):
        email = self.cleaned_data.get("Email")
        mail = User.objects.filter(email=email)
        if len(mail):
            raise forms.ValidationError(f" {email} از قبل وجود دارد ")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("Password")
        re_Password = self.cleaned_data.get("re_Password")
        if re_Password != password:
            raise forms.ValidationError("لطفا از یکسان بودن رمز عبور خود اطمینان حاصل فرمایید")
        return data

    # def clean_userName(self):
    #     # User = get_user_model()
    #     userName = self.cleaned_data.get("User_name")
    #     qs = User.objects.filter(username=userName)
    #     if qs.exists():
    #         raise forms.ValidationError("نام کاربری قبلا استفاده شده است")
    #     return userName
    #
    # def clean_email(self):
    #
    #     email = self.cleaned_data.get("Email")
    #     qs = User.objects.filter(email=email)
    #     if qs.exists():
    #         raise forms.ValidationError("ایمیل از قبل وجود دارد")
    #     return email
    #
    # def clean(self):
    #     data = self.cleaned_data
    #     password = self.cleaned_data.get("Password")
    #     password2 = self.cleaned_data.get("re_Password")
    #
    #     if password != password2:
    #         raise forms.ValidationError("لطفا از یکسان بودن رمز عبور خود اطمینان حاصل فرمایید")
    #     return data


class Loginform(forms.Form):
    User_name = forms.CharField(required=True, label="نام کاربری ", widget=forms.TextInput(attrs={"class": "e-field-inner",
                                                                                                  "placeholder": "نام کاربری مورد نظر را وارد کنید"}))

    Password = forms.CharField(required=True, label=" رمز", widget=forms.PasswordInput(attrs={"class": "e-field-inner",
                                                                                              "placeholder": "رمز عبور"}))