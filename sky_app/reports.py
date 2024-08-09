from django.db import connection
from rest_framework import status as st
from rest_framework.response import Response
from datetime import datetime

class CustomerCls:
    @staticmethod
    def add_customer(data):
        cur = connection.cursor()
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

            cur.execute(query)

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'message': 'Something went wrong.',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            if cur is not None:
                cur.close()

    @staticmethod
    def update_customer(name, get_class, f_name, section, data, fees):
        cur = connection.cursor()
        try:

            query = """UPDATE student_info SET 
            `name`= '{}', get_class='{}', f_name='{}',section='{}', updated_at='{}', fees={} 
            WHERE mobile='{}';""".format(name, get_class, f_name, section, datetime.now().strftime("%Y-%m-%d %H-%M-%S"), fees, data.mobile)

            cur.execute(query)

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'message': 'Something went wrong.',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            if cur is not None:
                cur.close()

    @staticmethod
    def get_customer_list(mobile):
        cur = connection.cursor()
        try:
            query = """SELECT `name` AS `name`, get_class AS class, mobile AS mobile, 
                    f_name AS f_name, email AS email, section AS section, fees AS fees 
                    FROM student_info {};""".format('WHERE mobile={}'.format(mobile) if len(mobile) > 0 else '')

            cur.execute(query)
            customer_lst = cur.fetchall()
            columns = [col[0] for col in cur.description]
            result = [dict(zip(columns, row)) for row in customer_lst]
            return result

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            result = []

        finally:
            if cur is not None:
                cur.close()

class UserCls:
    @staticmethod
    def add_user(password, username, first_name, last_name, email):
        cur = connection.cursor()
        try:

            query = """INSERT INTO `auth_user` (`password`, username, first_name, last_name, email, date_joined)
VALUES ('{}', '{}', '{}', '{}', '{}', '{}');""".format(password, username, first_name, last_name, email, datetime.now().strftime("%Y-%m-%d %H-%M-%S"))

            cur.execute(query)

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'message': 'Something went wrong.',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            if cur is not None:
                cur.close()

    @staticmethod
    def add_user_info(mobile, user_id, address):
        cur = connection.cursor()
        try:

            query = """INSERT INTO `user_info` (mobile, user_id, address)
VALUES ('{}',{},'{}');""".format(mobile, user_id, address)

            cur.execute(query)

        except Exception as e:
            print("Exception:- {}".format(str(e)))
            return Response({
                'message': 'Something went wrong.',
                'response_object': []
            }, status=st.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            if cur is not None:
                cur.close()
