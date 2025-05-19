# PINGME

![PingMe](readme_assets/responsive.png)

This section of the project provides a Django Rest Framework API for the [PingMe!](https://ping-me-pp5-frontend-c34a5313765d.herokuapp.com) react web app. It has also been designed and optimzed for mobile environments in the future.

---

Ping me is a lightweight discord clone that allows the user to view signup and join chatrooms to chat with other users, the sole aim of the project is to document my skills with react/typescript mui and django rest framework

As this is a backend site there is no deployed site to visit but you can view the schema [here](https://ping-me-pp5-backend-6aaeef173b97.herokuapp.com/api/docs/schema/ui/#/) this has a list of endpoints and what they do, sadly they are not interactable as for security the endpoints are all protected by authentication requirementss

## Table of contents
- [PingMe](#pingme)
  * [Project goals](#project-goals)
  * [Table of contents](#table-of-contents)
  * [Planning](#planning)
  * [Data models](#data-models)
  * [API endpoints](#api-endpoints)
  * [Frameworks, libraries and dependencies](#frameworks--libraries-and-dependencies)
  * [Testing](#testing)
  * [Bugs](#bugs)
  * [Deployment](#deployment)
  * [Credits](#credits)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Planning
Planning started by creating epics and user stories for the frontend application, based on the project goals. The user stories were used to inform wireframes mapping out the intended functionality and 'flow' through the app. From there we build the various models and endpoints out to meet these goals

### Data models
Data model schema were planned in parallel with the API endpoints, using an entity relationship diagram.

Custom models implemented for Ping me were

#### **Account**
Represents the user Account, using a one-to-one relationsip to the user model. A Account instance is automatically created on user registration. The Account model includes includes various fields that we the dev can use to distinguish it and link it to other parts of the app

#### **Server**
This model handles all of our server logic, including creation editing and deleting, its' used in the front end by our server context consumers to pass server data efficiently and easily

#### **Category**
The category is our primary sorting model for servers, upon server creation it is given a category to be filtered by we then utilized these so users can view the servers that appealed to them

### **Channel**
The channel model was responsible for our channel creation and management, and allows us to enter the channel and chat to users via the messenger / conversation model

### **Conversation**
The conversation model handles storing all of our conversation message objects, this allowed us to have hundreds of messages per conversation and load them all rapidly from our api to our frontend

### **Message**
This was our chief message model each one created a message object, we took this approach to ensure that messages were easy to manipulate

## API endpoints

A list of all api endpoints can be found in our [schema](https://ping-me-pp5-backend-6aaeef173b97.herokuapp.com/api/docs/schema/ui/#/) 
To test this schema and the api endpoints the tester must be authorized, to authorize use the test user credentials provided or create an account, and 
run the token auth endpoint to get an auth token. Posting said auth token into the authorize will allow you access to the scema api

## Frameworks, libraries and dependencies
### django-cloudinary-storage
https://pypi.org/project/django-cloudinary-storage/

Enables cloudinary integration for storing user Account images in cloudinary.

### dj-allauth
https://django-allauth.readthedocs.io/en/latest/

Used for user authentication. While not currently utilised, this package enables registration and authentication using a range of social media accounts. This may be implemented in a future update.

### dj-rest-auth
https://dj-rest-auth.readthedocs.io/en/latest/introduction.html

Provides REST API endpoints for login and logout. The user registration endpoints provided by dj-rest-auth are not utilised by the Serverhub frontend, as custom functionality was required and implemented by the Serverhub API.

### djangorestframework-simplejwt
https://django-rest-framework-simplejwt.readthedocs.io/en/latest/

Provides JSON web token authentication.

### dj-database-url
https://pypi.org/project/dj-database-url/

Creates an environment variable to configure the connection to the database.

### psychopg2
https://pypi.org/project/psycopg2/

Database adapater to enable interaction between Python and the PostgreSQL database.

### django-cors-headers
https://pypi.org/project/django-cors-headers/

This Django app adds Cross-Origin-Resource Sharing (CORS) headers to responses, to enable the API to respond to requests from origins other than its own host.
ServerHub is configured to allow requests from all origins, to facilitate future development of a native movile app using this API.

### django-channels
https://channels.readthedocs.io/en/latest/

This django add on was our primary means of setting up and maintaining websockets for real time communication coupling this with redis servers from heroku allowed us to create a fully functioning real time application akin to discord


## Testing

### Manual testing

A series of manual tests were undertaken to determine api viability, and test to see if the user got the correct details back, as well as this we double and triple checked every endpoint to make sure the user needs authentication to access any of these endpoints

|                 TEST                  |              Expected outcome              |              Actual outcome               | Pass/Fail |
| :-----------------------------------: | :----------------------------------------: | :---------------------------------------: | :-------: |
|     POST /auth/register (valid)      | 201 Created, user object, email sent       | 201 Created, user object, email sent      |   Pass    |
|   POST /auth/register (invalid)      | 400 Bad Request, validation errors         | 400 Bad Request, validation errors        |   Pass    |
|    POST /auth/login (valid creds)    | 200 OK, JWT token returned                 | 200 OK, JWT token returned                |   Pass    |
|  POST /auth/login (invalid creds)    | 401 Unauthorized, error message            | 401 Unauthorized, error message           |   Pass    |
| POST /auth/login (unverified email)  | 403 Forbidden, verification prompt         | 403 Forbidden, verification prompt        |   Pass    |
|         POST /auth/logout            | 200 OK, token invalidated                  | 200 OK, token invalidated                 |   Pass    |
|      POST /auth/verify-email         | 200 OK, user status updated                | 200 OK, user status updated               |   Pass    |
| POST /auth/resend-verification       | 200 OK, verification email sent            | 200 OK, verification email sent           |   Pass    |
|          GET /users/me               | 200 OK, user profile returned              | 200 OK, user profile returned             |   Pass    |
|     PATCH /users/me (valid data)     | 200 OK, profile updated                    | 200 OK, profile updated                   |   Pass    |
|   PATCH /users/me (invalid data)     | 400 Bad Request, validation errors         | 400 Bad Request, validation errors        |   Pass    |
|          DELETE /users/me            | 204 No Content, user deleted               | 204 No Content, user deleted              |   Pass    |
|            GET /servers              | 200 OK, list of servers                    | 200 OK, list of servers                   |   Pass    |
|    POST /servers (valid data)        | 201 Created, server returned               | 201 Created, server returned              |   Pass    |
| POST /servers (duplicate name)       | 409 Conflict, error message                | 409 Conflict, error message               |   Pass    |
|   PATCH /servers/:id (is owner)      | 200 OK, server updated                     | 200 OK, server updated                    |   Pass    |
| PATCH /servers/:id (not owner)       | 403 Forbidden, action blocked              | 403 Forbidden, action blocked             |   Pass    |
|  DELETE /servers/:id (is owner)      | 204 No Content, server deleted             | 204 No Content, server deleted            |   Pass    |
| DELETE /servers/:id (not owner)      | 403 Forbidden, action blocked              | 403 Forbidden, action blocked             |   Pass    |
|     GET /servers/:id/channels        | 200 OK, list of channels                   | 200 OK, list of channels                  |   Pass    |
|  POST /channels (admin permission)   | 201 Created, channel returned              | 201 Created, channel returned             |   Pass    |
| POST /channels (no admin rights)     | 403 Forbidden, action blocked              | 403 Forbidden, action blocked             |   Pass    |
| PATCH /channels/:id (admin)          | 200 OK, channel updated                    | 200 OK, channel updated                   |   Pass    |
| PATCH /channels/:id (not admin)      | 403 Forbidden, action blocked              | 403 Forbidden, action blocked             |   Pass    |
| DELETE /channels/:id (admin)         | 204 No Content, channel deleted            | 204 No Content, channel deleted           |   Pass    |
| DELETE /channels/:id (not admin)     | 403 Forbidden, action blocked              | 403 Forbidden, action blocked             |   Pass    |
|           GET /categories            | 200 OK, list of categories                 | 200 OK, list of categories                |   Pass    |
|     GET /categories/{id}            | 200 OK, category details                   | 200 OK, category details                  |   Pass    |
| GET /servers?category=xyz            | 200 OK, filtered servers returned          | 200 OK, filtered servers returned         |   Pass    |
|       GET /protected (no auth)       | 401 Unauthorized, error message            | 401 Unauthorized, error message           |   Pass    |
| GET /admin-only (user role)          | 403 Forbidden, access denied               | 403 Forbidden, access denied              |   Pass    |
|      GET /unknown-route              | 404 Not Found, error message               | 404 Not Found, error message              |   Pass    |
|     API error returns JSON object    | Proper JSON error message                  | Proper JSON error message                 |   Pass    |
|      Rate limit exceeded             | 429 Too Many Requests, rate error          | 429 Too Many Requests, rate error         |   Pass    |
|        CORS headers present          | Access-Control-Allow-Origin in headers     | Access-Control-Allow-Origin in headers    |   Pass    |
|  All endpoints require auth (secure) | 401 Unauthorized for unauthenticated users | 401 Unauthorized for unauthenticated users|   Pass    |
| GET /api/account/me/                 | 200 OK, user data returned                 | 200 OK, user data returned                |   Pass    |
| PATCH /api/account/edit_me/          | 200 OK, user updated                       | 200 OK, user updated                      |   Pass    |
| GET /api/account/my_servers/         | 200 OK, servers returned                   | 200 OK, servers returned                  |   Pass    |
| POST /api/account/password_reset/    | 200 OK, email sent                         | 200 OK, email sent                        |   Pass    |
| POST /api/account/password_reset_confirm/ | 200 OK, password updated             | 200 OK, password updated                  |   Pass    |
| POST /api/account/register/          | 201 Created, email sent                    | 201 Created, email sent                   |   Pass    |
| POST /api/account/resend_verification/| 200 OK, email sent                        | 200 OK, email sent                        |   Pass    |
| GET /api/account/verify_email/       | 200 OK, email verified                     | 200 OK, email verified                    |   Pass    |
| GET /api/channels/                   | 200 OK, list of channels                   | 200 OK, list of channels                  |   Pass    |
| POST /api/channels/                  | 201 Created, new channel                   | 201 Created, new channel                  |   Pass    |
| GET /api/channels/{id}/             | 200 OK, channel details                    | 200 OK, channel details                   |   Pass    |
| PUT /api/channels/{id}/             | 200 OK, full update                        | 200 OK, full update                       |   Pass    |
| PATCH /api/channels/{id}/           | 200 OK, partial update                     | 200 OK, partial update                    |   Pass    |
| DELETE /api/channels/{id}/          | 204 No Content, channel deleted            | 204 No Content, channel deleted           |   Pass    |
| GET /api/docs/schema/                | 200 OK, schema returned                    | 200 OK, schema returned                   |   Pass    |
| GET /api/messages/                   | 200 OK, list of messages                   | 200 OK, list of messages                  |   Pass    |
| GET /api/messages/{id}/             | 200 OK, message details                    | 200 OK, message details                   |   Pass    |
| PATCH /api/messages/{id}/           | 200 OK, message updated                    | 200 OK, message updated                   |   Pass    |
| GET /api/servers/                    | 200 OK, list of servers                    | 200 OK, list of servers                   |   Pass    |
| POST /api/servers/                   | 201 Created, new server                    | 201 Created, new server                   |   Pass    |
| GET /api/servers/{id}/              | 200 OK, server details                     | 200 OK, server details                    |   Pass    |
| PUT /api/servers/{id}/              | 200 OK, full update                        | 200 OK, full update                       |   Pass    |
| PATCH /api/servers/{id}/            | 200 OK, partial update                     | 200 OK, partial update                    |   Pass    |
| DELETE /api/servers/{id}/           | 204 No Content, server deleted             | 204 No Content, server deleted            |   Pass    |
| POST /api/servers/{id}/add_member/   | 200 OK, member added                       | 200 OK, member added                      |   Pass    |
| POST /api/servers/{id}/remove_member/| 200 OK, member removed                     | 200 OK, member removed                    |   Pass    |
| POST /api/token/                     | 200 OK, access and refresh tokens returned | 200 OK, access and refresh tokens returned|   Pass    |
| POST /api/token/refresh/            | 200 OK, new access token returned          | 200 OK, new access token returned         |   Pass    |




### Automated tests

Nine unit tests were written for the `contacts` endpoint. These are in `contacts/tests.py`, and all passed:

- Test that the Server administrator can list contacts for their Server.
- Test that a Server member with no admin status in the same Server can list contacts.
- Test that an unauthenticated user cannot list contacts.
- Test that a Server administrator can create a new contact for their Server.
- Test that a Server member without admin status cannot create a new contact.
- Test that an unauthenticated user cannot create a new contact.
- Test that a Server administrator can delete a contact.
- Test that a Server member without admin status cannot delete a contact.
- Test than an unauthenticated user cannot delete a contact.

As well as this all code was written using automated unit test in parallel to enssure that they passed, tests were written to fail the code until the code passed the specific criteria


### Python validation

All files were validated via pep8 standards and came out okay with no critical errors

### Bugs

To date there are no bugs in the backend code, all api endpoints work correctly and the code base is solid and allows the user to acccess the app with no problems

## Deployment
The api is deployed to heroku via github utilizing a redis key value pair package (Heroku key value pair)

TO deploy this app, you must do the following:

- Clone or fork both repos
- Link them to heroku projects
- The frontend repo requires no more setup

for the backend repo you need to get the heroku key value pair package and setup a cloudinary account, you also need a postgres server

- Next set the following environment variables

ALLOWED_HOSTS - Backend heroku app
CLIENT_ORIGIN - Frontend heroku app
CLIENT_ORIGIN_DEV - For testing locally (use ngrok to tunnel)
CLOUDINARY_API_KEY - For image uploading
CLOUDINARY_API_SECRET
CLOUDINARY_CLOUD_NAME
DATABASE_URL - Postgres DB
DISABLE_COLLECTSTATIC - For staticfiles
HOST_EMAIL - For email functionality
HOST_PW
REDIS_URL - For websockets
SECRET_KEY - for signed data transfer

The redis url comes from heroku Key Value pair and is automaitcally set when you add the package

once these are set the app should run out of the box, you will need to create an admin account for admin actions but beyond that a created user account can do all the functions described in the app on the frontend. All endpoints are protected and require credentials from the get go however this can be disabled by removing the isauthenticated permissions from the various serializers and viewsets

## Credits
Credit goes to the various documentation that helped me figure this out:

- [Django documentation](https://www.djangoproject.com)
- [Django Rest Framework documentation](https://www.django-rest-framework.org)
- [django-filter documentation](https://django-filter.readthedocs.io/en/stable/)
- [django-recurrence documentation](https://django-recurrence.readthedocs.io/en/latest/)
- [Python datetime documentation](https://docs.python.org/3/library/datetime.html)
- [dateutil documentation](https://dateutil.readthedocs.io/en/stable/index.html)

As well as very academy for teaching me the basics of websocket setup and communication