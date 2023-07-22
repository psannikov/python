import smtplib, ssl
from email.header import Header
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

class EmailWorker:

    def __init__(self, config):
        home_directory = os.path.expanduser( '~' )
        project_path = os.path.join(home_directory, 'project')
        self.SENDER_EMAIL = config['EmailWorker']['SENDER_EMAIL']
        self.RECEIVER_EMAIL = config['EmailWorker']['RECEIVER_EMAIL']
        self.SMTP_SERVER = config['EmailWorker']['SMTP_SERVER']
        self.PORT = int(config['EmailWorker']['PORT'])
        self.LOGIN = config['EmailWorker']['LOGIN']
        self.PASSWORD = config['EmailWorker']['PASSWORD']
        self.message = MIMEMultipart()
        self.TOP_SKILL_IN_ALL_VACANCY = os.path.join(project_path, config['SQLWorker']['TOP_SKILL_IN_ALL_VACANCY'])
        self.TOP_SKILL_IN_VACANCY_BY_INDUSTRY_ID = os.path.join(project_path, config['SQLWorker']['TOP_SKILL_IN_VACANCY_BY_INDUSTRY_ID'])
        self.TOP_SKILL_IN_VACANCY_FILTER_COMPANIES = os.path.join(project_path, config['SQLWorker']['TOP_SKILL_IN_VACANCY_FILTER_COMPANIES'])

    def prepareMessage(self):
        self.message = MIMEMultipart()
        self.message["Subject"] = Header('Отчет о ТОП скиллах для телекомуникационных компаний', 'utf-8')
        self.message["From"] = self.SENDER_EMAIL
        self.message["To"] = self.RECEIVER_EMAIL
        html = """\
            <html>
            <body>
            <p>Привет!<br>
            Это сообщение - результат работы финального проекта курса <strong>Python для продвинутых специалистов.</strong>
            </p>
            --
            <p>Выполнена загрузка, обработка и сохранение данных <a href='https://ofdata.ru/open-data/download/okved_2.json.zip'>ЕГРЮЛ</a>.</p>
            <p>Выполнена загрузка, обработка и сохранение данных <a href='hh.ru'>вакансий HeadHunter</a>.</p>
            <p>Выполнена выборка итоговых результатов и подсчет данных</p>
            <p>ТОП10 навыков и количество упоминаний во вложениях:
            <ul>
            <li>top10all.xlsx - ТОП10 скилов во всех вакансиях</li>
            <li>top10industry.xlsx - ТОП10 скилов в вакансиях с фильтром по данным HeadHunter</li>
            <li>top10okved.xlsx - ТОП10 скилов в вакансиях компаний по ОКВЕД ТЕЛЕКОМ</li>
            </ul>
            </p>
            </body>
            </html>
            """
        self.message.attach(MIMEText(html, 'html', 'utf-8'))
        filenames = [self.TOP_SKILL_IN_ALL_VACANCY, self.TOP_SKILL_IN_VACANCY_BY_INDUSTRY_ID, self.TOP_SKILL_IN_VACANCY_FILTER_COMPANIES]
        for filename in filenames:
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition",f"attachment; filename= {filename}")
            self.message.attach(part)

    def send_mail(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.SMTP_SERVER, self.PORT, context=context) as server:
            server.login(self.LOGIN, self.PASSWORD)
            server.sendmail(self.SENDER_EMAIL, self.RECEIVER_EMAIL, self.message.as_string())
            print("Письмо отправлено!")
