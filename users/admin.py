from django.contrib import admin
from .forms import UserRegisterForm
from .models import Profile

admin.site.register(Profile)
#admin.site.register(UserRegisterForm)
