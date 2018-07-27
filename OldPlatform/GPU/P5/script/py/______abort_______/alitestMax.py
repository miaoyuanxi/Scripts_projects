#!/usr/bin/env python
import httplib
import simplejson
import base64
import re
import sys
import os
from config import *

def generate_render_argument_and_instance_count():
    input_path = ACCESS_ID + '@' + ACCESS_KEY + ':' + BUCKET + '$' + INPUT_PATH 
    output_path = ACCESS_ID + '@' + ACCESS_KEY + ':' + BUCKET + '$' + OUTPUT_PATH 

    scene_desc_json = open('3dmax_description.json')
    scene_desc = simplejson.load(scene_desc_json)
    scene_desc_json.close()

    render_job_desc = scene_desc
    render_job_desc['DivideMode'] = 0 #if split the render job by layer
    render_job_desc['JobType'] = 0 #if it is a estimate job
    render_job_desc['NumThread'] = 10
    render_job_desc['FrameStep'] = 1
    render_job_desc['InputFilePath'] = input_path
    render_job_desc['OutputFilePath'] = output_path

    render_job_desc_str = simplejson.dumps(render_job_desc)
    render_job_desc_base64_str = re.sub('\n', '', base64.encodestring(render_job_desc_str))

    instance_cout = render_job_desc['EndFrame'] - render_job_desc['StartFrame'] + 1

    return render_job_desc_base64_str, instance_cout

def generate_diku_request_body():
    
    resource_desc = {}
    resource_desc['Cpu'] = CPU
    resource_desc['Memory'] = MEMORY

    program_arguments, instance_cout = generate_render_argument_and_instance_count()

    device_mapping = {}
    device_mapping = {
        '/dev/vda': { 'SnapshotId': SNAPSHOT_C},
        '/dev/vdb': { 'SnapshotId': SNAPSHOT_D}
        }

    task_desc = {} 
    task_desc['ResourceDescription'] = resource_desc
    task_desc['ProgramArguments'] = program_arguments
    task_desc['InstanceCount'] = instance_cout 
    task_desc['BlockDeviceMapping'] = device_mapping
    task_desc['ProgramName'] = PROGRAM
    task_desc['ProgramType'] = 'python'
    task_desc['Timeout'] = TASK_TIMEOUT
    task_desc['PackageUri'] = 'oss://' + BUCKET + '/' + PROGRAM_PACKAGE_PATH 
    task_desc['StderrRedirectPath'] = 'oss://' + BUCKET + '/' + LOG_PATH #assign a path in your oss space
    task_desc['StdoutRedirectPath'] = 'oss://' + BUCKET + '/' + LOG_PATH #assign a path in your oss space
    task_desc['EnvironmentVariables'] = {}


    task_desc_map = {} 
    task_desc_map['MapTask'] = task_desc
    
    dependence_map = {}

    task_dag_desc = {}
    task_dag_desc['Dependences'] = { "": [] }
    task_dag_desc['TaskDescMap'] = task_desc_map

    request_body = {}
    request_body['TaskDag'] = task_dag_desc
    request_body['JobName'] = JOB_NAME
    request_body['JobTag'] = 'JobTag'
    request_body['Priority'] = 0

    return request_body


def submit_diku_job():
    request_body = generate_diku_request_body()
    body = simplejson.dumps(request_body)
    print body
    conn = httplib.HTTPConnection(DIKU_SERVER_ADDRESS, DIKU_SERVER_PORT)
    url = '/' + DIKU_SERVER_VERSION + '/jobs?AccessId=' + ACCESS_ID
    conn.request(method="POST", url=url, body=body)
    response = conn.getresponse().read()
    print 'response:' + response
    conn.close()



def list_diku_job():
    conn = httplib.HTTPConnection(DIKU_SERVER_ADDRESS, DIKU_SERVER_PORT)
    url = '/' + DIKU_SERVER_VERSION + '/jobs?AccessId=' + ACCESS_ID
    conn.request(method="GET", url=url)
    response = conn.getresponse().read()
    print response
    conn.close()

def list_diku_tasks(job_id):
    conn = httplib.HTTPConnection(DIKU_SERVER_ADDRESS, DIKU_SERVER_PORT)
    url = '/' + DIKU_SERVER_VERSION + '/jobs/' + job_id + '/tasks?AccessId=' + ACCESS_ID
    conn.request(method="GET", url=url)
    response = conn.getresponse().read()
    print response
    conn.close()

def stop_diku_job(job_id):
    conn = httplib.HTTPConnection(DIKU_SERVER_ADDRESS, DIKU_SERVER_PORT)
    url = '/' + DIKU_SERVER_VERSION + '/jobs/' + job_id + '?AccessId=' + ACCESS_ID + '&Action=Stop'
    conn.request(method="PUT", url=url)
    response = conn.getresponse().read()
    print response
    conn.close()


def delete_diku_job(job_id):
    conn = httplib.HTTPConnection(DIKU_SERVER_ADDRESS, DIKU_SERVER_PORT)
    url = '/' + DIKU_SERVER_VERSION + '/jobs/' + job_id + '?AccessId=' + ACCESS_ID
    conn.request(method="DELETE", url=url)
    response = conn.getresponse().read()
    print response
    conn.close()


def usage():
    print 'python render_max.py submit'
    print 'python render_max.py start (prepair & submit)'
    print 'python render_max.py list'
    print 'python render_max.py stop jobid'
    print 'python render_max.py delete jobid'
    print 'python render_max.py list_tasks jobid' 

if __name__ == '__main__':
    if not len(sys.argv) >= 2:
        usage()
    else:
        if sys.argv[1] == 'submit':
            submit_diku_job()
        elif sys.argv[1] == 'start':
            os.system("python prepare.py")
            submit_diku_job()
        elif sys.argv[1] == 'list':
            list_diku_job()
        elif sys.argv[1] == 'list_tasks':
            list_diku_tasks(sys.argv[2])
        elif sys.argv[1] == 'delete':
            delete_diku_job(sys.argv[2])
        elif sys.argv[1] == 'stop':
            stop_diku_job(sys.argv[2])
        else:
            usage()


