from rest_framework import viewsets
from rest_framework import status as st
from rest_framework.response import Response
from django.db.models import Q
from cryptography.fernet import Fernet
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .reports import UserCls
from .models import UserInfo

class CreateUserView(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            f_name = request.data.get('f_name')
            l_name = request.data.get('l_name')
            email = request.data.get('email')
            mobile = request.data.get('mobile')
            address = request.data.get('address')
            password = request.data.get('password')

            username = f_name[0].upper() + f_name[1:]
            check_user = User.objects.filter(email=email).first()

            if check_user is None:
                get_encrypt_pass = CreateUserView.create_encrypt_password(password)

                UserCls.add_user(get_encrypt_pass, username, f_name, l_name, email)

                user_info = User.objects.get(email=email)
                UserCls.add_user_info(mobile, user_info.id, address)
                CreateUserView.create_user_token(email)

                return Response({
                    'message': 'User created successfully.',
                    'response_object': []
                }, status=st.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'message': 'User already exist.',
                    'response_object': []
                }, status=st.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'message': 'Something went wrong',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def create_encrypt_password(password):
        try:
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encrypted_password = fernet.encrypt(password.encode()).decode('utf-8')

            return encrypted_password
        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'message': 'Something went wrong',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def create_user_token(email):
        try:
            user = User.objects.get(email=email)
            token, created = Token.objects.get_or_create(user_id=user.id)
            return token.key

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'message': 'Something went wrong',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            check_user_info = UserInfo.objects.filter(mobile=username).first() if username.isnumeric() else User.objects.filter(Q(email=username) | Q(username=username)).first()

            if check_user_info is not None:
                get_password = User.objects.filter(id=check_user_info.user_id).first() if username.isnumeric() else User.objects.filter(id=check_user_info.id).first()
            else:
                return Response({
                    'message': 'Invalid username or password.',
                    'response_object': []
                }, status=st.HTTP_400_BAD_REQUEST)

            if get_password is not None:
                get_decrypted_password = CreateUserView.create_encrypt_password(password)
            else:
                return Response({
                    'message': 'Invalid username or password.',
                    'response_object': []
                }, status=st.HTTP_400_BAD_REQUEST)

            if check_user_info is not None and get_password.password.__contains__(get_decrypted_password):
                print('yess')

                return Response({
                    'message': 'User created successfully.',
                    'response_object': []
                }, status=st.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'message': 'Invalid username or password.',
                    'response_object': []
                }, status=st.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'message': 'Something went wrong',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

