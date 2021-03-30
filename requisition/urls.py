    
    
from django.contrib import admin
from django.urls import path,include
from. import views


urlpatterns = [   
    path('', views.RequisitionListView.as_view(), name='requisition-home'),


    #Details

    path('update/<pk>/', views.RequisitionUpdateView.as_view(), name='update-requisition'),

    #requisitarNew
    path('create/', views.requisitionEntry, name='create-requisition'),
    #requisition-confirm
    
    
    #vertodos
    path('seeAll/',views.seeAll, name='see-all'),
   
    path('<pk>/', views.RequisitionDetailView.as_view(), name='detail-requisition'),


    path('seeNotification/<pk>/', views.seeNotification, name='see-notification'),


    #ajax
    #check user
    path('ajax/checkUser', views.checkUser, name='ajax-check-user'),

    path('ajax/addBook', views.addBook, name='ajax-add-book'),

    path('ajax/confirmRequisition', views.confirmRequisition, name='ajax-confirm-requisition'),

    

    

    ##Funções
    #

   
#     path('requisition/confirm', RequisitionCreateView.as_view(), name='requisition-confirm'),
#     path('cancelRequisition', views.cancelRequisition , name='requisition-cancel'),
#     path('requisition/list', views.RequisitionListView.as_view(), name='requisition-list'),
#     path('requisition/<pk>/', views.RequisitionUpdateView.as_view(), name='requisition-update'),
]