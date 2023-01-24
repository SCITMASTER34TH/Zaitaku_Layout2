from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(SkypeUserModel)
admin.site.register(SkypeMyNameModel)

####################################################stripe####################################################
class PriceInlineAdmin(admin.TabularInline):
    model = Price
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    inlines = [PriceInlineAdmin]

# 管理画面に商品マスタと価格マスタを表示
admin.site.register(Product, ProductAdmin)
admin.site.register(Price)
admin.site.register(Transaction)
admin.site.register(Order)
########################################################################################################
admin.site.register(ChatModel)
admin.site.register(AttendanceRecord)
########################################################################################################
admin.site.register(UserImageModel)
########################################################################################################
admin.site.register(ChatGptModel)
