import argparse
import os
import json
import requests
import time

# Please replace _apiServerUrl, _clientId and _clientSecret with credentials from your Animate 3D Rest API Portal

_apiServerUrl = 'copy_your_Production URL_here_from_API_portal'
_clientId = 'copy_your_clientId_here_from_API_portal'
_clientSecret = 'copy_your_clientSecret_here_from_API_portal'

def check_json(fpath):
    if not os.path.exists(fpath):
        raise argparse.ArgumentTypeError('Filename %r doesn\'t exist.' % fpath)
    
    if fpath[-5:] != '.json':
        raise argparse.ArgumentTypeError('%r is not a JSON file.' % fpath)

    return fpath

def parse_user_credentials():
    parser = argparse.ArgumentParser(prog='DMBT API CLI Demo', 
            description='Specify JSON file with user credentials')
    parser.add_argument('credentials', 
        nargs='?', type=check_json, 
        help='A JSON file must be specified')
    args = parser.parse_args()
    return args.credentials

def set_user_credentials():
    global _sessionCredentials
    _sessionCredentials = _clientId, _clientSecret
    global session
    session = get_session()
    print('Credentials successfully set. \n')

def get_session():
    authUrl = _apiServerUrl + '/session/auth'
    session = requests.Session()
    session.auth = _sessionCredentials
    request = session.get(authUrl)
    if request.status_code == 200:
        return session
    else:
        print('Failed to authenticate ' + str(request.status_code) + '\n')
        main_options()

def get_response(urlPath):
    respUrl = _apiServerUrl + urlPath
    resp = session.get(respUrl)
    if resp.status_code == 200:
        return resp
    else:
        print('Failed to contact server ' + resp.status_code + '\n')
        main_options()

def print_list_portion(inputList, nameDelim, idDelim, timeDelim, currPos):
    endOfPortion = currPos + 25
    if endOfPortion > len(inputList):
        endOfPortion = len(inputList)
    while currPos < endOfPortion:
        cPosStr = str(currPos + 1) + ')'
        while len(cPosStr) < 6:
            cPosStr += ' '
        print(cPosStr + inputList[currPos][nameDelim], end='')
        if idDelim != '':
            print('\t\t' + inputList[currPos][idDelim], end='')
        if timeDelim != '':
            print('\t\t' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(inputList[currPos][timeDelim]/1000.0)), end='')
        currPos += 1
        print('')

    listFinished = False
    if endOfPortion >= len(inputList):
        listFinished = True
    listStatus = (currPos, listFinished)
    return listStatus

def call_print_list_portion(inputList, nameDelim, idDelim = '', timeDelim = ''):
    currPos = 0
    listComplete = False
    selection = 'Y'
    while not listComplete:
        print('')
        if currPos != 0:
            selection = input('Press Y to show more inputs, N to exit: ')

        selection = selection.lower()
        if selection == 'n':
            break
        if selection != 'y':
            print('Please use "y", "Y", "n", or "N"')
            continue
        print('')
        listStatus = print_list_portion(inputList, nameDelim, idDelim, timeDelim, currPos)
        listComplete = listStatus[1]
        currPos = listStatus[0]

def display_models():
    respText = get_response('/character/listModels?stockModel=all').text
    jsonResp = json.loads(respText)
    charList = jsonResp['list']
    call_print_list_portion(charList, 'name', 'id')
    return charList
    
def list_models():
    print('')
    display_models()
    print('')
    main_options()
    
def get_job_list(listPath):
    respText = get_response(listPath).text
    jsonResp = json.loads(respText)
    return jsonResp

def get_job_status(listPath):
    respText = get_response(listPath).text
    jsonResp = json.loads(respText)
    return jsonResp

def list_jobs():
    print("""\n=== Job Status List Filter ===
    1) IN PROGRESS
    2) SUCCEEDED
    3) FAILED
    4) ALL\n""")
    selection = int(input('Select option number from the list: '))
    print('')
    jobList = []

    if selection == 1 or selection == 4:
        jsonResp = get_job_list('/list/PROGRESS')
        print('Jobs in progress: ' + str(jsonResp['count']))
        jobList += jsonResp['list']

    if selection == 2 or selection == 4:
        jsonResp = get_job_list('/list/SUCCESS')
        print('Jobs succeeded: ' + str(jsonResp['count']))
        jobList += jsonResp['list']

    if selection == 3 or selection == 4:
        jsonResp = get_job_list('/list/FAILURE')
        print('Jobs failed: ' + str(jsonResp['count']))
        jobList += jsonResp['list']

    call_print_list_portion(sorted(jobList, key=lambda x : x['ctime'], reverse=True), 'fileName', 'rid', 'ctime')
    
    print('')
    main_options()

download_format = {
    1: 'bvh',
    2: 'fbx',
    3: 'mp4'
}
character_select = {
    1: 'male-young',
    2: 'male-normal',
    3: 'male-fat',
    4: 'female-normal',
    5: 'female-thin',
    6: 'child'
}

def ends_with_MP_trackedID(s):
    return s[-4] == '_' and s[-3:].isdigit() and len(s[-3:]) == 3

def download_job():
    print('download job started\n')
    print("""A list of jobs will appear. Once you find the job you
want to download, exit the listing and input the number of the
job you want to download.\n""")
    input('Press Enter to continue...\n')
    jobListJson = get_job_list('/list/SUCCESS')
    numJobs = jobListJson['count']
    jobListJson['list'] = sorted(jobListJson['list'], key=lambda x : x['ctime'], reverse=True)
    print('Jobs available for download: ' + str(numJobs))
    call_print_list_portion(jobListJson['list'], 'fileName', 'rid', 'ctime', )
    jobSelection = int(input('Input job number to download: '))
    if jobSelection > numJobs:
        print('Selection is out of range.\n')
        main_options()
    rid = jobListJson['list'][jobSelection - 1]['rid']

    dPath = os.getcwd() + os.path.sep + rid + '-'
    downloadResp = get_response('/download/' + rid)
    downloadRespTxt = downloadResp.text
    downloadRespJson = json.loads(downloadRespTxt)
    print(downloadRespJson)
    if downloadRespJson['count'] > 0:
        urls = downloadRespJson['links'][0]['urls']
        for fileUrl in urls:
            name = fileUrl['name'] 
            if ends_with_MP_trackedID(name) or name.startswith('inter'):
                continue
            files = fileUrl['files']
            for file in files:
                if 'bvh' in file:
                    uri = file['bvh']
                    dowloadResp = session.get(uri)
                    outputFile = dPath + fileUrl['name'] + '.bvh' + ('.zip' if name == 'all_characters' else '')
                    with open(outputFile, 'wb') as f:
                        f.write(dowloadResp.content)
                        print('\nFile saved to ' + outputFile)
                if 'fbx' in file:
                    uri = file['fbx']
                    dowloadResp = session.get(uri)
                    outputFile = dPath + fileUrl['name'] + '.fbx' + '.zip'
                    with open(outputFile, 'wb') as f:
                        f.write(dowloadResp.content)
                        print('\nFile saved to ' + outputFile)
                if 'mp4' in file:
                    uri = file['mp4']
                    dowloadResp = session.get(uri)
                    outputFile = dPath + fileUrl['name'] + '.mp4'
                    with open(outputFile, 'wb') as f:
                        f.write(dowloadResp.content)
                        print('\nFile saved to ' + outputFile)
                if 'glb' in file:
                    uri = file['glb']
                    dowloadResp = session.get(uri)
                    outputFile = dPath + fileUrl['name'] + '.glb' + ('.zip' if name == 'all_characters' else '')
                    with open(outputFile, 'wb') as f:
                        f.write(dowloadResp.content)
                        print('\nFile saved to ' + outputFile)

    print('')
    main_options()

def printProgress(percent):
    prefix = 'Progress:'
    suffix = 'Complete'
    printEnd = "\r"
    print(f'{prefix} {percent}% {suffix}', end = printEnd)


def showProgress(rid, prefix):
    jobDone = False
    while jobDone == False:
        pStatusRespJson = get_job_status ('/status/' + rid)
        if int(pStatusRespJson["count"]) > 0:
            statusData = pStatusRespJson["status"][0]; #We have one status for a single rid
            if statusData["status"] == "PROGRESS":
                total = float(statusData["details"]["total"])
                current = float(statusData["details"]["step"])
                if current > total:
                    current = total
                percentage = round((current * 100.0) / total, 2)
                printProgress(str(percentage))
                
            elif statusData["status"] == "FAILURE":
                print(prefix + ' is completed with Failure.')
                jobDone = True

            elif statusData["status"] == "SUCCESS":
                print(prefix + ' is completed successfully.')
                jobDone = True
            else:
                print(prefix + ' is in unknown status.')
                jobDone = True

        else:
            jobDone = True
    
        time.sleep(10)

        
def new_job():
    currPath = os.path.abspath(os.path.dirname(__file__))
    inputPath = input('Input relative path to video to upload: ')
    fullPath = os.path.normpath(os.path.join(currPath, inputPath))
    vFile = None
    if not os.path.exists(fullPath):
        raise argparse.ArgumentTypeError('Filename %r doesn\'t exist.' % fullPath)
    with open(fullPath, 'rb') as f:
        vFile = f.read()
    if vFile == None:
        raise argparse.ArgumentTypeError('Could not read %r.' % fullPath)

    charList = display_models()
    charSel = int(input("""\nInput the index of the character you want to use : """))
    modelStr = 'model=' + charList[charSel - 1]['id']
    print(modelStr)

    print("""\nSelect formats to process:
    1) BVH
    2) FBX
    3) MP4
    4) All\n""")
    formatSelection = int(input('Input format number: '))
    formatProcess = ''
    if formatSelection != 4:
        formatSel = download_format[formatSelection]
        formatProcess = "formats=" + formatSel
    else:
        formatProcess = "formats=bvh,fbx,mp4"

    headerContent = {'Content-length': str(len(vFile)), 'Content-type': 'application/octet-stream'}
    vPath = os.path.basename(fullPath)
    vName, vExt = os.path.splitext(vPath)

    uploadUrl = _apiServerUrl + '/upload?name=' + vName + '&resumable=0'
    resp = session.get(uploadUrl)
    if resp.status_code == 200:
        jsonResp = json.loads(resp.text)
        gcsUrl = jsonResp['url']
        uploadResp = session.put(gcsUrl, headers=headerContent, data=vFile)
        if uploadResp.status_code == 200:
            processUrl = _apiServerUrl + '/process'
            processCfgJson = None
            if modelStr == '':
                processCfgJson = {
                    "url": gcsUrl,
                    "processor": "video2anim",
                    "params": [
                        "config=configDefault",
                        formatProcess
                    ]
                }
            else:
                processCfgJson = {
                    "url": gcsUrl,
                    "processor": "video2anim",
                    "params": [
                        "config=configDefault",
                        formatProcess,
                        modelStr
                    ]
                }
            processResp = session.post(processUrl, json=processCfgJson)
            if processResp.status_code == 200:
                pRespJson = json.loads(processResp.text)
                print('Job is processing: ' + pRespJson['rid'])
                showProgress(pRespJson['rid'], "Job")
                
            else:
                print(processResp.status_code)
                print('failed to process')
        else:
            print(uploadResp.status_code)
            print('failed to upload')

    print('')
    main_options()


def new_mp_job():
    error = True
    currPath = os.path.abspath(os.path.dirname(__file__))
    inputPath = input('Input relative path to video to upload: ')
    fullPath = os.path.normpath(os.path.join(currPath, inputPath))
    vFile = None
    if not os.path.exists(fullPath):
        raise argparse.ArgumentTypeError('Filename %r doesn\'t exist.' % fullPath)
    with open(fullPath, 'rb') as f:
        vFile = f.read()
    if vFile == None:
        raise argparse.ArgumentTypeError('Could not read %r.' % fullPath)
    
    headerContent = {'Content-length': str(len(vFile)), 'Content-type': 'application/octet-stream'}
    vPath = os.path.basename(fullPath)
    vName, vExt = os.path.splitext(vPath)

    uploadUrl = _apiServerUrl + '/upload?name=' + vName + '&resumable=0'
    resp = session.get(uploadUrl)
    if resp.status_code == 200:
        jsonResp = json.loads(resp.text)
        gcsUrl = jsonResp['url']
        uploadResp = session.put(gcsUrl, headers=headerContent, data=vFile)
        if uploadResp.status_code == 200:
            processUrl = _apiServerUrl + '/process'
            processCfgJson = None

            processCfgJson = {
                "url": gcsUrl,
                "processor": "video2anim",
                "params": [
                    "config=configDefault",
                    "pipeline=mp_detection"
                ]
            }

            processResp = session.post(processUrl, json=processCfgJson)
            if processResp.status_code == 200:
                pRespJson = json.loads(processResp.text)
                print('persons are being detected: ' + pRespJson['rid'])
                showProgress( pRespJson['rid'], "Persons detection")
                print("processing detected persons...")

                personIds = []
                ridMPDetection = pRespJson['rid']

                dPath = os.getcwd() + os.path.sep + pRespJson['rid'] + '.'
                downloadResp = get_response('/download/' + pRespJson['rid'])
                downloadRespTxt = downloadResp.text
                downloadRespJson = json.loads(downloadRespTxt)
                if downloadRespJson['count'] > 0:
                    urls = downloadRespJson['links'][0]['urls']
                    for fileUrl in urls:
                        files = fileUrl['files']
                        for file in files:
                            if 'cdsave' in file:
                                uri = file['cdsave']
                                cdsaveDowloadResp = session.get(uri)
                                ids = set()
                                cdsaveDowloadRespJson = json.loads(cdsaveDowloadResp.text)
                                for frame in cdsaveDowloadRespJson['detectionResults']:
                                    for person in frame:
                                        ids.add(person['id'])                               
                                personIds = list(ids)
                                break
                        
                    for pid in personIds:
                        for fileUrl in urls:
                            if fileUrl['name'] == "thumbnail_character_" + str(pid).zfill(3):
                                files = fileUrl['files']
                                for file in files:
                                    if 'png' in file:
                                        uri = file['png']
                                        escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'
                                        print(str(pid) + " : " + escape_mask.format('', uri, "(person's image link)"))
                    

                    if len(personIds)>0:
                        trackedIds = input('Input person ids (separated by comma) for whom you would like to run animation tracking process: ')
                        trackedIds = trackedIds.split(",")
                        trackedIds= [x.strip() for x in trackedIds if x.strip()!= ""]
                        print(trackedIds)
                        
                        charList = display_models()
                        charSel = int(input("""\nInput the index of the character you want to use (for representing all tracked persons as an example) : """))

                        if charSel != len(charList) + 1:
                            charSel = charList[charSel - 1]['id']
                        models = []
                        for pid in trackedIds:
                            model = {}
                            model["trackingId"] = str(pid).zfill(3)
                            model["modelId"] = charSel
                            models.append(model) 
                        
                        modelStr = 'models=' + json.dumps(models)
                        print(modelStr)

                        print("""\nSelect formats to process:
                        1) BVH
                        2) FBX
                        3) MP4
                        4) All\n""")
                        formatSelection = int(input('Input format number: '))
                        formatProcess = ''
                        if formatSelection != 4:
                            formatSel = download_format[formatSelection]
                            formatProcess = "formats=" + formatSel
                        else:
                            formatProcess = "formats=bvh,fbx,mp4"
                       
                        processUrl = _apiServerUrl + '/process'
                        processCfgJson = {
                            "rid_mp_detection": ridMPDetection,
                            "processor": "video2anim",
                            "params": [
                                "config=configDefault",
                                formatProcess,
                                modelStr
                            ]
                        }
                        processResp = session.post(processUrl, json=processCfgJson)
                        if processResp.status_code == 200:
                            pRespJson = json.loads(processResp.text)
                            print('Job is processing: ' + pRespJson['rid'])
                            time.sleep(10)
                            showProgress(pRespJson['rid'], "Job")
                            error = False


    if error == True:
        print('failed to process')

    print('')
    main_options()



def upload_character():
    currPath = os.path.abspath(os.path.dirname(__file__))
    cInputPath = input('Input relative path of character model to upload: ')
    cFullPath = os.path.normpath(os.path.join(currPath, cInputPath))
    cFile = None
    if not os.path.exists(cFullPath):
        raise argparse.ArgumentTypeError('Filename %r doesn\'t exist.' % cFullPath)
    with open(cFullPath, 'rb') as f:
        cFile = f.read()
        f.close()
    if cFile == None:
        raise argparse.ArgumentTypeError('Could not read %r.' % cFullPath)
    cHeader = {'Content-Length': str(len(cFile)), 'Content-Type': 'application/octet-stream'}

    cFName, cExt = os.path.splitext(os.path.basename(cFullPath))
    uploadingUrl = _apiServerUrl + '/character/getModelUploadUrl?name=' + cFName + '&modelExt=' + cExt[1:] + '&resumable=0'
    resp = session.get(uploadingUrl)
    if resp.status_code == 200:
        jsonResp = json.loads(resp.text)
        gcsModelUrl = jsonResp['modelUrl']
        cUploadResp = session.put(gcsModelUrl, headers=cHeader, data=cFile)
        if cUploadResp.status_code == 200:
            print('Uploaded model ' + cFName)
        else:
            print('Failed to upload model')
            main_options()
        storeUrl = _apiServerUrl + '/character/storeModel'
        storeCfg = {
            "modelId": None,
            "modelUrl": gcsModelUrl,
            "thumbUrl": None,
            "modelName": cFName
        }
        storeResp = session.post(storeUrl, json=storeCfg)
        if storeResp.status_code == 200:
            print('Successfully stored model ' + json.loads(storeResp.text)['modelId'])
        else:
            print('Failed to store model')
    else:
        print('Failed to contact API server for upload.')

    print('')
    main_options()

def check_credits_balance():
    respText = get_response('/account/creditBalance').text
    jsonResp = json.loads(respText)
    print(jsonResp['credits'])
    
    print('')
    main_options()

mainOptions = {
    1: list_models,
    2: list_jobs,
    3: download_job,
    4: new_job,
    5: new_mp_job,
    6: upload_character,
    7: check_credits_balance,
    8: exit
}

def main_options():
    print("""=== OPTIONS ===
    1) List Models
    2) List Jobs
    3) Download Completed Job
    4) Start New Job
    5) Start New MP Job
    6) Upload Custom Character
    7) Check Credits Balance
    8) Exit\n""")
    selection = int(input('Select option number from the list: '))
    mainOptions[selection]()

def main():
    set_user_credentials()
    main_options()

if __name__ == '__main__':
    args = parse_user_credentials()
    main()