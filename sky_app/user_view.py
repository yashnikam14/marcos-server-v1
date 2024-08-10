from rest_framework import viewsets
from rest_framework import status as st
from rest_framework.response import Response
from django.db.models import Q
from cryptography.fernet import Fernet
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .reports import UserCls

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
                    'status': 'success',
                    'message': 'User created successfully.',
                    'response_object': []
                }, status=st.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'status': 'fail',
                    'message': 'User already exist.',
                    'response_object': []
                }, status=st.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'status': 'fail',
                'message': 'Something went wrong',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def create_encrypt_password(password, is_update=False):
        try:
            # key = Fernet.generate_key()
            key = b'ewvd1sGLZlF4Y5bdmQ3qZLPuD5ZNj1nZdFsUpMFm90c='
            fernet = Fernet(key)
            encrypted_password = fernet.encrypt(password.encode()).decode('utf-8')
            if is_update:
                decrypted_pass = fernet.decrypt(password).decode('utf-8')
                return decrypted_pass
            else:
                return encrypted_password
        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'status': 'fail',
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
                'status': 'fail',
                'message': 'Something went wrong',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            check_user = User.objects.get(username=username)

            if check_user:
                check_password = check_user.password
                get_password = CreateUserView.create_encrypt_password(check_password, is_update=True)

                if password == get_password:
                    get_token = Token.objects.get(user_id=check_user.id)
                    response_object = {
                        'id': check_user.id,
                        'username': username,
                        'token': get_token.key
                    }
                    return Response({
                        'status': 'success',
                        'message': '',
                        'response_object': response_object
                    }, status=st.HTTP_200_OK)
                else:
                    return Response({
                        'status': 'fail',
                        'message': 'Invalid credentials',
                        'response_object': []
                    }, status=st.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({
                'status': 'fail',
                'message': 'No User exists.',
                'response_object': []
            }, status=st.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'status': 'fail',
                'message': 'Something went wrong',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)
