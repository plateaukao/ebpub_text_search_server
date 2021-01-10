from flask import Flask, render_template, request
from epubgrep import EpubGrep
import subprocess

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("index.html", results={})   

@app.route('/s', methods=["GET", "POST"])
def search_page():
    tag = request.values['tag']
    tag = tag if len(tag) != 0 else 'favorite'
    context = request.values['context']
    keyword = request.values['keyword']
    search_result = search_by_grep(tag, context, keyword)
    return render_template("index.html", results=search_result, tag = tag, context = context, keyword = keyword)   

def search_by_grep(tag, context, keyword):
    #print('keyword:', keyword)
    books = search_books(tag)

    results = {}
    for book in books:
        grep = EpubGrep(keyword)
        grep.setPreview(True)
        if context != None and context != '':
            grep.setPreviewLead(int(context))
            grep.setPreviewLag(int(context))
        grep_result = grep.searchin(book.path)
        #print('grep_results:', grep_result)
        if grep_result != None and grep_result != '':
            results[book] = grep_result

    return results

def search_books(tag):
    out = subprocess.run(['calibredb', 'list', '-s', 'tag:' + tag, '-f', 'title,formats'], stdout=subprocess.PIPE) 
    result = out.stdout.decode('utf-8')
    lines = result.split('\n')
    if len(lines) <= 2:
        return []

    return convert_lines_to_books(lines)

def convert_lines_to_books(lines):
    books = []
    for line in lines:
        if line.startswith('Failed') or line.startswith('id '):
            continue
        # format: 145 マルセイユ      [...]
        #print(line)
        segments = line.split('[')
        if len(segments) < 2:
            continue

        book_id, book_title = segments[0].strip().split(' ', 1)
        formats = segments[1][:-1].split(', ')
        book_filepath = ''
        for format in formats:
            if format.endswith('epub'):
                book_filepath = format
                break

        books.append(Book(book_id, book_title, book_filepath))
    return books

class Book:
    def __init__(self, id, title, path):
        self.id = id
        self.title = title
        self.path = path

    def __repr__(self):
        return '\nid:' + self.id + '\ntitle:' + self.title + '\npath:' + self.path

if __name__ == '__main__':
    app.run(host='0.0.0.0')

