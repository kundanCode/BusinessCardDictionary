from waitress import serve

from ocr_app.wsgi import application
# from ocr_app  import wsgi
# documentation: https://docs.pylonsproject.org/projects/waitress/en/stable/api.html

if __name__ == '__main__':
    serve(application, host = 'localhost', port='8080')