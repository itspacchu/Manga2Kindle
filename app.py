from flask import Flask, request, render_template
from flask_mail import Mail,Message
from manga_py.util import run_util
import smtplib, ssl
import subprocess,os
import uuid

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='mail.riseup.net',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'scrclab@riseup.net',
    MAIL_PASSWORD = ''
)
mail = Mail(app)

@app.route("/",methods=["GET"])
def main():
    EMAIL = "pacchu@kindle.com"
    URL = 'https://www.webtoons.com/en/fantasy/crimson-heart/list?title_no=4898'
    START_VOLUME = 0
    GET_VOLUME = 1

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

    x = run_util(test_args)
    files = os.listdir(f'static/{gen_name}/')
    subprocess.run(["kcc-c2e","-m","-p","KPW","-f","MOBI",f"static/{gen_name}/{files[0]}"])
    msg = Message(files[0],
                  sender="scrclab@riseup.net",
                  recipients=["pacchu@kindle.com"]
                )
    with app.open_resource(f"static/{gen_name}/{files[0]}".replace(".cbz",".mobi")) as fp:
        msg.attach(f"{files[0]}".replace(".cbz",".mobi"), 'application/x-mobipocket-ebook', fp.read())
    mail.send(msg)
    return "0"

if(__name__=="__main__"):
    app.run("0.0.0.0",8090)
    main()