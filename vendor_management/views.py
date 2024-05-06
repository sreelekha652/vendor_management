from django.shortcuts import render
import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from .serializers import *
from .models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import PurchaseOrder
from datetime import datetime,timezone
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


#A class that handles the login functionality for the API.
class LoginAPI(APIView):
    def post(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        except User.DoesNotExist:
            return Response({"error": "Invalid username"}, status=400)



# This class likely handles API requests related to managing vendor profiles.
class Vendor_Profile_Management(APIView):
    permission_classes = [IsAuthenticated]
    
    serializer_class = Vendor_Serializer

    """
        This function retrieves vendor data based on the provided vendor ID or returns all vendor data
        if no ID is specified.
        
        
        """
    def get(self, request,vendor_id = None , *args, **kwargs):
      
        try:
            if vendor_id :
                vendor_obj=Vendor.objects.get(id=vendor_id)
                serializer=self.serializer_class(vendor_obj)
                return Response({'status': True, 'data': serializer.data, 'message': 'Data passed successfully'})
            vendor_obj=Vendor.objects.all()
            serializer=self.serializer_class(vendor_obj,many=True)
            return Response({'status': True, 'data': serializer.data, 'message': 'Data passed successfully'})
        except Exception as e:
            print(e)
            return Response({"status": False, "data": str(e), "message": "Something went wrong!"})
    """
    The function receives a POST request, validates the data using a serializer, saves the data if
    valid, and returns a response with status, data, and a message.
    
    """
    def post(self, request, *args, **kwargs):
      
        try:
            serializer=Vendor_Serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'data': serializer.data, 'message': 'Data passed successfully'})
            else:
                return Response({'status': True, 'data': serializer.errors, 'message': 'Data passed successfully'})
        except Exception as e:
            print(e)
            return Response({"status": False, "data": str(e), "message": "Something went wrong!"})
    """
    This Python function updates vendor data and handles exceptions gracefully.
    
    
    """  
    def put(self, request, vendor_id, *args, **kwargs):
     
        try:
            vendor_obj = Vendor.objects.get(id=vendor_id)
            serializer = self.serializer_class(vendor_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'data': serializer.data, 'message': 'Data updated successfully'})
            return Response({'status': False, 'data': serializer.errors, 'message': 'Invalid data provided'}, status=400)
        except Vendor.DoesNotExist:
            return Response({'status': False, 'message': 'Vendor not found'}, status=404)
        except Exception as e:
            print(e)
            return Response({"status": False, "data": str(e), "message": "Something went wrong!"}, status=500)
    """
    This function deletes a vendor object by its ID and returns a success message if the deletion is
    successful, or an error message if the vendor is not found or an exception occurs.

    """ 
    def delete(self, request, vendor_id, *args, **kwargs):
      
        try:
            vendor_obj = Vendor.objects.get(id=vendor_id)
            vendor_obj.delete()
            return Response({'status': True, 'message': 'Vendor deleted successfully'})
        except Vendor.DoesNotExist:
            return Response({'status': False, 'message': 'Vendor not found'}, status=404)
        except Exception as e:
            print(e)
            return Response({"status": False, "data": str(e), "message": "Something went wrong!"}, status=500)
        

class Purchase_Order_Tracking_Api(APIView):
    permission_classes = [IsAuthenticated]
    
    serializer_class = PurchaseOrderSerializer
    """
This Python function retrieves a PurchaseOrder object by ID or returns all PurchaseOrder objects
serialized in a response.

"""
    def get(self, request,po_id = None , *args, **kwargs):
   
        try:
            if po_id :
                po_obj=PurchaseOrder.objects.get(id=po_id)
                serializer=self.serializer_class(po_obj)
                return Response({'status': True, 'data': serializer.data, 'message': 'Data passed successfully'})
            po_obj=PurchaseOrder.objects.all()
            serializer=self.serializer_class(po_obj,many=True)
            return Response({'status': True, 'data': serializer.data, 'message': 'Data passed successfully'})
        except Exception as e:
            print(e)
            return Response({"status": False, "data": str(e), "message": "Something went wrong!"})
        
    """
        This function is a POST request handler that validates and saves purchase order data, returning a
        success response if valid or error response if not.
        
        """
    def post(self, request, *args, **kwargs):
      
        try:
            serializer=PurchaseOrderSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid():
                print("kkkk")
                summ=serializer.save()
                print(summ)
            
                return Response({'status': True, 'data': serializer.data, 'message': 'Data passed successfully'})
            else:
                print(serializer.errors)
                return Response({'status': True, 'data': serializer.errors, 'message': 'Data passed successfully'})
        except Exception as e:
            print(e)
            return Response({"status": False, "data": str(e), "message": "Something went wrong!"})
    """
        This Python function updates a PurchaseOrder object based on the provided ID and returns a response
        indicating the success or failure of the operation.
        
    
        """    
    def put(self, request, po_id, *args, **kwargs):
       
      
        try:
            po_obj = PurchaseOrder.objects.get(id=po_id)
            serializer = self.serializer_class(po_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'data': serializer.data, 'message': 'Data updated successfully'})
            return Response({'status': False, 'data': serializer.errors, 'message': 'Invalid data provided'}, status=400)
        except PurchaseOrder.DoesNotExist:
            return Response({'status': False, 'message': 'order not found'}, status=404)
        except Exception as e:
            print(e)
            return Response({"status": False, "data": str(e), "message": "Something went wrong!"}, status=500)
    """
        This function deletes a PurchaseOrder object by its ID and returns a success message if the
        deletion is successful, otherwise it returns an error message.
      
        """    
    def delete(self, request, po_id, *args, **kwargs):
      
        try:
            po_obj = PurchaseOrder.objects.get(id=po_id)
            po_obj.delete()
            return Response({'status': True, 'message': 'purchase order deleted successfully'})
        except PurchaseOrder.DoesNotExist:
            return Response({'status': False, 'message': 'order not found'}, status=404)
        except Exception as e:
            print(e)
            return Response({"status": False, "data": str(e), "message": "Something went wrong!"}, status=500)

# This Python class named Vendor_Performance retrieves performance data for a specific vendor based on
# the provided vendor ID.
class Vendor_Performance(APIView):
    permission_classes = [IsAuthenticated]
   
    def get(self, request,vendor_id = None , *args, **kwargs):
        try:
            print(request.user)
            if vendor_id :
                vendor_obj=Vendor.objects.filter(id=vendor_id).values('on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate')
                
                return Response({'status': True, 'data': vendor_obj, 'message': 'Data passed successfully'})
            
            
        except Exception as e:
            print(e)
            return Response({"status": False, "data": str(e), "message": "Something went wrong!"})
        
# This Python class acknowledges a purchase order by updating its acknowledgment date and vendor
# metrics.
class acknowledge_purchase_order(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request, po_id):
        try:
           
            purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
        
            purchase_order.acknowledgment_date = timezone.now()
            
            purchase_order.update_vendor_metrics()
            purchase_order.save()
            return JsonResponse({'message': 'Purchase order acknowledged successfully.'})
        except Exception as e:
            print(e)
            return Response({"status": False, "data": str(e), "message": "Something went wrong!"})

