import os
import subprocess
import sys
import json
import xml.etree.ElementTree as ET
import paralleldots
import csv

paralleldots.set_api_key("E3snzMWImpvhhzGzRuQVJhn4brukZx9la19IctCRqB8")


def segment_text(file, transcript_id):
    if not os.path.exists('output'):
        os.mkdir('output')

    print(subprocess.call(['sh','topictiling.sh','-ri','5','-tmd','topic-model','-tmn','model-final','-fp',file,
                           '-fd','/opt/transcripts/','-out','output/{}.xml'.format(transcript_id), '-dn']))


def convert_milli_secs_to_hms(millis):
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    hours=(millis/(1000*60*60))%24
    return "%d:%d:%d" % (hours, minutes, seconds)


def get_keywords(text):
    response = paralleldots.keywords(text)
    print('request sent')
    keywords = []
    for item in response['keywords']:
        with open('words.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                word = ''.join(row)
                if word.lower() == item['keyword'].lower() and item['keyword'] not in keywords:
                    keywords.append(item['keyword'])
    return keywords


def read_xml(transcript_id):
    tree = ET.parse('output/'+transcript_id+'.xml')
    root = tree.getroot()
    doc = root.find('document')
    segments = doc.find('segments')

    timestamps = []
    text_segments = []
    for segment in segments.findall('segment'):
        text = segment.find('text').text
        text = text.replace("\n", " ")
        text_segments.append(text)
        words = text.split(" ")
        words = list(filter(lambda a: a != '', words))
        words = words[-5:]
        # print(words)
        with open('{}-timestamps.txt'.format(transcript_id)) as json_file:
            data = json.load(json_file)
            count = 0
            for word in data['words']:
                if word['text'] == words[count]:
                    count = count +1
                    if count == 5:
                        timestamps.append(word['end'])
                        break
                else:
                    count = 0
    filtered_timestamps = [timestamps[0]]
    paragraph = str(text_segments[0])
    result = []
    for i in range(1, len(timestamps)):
        paragraph = "%s %s" % (paragraph, text_segments[i])
        if timestamps[i]-filtered_timestamps[len(filtered_timestamps)-1] >= 900000:
            filtered_timestamps.append(timestamps[i])
            # response = paralleldots.keywords(paragraph)
            keywords = get_keywords(paragraph)
            # for item in response['keywords']:
            #     keywords.append(item['keyword'])
            result.append({"keywords": keywords, "time": convert_milli_secs_to_hms(filtered_timestamps[len(filtered_timestamps)-2]),
                           "topic": "Topic %d" % (len(filtered_timestamps)-1)})
    return result

