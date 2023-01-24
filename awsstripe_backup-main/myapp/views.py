from django.shortcuts import render
from django.views.generic import TemplateView

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from .models import *

from django.contrib.auth.views import LoginView
from  .forms import *

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

import requests
import json

def LoginView(request):
    return HttpResponseRedirect('social:begin', kwargs=dict(backend='google-oauth2'))

#class TopView(LoginRequiredMixin, TemplateView): #user_account
    #login_url = reverse_lazy("login") # リダイレクト先の指定
class TopView(TemplateView):
    #template_name = "myapp/index.html"
    

    def __init__(self):
        self.params = {}

    #@login_required
    def get(self,request):
        print("##########TopView##########")
        #self.params["sample"] = request.user.email
        #self.params["sample"] = Skype.objects.select_related('user').get(id=1).skype_id

        if request.user.is_authenticated:

            # other_user = SkypeUserModel.objects.select_related('user').filter(user=request.user)
            # other_user_skype = SkypeMyNameModel.objects.filter(user__in=list(other_user))
            # self.params["sample"] = other_user_skype

            #other_user = SkypeUserModel.objects.select_related('user').filter(user=request.user)

            #other_user_skype = SkypeMyNameModel.objects.filter(user__in=list(other_user))

            #other_user_arr = [i.other_user.username for i in list(other_user)]

            #########################################################################################################
            #other_user = SkypeUserModel.objects.select_related('user').filter(user=request.user)
            # other_user_arr = []
            # for i in list(other_user):
            #     i.other_user.username
            #     # skype_id = User.objects.get(username=i.other_user.username).user_skype_id.skype_id
            #     # other_user_arr.append(skype_id)
            #     skype_id = User.objects.get(username=i.other_user.username)
            #     other_user_arr.append(skype_id)
            #########################################################################################################

            #other_user_skype = SkypeMyNameModel.objects.filter(user__in=other_user_arr)

            #other_user_arr = SkypeMyNameModel.objects.all()
            #other_user_arr = SkypeMyNameModel.objects.exclude(id=request.user.id)

            other_user_arr = SkypeMyNameModel.objects.exclude(user=request.user)
            #other_user_arr = SkypeMyNameModel.objects.filter(id=1)
            #other_user_arr = SkypeMyNameModel.objects.all()
            self.params["sample"] = other_user_arr
            #self.params["sample2"] = request.user.id

            #self.params["sample"] = other_user_skype

            #workplace_obj = User.objects.filter(workplace="裾野").prefetch_related('workplace_key')


            #obj = User.objects.get(user=request.user).user_set.skype_id
            #obj = User.objects.get(user=request.user)

            #obj = User.objects.get(id=request.user.id).user_skype_id
            #obj = User.objects.get(id=2).user_skype_id.skype_id

            #obj = User.objects.get(user=request.user).user_skype_id.skype_id

            #20221213###################################################stripe####################################################
            try:
                order = Order.objects.filter(user=User.objects.get(id=request.user.id)).first()
                #order = Order.objects.get(id=2)
                subscription_id = stripe.checkout.Session.retrieve(order.stripe)['subscription']
                self.params['subscription_id'] = subscription_id
                # self.params['order_name'] = order.name #20221214
            except:
                self.params['subscription_id'] = 123
            ########################################################################################################

            #20230111###################################################img####################################################
            try:
                #userimagemodel = UserImageModel.objects.get(id=2)
                userimagemodel = SkypeMyNameModel.objects.get(user=User.objects.get(id=request.user.id))
                self.params['user_image_model'] = userimagemodel
                #self.params['MEDIA_URL'] = settings.MEDIA_URL + settings.AWS_LOCATION + '/'
                self.params['MEDIA_URL'] = "https://uenotomoki-skype-stripe-s3bucket.s3.ap-northeast-1.amazonaws.com/" + settings.AWS_LOCATION + '/'
            except:
                self.params['user_image_model'] = "images/user_image.jpg"
                self.params['MEDIA_URL'] = "https://uenotomoki-skype-stripe-s3bucket.s3.ap-northeast-1.amazonaws.com/static/"
            ########################################################################################################

            #20230111###################################################weather####################################################
            API_TOKEN = "1ab2c959e5056a4773437f60a8efebc7"

            response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                ## 緯度・軽度を指定する場合
                # "lat": "35.68944",
                # "lon": "139.69167",

                ## 都市名で取得する場合
                "q": "tokyo",

                "appid": API_TOKEN,
                "units": "metric",
                "lang": "ja",
                },
            )
            #ret = json.loads(response.text)['weather'][0]['description']
            ret = json.loads(response.text)

            self.params['weather_0_description'] = ret['weather'][0]['description']
            self.params['weather_name'] = ret['name']
            self.params['weather_main_temp'] = ret['main']['temp']
            ########################################################################################################

            return render(request,'myapp/home.html',self.params)

        #return render(request,'myapp/home.html',self.params)
        return render(request,'myapp/home_logout.html',self.params)

    def post(self, request):
        return render(request,'myapp/home.html',self.params)

# class Login(LoginView):
#     form_class = LoginForm
#     template_name = "myapp/login.html"

def index(request):
    return render(request, 'myapp/index.html')

####################################################stripe####################################################
import json
import stripe

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.core.mail import send_mail

from django.views.generic import TemplateView


from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.views import View

# from .models import Product
# from .models import Price
# from .models import Transaction # 追加

import datetime   # 追加
from django.views.decorators.http import require_POST, require_GET

from datetime import date
# from dateutil.relativedelta import relativedelta
# from django.utils.timezone import make_aware

# STRIPEのシークレットキー
stripe.api_key = settings.STRIPE_SECRET_KEY

# WEBHOOKのシークレットキー
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

# 決済成功画面
class SuccessPageView(TemplateView):
    template_name = 'myapp/success.html'

# 決済キャンセル画面
class CancelPageView(TemplateView):
    template_name = 'myapp/cancel.html'

#class ProductTopPageView(TemplateView):
    # def __init__(self):
    #     self.params = {}

    # def get(self,request):
    #     return render(request,'myapp/product-top.html',self.params)

    # def post(self, request):
    #     return render(request,'myapp/product-top.html',self.params)

class ProductTopPageView(ListView):
    # 商品マスタ
    model = Product
    # ページリンク
    template_name = "myapp/product-top.html"
    #レコード情報をテンプレートに渡すオブジェクト
    context_object_name = "product_list"

# 決済画面
class CreateCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        # 商品マスタ呼出
        product = Product.objects.get(id=self.kwargs["pk"])
        price   = Price.objects.get(product=product)

        customer = request.user #20221213

        # ドメイン
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        #YOUR_DOMAIN = "http://uenotomoki-docker-django-nlb-07bde5140e8878e1.elb.ap-northeast-1.amazonaws.com"

        # 決済用セッション
        checkout_session = stripe.checkout.Session.create(
            # 決済方法
            payment_method_types=['card'],
            # 決済詳細
            line_items=[
                {
                    'price': price.stripe_price_id,       # 価格IDを指定
                    'quantity': 1,                        # 数量
                },
            ],
            # POSTリクエスト時にメタデータ取得
            metadata = {
                        "customer_id": customer.id, #20221213
                        "product_id":product.id,
                       },
            #mode='payment',                               # 決済手段（一括）
            mode='subscription',

            #success_url=YOUR_DOMAIN + '/success/',        # 決済成功時のリダイレクト先
            #success_url=YOUR_DOMAIN + '/login/',        # 決済成功時のリダイレクト先
            success_url=YOUR_DOMAIN,        # 決済成功時のリダイレクト先
            cancel_url=YOUR_DOMAIN + '/cancel/',          # 決済キャンセル時のリダイレクト先

            # #20221215
            # consent_collection={
            #     'terms_of_service': 'required',
            # },
        )

        #20221214
        order = Order.objects.create(
            #user=User.objects.get(id=checkout_session['metadata']['customer_id']),
            user=User.objects.get(id=customer.id),
            stripe=checkout_session['id']
        )

        return redirect(checkout_session.url)



# イベントハンドラ
@csrf_exempt
def stripe_webhook(request):

    # サーバーのイベントログからの出力ステートメント
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # 有効でないpayload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # 有効でない署名
        return HttpResponse(status=400)

    # checkout.session.completedイベント検知
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # イベント情報取得
        customer_name  = session["customer_details"]["name"]     # 顧客名
        customer_email = session["customer_details"]["email"]    # 顧客メール
        product_id     = session["metadata"]["product_id"]       # 購入商品ID
        product        = Product.objects.get(id=product_id)      # 購入商品情報
        product_name   = product.name                            # 購入した商品名
        amount         = session["amount_total"]                 # 購入金額（手数料抜き）
        print("customer_name")
        print(customer_name)
        print("customer_email")
        print(customer_email)
        print("product_id")
        print(product_id)
        print("product")
        print(product)
        print("product_name")
        print(product_name)
        print("amount")
        print(amount)

        # DBに結果を保存
        SaveTransaction(product_name, customer_name, customer_email, amount)

        fulfill_order(session) #20221213

        # 決済完了後メール送信（Djangoのメール機能利用）
        send_mail(
            subject = '商品購入完了！',                                                                                     # 件名
            message = '{}様\n商品購入ありがとうございます。購入された商品URLはこちら{}'.format(customer_name,product.url),  # メール本文
            recipient_list = [customer_email],                                                                              # TO
            from_email = 'githubfreezing45@gmail.com'                                                                  # FROM
        )
        # 結果確認
        print(session)

    ###############################csncel_subsc###############################
    if event['type'] == 'customer.subscription.updated':
        session = event['data']['object']
        cancel_order(session)
    ##############################################################

    return HttpResponse(status=200)


# 顧客の商品購入履歴を保存
def SaveTransaction(product_name, customer_name, customer_email, amount):
    # DB保存
    print("def SaveTransaction(product_name, customer_name, customer_email, amount):")
    saveData = Transaction.objects.get_or_create(
                        product_name   =  product_name,
                        date           = datetime.datetime.now(),
                        customer_name  = customer_name,
                        email          = customer_email,
                        product_amount = amount
                        )
    return saveData

def fulfill_order(session):
    print(session['metadata'])
    order = Order.objects.create(
        user=User.objects.get(id=session['metadata']['customer_id']),
        stripe=session['id']
    )
    print("Fulfilling order")
########################################################################################################
####################################################stripe_stop_subsc####################################################
@csrf_exempt
@require_POST
def stop_subscription_session(request):
    #customer = request.user
    subscriptionId = request.POST.get('subscriptionId')
    # session = stripe.Subscription.modify(
    #     subscriptionId,
    #     #cancel_at_period_end=True,
    #     metadata={
    #         'customer_id': customer.id,
    #         'meta_flag': 'cancel_scheduled',
    #     }
    # )

    stripe.Subscription.delete(subscriptionId)
    #return redirect('stop_success')
    #orderName = request.POST.get('orderName')
    #print(orderName)
    Order.objects.filter(user=User.objects.get(id=request.user.id)).delete()

    return redirect('top')


def cancel_order(session):
    print(session['metadata'])
    if session['metadata'] and session['metadata']['meta_flag'] == 'cancel_scheduled':
        order = Order.objects.filter(user=User.objects.get(
            id=session['metadata']['customer_id']), deleted_date=None).first()
        order.stripe = session['id']

        #today = make_aware(datetime.now())
        today = datetime.now()

        ordered_at = order.created_at
        if date(today.year, today.month, ordered_at.day) > date(today.year, today.month, today.day):
            o_deleted_date = date(today.year, today.month, ordered_at.day)
        else:
            #o_deleted_date = date(today.year, today.month, ordered_at.day) + relativedelta(months=1)
            o_deleted_date = date(today.year, today.month, ordered_at.day)
        order.deleted_date = o_deleted_date
        order.save()
########################################################################################################
from django.db.models import Q

class ChatView(TemplateView):
    #template_name = "myapp/index.html"

    def __init__(self):
        self.params = {}

    #@login_required
    def get(self,request, someone_id):
        print("##########TopView##########")
        if request.user.is_authenticated:
            self.params["someone_id"] = someone_id

            user_id = request.user.id
            self.params["user_id"] = user_id

            #chat_model = ChatModel.objects.filter(user=User.objects.get(id=user_id))
            # chat_model = ChatModel.objects.filter(Q(user=User.objects.get(id=int(user_id))) |
            #                                       Q(someone=User.objects.get(id=int(someone_id)))
            #                                       )
            chat_model = ChatModel.objects.filter(Q(user=User.objects.get(id=user_id) ,someone=User.objects.get(id=someone_id)) |
                                                  Q(user=User.objects.get(id=someone_id) ,someone=User.objects.get(id=user_id))
                                                  ).order_by('chated_at').reverse()
            #.distinct()
            self.params["chat_model"] = chat_model

            #20221220
            self.params["someone"] = User.objects.get(id=someone_id)

            return render(request,'myapp/chat.html',self.params)

        self.params["someone_id"] = someone_id
        self.params["user_id"] = request.user.id
        return render(request,'myapp/chat.html',self.params)

    def post(self, request, someone_id):
        #user_id = int(request.POST.get('user_id'))
        user_id = request.user.id
        #someone_id = int(request.POST.get('someone_id'))
        someone_id = someone_id
        chat_context = request.POST.get('chat_context')

        #chat_model = ChatModel.objects.filter(user=User.objects.get(id=user_id))
        chat_model = ChatModel.objects.filter(Q(user=User.objects.get(id=user_id) ,someone=User.objects.get(id=someone_id)) |
                                                Q(user=User.objects.get(id=someone_id) ,someone=User.objects.get(id=user_id))
                                                ).order_by('chated_at').reverse()
        #.distinct()
        self.params["chat_model"] = chat_model

        #20221220
        self.params["someone"] = User.objects.get(id=someone_id)

        ChatModel.objects.create(user=User.objects.get(id=user_id),
                                 someone=User.objects.get(id=someone_id),
                                 chat_context = chat_context,
                                 chated_at = datetime.datetime.today(),
                                 )
        #chated_at = datetime.datetime.today(),

        self.params["user_id"] = user_id
        self.params["someone_id"] = someone_id

        return render(request,'myapp/chat.html',self.params)

######################################################################################################
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """ログインした際に呼ばれる"""
    print("20221219##########################################################################################################################################")
    AttendanceRecord.objects.create(user=User.objects.get(id=request.user.id), login_time=timezone.now())




############CHATGPT##########################################################################################
import openai

class ChatGptView(TemplateView):
    def __init__(self):
        self.params = {}

    #@login_required
    def get(self, request):
        self.params["chatgpt"] = ChatGptModel.objects.all()
        return render(request,'myapp/chatgpt.html',self.params)

    def post(self, request):
        chatgpt_user_chat = request.POST.get("chatgpt")
        print(chatgpt_user_chat)

        openai.api_key = "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"

        response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=chatgpt_user_chat,
                max_tokens=1024,
                temperature=0.5,
        )

        ChatGptModel.objects.create(chatgpt_user = chatgpt_user_chat,
                                    chatgpt_cp = response['choices'][0]['text'])

        self.params["chatgpt"] = ChatGptModel.objects.all()

        return render(request,'myapp/chatgpt.html',self.params)
