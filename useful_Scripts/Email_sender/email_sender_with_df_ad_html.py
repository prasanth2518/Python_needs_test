import http
import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

import pandas as pd

fromaddr = "pskr324@gmail.com"
sendto = ['prasanthutti@exponentialai.com', 'pskr324@gmail.com', "prasanth.utti@anthem.com"]

j = [{"respcd": 758, "no_case": 2}, {"respcd": 753, "no_case": 8}, {"respcd": 759, "no_case": 4}]
df = pd.DataFrame(j)

df.to_csv("reprocess_report.csv")


def email_sender_with_df_ad_html(df, fromaddr, sendto):
    try:
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ', '.join(sendto)
        msg['Subject'] = 'This 2nd time'
        msg['Date'] = formatdate(localtime=True)

        body = "this is the body of the text message"

        html = """\
        <html>
          <head></head>
          <body>
            {0}
          </body>
        </html>
        """.format(df.to_html())

        msg.attach(MIMEText(body, 'plain'))

        part = MIMEText(html, 'html')
        msg.attach(part)

        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login('pskr324@gmail.com', 'Gmail#24')

        text = msg.as_string()
        smtpObj.sendmail(fromaddr, sendto, text)
        smtpObj.quit()
        result = {"messsage": "e-Mail sent successfullly", "status_code": http.HTTPStatus.OK}
    except Exception as e:
        result = {"error": str(e), "traceback": str(traceback.format_exc()), "status_code": http.HTTPStatus.BAD_GATEWAY}

    return result
