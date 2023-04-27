from flask import Flask, request, render_template
from manga_py.util import run_util
import smtplib, ssl
from threading import Thread
import subprocess,os
import uuid

import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Set up email details
smtp_server = 'mail.riseup.net'
smtp_port = 587
sender_email = 'panifically@riseup.net'
sender_password = ''
recipient_email = 'prashantn@riseup.net'


app = Flask(__name__)
app.config.update(
    MAIL_SERVER='mail.riseup.net',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'panifically@riseup.net',
    MAIL_PASSWORD = ''
)

ERRCOUNT = 3
threaded_queue = [] #this is so bad

def send_mail(body,subject,recipient_email,filename):
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
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)


#TODO do a threaded queue to serve one manga request at once [Celery?]
def fetch_and_deliver(__request__,URL,EMAIL,START_VOLUME,GET_VOLUME):
        gen_name = str(uuid.uuid1())   
        test_args = {
            'url': URL, 
            'name': gen_name, 
            'destination': 'static', 
            'no_progress': False, 
            'global_progress': False, 
            'arguments': None,
            'skip_volumes': START_VOLUME, 
            'max_volumes': GET_VOLUME, 
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
        for attempt in range(ERRCOUNT):
            try:
                run_util(test_args)
                break
            except:
                if(attempt == ERRCOUNT-1):
                    return "Failed"
        files = os.listdir(f'static/{gen_name}/')
        is_webtoon = "-m"
        if("webtoon" in URL):
            is_webtoon = "-w"
        subprocess.run(["kcc-c2e",is_webtoon,"-p","KPW","-f","EPUB",f"static/{gen_name}/{files[0]}"])
        send_mail(f"Your requested manga from {URL} is delivered\n Cheers, pacchu",f"Your requested manga from {URL} is delivered",EMAIL,f"static/{gen_name}/{files[0]}".replace(".cbz",".epub"))
        print(f"Sent mail to mailto://{EMAIL}")
        threaded_queue.pop()
        return "Ok"

@app.route("/",methods=["GET","POST"])
def main():
    if request.method == 'GET':
        return render_template("index.html")

    if request.method == 'POST':
        
        URL = request.form.get('manga-link')
        START_VOLUME = int(request.form.get('chapter'))
        EMAIL = request.form.get('email')
        print(f"Got a request for {URL} from {EMAIL} for {START_VOLUME} chapters")
        if(START_VOLUME < 0):
            return render_template("index.html",err="Use proper numbers for chapter count. Can't afford a time machine") 
        if("@" not in EMAIL or len(EMAIL) < 1):
            return render_template("index.html",err="null@null.null not found? Do you have a kindle?") 
        GET_VOLUME = 1
        do_in_thread = Thread(target=fetch_and_deliver,args=(request,URL,EMAIL,START_VOLUME,GET_VOLUME))
        do_in_thread.start()
        threaded_queue.append(do_in_thread)
        return render_template("index.html",saysomething=f"Your request has been recorded and will be delivered\nCurrently {len(threaded_queue)} pending") 

if(__name__=="__main__"):
    app.run("0.0.0.0",8090)
    main()