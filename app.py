from manga_py.util import run_util
import smtplib, ssl
from threading import Thread
import subprocess,os
import uuid
import argparse

import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Set up email details
smtp_server = 'mail.riseup.net'
smtp_port = 587
sender_email = 'panifically@riseup.net'
sender_password = os.environ["LOGIN_PASSWORD"]
recipient_email = 'prashantn@riseup.net'


ERRCOUNT = 3

def dictionary_to_parser(dictionary):
    parser = argparse.ArgumentParser()
    for key, value in dictionary.items():
        parser.add_argument(f'--{key}', default=value)
    return parser


def send_mail(body,subject,recipient_email,filename):
    print(f"Sending to {recipient_email}")
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'File attachment'

    with open(filename, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='epub')
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        print(smtp.login(sender_email, sender_password))
        print(smtp.send_message(msg))





#TODO do a threaded queue to serve one manga request at once [Celery?]
def fetch_and_deliver(URL,EMAIL,START_VOLUME,GET_VOLUME):
        gen_name = str(uuid.uuid1())
        test_args = {
            'url': URL, 
            'name': gen_name, 
            'destination': '/tmp/static', 
            'no_progress': False, 
            'global_progress': False, 
            'arguments': None,
            'skip_volumes': int(START_VOLUME), 
            'max_volumes': int(GET_VOLUME), 
            'user_agent': None, 
            'cookies': None, 
            'proxy': None, 
            'reverse_downloading': False, 
            'rewrite_exists_archives': False, 
            'max_threads': 4, 
            'zero_fill': False, 
            'force_provider': None, 
            'with_manga_name': False, 
            'override_archive_name': 'manga.cbz', 
            'min_free_space': 100, 
            'skip_incomplete_chapters': True, 
            'wait_after_page': 0, 
            'wait_after_chapter': 0, 
            'create_empty_files': False, 
            'auto_skip_deleted': False, 
            'flare_solver_url': None, 
            'cbz': True, 
            'rename_pages': False, 
            'not_change_files_extension': False, 
            'no_webp': False, 
            'print_json': False, 
            'simulate': False,
            'show_current_chapter_info': False, 
            'save_current_chapter_info': False, 
            'show_chapter_info': False, 
            'save_chapter_info': False, 
            'save_manga_info': False, 
            'debug': False,
            'debug_version': None, 
            'quiet': False
        }
        #run_util(dictionary_to_parser(test_args))
        run_util(test_args)
        # for attempt in range(ERRCOUNT):
        #     try:
        #         run_util(test_args)
        #         break
        #     except:
        #         if(attempt == ERRCOUNT-1):
        #             return "Failed"
        files = os.listdir(f'/tmp/static/{gen_name}/')
        is_webtoon = "-m"
        if("webtoon" in URL):
            is_webtoon = "-w"
        os.system(" ".join(["kcc-c2e",is_webtoon,"-p","KPW","-f","EPUB",f"/tmp/static/{gen_name}/{files[0]}"]))
        send_mail(f"Your requested manga from {URL} is delivered\n Cheers, pacchu",f"Your requested manga from {URL} is delivered",EMAIL,f"/tmp/static/{gen_name}/{files[0]}".replace(".cbz",".epub"))
        print(f"Sent mail to mailto://{EMAIL}")
        os.remove(f"/tmp/static/{gen_name}/{files[0]}".replace(".cbz",".epub"))
        return "Ok"

if(__name__=="__main__"):
    URL = os.environ["URL"]
    EMAIL = os.environ["EMAIL"]
    START = os.environ["START"]
    fetch_and_deliver(URL,EMAIL,START,1)
