from rest_framework import status as st
from rest_framework.response import Response
from datetime import datetime
from sky_an_app.query_handler import execute_query, insert_query

class CustomerCls:
    @staticmethod
    def add_customer(data):
        try:
            name = data.get('name')
            get_class = data.get('get_class')
            mobile = data.get('mobile')
            f_name = data.get('f_name')
            email = data.get('email')
            section = data.get('section')
            fees = data.get('fees')
            query = """insert into student_info (`name`,get_class,mobile,f_name,email,section,created_at,fees) 
                     values ('{}', '{}', '{}', 
                     '{}', '{}', '{}', '{}', {})""".format(name, get_class, mobile, f_name, email, section, datetime.now().strftime("%Y-%m-%d %H-%M-%S"), fees)

            insert_query(query)

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'message': 'Something went wrong.',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)


    @staticmethod
    def update_customer(name, get_class, f_name, section, data, fees):
        try:

            query = """UPDATE student_info SET 
            `name`= '{}', get_class='{}', f_name='{}',section='{}', updated_at='{}', fees={} 
            WHERE mobile='{}';""".format(name, get_class, f_name, section, datetime.now().strftime("%Y-%m-%d %H-%M-%S"), fees, data.mobile)

            insert_query(query)

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'message': 'Something went wrong.',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_customer_list(name):
        try:
            query = """SELECT `name` AS `name`, get_class AS class, mobile AS mobile, 
                    f_name AS f_name, email AS email, section AS section, fees AS fees 
                    FROM student_info {};""".format('WHERE `name` LIKE "%{}%"'.format(name) if len(name) > 0 else '')

            return execute_query(query)

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            result = []

class UserCls:
    @staticmethod
    def add_user(password, username, first_name, last_name, email):
        try:

            query = """INSERT INTO `auth_user` (`password`, username, first_name, last_name, email, date_joined)
VALUES ('{}', '{}', '{}', '{}', '{}', '{}');""".format(password, username, first_name, last_name, email, datetime.now().strftime("%Y-%m-%d %H-%M-%S"))

            insert_query(query)

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'message': 'Something went wrong.',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def add_user_info(mobile, user_id, address):
        try:

            query = """INSERT INTO `user_info` (mobile, user_id, address)
VALUES ('{}',{},'{}');""".format(mobile, user_id, address)

            insert_query(query)

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'message': 'Something went wrong.',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)
