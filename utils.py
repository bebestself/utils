import smtplib
import unittest
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pymysql
import requests


class Utils:
    '''
    辅助方法类
    '''

    @classmethod
    def get_data_from_csv(cls, path, sep=',|-'):
        '''
        从数据层文件获取数据并返回列表
        :param path:
        :param sep:
        :return:
        '''
        data = []
        with open(path, "r", encoding='UTF8') as f:
            for i in f:
                if sep == ',':
                    userinfo = i.strip().split(',')
                    data.append(userinfo)
                else:
                    userinfo = i.strip().split('-')
                    data.append(userinfo)
        return data

    def login_success(self):
        body = {
            'username': 'jusenhao',
            'password': 'jsh123'
        }
        r = requests.post("https://patienttest.medtion.com/dev/medical/login/signin", json=body)
        token = r.json()['data']['token']
        return token

    @classmethod
    def send_email(cls, file_path, filename):
        '''
        测试报告邮件发送
        :param filename:
        :return:
        '''
        smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)
        smtp.login("1049816406@qq.com", "nefbcjgoctwjbfai")

        smg = MIMEMultipart()
        text_smg = MIMEText("接口测试报告展示", "plain", "utf8")  # 邮件内容
        smg.attach(text_smg)  # 添加到邮件

        file_msg = MIMEApplication(open(file_path, "rb").read())
        file_msg.add_header('content-disposition', 'attachment', filename=filename)
        smg.attach(file_msg)

        smg["Subject"] = "Api测试"  # 主题
        smg["From"] = "1049816406@qq.com"  # 邮件内显示的发件人
        smg["To"] = "bebestself528@gmail.com"  # 邮件内显示的收件人
        smtp.send_message(smg, from_addr="1049816406@qq.com", to_addrs="bebestself528@gmail.com")


    @classmethod
    def connect_db(cls,sql,where):
        '''
        连接数据库执行sql
        :param sql: 外部传入的sql
        :return:
        '''
        if where == 1:
            host = '120.78.178.42'
            port = 3308
            user = 'naoyihui_patient_dev'
            passwd = 'o@Yn2mz@OMb^iVKv'
            database = 'naoyihui-patient-dev'
            charset = 'utf8'
            db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, database=database, charset=charset)
            cu = db.cursor()
            try:
                cu.execute(sql)
                db.commit()
                print('数据库操作成功')
            except:
                db.rollback()
            db.close()
            r = cu.fetchall()  # 查询结果
            return r
        if where == 2:
            host = '120.77.248.37'
            port = 13306
            user = 'naoyihui_doctor_dev'
            passwd = 'ByFlpSr3je*$u7D&'
            database = 'naoyihui-doctor-dev'
            charset = 'utf8'
            db = pymysql.connect(host=host,port=port,user=user,passwd=passwd,database=database,charset=charset)
            cu = db.cursor()
            try:
                cu.execute(sql)
                db.commit()
                print('数据库操作成功')
            except:
                db.rollback()
            db.close()
            r = cu.fetchall()#查询结果
            return r



if __name__ == '__main__':
    unittest.main()
Utils().connect_db('select count(1) from user_basic;',1)
