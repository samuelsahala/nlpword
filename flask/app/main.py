import os

from flask import Blueprint, render_template, request
import requests
import docx
from bs4 import BeautifulSoup
from .helper import lxml_tag_visible, re_clean_text_bag, url_reachable, trie_word_save, \
    trie_search_word

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index.html')
def index():
    return render_template('index.html', message="")


@main.route('/ws')
def ws():
    return render_template('ws.html', message="")


@main.route('/search', methods=['POST'])
def search_word():
    _word = request.form['search_word']
    res = trie_search_word(_word)
    if res:
        return render_template('ws.html', **res)
    else:
        return render_template('ws.html', message="'"+_word+"' does not exist,<br/> please try another word")


@main.route('/submit-string', methods=['POST'])
def string_to_text_bag():
    if request.method == 'POST':
        texts = request.form['string']
        if texts == '':
            return render_template('index.html', message="please enter required fields")
        if "target" in texts:
            if texts.endswith("\r\n"):
                texts = texts[:-2]
            filename = texts[texts.index("=") + len("="):]
            script_dir = os.path.dirname(__file__)
            rel_path = "static/uploads/" + filename
            abs_file_path = os.path.join(script_dir, rel_path)
            f = open(abs_file_path, "r")
            text_bag = f.read()
            clean_text_bag = re_clean_text_bag(text_bag)
            status = trie_word_save(clean_text_bag)
            return render_template('success.html', message=status)
        else:
            clean_text_bag = re_clean_text_bag(texts)
            status = trie_word_save(clean_text_bag)
            return render_template('success.html', message=status)
       

@main.route('/submit-url', methods=['POST'])
def url_to_text_bag():
    url = request.form['url']
    if len(url) and url_reachable(url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, "lxml")
        texts = soup.findAll(text=True)
        visible_texts = filter(lxml_tag_visible, texts)
        text_bag = u" ".join(t.strip() for t in visible_texts)
        clean_text_bag = re_clean_text_bag(text_bag)
        status = trie_word_save(clean_text_bag)
        return render_template('success.html', message=status)
    else:
        return render_template('index.html', message="please enter valid url")


@main.route('/submit-file', methods=['POST'])
def file_to_text_bag():
    if request.method == "POST":
        if request.files:
            file = request.files["doc_file"]
            doc = docx.Document(file)
            text_bag = u" ".join(p.text for p in doc.paragraphs if p.text)
            clean_text_bag = re_clean_text_bag(text_bag)
            status = trie_word_save(clean_text_bag)
            return render_template('success.html', message=status)
    else:
        return render_template('index.html', message="please enter valid file format doc,docx")


# @main.errorhandler(TemplateNotFound)
# def handle_error(error):
#     message = [str(x) for x in error.args]
#     status_code = 500
#     success = False
#     response = {
#         'success': success,
#         'error': {
#             'type': error.__class__.__name__,
#             'message': message
#         }
#     }
#     return jsonify(response), status_code
#
# # For any other exception, it will send the reponse with a custom message
# @main.errorhandler(Exception)
# def handle_unexpected_error(error):
#     status_code = 500
#     success = False
#     response = {
#         'success': success,
#         'error': {
#             'type': 'UnexpectedException',
#             'message': 'An unexpected error has occurred.'
#         }
#     }
#
#     return jsonify(response), status_code
#
#
#
#
#
