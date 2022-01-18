from django.urls import path, include
from . import views

urlpatterns = [
    path('gettoken/<str:id>/<str:token>', views.validate_user_session, name="token.generate"),
    path('gettoken/<str:id>/<str:token>', views.process_payment, name="payment.process"),

]