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

            query = """insert into student_info (`name`,get_class,mobile,f_name,email,section,created_at) 
                     values ('{}', '{}', '{}', 
                     '{}', '{}', '{}', '{}')""".format(name, get_class, mobile, f_name, email, section, datetime.now().strftime("%Y-%m-%d %H-%M-%S"))

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
    def update_customer(name, get_class, f_name, section, data):
        cur = connection.cursor()
        try:

            query = """UPDATE student_info SET 
            `name`= '{}', get_class='{}', f_name='{}',section='{}', updated_at='{}' 
            WHERE mobile='{}';""".format(name, get_class, f_name, section, datetime.now().strftime("%Y-%m-%d %H-%M-%S"), data.mobile)

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
    def get_customer_list():
        cur = connection.cursor()
        try:
            query = """SELECT `name` AS `name`, get_class AS class, mobile AS mobile, 
                    f_name AS f_name, email AS email, section AS section 
                    FROM student_info;"""

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

