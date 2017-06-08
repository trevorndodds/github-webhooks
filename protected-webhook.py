#!/usr/bin/env python
import json
import os
import urllib2
from flask import Flask, request

port = 5000
githubserver = ''
api_token = ''

app = Flask(__name__)
app.debug = os.environ.get('DEBUG') == 'true'


@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return "You found me"
    elif request.method == 'POST':
        pass

    event = request.headers.get('X-GitHub-Event')
    if event == 'create':
        print "we have received a %s event from GHE" % event
        payload = json.loads(request.data)
        if payload['ref_type'] == 'branch':
            if 'protected' in payload['ref'].lower():
                print "Protected Branch - %s - %s" % (payload['repository']['full_name'], payload['ref'])
                response = invoke_protected(payload)
                return response
            else:
                return "Not a protected branch"
        else:
            return "Not a branch but a %s" % payload['ref_type']
    elif event == 'ping':
        return "Pong"
    else:
        return "Wrong Event Type"


def invoke_protected(data):
    branch = data['ref']
    repo_full = data['repository']['full_name']
    protected = '{"protection": {"enabled": true}}'
    req_pull_req = '{"include_admins": true}'
    url = githubserver+"/api/v3/repos/"+repo_full+"/branches/"+branch

    try:
        print "Calling GitHub API to set %s to protected" % branch
        req = urllib2.Request(url, data=protected)
        req.add_header('Authorization', 'token %s' % api_token)
        req.add_header('Accept', 'application/vnd.github.loki-preview+json')
        req.get_method = lambda: 'PATCH'
        f = urllib2.urlopen(req)
        if f.info()['status'] == '200 OK':
            try:
                print "Calling GitHub API to set %s to require pull requests" % branch
                url = githubserver + "/api/v3/repos/" + repo_full + "/branches/" + branch \
                    + "/protection/required_pull_request_reviews"
                req_pull = urllib2.Request(url, data=req_pull_req)
                req_pull.add_header('Authorization', 'token %s' % api_token)
                req_pull.add_header('Accept', 'application/vnd.github.loki-preview+json')
                req_pull.get_method = lambda: 'PATCH'
                r = urllib2.urlopen(req_pull)
                return 'Protected: %s - Pull Requests: %s' % (f.info()['status'], r.info()['status'])
            except urllib2.HTTPError, e:
                print 'We failed with error code - %s.' % e.code
                return 'We failed with error code - %s.' % e.code
        else:
            return 'Something went wrong - %s' % f.info()['status']
    except urllib2.HTTPError, e:
        print 'We failed with error code - %s.' % e.code
        return 'We failed with error code - %s.' % e.code

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
