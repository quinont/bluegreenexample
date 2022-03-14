from bottle import route, post, get, put, delete, run, template, request, HTTPResponse, response
import json

# Status => TODO, WORKING, DONE
class Issue:
  def __init__(self, id, status):
    self.id = id
    if status:
      self.status = status
    else:
      self.status = "TODO"
  def nextStep(self):
    if self.status == "TODO":
      self.status = "WORKING"
    elif self.status == "WORKING":
      self.status = "DONE"

issues=[]


@route('/hc')
def hc():
    return HTTPResponse(status=200, body="OK")

@post('/api/issue')
def new_issue():
    new_body = request.json
    new_id = new_body.get('id')
    issue = next((issue for issue in issues if issue.id == new_id), None)
    if issue != None:
        return HTTPResponse(status=409, body="Issue id exists!")
    new_status = new_body.get('status')
    if new_status == None:
        new_status = "TODO"
    if new_status.upper() not in ["TODO", "WORKING", "DONE"]:
        return HTTPResponse(status=400, body="Status must be TODO WORKING or DONE")
    new_issue = Issue(new_id, new_status.upper())
    issues.append(new_issue)
    return HTTPResponse(status=201, body="OK")


@get('/api/issue')
@get('/api/issue/<id>')
def get_issue(id = None):
    issues_list = [ob.__dict__ for ob in issues]
    response.content_type = 'application/json'
    if id == None:
        if issues_list == None:
            issues_list = {}
        return json.dumps(issues_list)
    issue = next((issue for issue in issues_list if issue["id"] == id), None)
    if issue:
        return json.dumps(issue)
    return HTTPResponse(status=410, body="[{\"id\": \"-1\", \"status\": \"Issue is missing\"}]")

@put('/api/issue/<id>')
def next_step_issue(id):
    issue = next((issue for issue in issues if issue.id == id), None)
    response.content_type = 'application/json'
    if issue:
        index = issues.index(issue)
        issues[index].nextStep()
        return HTTPResponse(status=204)
    return HTTPResponse(status=410, body="[{\"id\": \"-1\", \"status\": \"Issue is missing\"}]")

@delete('/api/issue/<id>')
def delete_issue(id):
    issue = next((issue for issue in issues if issue.id == id), None)
    response.content_type = 'application/json'
    if issue:
        issues.remove(issue)
        return HTTPResponse(status=204)
    return HTTPResponse(status=410, body="[{\"id\": \"-1\", \"status\": \"Issue is missing\"}]")

run(host='0.0.0.0', port=8080)
