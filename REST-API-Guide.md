# Animate 3D REST API

## Revisions

_Alpha v1.0._

Initial rest APIs

_Alpha v1.0._

Added model parameter to the /process API

_Alpha v1.2._

Added custom character end points /character

_Alpha v1.2._

Added the “sim” parameter to API 3: Start Video Processing

_Alpha v1.2._

Added the “camera” parameter to API 3: Start VideoProcessing

_Alpha v1.3._

Added webhook APIs

_Alpha v1.4._

Added footLockingMode parameter to the /process API
Added new minutesBalance API

_Alpha v1.4._

Added flag “createThumb” to /character/storeModelAPI

The Animate 3D REST API lets you convert videos into3D animations without having to use the
DeepMotionWeb Portal. Instead you can upload, process,and download the resulting FBX/BVH
animations directly from an external application likea web or desktop app.

## Authentication

###### The Animate 3D REST API uses basic HTTP Authentication to keep your requests and data

###### secure. To use theAPIyou will need a Client ID anda Client Secret which are provided by

DeepMotion. If you do not have these please contactDeepMotion Support or your sales representative.

To retrieve your API access token you need to addthe following Authorization header to your token
request:

Authorization: Basic Base64(<clientId>:<clientSecret>)


where the value of<clientId>:<clientSecret>is **base 64** encoded. For Example, if your Client ID
is1a2band your client Secret is3c4dthen your authorizationheader should look like this:

Authorization: Basic MWEyYjozYzRk

###### whereMWEyYjozYzRkis the base64 encoded value of1a2b:3c4d.

**Note** : Optionally it is possible to send a unique useridentifier (via x-useruid HTTP(S) header) along
with the authorization header. See example below:

Curl -v -H “Authorization: Basic MWEyYjozYzRk” -H“x-useruid:me.us@test.com” -X GET “{host}/auth”

## API Endpoints

###### All Animate 3D API requests must be made against thefollowing base URL using the HTTPS

###### protocol and port:

Staging Environment: https://petest.deepmotion.com:
Production Environment: (Contact DeepMotion)

## API Reference

**API 1: Get Access Token**

```
Desc Authenticate client credentials and returns a timelimited session
cookie to be used in the subsequent REST API calls.After the session
expiration, this API needs to be called again to geta new session
cookie
```
```
Method + URI GET {host}/session/auth
```
```
Header(s) Authorization: Basic Base64(<clientId>:<clientSecret>)
```
```
Request
```
```
Response Sample Response Header:
set-cookie:
dmsess=s%3AEsF23MoyDEq7tTWQM8KfA_wjKkSrOFwU.2fjJTfDP%
2FT2BeA5DFenwOH4t8XzqZsbSc6M2mZwS%2BWg;
Domain=.deepmotion.com; Path=/; Expires=Mon, 03 Aug 2020
13:36:26 GMT; HttpOnly
```
```
(Note: dmsess is the session cookie. This cookie needsto be sent in
all subsequent REST API calls.
```

```
Sample Request Header for other API calls:
cookie:dmsess=s%3AEsF23MoyDEq7tTWQM8KfA_wjKkSrOFwU.2fjJ
TfDP%2FT2BeA5DFenwOH4t8XzqZsbSc6M2mZwS%2BWg)
```
**API 2: Upload Video**

```
Desc Retrieves a signed url to upload video
```
```
Method + URI GET {host}/upload
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```
```
Request Query parameters:
<name>: video file name (optional)
<resumable>: 0 or 1(default) returns resumable orregular signed url
(optional)
```
```
Response JSON object:
{
"url": signed url
}
```
```
After retrieving the url, actual video upload is requiredto that storage
url. If ’resumable’ option is set in the request, we need one POST and
one subsequent PUT request, otherwise a single PUTrequest will do
the job.
```
```
POST request to url:
<x-goog-resumable>: start (set in the request header)
<location>: resumable url (set in the response headerby server)
```
```
Put request to resumable url/url:
attach raw bytes of the video file in the requestbody.
```
**API 3: Start Video Processing**

```
Desc Start processing video after file has been uploadedto the designated
URL
```
```
Method + URI POST {host}/process
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```
```
Request POST body should include a JSON object:
```

{
“url”: <upload url>
“processor”: <processor_id>
“params": [<params>, ...]
}

<upload_url> should match url returned from GET /uploadrequest

<processor_id> specifies which processor to use toprocess the video
file, must be one of the following:

```
Processor Id Description
```
```
video2anim Deepmotion video to animation processor
```
<params> specifies additional parameters that willbe passed to the
specified processor, for example:
"params": [
"config=configDefault",formats=bvh,fbx,mp4,model=<modelId>]

Additional important parameter: **sim**

###### This physics simulation parameter needs more clarification.This

###### parameter influences Pose Estimation result to improveit in some

###### cases like body parts inter penetration etc.If wewould like to turn

this ON, add sim=1 OR add sim=0 to turn it OFF. Ifwe don’t add this
parameter, simulation is turned off by default.

For camera behavior in output video generation (mp4for now), the
default value for the **camera** parameter is **render.camera=closeup**
which always keeps the simulated character in thecamera frame with
maximum zoom possible. **render.camera=fixed** is theother value that
keeps the camera stationary.

###### Another new parameter is: poseEstimation.footLockingMode or

###### simply footLockingMode

```
● This parameter value can be one of the below:
○ auto : default mode, automatic switching between
locking and gliding modes of the foot, recommendedfor
general cases
```
###### ○ always : forced foot locking all the time. only used

```
when Auto mode can not remove all the foot gliding
unsired
○ never : forced to disable foot locking and character
grounding. used when the motion is completely in theair
or in the water and therefore neither foot lockingnor
character grounding is needed.
```

###### ○ grounding : forced disabling foot locking, however

```
character is still grounded. Only used when Auto mode
prevents the desired foot gliding (i.e. during shuffling
dances) in the motion or locks the foot for too longon
the ground during fast and short foot/ground contacts
(i.e. during sprints or jumps.)
```
```
Response JSON object:
{
"rid": <request id>
}
```
**API 4: Poll for Job Status**

```
Desc Polls for real-time status of a given processing job
```
```
Method + URI GET {host}/status/rid
GET {host}/status/rid1,rid2,..,rid
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```
```
Request Clients can request current status of previously submittedprocessing
requests (API3).
```
```
Use comma (‘,’) to separate multiple request ids ifretrieving status for
more than 1 request.
```
```
Response JSON object:
{
"count": <number of records in status array>,
"status": [
<status>,
... ...
]
}
```
```
Each element in status array is a JSON object:
{
"rid": <request id>,
"status": <status name>
"details": <status details, see below>
}
```
```
<status name> is one of the following case sensitive values:
```
```
Status Name Description
```

```
PROGRESS Request is still being processed
```
```
SUCCESS Request is processed successfully
```
```
RETRY Request has failed for some reason, but is
being retried
```
```
FAILURE Request has failed
```
```
<status details> for PROGRESS:
{
“step”: <current step>,
“total”: <expected total number of steps>
}
```
```
<status details> for SUCCESS:
{
“In”: <original video file>,
“out”: <processed video file>
}
```
```
<status details> for RETRY and FAILURE include lasterror message.
Currently the format is:
{
“exc_message”: <exception message, if any>,
“exc_type”: <exception type, if any>
}
But please note the format may change if we decideto mask error
information (or pass more information) to client applications.
```
**API 5: Get Download URLs**

```
Desc Get download URLs for the specified request ids
```
```
Method + URI GET {host}/download/rid
GET {host}/download/rid1,rid2,...,rid
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```
```
Request Clients can request download URLs for finished processingrequests.
```
```
Use comma (‘,’) to separate request ids if retrievingdownload URLs for
multiple processing requests.
```
```
Response JSON object:
{
“count”: <number of records in links array>,
```

```
“links”: [
<link>,
... ...
]
}
```
```
Each element in links array is a JSON object:
{
“rid”: <request id>,
“name”: <name of the video>
“size”: <size of the video>
“duration”: <duration of the video>
“input”: <link of the video>
“urls”: [
{
“name”: <name of the downloadable item>
“files”: <links of the files by extension> [
{ <file type>: <URL to download the correspondingfile>},
{<file type>: <URL to download the correspondingfile>}
]
}
]
}
```
```
For example, if a processor outputs both bvh and fbxfiles, then the
download link object will look like:
{
“rid”: “1234567890”,
“urls”:[ {
“files”: [
{“bvh”: “https://.../...”},
{“fbx”: “https://.../...”}
]
}]
}
```
```
Please note that if the specified request has notfinished yet or has
failed, the response will not include any downloadurls, and the link
object will look like:
{
“rid”: “1234567890”
}
```
**API 6: List All Video Processing requests by Status**


**Desc** List past and current request ids
Note: failed jobs and old jobs may be removed by systemafter a
predefined retention period

**Method + URI** GET {host}/list
GET {host}/list/status1,...,status

**Header(s)** cookie:dmsess=<cookie-value-returned-from-authentication-api>

**Request** Client can request to get list of existing requestids of current user

```
Client can specify one or multiple status value(s)to retrieve only
request ids with the same status value(s). For example,GET
/list/PROGRESS will only return list of requests thatare still being
processed
```
**Response** JSON object:
{
"count": <number of records in the rids array>,
"list": [
{
"rid": "1234567890-1234567890-1234",
"fileName":"",
"fileSize":0,
"fileDuration":0,
"status": "PROGRESS",
"ctime": <creation time>,
"mtime": <last modification time>
},
... ...
]
}

```
Each element in list is a JSON object with the followingfields defined:
```
```
Field Description
```
```
rid Request/emoji id
```
```
fileName Input video file name
```
```
fileSize Input video file size in bytes
```
```
fileDuration Input video duration in seconds
```
```
status Current status (STARTING, PROGRESS, SUCCESS,
FAILURE, RETRY)
```

```
ctime Creation time (milliseconds since epoch)
```
```
mtime Last modification time (milliseconds since epoch)
```
**API 7: Minutes Balance**

```
Desc Retrieves Minutes Balance for an user
```
```
Method + URI GET {host}/account/minutesBalance
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```
```
Request n/a
```
```
Response JSON object:
{
"minutes":<value>
}
```

### Custom Character APIs

**Note:** To make uploaded model(s) available to all animationjobs, please make sure x-useruid HTTP(S)
header should have **not** been passed to the {host}/authAPI to get the session for API 1 and API 2
below.

**API 1: Model Upload Url**

```
Desc Retrieves signed urls to upload 3d model data(fbxformat) and
thumbnail(preferably png format)
```
```
Method + URI GET {host}/character/getModelUploadUrl
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```
```
Request Query parameters:
<name>: base name of the files (without extension)(optional)
<modelExt>: file extension of the model file. Example:fbx (optional)
<thumbExt>: file extension of the thumb file. Example:jpg (optional)
<resumable>: 0 or 1(default) returns resumable orregular signed url
(optional)
```
```
Response JSON object:
{
“modelUrl”: signed url
“thumbUrl”: signed url
}
```
```
After retrieving the urls, actual model & thumbnailupload are required
to that storage urls. If ’resumable’ option is setin the request, we need
one POST and one subsequent PUT request for each signedurl,
otherwise a single PUT request will do the job perurl.
```
```
POST request to url:
<x-goog-resumable>: start (set in the request header)
<location>: resumable url (set in the response headerby server)
```
```
PUT request to resumable url location/url:
attach raw bytes of the model or thumbnail file inthe request body.
```
**API 2: Store Model**

```
Desc Store the asset paths returned from getModelUploadUrlin database
```

```
Method + URI POST {host}/character/storeModel
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```
```
Request Body parameters:
<modelUrl>: model url returned from API 1 (optionalif <modelId> is
provided)
<modelName>: model name (optional)
<thumbUrl>: thumbnail url returned from API 1 (optional)
<modelId>: model id to update existing model info(name or thumb)
(optional if <modelUrl> is provided)
<createThumb>: 0 (default) or 1, indicate if the thumbnailof the model
needs to be generated (optional)
```
```
Response JSON object:
{
“modelId: Unique model id that can be passed tovideo process API
}
```
**API 3: List Models**

```
Desc List models based on specific query or without
```
```
Method + URI GET {host}/character/listModels
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```
```
Request Query parameters:
<modelId>: existing model id (optional)
<searchToken>: for example search by model name (optional)
```
```
Response JSON object:
[
{
“Id: Unique model id that can be passed to videoprocess API
“name”: name of the model
“thumb”: url of the thumbnail if exist
“rigId”: rigTemplate id with which this model isassociated with
“ctime”: creation timestamp
“mtime”: modification timestamp
}
]
```

### Experimental Webhook APIs

#### Event Payload

##### Headers:

HTTP POST payloads that are delivered to your webhook'sconfigured URL endpoint will contain the
following headers:
X-DeepMotion-Signature: <signature>
Note: Signature is your client ID. It is supposedto be verified by your event handling code.

##### Body:

The event body is a JSON object described below:
{
"eventType": <event type>,
"data" <event data>
}

The following table explains the currently supportedevent types and their data sub-attributes. Data
sub-attributes is also a JSON object:

```
eventType Description data Note
```
```
job.completed A task is
completed
```
```
{
"taskId": <request ID>
“status”: <success|failure>
}
```
```
taskId is the rid that returned by
the POST {host}/process API
```
**API 1: Create a webhook endpoint**

```
Desc Create a webhook endpoint
```
```
Method + URI POST {host}/webhook_endpoints
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```
```
Request JSON object:
{
"url": <endpoint URL>,
"events": <array of events that would registerwith this endpoint>
}
```

```
Response JSON object:
{
"id": <endpoint ID>,
"object": "webhook_endpoint",
"url": <endpoint URL>,
"events": <array of events that would registerwith this endpoint>
}
```
**API 2: Retrieve a webhook endpoint**

```
Desc Retrieve a webhook endpoint
```
```
Method + URI GET {host}/webhook_endpoints/<endpoint ID>
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```
```
Request
```
```
Response JSON object:
Response:
{
"id": <endpoint ID>,
"object": "webhook_endpoint",
"url": <endpoint URL>,
"events": <array of events that would registerwith this endpoint>
}
```
**API 3: List webhook endpoints**

```
Desc List webhook endpoints
```
```
Method + URI GET {host}/webhook_endpoints
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```
```
Request
```
```
Response JSON object:
{
"count": <number of endpoints>,
"endpoints": [
{
"id": <endpoint ID>,
"object": "webhook_endpoint",
"url": <endpoint URL>,
"events": <array of events that wouldregister with this endpoint>
}, ...
```

```
]
}
```
**API 4: Update a webhook endpoint**

```
Desc Update a webhook endpoint
```
```
Method + URI POST {host}/webhook_endpoints/<endpoint ID>
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```
```
Request JSON object:
{
"url": <endpoint URL>,
"events": <array of events that would registerwith this endpoint>
}
```
```
Response JSON object:
{
"id": <endpoint ID>,
"object": "webhook_endpoint",
"url": <endpoint URL>,
"events": <array of events that would registerwith this endpoint>
}
```
**API 5: Delete a webhook endpoint**

```
Desc Delete a webhook endpoint
```
```
Method + URI DELETE {host}/webhook_endpoints/<endpoint ID>
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```
```
Request
```
```
Response JSON object:
{
"id": <endpoint ID>,
"object": "webhook_endpoint",
"deleted": true
}
```

