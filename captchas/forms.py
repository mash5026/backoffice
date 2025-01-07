from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import authenticate
from django import forms

# class CaptchaAdminAuthenticationForm(AdminAuthenticationForm):
#     captcha = forms.CharField(
#         max_length=2,
#         required=True,
#         label='حاصل جمع',
#         widget=forms.TextInput(attrs={
#             'class': 'form-control', 
#             'placeholder': 'حاصل جمع را وارد کنید'
#         })
#     )

#     def clean(self):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')
#         captcha = self.cleaned_data.get('captcha')
#         stored_captcha = self.request.session.get('captcha_answer')

#         if not captcha or not stored_captcha:
#             raise forms.ValidationError('Please solve the math problem')

#         if captcha != stored_captcha:
#             raise forms.ValidationError('جواب درست نبود، مجددا امتحان کنید')

#         if username and password:
#             self.user_cache = authenticate(
#                 self.request,
#                 username=username,
#                 password=password
#             )
#             if self.user_cache is None:
#                 raise forms.ValidationError(
#                     self.error_messages['invalid_login'],
#                     code='invalid_login',
#                     params={'username': self.username_field.verbose_name},
#                 )
#             else:
#                 self.confirm_login_allowed(self.user_cache)

#         # Clear the stored CAPTCHA after successful validation
#         del self.request.session['captcha_answer']
#         return self.cleaned_data
    

# from django.contrib.admin.forms import AdminAuthenticationForm
# from django import forms

# class CaptchaAdminAuthenticationForm(AdminAuthenticationForm):
#     captcha = forms.CharField(max_length=4, required=True)
    
#     def clean_captcha(self):
#         captcha = self.cleaned_data.get('captcha')
#         stored_captcha = self.request.session.get('captcha_text')
        
#         if not captcha or not stored_captcha:
#             raise forms.ValidationError('CAPTCHA is required')
            
#         if captcha != stored_captcha:
#             raise forms.ValidationError('Invalid CAPTCHA')
            
#         # Clear the stored CAPTCHA
#         del self.request.session['captcha_text']
#         return captcha


# forms.py
class CaptchaAdminAuthenticationForm(AdminAuthenticationForm):
    captcha = forms.CharField(
        max_length=5,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'کد کپچا را وارد نمایید'
        })
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        captcha = self.cleaned_data.get('captcha')
        stored_captcha = self.request.session.get('captcha_text')

        if not captcha or not stored_captcha:
            raise forms.ValidationError('کد کپچا را وارد نکردید')

        if captcha.upper() != stored_captcha:
            raise forms.ValidationError('اشتباه شد، مجددا تلاش کنید')

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        del self.request.session['captcha_text']
        return self.cleaned_data
