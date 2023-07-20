import smtplib, ssl
from email.header import Header
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailWorker:

    SENDER_EMAIL = 'sannikovpv.87@yandex.ru'
    RECEIVER_EMAIL = 'psannikov87@gmail.com'
    SMTP_SERVER = 'smtp.yandex.ru'
    PORT = 465
    LOGIN = 'sannikovpv.87'
    PASSWORD = "iwuaqdxbximunilr"
    message = MIMEMultipart()

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
        filenames = ['top10all.xlsx','top10industry.xlsx','top10okved.xlsx']
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
