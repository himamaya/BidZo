
from django.contrib import admin
from .models import UserRegister
# Register your models here.
admin.site.register(UserRegister)

from .models import *


admin.site.register(Category)
admin.site.register(SubCategory)