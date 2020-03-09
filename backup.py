import time
import os
import sys
import tarfile
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
# Config
# Source directories
DIRECTORY_LIST = (
    "/home/feelan/project/",
    "/home/feelan/Downloads/"
)
# Target directory to store the backup
TARGET_DIRECTORY = "/home/feelan/backup/"
timestamp = time.strftime("%d.%m.%Y")

numBackupItems = len(DIRECTORY_LIST)
currBackupItem = 0
nameBackup = (f"backup-{timestamp}.tar.gz")
gpgname = "feelan"
filepath = TARGET_DIRECTORY+nameBackup

with tarfile.open(TARGET_DIRECTORY + nameBackup, "w:gz") as tar:
    for i in range(len(DIRECTORY_LIST)):
        tar.add(
            DIRECTORY_LIST[i], arcname=f"backup/{DIRECTORY_LIST[i].split('/')[-2]}")
    tar.close()
subprocess.call(
    f'gpg -r {gpgname} --armor --encrypt {filepath} && rm {filepath}', shell=True)

fromaddress = "*******"
toaddress = "*******"
# Template email
part = MIMEBase('application', 'octet-stream')
part.set_payload(open(filepath+'.asc', 'rb').read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="%s"' %
                nameBackup+'.asc')

msg = MIMEMultipart()
msg['From'] = fromaddress
msg['To'] = toaddress
msg.attach(part)
# SMTP settings
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddress, '****')
server.sendmail(fromaddress, toaddress, msg.as_string())
server.quit()
