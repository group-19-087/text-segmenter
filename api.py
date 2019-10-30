# import ConfigParser
# import cPickle
import json
import os
import time

# import jsonschema
import requests
import requests.auth
from flask import Flask, render_template, request

# import jschema
from decorators import *
from log import logger
import topictiling

app = Flask(__name__)
api_prefix = '/vtutor-transcriptions-api/v1'
API_TOKEN = "c91036f1ae3547759bb56297e28d9730"

headers = {'Authorization': API_TOKEN, 'Content-Type': 'application/json'}


@app.route('{}/get-transcript'.format(api_prefix), methods=['POST'])
def get_transcript():
    print("Hello")
    data = None
    if request.is_json:
        try:
            data = request.get_json()
        except Exception as e:
            logger.error('get_json error - {}'.format(e))
        if data['status'] == 'completed':
            transcript_id = data['transcript_id']
            get_trasncription_endpoint = "https://api.assemblyai.com/v2/transcript/{}".format(transcript_id)
            try:
                transcript = requests.get(get_trasncription_endpoint, headers=headers)
                if transcript.status_code == 200:
                    # print(transcript)
                    transcript_json = transcript.json()

                    transcript_text = transcript_json['text']
                    words = transcript_json['words']
                    timestamps = {"words" : words}
                    file_name = "{}.txt".format(transcript_id)
                    file_path = "/opt/transcripts/%s" % file_name
                    f = open(file_path, "w+")
                    f.write(transcript_text)
                    f.close()
                    with open('{}-timestamps.txt'.format(transcript_id), 'w') as outfile:
                        json.dump(timestamps, outfile)

                    if transcript_json['audio_duration'] > 1200:
                        topictiling.segment_text(file_name,transcript_id)
                        segmentation_points = topictiling.read_xml(transcript_id)
                    else:
                        segmentation_points = []
                    result = {"times": segmentation_points}
                    return json.dumps({"status": 200, "result": {"timestamps": segmentation_points, "transcript": transcript_text, "words": words}})
                else:
                    logger.error("Request failed with status code : %s" % str(transcript.status_code))
                    return json.dumps({"status": transcript.status_code, "result": {"error": "Transcription endpoint error"}})
            except requests.exceptions.HTTPError as err:
                logger.error("HTTP error : %s" % str(err))
                return json.dumps({"status": 500, "result": {"error": str(err)}})
            except requests.exceptions.ConnectionError as err:
                logger.error("Connection error : %s" % str(err))
                return json.dumps({"status": 500, "result": {"error": str(err)}})
            except requests.exceptions.Timeout as err:
                logger.error("Timeout error : %s" % str(err))
                return json.dumps({"status": 500, "result": {"error": str(err)}})
            except requests.exceptions.RequestException as err:
                logger.error("Request exception : %s" % str(err))
                return json.dumps({"status": 500, "result": {"error": str(err)}})

        else:
            logger.debug('Transcription failed - {}'.format(data))


    else:
        logger.error('Request is not json')
        return jsonify(api_message="Request was not JSON", error='true')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
