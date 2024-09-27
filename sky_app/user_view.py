from rest_framework import viewsets
from rest_framework import status as st
from cryptography.fernet import Fernet
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from sky_app.reports import UserCls
from sky_an_app.response_handler import api_response
from utils.loggers import log_message
class CreateUserView(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            log_message({"function": "CreateUserView", "Started": True})
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

                log_message({"function": "CreateUserView", "Completed": True})
                return api_response('success', 'User created successfully.', [], st.HTTP_201_CREATED)

            else:
                log_message({"function": "CreateUserView", "Completed": True})
                return api_response('fail', 'User already exist.', [], st.HTTP_400_BAD_REQUEST)

        except Exception as e:
            api_response('fail', 'Something went wrong. Error: {}'.format(str(e)), [],
                         st.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def create_encrypt_password(password, is_update=False):
        try:
            log_message({"function": "create_encrypt_password", "Started": True})
            # key = Fernet.generate_key()
            key = b'ewvd1sGLZlF4Y5bdmQ3qZLPuD5ZNj1nZdFsUpMFm90c='
            fernet = Fernet(key)
            encrypted_password = fernet.encrypt(password.encode()).decode('utf-8')
            if is_update:
                decrypted_pass = fernet.decrypt(password).decode('utf-8')
                log_message({"function": "create_encrypt_password", "Completed": True})
                return decrypted_pass
            else:
                log_message({"function": "create_encrypt_password", "Completed": True})
                return encrypted_password
        except Exception as e:
            api_response('fail', 'Something went wrong. Error: {}'.format(str(e)), [],
                         st.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def create_user_token(email):
        try:
            log_message({"function": "create_user_token", "Started": True})
            user = User.objects.get(email=email)
            token, created = Token.objects.get_or_create(user_id=user.id)
            log_message({"function": "create_user_token", "Completed": True})
            return token.key

        except Exception as e:
            api_response('fail', 'Something went wrong. Error: {}'.format(str(e)), [],
                         st.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            log_message({"function": "UserLoginView", "Started": True})
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
                    log_message({"function": "UserLoginView", "Completed": True})
                    return api_response('success', '', [], st.HTTP_200_CREATED)

                else:
                    log_message({"function": "UserLoginView", "Completed": True})
                    return api_response('fail', 'Invalid credentials', [], st.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return api_response('fail', 'No User exists.', [], st.HTTP_400_BAD_REQUEST)

        except Exception as e:
            api_response('fail', 'Something went wrong. Error: {}'.format(str(e)), [],
                         st.HTTP_500_INTERNAL_SERVER_ERROR)
