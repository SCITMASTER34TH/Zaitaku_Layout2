from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *

from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='myapp/logged_out.html'), name='logout'),#20221226ログアウト画面遷移先変更
    path('logout/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('accounts/profile/', views.index, name='index'),
    path('', TopView.as_view(), name='top'),
    # #path('login/', views.LoginView, name='login'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('login/',auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    # #path('accounts/login/', TemplateView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('oauth/', include('social_django.urls', namespace='social')),  # Social Django用
    # path('auth/', include('social_django.urls', namespace='social')), # <- 追記
    path("product/", ProductTopPageView.as_view(), name="product-top-page"),                                       # 商品トップ
    path("create-checkout-session/<pk>/", CreateCheckoutSessionView.as_view(), name="create-checkout-session"),    # 個別商品決済画面
    path("success/", SuccessPageView.as_view(), name="success"),                                                   # 決済成功時にリダイレクト先
    path("cancel/", CancelPageView.as_view(), name="cancel"),                                                      # 決済キャンセル時のリダイレクト先
    path("webhook/", stripe_webhook, name="webhook"),
    path('stop_subscription_session/', views.stop_subscription_session, name='stop_subscription_session'),
    path('chat/<int:someone_id>/', ChatView.as_view(), name='chat'), #20221219_make to chat view
    path('chatgpt/', ChatGptView.as_view(), name='chatgpt'), #20230116 to chatgpt view
]
