from flask import Flask, request, render_template
from manga_py.util import run_util
import subprocess,os
import uuid

app = Flask(__name__)

@app.route("/",methods=["GET"])
def main():
    EMAIL = "pacchu@kindle.com"
    #URL = 'https://www.webtoons.com/en/challenge/bright-futures/list?title_no=824476'
    URL = 'https://www.mangaread.org/manga/vagabond/'
    START_VOLUME = 0
    GET_VOLUME = 1
    gen_name = str(uuid())
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
    #subprocess.run(["kcc-c2e","-m","-p","KPW","-f","EPUB","static/vagabond/vol_001.cbz"])
    print("done")

if(__name__=="__main__"):
    #app.run("0.0.0.0",8090)
    main()