from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status as st
from .reports import CustomerCls
from rest_framework.response import Response
from .models import StudentInfo
from django.db.models import Q
# Create your views here.


class AddCustomerAPI(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            name = request.data.get('fullname')
            get_class = request.data.get('class')
            mobile = request.data.get('mobile')
            f_name = request.data.get('father_name')
            email = request.data.get('email')
            section = request.data.get('section')
            fees = request.data.get('fees')
            is_update = bool(request.data.get('is_update', False))
            status_code = st.HTTP_200_OK
            message = 'Customer updated successfully.'
            if is_update:
                log_entries = []
                student_details = StudentInfo.objects.get(Q(email=email) | Q(mobile=mobile))
                # log_entries.append({
                #     'table_name': 'student_info',
                #     'column_name': 'name',
                #     'old_value': student_details.name,
                #     'new_value': name,
                #     'reference_id': student_details.id
                # })
                # student_details.name = name
                CustomerCls.update_customer(name, get_class, f_name, section, student_details, fees)

            else:
                student_details = StudentInfo.objects.filter(Q(email=email) | Q(mobile=mobile)).first()
                if student_details is None:
                    data_dict = {
                        'name': name,
                        'get_class': get_class,
                        'mobile': mobile,
                        'f_name': f_name,
                        'email': email,
                        'section': section,
                        'fees': fees
                    }
                    message = 'Customer added successfully.'
                    CustomerCls.add_customer(data_dict)
                    status_code = st.HTTP_201_CREATED
                else:
                    message = 'Customer already exists.'
                    status_code = st.HTTP_400_BAD_REQUEST
            return Response({
                'message': message,
                'response_object': []
            },  status=status_code)

        except StudentInfo.DoesNotExist:
            return Response({
                'message': 'No Student exists with given email/phone.',
                'response_object': []
            }, status=st.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'message': 'Something went wrong',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)


class GetCustomerAPI(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            status_code = st.HTTP_200_OK
            mobile = request.data.get('mobile')
            customer_lst = CustomerCls.get_customer_list(mobile)
            response_object = [{
                'name': customer.get('name'),
                'class': customer.get('class'),
                'mobile': customer.get('mobile'),
                'f_name': customer.get('f_name'),
                'email': customer.get('email'),
                'section': customer.get('section'),
                'fees': customer.get('fees')
            }for customer in customer_lst]
            return Response({
                'message': '',
                'response_object': response_object
            },  status=status_code)

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'message': 'Something went wrong',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

