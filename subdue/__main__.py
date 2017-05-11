import sys
import logging

import flask
import markdown

import subdue.daqmx as daqmx
import subdue.visa as visa
import subdue.tc08 as tc08
import subdue.utilities as utilities
import subdue.cmd as cmd

from waitress import serve


logger = logging.getLogger(__name__)
app = flask.Flask(__name__)


@app.route("/")
def index():
    with open('./static/index.md', 'r') as f:
        raw_text = f.read()
        text = raw_text.replace('__version__', utilities.get_package_version())

        html = markdown.markdown(text)

    return html, 200


@app.route('/attached', methods=['GET', 'POST'])
def attached():
    attached_devices = {}

    # find daq devices:
    s = daqmx.NIDAQmxSearch()
    devices = s.list_references()
    if devices:
        attached_devices['daq'] = list(devices)

    # find visa devices
    s = visa.VisaInstrumentSearch()
    devices = s.list_references()
    if devices:
        attached_devices['visa'] = devices

    # find attached tc08 devices
    s = tc08.ThermocoupleSearch()
    devices = s.list_references()
    if devices:
        attached_devices['thermocouple'] = devices

    return flask.jsonify(attached_devices), 200


@app.route('/daq/<device_name>', methods=['POST'])
def daq(device_name):
    commands = flask.request.get_json()

    if isinstance(commands, list):
        results = []
        for command in commands:
            results.append(utilities.parse_daq_command(device_name, command))
        results = [x for x in results if x != {}]
        return flask.jsonify(results), 200
    else:
        command = commands
        return flask.jsonify(utilities.parse_daq_command(device_name, command)), 200


@app.route('/thermocouple/<device_name>', methods=['POST'])
def thermocouple(device_name):
    commands = flask.request.get_json()

    try:
        return flask.jsonify(utilities.parse_thermocouple_command(device_name, commands)), 200
    except AttributeError:
        return 'Device Not Found', 404


@app.route('/visa/<serial_number>', methods=['POST'])
def visa_by_model_number(serial_number=None):
    command = flask.request.get_json()

    result = utilities.parse_visa_command(command, serial_number=serial_number)

    return flask.jsonify(result), 200


def main():
    logging.basicConfig(level=logging.INFO)

    host = cmd.get_host(sys.argv)
    port = cmd.get_port(sys.argv)

    #app.run(host=host, port=port, debug=True, threaded=True)
    serve(app, host=host, port=port)

if __name__ == '__main__':
    main()
