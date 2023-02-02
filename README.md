# **Animate 3D REST API**


## Revisions


# _Alpha v1.0.0_

Initial rest APIs


# _Alpha v1.0.1_

Added model parameter to the /process API


# _Alpha v1.2.0_

Added custom character end points  /character


# _Alpha v1.2.1_

Added the “sim” parameter to API 3: Start Video Processing


# _Alpha v1.2.2_

Added the “camera” parameter to API 3: Start Video Processing


# _Alpha v1.3.0_

Added webhook APIs


# _Alpha v1.4.0_

Added footLockingMode parameter to the /process API

Added new minutesBalance API


# _Alpha v1.4.1_

Added flag “createThumb” to /character/storeModel API


# _Alpha v1.5.0_

Exposed mp4 render out parameters in /process API

Added Face Tracking parameter in /process API


# _Alpha v1.5.1_

Added /videoInfo API

Added videoSpeedMultiplier, poseFilteringStrength, rootAtOrigin parameters & new mp4 options in /process API


# _Alpha v1.5.2_

Added /character/deleteModel API


# _Alpha v1.5.3_

Added trim & crop parameters in /process API


# _Alpha v1.5.4_

Added /account/creditBalance API


# _Alpha v1.5.5_

Added Hand/Finger Tracking parameter in /process API


# _Alpha v1.5.6_

Added parameter for rerunning  a job in /process API. API Error codes with information have been added.


# _Alpha v1.5.7_

Added error messages

The Animate 3D REST API lets you convert videos into 3D animations without having to use the DeepMotion [Web Portal](https://portal.deepmotion.com/). Instead you can upload, process, and download the resulting FBX/BVH animations directly from an external application like a web or desktop app.


# Authentication

The Animate 3D REST API uses basic **HTTP Authentication** to keep your requests and data secure. To use the API you will need a **Client ID** and a **Client Secret **which are provided by DeepMotion. If you do not have these please contact DeepMotion Support or your sales representative.

To retrieve your API access token you need to add the following Authorization header to your token request:


```
Authorization: Basic Base64(<clientId>:<clientSecret>)
```


where the value of `&lt;clientId>:&lt;clientSecret>` is **base 64** encoded.  For Example, if your Client ID is `1a2b` and your client Secret is `3c4d` then your authorization header should look like this: 


```
Authorization: Basic MWEyYjozYzRk
```


where `MWEyYjozYzRk` is the base64 encoded value of `1a2b:3c4d.`


# API Endpoints

All Animate 3D API requests must be made against the following base URL using the HTTPS protocol and port:


```
Staging Environment: 		https://petest.deepmotion.com:443
Production Environment: 	(Contact DeepMotion)
```


**For using our API from browser javascript** locally (to avoid CORS error), please send request from any of the origin below:

[http://localhost:8080](http://localhost:8080/)

[http://localhost:8180](http://localhost:8180/)

For production deployment, please let us know your production url (scheme, host, port), so that we can configure our CORS setting accordingly.


# API Reference

**API 1: Get Access Token**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Authenticate client credentials and returns a time limited session cookie to be used in the subsequent REST API calls. After the session expiration, this API needs to be called again to get a new session cookie
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/session/auth
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>Authorization: Basic Base64(&lt;clientId>:&lt;clientSecret>)
   </td>
  </tr>
  <tr>
   <td><strong>Request </strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>Sample Response Header:
<p>
set-cookie: dmsess=s%3AEsF23MoyDEq7tTWQM8KfA_wjKkSrOFwU.2fjJTfDP%2FT2BeA5DFenwOH4t8XzqZsbSc6M2mZwS%2BWg; 
<p>
Domain=.deepmotion.com; Path=/; Expires=Mon, 03 Aug 2020 13:36:26 GMT; HttpOnly
<p>
(Note:<strong> dmsess </strong>is the session cookie. This cookie needs to be sent in all subsequent REST API calls.
<p>
Sample Request Header for other API calls:
<p>
cookie:dmsess=s%3AEsF23MoyDEq7tTWQM8KfA_wjKkSrOFwU.2fjJTfDP%2FT2BeA5DFenwOH4t8XzqZsbSc6M2mZwS%2BWg)
   </td>
  </tr>
</table>


**API 2: Upload Video**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Retrieves a signed url to upload video
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/upload
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>Query parameters:
<p>
&lt;name>: video/image file name with extension (like test.mp4 or test.jpg)
<p>
&lt;resumable>: 0 or 1(default) returns resumable or regular signed url (optional)
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
  "url": signed url
<p>
}
<p>
After retrieving the url, actual video upload is required to that storage url. If ’resumable’ option is set in the request,  we need one POST and one subsequent PUT request, otherwise a single PUT request will do the job.
<p>
POST request to url:
<p>
&lt;x-goog-resumable>: start (set in the request header)
<p>
&lt;location>: resumable url (set in the response header by server)
<p>
Put request to resumable url/url:
<p>
attach raw bytes of the video file in the request body.
   </td>
  </tr>
</table>


**API 3: Start Video Processing**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Start processing video after file has been uploaded to the designated URL
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>POST {host}/process
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>POST body should include a JSON object:
<p>
{
<p>
  “url”: &lt;upload url>
<p>
  “rid”: &lt;previous successful job’s request id>
<p>
  “processor”: &lt;processor_id>
<p>
  “params": [&lt;params>, ...]
<p>
}
<p>
&lt;upload_url> should match url returned from GET /upload request.
<p>
To rerun a job with different parameters, “rid” input should be used instead of “url”.
<p>
 
<p>
&lt;processor_id> specifies which processor to use to process the video file, must be one of the following:

<table>
  <tr>
   <td><strong>Processor Id</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td>video2anim
   </td>
   <td>Deepmotion video to animation processor
   </td>
  </tr>
</table>


&lt;params> specifies additional parameters that will be passed to the specified processor, for example:

   "params": [ "config=configDefault",formats=bvh,fbx,mp4,model=&lt;modelId> ]

For static pose, png/jpg can be included in the formats parameter, like: formats=bvh,fbx,png (to output rendered image instead of rendered video)

Additional important parameter: **sim**

This physics simulation parameter needs more clarification. This parameter influences Pose Estimation result to improve it in some cases like body parts inter penetration etc. If we would like to turn this ON, add  sim=1 OR add sim=0 to turn it OFF. If we don’t add this parameter, simulation is turned off by default. 

Added face tracking support:

**trackFace**



* Enable tracking basic facial expressions. Compatible with character models that contain ARKIT blend shapes. Enabling this option increases animation processing time (and additional charge if the server processes this for a compatible model).
* Default value is 0 and value can be either 0 or 1 

Added hand tracking support:

**trackHand**



* Enable tracking hand/finger movement. Compatible with character models that contain hand/finger joints. Enabling this option increases animation processing time (and additional charge if the server processes this for a compatible model).
* Default value is 0 and value can be either 0 or 1 

Another new parameter is: **poseEstimation.footLockingMode** or simply **footLockingMode**



* This parameter value can be one of the below:
    * **auto** : default mode, automatic switching between locking and gliding modes of the foot, recommended for general cases
    * **always** :  forced foot locking all the time. only used when Auto mode can not remove all the foot gliding unsired
    * **never** : forced to disable foot locking and character grounding. used when the motion is completely in the air or in the water and therefore neither foot locking nor character grounding is needed.
    * **grounding** : forced disabling foot locking, however character is still grounded. Only used when Auto mode prevents the desired foot gliding (i.e. during shuffling dances) in the motion or locks the foot for too long on the ground during fast and short foot/ground contacts (i.e. during sprints or jumps.)

We  have added few new parameters for better body tracking results:

**poseEstimation.videoSpeedMultiplier **or simply **videoSpeedMultiplier**



* For input videos that have been slowed down, enabling this option can help improve the resulting animation quality. For example, if your input video speed moves at 1/2 speed, then set the speed multiplier to 2x to improve animation quality
* Default value is 1.0 and range is 1.0 - 8.0

**poseEstimation.poseFilteringStrength **or simply **poseFilteringStrength**



* Applies an advanced AI filter that helps remove jitter and produce smoother animations though may result in lower animation accuracy for certain frames or sequences
* Default value is 0.0 and range is 0.0 - 1.0 

**rootAtOrigin**



* Place a root joint at the origin of the output character. This is helpful in some cases, for example, for UE4 retargeting.
* Default value is 0 and value can be either 0 or 1

Trim (input video only) & Cropping( input video/image)



* trim=from,to (in seconds, example: trim=1,2.6)
* crop=left,top,right,bottom (normalized coordinate value, origin[0,0] is left-top, example: crop=0.239,0.121,0.742,0.981 )

**Mp4 render out parameters:**

1. Please add this below parameter, if you would like to generate the mp4 with only animated character in a default background (and without the original video):

**render.sbs=0**

2. To replace the default background with a solid color (for green screening etc.)

**render.sbs=0**

**render.bgColor=0,177,64,0**  (RGBA color code in the range of 0-255 for each channel, please note, the last channel (alpha) value is not in effect )

3. To set a studio like background with a solid color tint

**render.sbs=0**

**render.backdrop=studio**

**render.bgColor=0,177,64,0 **

4. To enable character shadow

**render.shadow=1 **

5. **render.includeAudio**



* When enabled, it includes the audio of the original input video in the generated animation.
* Default value is 1 and value can be either 0 or 1

6. **render.CamMode**

values are below. Default is 0

0 (Cinematic) The character is kept in the center of the frame

1 (Fixed) Camera will stay fixed relative to the background

2 (Face) Camera keeps the torso and face in the center of frame

   </td>
  </tr>
  <tr>
   <td>**Response**

   </td>
   <td>JSON object:

{

  "rid": &lt;request id>

}

   </td>
  </tr>
</table>


**API 4: Poll for Job Status**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Polls for real-time status of a given processing job
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/status/rid
<p>
GET {host}/status/rid1,rid2,..,rid
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>Clients can request current status of previously submitted processing requests (API3).
<p>
Use comma (‘,’) to separate multiple request ids if retrieving status for more than 1 request.
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
  "count": &lt;number of records in status array>,
<p>
  "status": [
<p>
     &lt;status>,
<p>
     … …
<p>
  ]
<p>
}
<p>
Each element in status array is a JSON object:
<p>
{
<p>
  "rid": &lt;request id>,
<p>
  "status": &lt;status name>
<p>
  "details": &lt;status details, see below>
<p>
}
<p>
&lt;status name> is one of the following <strong>case sensitive</strong> values:

<table>
  <tr>
   <td><strong>Status Name</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td>PROGRESS
   </td>
   <td>Request is still being processed
   </td>
  </tr>
  <tr>
   <td>SUCCESS
   </td>
   <td>Request is processed successfully
   </td>
  </tr>
  <tr>
   <td>RETRY
   </td>
   <td>Request has failed for some reason, but is being retried
   </td>
  </tr>
  <tr>
   <td>FAILURE
   </td>
   <td>Request has failed
   </td>
  </tr>
</table>


&lt;status details> for PROGRESS:

{

  “step”: &lt;current step>,

  “total”: &lt;expected total number of steps>

}

&lt;status details> for SUCCESS:

{

  “In”: &lt;original video file>,

  “out”: &lt;processed video file>

}

&lt;status details> for RETRY and FAILURE include last error message. Currently the format is:

{

  “exc_message”: &lt;exception message, if any>,

  “exc_type”: &lt;exception type, if any>

}

But please note the format may change if we decide to mask error information (or pass more information) to client applications.

   </td>
  </tr>
</table>


**API 5: Get Download URLs**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Get download URLs for the specified request ids
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/download/rid
<p>
GET {host}/download/rid1,rid2,...,rid
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>Clients can request download URLs for finished processing requests.
<p>
Use comma (‘,’) to separate request ids if retrieving download URLs for multiple processing requests.
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
  “count”: &lt;number of records in links array>,
<p>
  “links”: [
<p>
    &lt;link>,
<p>
    … ...
<p>
  ]
<p>
}
<p>
Each element in links array is a JSON object:
<p>
{
<p>
  “rid”: &lt;request id>,
<p>
  “name”: &lt;name of the video>
<p>
  “size”: &lt;size of the video> 
<p>
  “duration”: &lt;duration of the video>
<p>
  “input”: &lt;link of the video>
<p>
  “urls”: [
<p>
   {
<p>
    “name”: &lt;name of the downloadable item>
<p>
    “files”: &lt;links of the files by extension> [
<p>
     { &lt;file type>: &lt;URL to download the corresponding file>},
<p>
     {&lt;file type>: &lt;URL to download the corresponding file>}
<p>
     ]
<p>
   }
<p>
  ]
<p>
}
<p>
For example, if a processor outputs both bvh and fbx files, then the download link object will look like:
<p>
{
<p>
  “rid”: “1234567890”,
<p>
  “urls”:[ {
<p>
    “files”: [
<p>
      {“bvh”: “https://.../…”},
<p>
      {“fbx”: “https://.../…”}
<p>
    ]
<p>
  }]
<p>
}
<p>
Please note that if the specified request has not finished yet or has failed, the response will not include any download urls, and the link object will look like:
<p>
{
<p>
  “rid”: “1234567890”
<p>
}
<p>
Note: .dmpe format is available with the name <strong>landmarks.dmpe</strong>
   </td>
  </tr>
</table>


**API 6: List All Video Processing requests by Status**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>List past and current request ids
<p>
Note: failed jobs and old jobs may be removed by system after a predefined retention period
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/list
<p>
GET {host}/list/status1,...,status
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>Client can request to get list of existing request ids of current user
<p>
Client can specify one or multiple status value(s) to retrieve only request ids with the same status value(s). For example, GET /list/PROGRESS will only return list of requests that are still being processed
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
   "count": &lt;number of records in the rids array>,
<p>
  "list": [
<p>
    {
<p>
      "rid": "1234567890-1234567890-1234",
<p>
      "fileName":"",
<p>
      "fileSize":0,
<p>
      "fileDuration":0,
<p>
      "status": "PROGRESS",
<p>
      "ctime": &lt;creation time>,
<p>
      "mtime": &lt;last modification time>
<p>
    },
<p>
    ... ...
<p>
  ]
<p>
}
<p>
Each element in list is a JSON object with the following fields defined:

<table>
  <tr>
   <td><strong>Field</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td>rid
   </td>
   <td>Request/emoji id
   </td>
  </tr>
  <tr>
   <td>fileName
   </td>
   <td>Input video file name
   </td>
  </tr>
  <tr>
   <td>fileSize
   </td>
   <td>Input video file size in bytes
   </td>
  </tr>
  <tr>
   <td>fileDuration
   </td>
   <td>Input video duration in seconds
   </td>
  </tr>
  <tr>
   <td>status
   </td>
   <td>Current status (STARTING, PROGRESS, SUCCESS, FAILURE, RETRY)
   </td>
  </tr>
  <tr>
   <td>ctime
   </td>
   <td>Creation time (milliseconds since epoch)
   </td>
  </tr>
  <tr>
   <td>mtime
   </td>
   <td>Last modification time (milliseconds since epoch)
   </td>
  </tr>
</table>


   </td>
  </tr>
</table>


**API 7: Credit Balance**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Retrieves Credit Balance for an user
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/account/creditBalance
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>n/a
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
 "credits":&lt;value>
<p>
}
   </td>
  </tr>
</table>


**API 8: Input Video Information**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Get Video information such as resolution, fps etc.
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>POST {host}/videoInfo
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>POST body should include a JSON object:
<p>
{
<p>
  “url”: &lt;upload url>
<p>
}
<p>
&lt;upload_url> should match url returned from GET /upload request AND the video needs to be uploaded to that url in GCS before calling this API
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{"width":1080,"height":1080,"fps":30,"duration":3,"codec":"h264","size":186615}
   </td>
  </tr>
</table>



# 


# Custom Character APIs

**Note: **To make uploaded model(s) available to all animation jobs, please make sure x-useruid HTTP(S) header should have **not** been passed to the  {host}/auth API to get the session for API 1 and API 2 below.

**API 1: Model Upload Url**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Retrieves signed urls to upload 3d model data(fbx, glb, gltf, or vrm format) and thumbnail(preferably png format)
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/character/getModelUploadUrl
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>Query parameters:
<p>
&lt;name>: base name of the files (without extension) (optional)
<p>
&lt;modelExt>: file extension of the model file. Example: fbx  (optional)
<p>
&lt;thumbExt>: file extension of the thumb file. Example: jpg (optional)
<p>
&lt;resumable>: 0 or 1(default) returns resumable or regular signed url (optional)
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
  “modelUrl”: signed url
<p>
  “thumbUrl”: signed url
<p>
}
<p>
After retrieving the urls, actual model & thumbnail upload are required to that storage urls. If ’resumable’ option is set in the request,  we need one POST and one subsequent PUT request for each signed url, otherwise a single PUT request will do the job per url.
<p>
POST request to url:
<p>
&lt;x-goog-resumable>: start (set in the request header)
<p>
&lt;location>: resumable url (set in the response header by server)
<p>
PUT request to resumable url location/url:
<p>
attach raw bytes of the model or thumbnail file in the request body.
   </td>
  </tr>
</table>


**API 2: Store Model**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Store the asset paths returned from getModelUploadUrl in database
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>POST {host}/character/storeModel
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>Body parameters:
<p>
&lt;modelUrl>: model url returned from API 1 (optional if  &lt;modelId> is provided)
<p>
&lt;modelName>: model  name (optional)
<p>
&lt;thumbUrl>: thumbnail url returned from API 1 (optional)
<p>
&lt;modelId>: model id to update existing model info (name or thumb) (optional if  &lt;modelUrl> is provided)
<p>
&lt;createThumb>: 0 (default) or 1, indicate if the thumbnail of the model needs to be generated (optional)
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
  “modelId: Unique model id that can be passed to video process API
<p>
}
   </td>
  </tr>
</table>


**API 3: List Models**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>List models based on specific query or without
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/character/listModels
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>Query parameters:
<p>
&lt;modelId>: existing model id (optional)
<p>
&lt;searchToken>: for example search by model name (optional)
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
[
<p>
 {
<p>
   “Id: Unique model id that can be passed to video process API
<p>
   “name”: name of the model
<p>
   “thumb”: url of the thumbnail if exist
<p>
   “rigId”: rigTemplate id with which this model is associated with
<p>
   “ctime”: creation timestamp
<p>
   “mtime”: modification timestamp
<p>
 }
<p>
]
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>
   </td>
  </tr>
</table>


**API 4: Delete Model**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Delete model with specific model ID
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>DELETE {host}/character/deleteModel/&lt;model ID>
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
  “count”: number of models that have been deleted
<p>
}
   </td>
  </tr>
</table>



# Experimental Webhook APIs


## Event Payload


### Headers: 

HTTP POST payloads that are delivered to your webhook's configured URL endpoint will contain the following headers:

	X-DeepMotion-Signature: &lt;signature>

Note: Signature is your client ID. It is supposed to be verified by your event handling code.


### Body:

The event body is a JSON object described below:

{

	"eventType": &lt;event type>,

	"data" &lt;event data>

}

The following table explains the currently supported event types and their data sub-attributes. Data sub-attributes is also a JSON object:


<table>
  <tr>
   <td><strong>eventType</strong>
   </td>
   <td><strong>Description</strong>
   </td>
   <td><strong>data</strong>
   </td>
   <td><strong>Note</strong>
   </td>
  </tr>
  <tr>
   <td>job.completed
   </td>
   <td>A task is completed
   </td>
   <td>{
<p>
    "taskId": &lt;request ID> 
<p>
    “status”: &lt;success|failure> 
<p>
}
   </td>
   <td><em>taskId </em>is the rid that returned by the POST {host}/process API 
   </td>
  </tr>
</table>


**API 1: Create a webhook endpoint**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Create a webhook endpoint
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>POST {host}/webhook_endpoints
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
    "url": &lt;endpoint URL>,
<p>
    "events": &lt;array of events that would register with this endpoint>
<p>
}
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
    "id": &lt;endpoint ID>,
<p>
    "object": "webhook_endpoint",
<p>
    "url": &lt;endpoint URL>,
<p>
    "events": &lt;array of events that would register with this endpoint>
<p>
}
   </td>
  </tr>
</table>


**API 2: Retrieve a webhook endpoint**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Retrieve a webhook endpoint
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/webhook_endpoints/&lt;endpoint ID>
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
Response:
<p>
{
<p>
    "id": &lt;endpoint ID>,
<p>
    "object": "webhook_endpoint",
<p>
    "url": &lt;endpoint URL>,
<p>
    "events": &lt;array of events that would register with this endpoint>
<p>
}
   </td>
  </tr>
</table>


**API 3: List webhook endpoints**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>List webhook endpoints
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>GET {host}/webhook_endpoints
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
    "count": &lt;number of endpoints>,
<p>
    "endpoints": [
<p>
        {
<p>
            "id": &lt;endpoint ID>,
<p>
            "object": "webhook_endpoint",
<p>
            "url": &lt;endpoint URL>,
<p>
            "events": &lt;array of events that would register with this endpoint>
<p>
        }, ...
<p>
    ]
<p>
}
   </td>
  </tr>
</table>


**API 4: Update a webhook endpoint**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Update a webhook endpoint
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>POST {host}/webhook_endpoints/&lt;endpoint ID>
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
    "url": &lt;endpoint URL>,
<p>
    "events": &lt;array of events that would register with this endpoint>
<p>
}
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
    "id": &lt;endpoint ID>,
<p>
    "object": "webhook_endpoint",
<p>
    "url": &lt;endpoint URL>,
<p>
    "events": &lt;array of events that would register with this endpoint>
<p>
}
   </td>
  </tr>
</table>


**API 5: Delete a webhook endpoint**


<table>
  <tr>
   <td><strong>Desc</strong>
   </td>
   <td>Delete a webhook endpoint
   </td>
  </tr>
  <tr>
   <td><strong>Method + URI</strong>
   </td>
   <td>DELETE {host}/webhook_endpoints/&lt;endpoint ID>
   </td>
  </tr>
  <tr>
   <td><strong>Header(s)</strong>
   </td>
   <td>cookie:dmsess=&lt;cookie-value-returned-from-authentication-api>
   </td>
  </tr>
  <tr>
   <td><strong>Request</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td><strong>Response</strong>
   </td>
   <td>JSON object:
<p>
{
<p>
    "id": &lt;endpoint ID>,
<p>
    "object": "webhook_endpoint",
<p>
    "deleted": true
<p>
}
   </td>
  </tr>
</table>



# 


# Animate 3D Restful API Error Codes


<table>
  <tr>
   <td>Error Code
   </td>
   <td>Meaning
   </td>
  </tr>
  <tr>
   <td>201
   </td>
   <td>Error downloading the video or DM asset
   </td>
  </tr>
  <tr>
   <td>202
   </td>
   <td>Error converting the video
   </td>
  </tr>
  <tr>
   <td>503
   </td>
   <td>Error processing the parameters
   </td>
  </tr>
  <tr>
   <td>504
   </td>
   <td>Error loading the character assets
   </td>
  </tr>
  <tr>
   <td>505
   </td>
   <td>Physics Filter is incompatible with the custom characters
   </td>
  </tr>
  <tr>
   <td>506
   </td>
   <td>Error creating the pose estimation
   </td>
  </tr>
  <tr>
   <td>507
   </td>
   <td>Error while processing the body tracking
   </td>
  </tr>
  <tr>
   <td>508
   </td>
   <td>Input video or image doesn’t meet the requirements to generate animations of good quality 
   </td>
  </tr>
  <tr>
   <td>509
   </td>
   <td>Error loading the configurations
   </td>
  </tr>
  <tr>
   <td>510
   </td>
   <td>Error open internal files
   </td>
  </tr>
  <tr>
   <td>511
   </td>
   <td>Processing interrupted
   </td>
  </tr>
  <tr>
   <td>513
   </td>
   <td>Failed to detect character in the video
   </td>
  </tr>
  <tr>
   <td>599
   </td>
   <td>Body tracking timeout
   </td>
  </tr>
  <tr>
   <td>701
   </td>
   <td>Error processing the face tracking
   </td>
  </tr>
  <tr>
   <td>799
   </td>
   <td>Face tracking timeout
   </td>
  </tr>
  <tr>
   <td>901
   </td>
   <td>Error loading the mesh of the custom character
   </td>
  </tr>
  <tr>
   <td>902
   </td>
   <td>Error loading the BVH custom character
   </td>
  </tr>
  <tr>
   <td>903
   </td>
   <td>Error copying animations onto the custom character
   </td>
  </tr>
  <tr>
   <td>904
   </td>
   <td>Error exporting animations for the custom character
   </td>
  </tr>
  <tr>
   <td>905
   </td>
   <td>Custom character doesn’t include skinned mesh information
   </td>
  </tr>
  <tr>
   <td>906
   </td>
   <td>More than half of the required blendshapes are missing
   </td>
  </tr>
  <tr>
   <td>907
   </td>
   <td>Error loading facial definition for the custom character
   </td>
  </tr>
  <tr>
   <td>908
   </td>
   <td>Error loading facial tracking data
   </td>
  </tr>
  <tr>
   <td>909
   </td>
   <td>Error loading the metadata of the custom character
   </td>
  </tr>
  <tr>
   <td>999
   </td>
   <td>Animation baking timeout
   </td>
  </tr>
  <tr>
   <td>1301
   </td>
   <td>Error creating the hand estimation
   </td>
  </tr>
  <tr>
   <td>1302
   </td>
   <td>Error creating the hand estimation
   </td>
  </tr>
  <tr>
   <td>1303
   </td>
   <td>Error creating the hand estimation
   </td>
  </tr>
  <tr>
   <td>1304
   </td>
   <td>Error opening the video
   </td>
  </tr>
  <tr>
   <td>1305
   </td>
   <td>Error parsing video path
   </td>
  </tr>
  <tr>
   <td>1306
   </td>
   <td>Error loading internal files
   </td>
  </tr>
  <tr>
   <td>1307
   </td>
   <td>Error processing hand tracking
   </td>
  </tr>
  <tr>
   <td>1308
   </td>
   <td>Error processing the video
   </td>
  </tr>
  <tr>
   <td>1399
   </td>
   <td>Hand tracking timeout
   </td>
  </tr>
</table>