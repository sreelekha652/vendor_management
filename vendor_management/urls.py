from django.urls import path
from .views import *


urlpatterns = [
    path('loginapi/', LoginAPI.as_view() ),
    path('post/api/vendors/', Vendor_Profile_Management.as_view() ),
    path('get/api/vendors/', Vendor_Profile_Management.as_view() ),
    path('get/api/vendors/<int:vendor_id>/', Vendor_Profile_Management.as_view()),
    path('put/api/vendors/<int:vendor_id>/', Vendor_Profile_Management.as_view()),
    path('delete/api/vendors/<int:vendor_id>/', Vendor_Profile_Management.as_view()),
     path('post/api/purchase_order/', Purchase_Order_Tracking_Api.as_view() ),
    path('get/api/purchase_order/', Purchase_Order_Tracking_Api.as_view() ),
    path('get/api/purchase_order/<int:po_id>/', Purchase_Order_Tracking_Api.as_view()),
    path('put/api/purchase_order/<int:po_id>/', Purchase_Order_Tracking_Api.as_view()),
    path('delete/api/purchase_order/<int:po_id>/', Purchase_Order_Tracking_Api.as_view()),
    path('get/api/vendor/<int:vendor_id>/performance/', Vendor_Performance.as_view()),
    path('api/purchase_orders/<int:po_id>/acknowledge/', acknowledge_purchase_order.as_view()),
]
