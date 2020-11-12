    
    
from django.contrib import admin
from django.urls import path,include
from. import views


urlpatterns = [   
    path('', views.RequisitionListView.as_view(), name='requisition-home'),


    #Details

    path('update/<pk>/', views.RequisitionUpdateView.as_view(), name='update-requisition'),

    #requisitarNew
    path('create/', views.RequisitionView.as_view(), name='create-requisition'),
    #requisition-confirm
    path('create/confirm', views.RequisitionCreateView.as_view(), name='confirm-requisition'),
    
    #vertodos
    path('seeAll/',views.seeAll, name='see-all'),
    path('create/cancelRequisition', views.cancelRequisition , name='requisition-cancel'),
    path('<pk>/', views.RequisitionDetailView.as_view(), name='detail-requisition')


    ##Funções
    #

   
#     path('requisition/confirm', RequisitionCreateView.as_view(), name='requisition-confirm'),
#     path('cancelRequisition', views.cancelRequisition , name='requisition-cancel'),
#     path('requisition/list', views.RequisitionListView.as_view(), name='requisition-list'),
#     path('requisition/<pk>/', views.RequisitionUpdateView.as_view(), name='requisition-update'),
]