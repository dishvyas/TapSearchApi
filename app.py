import sys
import os
import json
import re
from flask import Flask, render_template, request, Response, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['pdf', 'txt'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('index.html', msg='No file selected')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return render_template('index.html', msg='No file selected')

        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))    

        # createDictionary(file)
        return render_template('index.html', msg='Uploaded Successfully')


    


@app.route('/index')
def index():
    wordsAdded = {}
    cwd = os.getcwd()
    os.chdir(cwd)
    fileList = os.listdir(os.getcwd() + UPLOAD_FOLDER)
    os.chdir(os.getcwd() + UPLOAD_FOLDER)
    # print(fileList)
    for file in fileList:

        with open(file, 'r') as f:

            words = f.read().lower().split()

            for word in words:

                if word[-1] in [',', '!', '?', '.']:
                    word = word[:-1]
                if word not in wordsAdded.keys():
                    wordsAdded[word] = [f.name]

                else:
                    if file not in wordsAdded[word]:
                        wordsAdded[word] += [f.name]
    resp=jsonify(wordsAdded)

    with open('result.json', 'w') as fp:
        json.dump(wordsAdded, fp)
    resp.status_code = 200
    # print(resp)
    return resp

@app.route('/search')
def searchword():
    return render_template('search.html')

@app.route('/search', methods= ['POST'])
def search():
    x={}
    # print(type(x))
    results = request.form['text']
    # print(results)
    # print(os.getcwd())
    filepath=os.getcwd() + UPLOAD_FOLDER + 'result.json'
    with open(filepath,'r') as f:
        data = json.load(f)
        for word, file in data.items():   
            if word == results:
                x=jsonify(file)
    x.status_code = 200
    return x

def record_word_cnt(words, bag_of_words):
   for word in words:
       if word != '':
           if word.lower() in bag_of_words:
               bag_of_words[word.lower()] += 1
           else:
               bag_of_words[word.lower()] = 1

@app.route('/indexpara',  methods=['GET', 'POST'])
def para():
    if request.method == 'GET':
        return render_template('indexpara.html')
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('indexpara.html', msg='No file selected')
        file = request.files['file']
        if file.filename == '':
            return render_template('indexpara.html', msg='No file selected')

        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))  
        # print(os.getcwd())  
        filepath = os.getcwd() + UPLOAD_FOLDER + file.filename
        print(filepath)
        bag_of_words = {}
        data={}
        with open(filepath, 'r') as fp:
            cnt = 1
            for line in fp:
                # with open('para.json', 'w') as JS:
                # print("doc {}  {}".format(cnt, line))
                data[cnt]=line
                        # json.dump(data,JS)
                record_word_cnt(line.strip().split(' '), bag_of_words)
                cnt += 1
        response=jsonify(data)
        with open('para.json', 'w') as JS:
            json.dump(data,JS)
        return response
#       sorted_words = order_bag_of_words(bag_of_words, desc=True)
#       print("Most frequent 10 words {}".format(sorted_words[:10]))
  
#       def order_bag_of_words(bag_of_words, desc=False):
#           words = [(word, cnt) for word, cnt in bag_of_words.items()]
#           return sorted(words, key=lambda x: x[1], reverse=desc)

@app.route('/searchpara')
def searchpar():
    return render_template('search.html')

@app.route('/searchpara', methods=['POST'])
def searchpara():
    x={}

    results = request.form['text']
    # print(type(results))
    # print(results)
    filepath=os.getcwd() + '/para.json'
    with open(filepath,'r') as f:
        data = json.load(f)
        # print(data)
        x=""
        y=""
        for word,file in data.items():
            # print(word)
            # print(file) 
            regex=re.findall(results,file)
            print(regex)
            if regex:
                x=word
                y=y+ ' ' +x
                # reg=jsonify(word)
                # print(regex)
                # print(word)
                # print(reg)  
    reg=jsonify(y)   
    reg.status_code = 200
    return reg

@app.route('/clear')
def create():
    filepath= os.getcwd() + UPLOAD_FOLDER + 'result.json'
    print(filepath)
    os.remove(filepath)
    files= os.getcwd() + '/para.json'
    os.remove(files)
    return Response("Successfully Cleared!")

if __name__ == '__main__':
  app.run(debug=True)
