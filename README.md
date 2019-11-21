# TapSearchApi
Inverted index with Python and Flask

This an example to generate Inverted Index for Multiple files as well as Multiple Paragraphs.

To use this flask app you need to clone the repository using :
git clone 
cd "cloned folder"
pip install -r requirements.txt

# To run locally :

flask run 
or 
gunicorn app:app --timeout 10    #for a production server, preferred because Flask doesn't seem to handle alot of requests together very well.

# There are 2 main features i have implemented here which are:

Inverted Index for multiple files  URL : https://tapsearch-pro.herokuapp.com/index     

Inverted Index for multiple paragraphs from a file URL : https://tapsearch-pro.herokuapp.com/indexpara   #POST method

You need to upload the files to create the inverted index which can be done by URL :  https://tapsearch-pro.herokuapp.com/Upload  #POST method

# Additional features include :

Searching a word and returning list of files containing that word in JSON format  url : https://tapsearch-pro.herokuapp.com/search  #POST method

Searching a word and returning list of unique paragraph ids containing that word in JSON format   url : https://tapsearch-pro.herokuapp.com/searchpara  #POST method

Clear both the index files url : https://tapsearch-pro.herokuapp.com/clear  

Refresh the app in case of 500 internal server error both when run locally or on the above mentioned link which is created because os.chdir() might not recognize the stored folder path correctly. Minor Inconvinience faced for not using a Database to store files.


The entrypoint for all of the sources is found in the file ./app.py


# DATA STORAGE :
Data or files are automatically stored to /static/uploads/ folder and can be accessed from there for search and clear queries.

# What did i learn? :
Deploying flask app to heroku without proper configurations will create alot of problems which means unnecessary errors.

It is currently deployed on Heroku. Link : https://tapsearch-pro.herokuapp.com/
