from bottle import route, run, template, request, HTTPResponse
import requests
import os

DOMINIO_APP1 = os.environ.get("DOMINIO_APP1", None)
PATH_APP1 = os.environ.get("PATH_APP1", None)


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/app1')
def app1():
    previewVersion = request.headers.get('PreviewVersion', None)
    headers_dict=None
    if previewVersion and previewVersion == "yes":
        headers_dict = {"PreviewVersion": "yes"}

    r = requests.get("http://" + DOMINIO_APP1 + PATH_APP1, headers=headers_dict)
    if r.status_code != 200:
        return HTTPResponse(status=503, body="Error with connection to app1")

    return template('<b>Server name: {{server}}</b></br>With the messaje: {{message}}', server=r.json()["Server"], message = r.json()["message"])

run(host='0.0.0.0', port=8080)
