from django.contrib.admin.sites import AdminSite
from django.shortcuts import render
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CaptchaAdminAuthenticationForm
from .utils import generate_captcha

# class CaptchaAdminSite(AdminSite):
#     login_form = CaptchaAdminAuthenticationForm
    
#     def login(self, request, extra_context=None):
#         if request.method == 'POST':
#             form = self.login_form(request, data=request.POST)
#             if form.is_valid():
#                 auth_login(request, form.get_user())
#                 return HttpResponseRedirect(reverse('admin:index'))
#         else:
#             form = self.login_form(request)
            
#         # Generate new math CAPTCHA
#         answer, captcha_image = generate_math_captcha()
#         request.session['captcha_answer'] = answer
        
#         context = {
#             'form': form,
#             'captcha_image': captcha_image,
#             **(extra_context or {})
#         }
        
#         return render(request, 'admin/login.html', context)
    


# from django.contrib.admin.sites import AdminSite
# from django.http import JsonResponse
# from .utils import generate_captcha_text, generate_captcha_image

# class CaptchaAdminSite(AdminSite):
#     login_form = CaptchaAdminAuthenticationForm
    
#     def login(self, request, extra_context=None):
#         # Generate new CAPTCHA for the login page
#         captcha_text = generate_captcha_text()
#         captcha_image = generate_captcha_image(captcha_text)
        
#         # Store in session
#         request.session['captcha_text'] = captcha_text
        
#         extra_context = extra_context or {}
#         extra_context['captcha_image'] = captcha_image
        
#         return super().login(request, extra_context)

# # Replace the default admin site
# admin.site = CaptchaAdminSite()


# views.py
class CaptchaAdminSite(AdminSite):
    login_form = CaptchaAdminAuthenticationForm
    
    def login(self, request, extra_context=None):
        if request.method == 'POST':
            form = self.login_form(request, data=request.POST)
            if form.is_valid():
                auth_login(request, form.get_user())
                return HttpResponseRedirect(reverse('admin:index'))
        else:
            form = self.login_form(request)
            
        # Generate new CAPTCHA
        captcha_text, captcha_image = generate_captcha()
        request.session['captcha_text'] = captcha_text
        
        context = {
            'form': form,
            'captcha_image': captcha_image,
            **(extra_context or {})
        }
        
        return render(request, 'admin/login.html', context)

