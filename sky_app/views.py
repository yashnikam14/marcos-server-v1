from rest_framework import viewsets
from rest_framework import status as st
from .reports import CustomerCls
from rest_framework.response import Response
from .models import StudentInfo
from django.db.models import Q
from marcos_server.utils.loggers import log_message
from marcos_server.sky_an_app.response_handler import api_response
# Create your views here.


class AddCustomerAPI(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            log_message({"function": "AddCustomerAPI", "Started": True})
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
                student_details = StudentInfo.objects.get(Q(email=email) | Q(mobile=mobile))
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
            log_message({"function": "AddCustomerAPI", "Completed": True})

            return api_response('success', '', [], status_code)

        except StudentInfo.DoesNotExist:
            return api_response('fail', 'No Student exists with given email/phone.', [], st.HTTP_400_BAD_REQUEST)

        except Exception as e:
            api_response('fail', 'Something went wrong. Error: {}'.format(str(e)), [], st.HTTP_500_INTERNAL_SERVER_ERROR)



class GetCustomerAPI(viewsets.ViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        try:
            log_message({"function": "GetCustomerAPI", "Started": True})
            status_code = st.HTTP_200_OK
            name = request.data.get('name')
            customer_lst = CustomerCls.get_customer_list(name)
            response_object = [{
                'name': customer.get('name'),
                'class': customer.get('class'),
                'mobile': customer.get('mobile'),
                'f_name': customer.get('f_name'),
                'email': customer.get('email'),
                'section': customer.get('section'),
                'fees': customer.get('fees')
            }for customer in customer_lst]
            log_message({"function": "GetCustomerAPI", "Completed": True})

            return api_response('success', '', [], status_code)

        except Exception as e:
            api_response('fail', 'Something went wrong. Error: {}'.format(str(e)), [],
                         st.HTTP_500_INTERNAL_SERVER_ERROR)


