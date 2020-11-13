#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from flask import Flask, jsonify, request, make_response, render_template, abort, url_for
import os
from werkzeug.exceptions import HTTPException
from tz_filter import getuserinfo, opportunitys

# Global Flask Application Variable: app
app = Flask(__name__)

# global strict slashes
#app.url_map.strict_slashes = False

# flask server environmental setup
host =  '0.0.0.0'
port =   5000



@app.errorhandler(404)
def handle_404(exception):
    """
    handles 404 errors, in the event that global error handler fails
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


@app.errorhandler(400)
def handle_400(exception):
    """
    handles 400 errros, in the event that global error handler fails
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)

@app.route('/')
def index():
    "Main page for utc filter"
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def status():
    """
    function for status route that returns the status
    """
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)

@app.route('/main_user/<userpbid>', methods=['GET'])
def main_user(userpbid):
    """
    function to return main user info
    """
    return jsonify(getuserinfo(userpbid))


@app.route('/same_utc/', methods=('GET', 'POST'))
def same_utc():
    """
    function to request opportunities and filter by utc
    """
    user_timezone = request.args.get('timezone')
    opportunitys_user = opportunitys(user_timezone)
    return opportunitys_user.to_html(classes='data', header="true")

if __name__ == "__main__":
    """
    MAIN Flask App
    """
    # start Flask app
    app.run(host=host, port=port,debug=True)
