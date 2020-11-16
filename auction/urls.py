from django.conf.urls import url
from django.views.generic import TemplateView, ListView

from .views import *
from django.urls import path
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetConfirmView, \
        PasswordResetDoneView

app_name = 'auction'

urlpatterns = [
        path('', customerItemsListToBid, name='home'),
        path('signup/', CustomerSignUp, name='signup'),
        # path('base/',TrendingItems, name='trending_items'),
        ######################PASSWORD RELATED########################
        path('change-password/', PasswordChangeView.as_view(), name='password_change'),
        path('change-password-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
        path('password-reset-form/', PasswordResetJBEmailView.as_view(), name='password_reset_form'),
        path('password-reset-done-form/', PasswordResetDoneView.as_view(), name='password_reset_done'),
        path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

        #############PROFILE###########
        path('profile_preview/', TemplateView.as_view(template_name='CustomerProfile_preview.html'), name='profile_preview'),
        path('edit_profile/',edit_customerProfile , name='edit_profile'),

        ###############CUSTOMER RELATED########################
        path('my_items/',customerItemsList , name='customer_items'),
        path('my_item_add/',addCustomerItems , name='customeritems_add'),
        path('my_item_edit/<int:pk>/',editCustomerItems , name='customeritems_edit'),
        path('my_item_delete/<int:pk>/',deleteCustomerItems , name='customeritems_delete'),
        path('my_item_repost/<int:pk>/',repostCustomerItems , name='customeritems_repost'),
        path('customer_item_bid_history/<int:pk>/', customerItemBidHistory, name='customeritem_bidhistory'),
        path('customer_item_bid_winner/<int:pk>/',customerBidWinner,name='customeritems_bidwinner'),
        url('customer_item_search/',customerItemSearch,name='customeritems_search'),


        ###############CUSTOMER RELATED BIDS########################
        path('my_bids/', customerBidsList, name='customer_bids'),
        path('customer_bidagain/<int:pk>/',customerBidAgain,name='customer_bid_again'),
        path('customer_bid/<int:pk>/',customerBidNow,name='customer_bid_now'),
        path('customer_bid_delete/<int:pk>/',customerBidDelete,name='customerbid_delete'),
        path('customer_bid_pdf/',sendpdfEmail,name='Customer_GetPDFBidslist'),



    ]
