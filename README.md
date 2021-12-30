# Animate 3D REST API

## Revisions

_Alpha v1.0.0_

Initial rest APIs

_Alpha v1.0.1_

Added model parameter to the /process API

_Alpha v1.2.0_

Added custom character end points /character

_Alpha v1.2.1_

Added the “sim” parameter to API 3: Start Video Processing

_Alpha v1.2.2_

Added the “camera” parameter to API 3: Start Video Processing

_Alpha v1.3.0_

Added webhook APIs

_Alpha v1.4.0_

Added footLockingMode parameter to the /process API
Added new minutesBalance API

_Alpha v1.4.1_

Added flag “createThumb” to /character/storeModel API

_Alpha v1.5.0_

Exposed mp4 render out parameters in /process API
Added Face Tracking parameterin /process API

_Alpha v1.5.1_

Added /videoInfo API
Added videoSpeedMultiplier, poseFilteringStrength, rootAtOrigin parameters & new mp4 options in
/process API

The Animate 3D REST API lets you convert videos into 3D animations without having to use the
DeepMotionWeb Portal. Instead you can upload, process,and download the resulting FBX/BVH
animations directly from an external application like a web or desktop app.


## Authentication

###### The Animate 3D REST API uses basic HTTP Authentication to keep your requests and data

###### secure. To use theAPIyou will need a Client ID anda Client Secret which are provided by

DeepMotion. If you do not have these please contact DeepMotion Support or your sales representative.

To retrieve your API access token you need to add the following Authorization header to your token
request:

Authorization: Basic Base64(<clientId>:<clientSecret>)

where the value of<clientId>:<clientSecret>is **base 64** encoded. For Example, if your Client ID
is1a2band your client Secret is3c4dthen your authorizationheader should look like this:

Authorization: Basic MWEyYjozYzRk

###### whereMWEyYjozYzRkis the base64 encoded value of1a2b:3c4d.

**Note** : Optionally it is possible to send a unique useridentifier (via x-useruid HTTP(S) header) along
with the authorization header. See example below:

Curl -v -H “Authorization: Basic MWEyYjozYzRk” -H “x-useruid:me.us@test.com” -X GET “{host}/auth”

## API Endpoints

###### All Animate 3D API requests must be made against the following base URL using the HTTPS

###### protocol and port:

Staging Environment: https://petest.deepmotion.com:
Production Environment: (Contact DeepMotion)

**For using our API from browser javascript** locally(to avoid CORS error), please send request from
any of the origin below:
[http://localhost:](http://localhost:)
[http://localhost:](http://localhost:)
For production deployment, please let us know your production url (scheme, host, port), so that we can
configure our CORS setting accordingly.

## API Reference

**API 1: Get Access Token**

```
Desc Authenticate client credentials and returns a time limited session
```

```
cookie to be used in the subsequent REST API calls. After the session
expiration, this API needs to be called again to get a new session
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
<name>: video/image file name with extension (like test.mp4 or
test.jpg)
<resumable>: 0 or 1(default) returns resumable or regular signed url
(optional)
```
```
Response JSON object:
{
"url": signed url
}
```
```
After retrieving the url, actual video upload is required to that storage
url. If ’resumable’ option is set in the request, we need one POST and
```

```
one subsequent PUT request, otherwise a single PUT request will do
the job.
```
```
POST request to url:
<x-goog-resumable>: start (set in the request header)
<location>: resumable url (set in the response header by server)
```
```
Put request to resumable url/url:
attach raw bytes of the video file in the request body.
```
**API 3: Start Video Processing**

```
Desc Start processing video after file has been uploaded to the designated
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
{
“url”: <upload url>
“processor”: <processor_id>
“params": [<params>, ...]
}
```
```
<upload_url> should match url returned from GET /upload request
```
```
<processor_id> specifies which processor to use to process the video
file, must be one of the following:
```
```
Processor Id Description
```
```
video2anim Deepmotion video to animation processor
```
```
<params> specifies additional parameters that will be passed to the
specified processor, for example:
"params": [
"config=configDefault",formats=bvh,fbx,mp4,model=<modelId> ]
```
```
For static pose, png/jpg can be included in the formats parameter, like:
formats=bvh,fbx,png (to output rendered image instead of rendered
video)
```
```
Additional important parameter: sim
```

This physics simulation parameter needs more clarification.This
parameter influences Pose Estimation result to improve it in some
cases like body parts inter penetration etc.If wewould like to turn
this ON, add sim=1 OR add sim=0 to turn it OFF. If we don’t add this
parameter, simulation is turned off by default.

Added face tracking support:
**trackFace**
● Enable tracking basic facial expressions. Compatible with
character models that contain ARKIT blend shapes. Enabling
this option increases animation processing time.
● Default value is 0 and value can be either 0 or 1

Another new parameter is: **poseEstimation.footLockingMode** or
simply **footLockingMode**
● This parameter value can be one of the below:
○ **auto** : default mode, automatic switching between
locking and gliding modes of the foot, recommended for
general cases
○ **always** : forced foot locking all the time. only used
when Auto mode can not remove all the foot gliding
unsired
○ **never** : forced to disable foot locking and character
grounding. used when the motion is completely in the air
or in the water and therefore neither foot locking nor
character grounding is needed.
○ **grounding** : forced disabling foot locking, however
character is still grounded. Only used when Auto mode
prevents the desired foot gliding (i.e. during shuffling
dances) in the motion or locks the foot for too long on
the ground during fast and short foot/ground contacts
(i.e. during sprints or jumps.)

We have added few new parameters for better body tracking results:

**poseEstimation.videoSpeedMultiplier** or simply
**videoSpeedMultiplier**
● For input videos that have been slowed down, enabling this
option can help improve the resulting animation quality. For
example, if your input video speed moves at 1/2 speed, then set
the speed multiplier to 2x to improve animation quality
● Default value is 1.0 and range is 1.0 - 8.

**poseEstimation.poseFilteringStrength** or simply
**poseFilteringStrength**


```
● Applies an advanced AI filter that helps remove jitter and
produce smoother animations though may result in lower
animation accuracy for certain frames or sequences
● Default value is 0.0 and range is 0.0 - 1.
```
**rootAtOrigin**
● Place a root joint at the origin of the output character. This is
helpful in some cases, for example, for UE4 retargeting.
● Default value is 0 and value can be either 0 or 1

**Mp4 render out parameters:**

1. Please add this below parameter, if you would like to generate the
mp4 with only animated character in a default background (and without
the original video):
**render.sbs=**
2. To replace the default background with a solid color (for green
screening etc.)
**render.sbs=
render.bgColor=0,177,64,0** (RGBA color code in therange of 0-
for each channel, please note, the last channel (alpha) value is not in
effect )
3. To set a studio like background with a solid color tint
**render.sbs=
render.backdrop=studio
render.bgColor=0,177,64,**
4. To enable character shadow
**render.shadow=**
5. **render.includeAudio**
    ● When enabled, it includes the audio of the original input video in
       the generated animation.
    ● Default value is 1 and value can be either 0 or 1
6. **render.CamMode**
values are below. Default is 0
0 (Cinematic) The character is kept in the center of the frame
1 (Fixed) Camera will stay fixed relative to the background
2 (Face) Camera keeps the torso and face in the center of frame


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
Request Clients can request current status of previously submitted processing
requests (API3).
```
```
Use comma (‘,’) to separate multiple request ids if retrieving status for
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
<status details> for RETRY and FAILURE include last error message.
Currently the format is:
{
“exc_message”: <exception message, if any>,
“exc_type”: <exception type, if any>
}
But please note the format may change if we decide to mask error
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
Request Clients can request download URLs for finished processing requests.
```
```
Use comma (‘,’) to separate request ids if retrieving download URLs for
multiple processing requests.
```
```
Response JSON object:
{
“count”: <number of records in links array>,
“links”: [
<link>,
... ...
]
}
```
```
Each element in links array is a JSON object:
{
```

```
“rid”: <request id>,
“name”: <name of the video>
“size”: <size of the video>
“duration”: <duration of the video>
“input”: <link of the video>
“urls”: [
{
“name”: <name of the downloadable item>
“files”: <links of the files by extension> [
{ <file type>: <URL to download the corresponding file>},
{<file type>: <URL to download the corresponding file>}
]
}
]
}
```
```
For example, if a processor outputs both bvh and fbx files, then the
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
Please note that if the specified request has not finished yet or has
failed, the response will not include any download urls, and the link
object will look like:
{
“rid”: “1234567890”
}
```
**API 6: List All Video Processing requests by Status**

```
Desc List past and current request ids
Note: failed jobs and old jobs may be removed by system after a
predefined retention period
```
```
Method + URI GET {host}/list
GET {host}/list/status1,...,status
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```

```
Request Client can request to get list of existing request ids of current user
```
```
Client can specify one or multiple status value(s) to retrieve only
request ids with the same status value(s). For example, GET
/list/PROGRESS will only return list of requests that are still being
processed
```
```
Response JSON object:
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
```
Each element in list is a JSON object with the following fields defined:
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
**API 8: Input Video Information**

```
Desc Get Video information such as resolution, fps etc.
```
```
Method + URI POST {host}/videoInfo
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```
```
Request POST body should include a JSON object:
{
“url”: <upload url>
}
```
```
<upload_url> should match url returned from GET /upload request
AND the video needs to be uploaded to that url in GCS before calling
this API
```
```
Response JSON object:
{"width":1080,"height":1080,"fps":30,"duration":3,"codec":"h264","size":
186615}
```

### Custom Character APIs

**Note:** To make uploaded model(s) available to all animationjobs, please make sure x-useruid HTTP(S)
header should have **not** been passed to the {host}/authAPI to get the session for API 1 and API 2
below.

**API 1: Model Upload Url**

```
Desc Retrieves signed urls to upload 3d model data(fbx, glb, gltf, or vrm
format) and thumbnail(preferably png format)
```
```
Method + URI GET {host}/character/getModelUploadUrl
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```
```
Request Query parameters:
<name>: base name of the files (without extension) (optional)
<modelExt>: file extension of the model file. Example: fbx (optional)
<thumbExt>: file extension of the thumb file. Example: jpg (optional)
<resumable>: 0 or 1(default) returns resumable or regular signed url
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
After retrieving the urls, actual model & thumbnail upload are required
to that storage urls. If ’resumable’ option is set in the request, we need
one POST and one subsequent PUT request for each signed url,
otherwise a single PUT request will do the job per url.
```
```
POST request to url:
<x-goog-resumable>: start (set in the request header)
<location>: resumable url (set in the response header by server)
```
```
PUT request to resumable url location/url:
attach raw bytes of the model or thumbnail file in the request body.
```
**API 2: Store Model**

```
Desc Store the asset paths returned from getModelUploadUrl in database
```

```
Method + URI POST {host}/character/storeModel
```
```
Header(s) cookie:dmsess=<cookie-value-returned-from-authentication-api>
```
```
Request Body parameters:
<modelUrl>: model url returned from API 1 (optional if <modelId> is
provided)
<modelName>: model name (optional)
<thumbUrl>: thumbnail url returned from API 1 (optional)
<modelId>: model id to update existing model info (name or thumb)
(optional if <modelUrl> is provided)
<createThumb>: 0 (default) or 1, indicate if the thumbnail of the model
needs to be generated (optional)
```
```
Response JSON object:
{
“modelId: Unique model id that can be passed to video process API
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
“Id: Unique model id that can be passed to video process API
“name”: name of the model
“thumb”: url of the thumbnail if exist
“rigId”: rigTemplate id with which this model is associated with
“ctime”: creation timestamp
“mtime”: modification timestamp
}
]
```

### Experimental Webhook APIs

#### Event Payload

##### Headers:

HTTP POST payloads that are delivered to your webhook's configured URL endpoint will contain the
following headers:
X-DeepMotion-Signature: <signature>
Note: Signature is your client ID. It is supposed to be verified by your event handling code.

##### Body:

The event body is a JSON object described below:
{
"eventType": <event type>,
"data" <event data>
}

The following table explains the currently supported event types and their data sub-attributes. Data
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
"events": <array of events that would register with this endpoint>
}
```

```
Response JSON object:
{
"id": <endpoint ID>,
"object": "webhook_endpoint",
"url": <endpoint URL>,
"events": <array of events that would register with this endpoint>
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
"events": <array of events that would register with this endpoint>
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
"events": <array of events that would register with this endpoint>
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
"events": <array of events that would register with this endpoint>
}
```
```
Response JSON object:
{
"id": <endpoint ID>,
"object": "webhook_endpoint",
"url": <endpoint URL>,
"events": <array of events that would register with this endpoint>
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

