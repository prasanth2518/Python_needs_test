import http
import smtplib
import traceback
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

fromaddr = "pskr324@gmail.com"
sendto = ['prasanthutti@exponentialai.com', 'pskr324@gmail.com']


def email_sender_with_body_and_file(fromaddr, sendto):
    try:
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ', '.join(sendto)
        msg['Subject'] = 'This 2nd time'
        msg['Date'] = formatdate(localtime=True)

        body = "this is the body of the text message"

        msg.attach(MIMEText(body, 'plain'))

        filename = 'dummy.xlsx"'
        # attachment = open('dummy.xlsx"', 'rb')

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open("dummy.xlsx", "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)

        msg.attach(part)

        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login('pskr324@gmail.com', '******')

        text = msg.as_string()
        smtpObj.sendmail(fromaddr, sendto, text)
        smtpObj.quit()
        result = {"messsage": "e-Mail sent successfullly", "status_code": http.HTTPStatus.OK}
    except Exception as e:
        result = {"error": str(e), "traceback": str(traceback.format_exc()), "status_code": http.HTTPStatus.BAD_GATEWAY}

    return result
