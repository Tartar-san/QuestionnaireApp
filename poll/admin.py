from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Questionnaire)
admin.site.register(Page)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Answer)
admin.site.register(Respondent)
admin.site.register(Condition)
admin.site.register(Video)