from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SkypeUserModel(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    other_user = models.ForeignKey(User, related_name='other_user', on_delete=models.CASCADE)

class SkypeMyNameModel(models.Model):
    user = models.OneToOneField(User, related_name='user_skype_id', on_delete=models.CASCADE)
    skype_id = models.CharField(max_length=100)
    images = models.ImageField(upload_to='images/')#20230111

    # def __str__(self):
    #     return self.user

####################################################stripe####################################################
# 商品マスタ
class Product(models.Model):
    # 商品名
    name = models.CharField(max_length=100)
    # 商品概要
    description = models.CharField(max_length=255, blank=True, null=True)
    # 商品ID（★stripeの商品IDを値に用いる）
    stripe_product_id = models.CharField(max_length=100)
    # 商品写真登録用のファイル
    file = models.FileField(upload_to="product_files/", blank=True, null=True)
    # 商品詳細ページのリンク
    url  = models.URLField()

    # admin画面で商品名表示
    def __str__(self):
        return self.name

# 価格マスタ
class Price(models.Model):
    # 外部キーで商品マスタを紐付け
    product = models.ForeignKey(Product, related_name='Prices', on_delete=models.CASCADE)
    # 価格ID（★stripeの価格IDを値に用いる）
    stripe_price_id = models.CharField(max_length=100)
    # 価格
    price = models.IntegerField(default=0)

    # Django画面に表示する価格
    def get_display_price(self):
        return self.price

# トランザクションマスタ
class Transaction(models.Model):
    # 購入日
    date   = models.CharField(max_length=100)
    # 購入者
    customer_name = models.CharField(max_length=100)
    # 購入者のメールアドレス
    email  = models.EmailField(max_length=100)
    # 購入商品名
    product_name = models.CharField(max_length=100)
    # 支払い金額
    product_amount = models.IntegerField()

    # admin画面で商品名表示
    def __str__(self):
        return self.date + '_' + self.product_name  + '_' + self.customer_name

#20221213
class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    stripe = models.CharField(verbose_name='Stripe Session', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_date = models.DateField(null=True, blank=True)
########################################################################################################

####################################################chat####################################################
#20221219
class ChatModel(models.Model):
    user = models.ForeignKey(
        User, related_name='chat_user', on_delete=models.CASCADE
    )
    someone = models.ForeignKey(
        User, related_name='chat_someone', on_delete=models.CASCADE
    )
    chat_context = models.CharField(max_length=100)
    chated_at = models.DateTimeField(auto_now_add=True)

########################################################################################################

####################################################log####################################################
#20221219
class AttendanceRecord(models.Model):
    """出勤簿"""

    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.PROTECT)
    login_time = models.DateTimeField('ログイン時刻', blank=True, null=True)
    #logout_time = models.DateTimeField('ログアウト時刻', blank=True, null=True)

    # def __str__(self):
    #     login_dt = timezone.localtime(self.login_time)
    #     return '{0} - {1.year}/{1.month}/{1.day} {1.hour}:{1.minute}:{1.second} - {2}'.format(
    #         self.user.username, login_dt, self.get_diff_time()
    #     )

    # def get_diff_time(self):
    #     """ログアウト時間ーログイン時間"""
    #     if not self.logout_time:
    #         return 'ログアウトしていません'
    #     else:
    #         td = self.logout_time - self.login_time
    #         return '{0}時間{1}分'.format(
    #             td.seconds // 3600, (td.seconds // 60) % 60)





########################################################################################################


########################################################################################################

class UserImageModel(models.Model):
    user = models.OneToOneField(User, related_name='user_image_id', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images/')

########################################################################################################
class ChatGptModel(models.Model):
    chatgpt_user = models.CharField(max_length=1024)
    chatgpt_cp = models.CharField(max_length=1024)