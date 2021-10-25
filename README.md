# Hello World API: Flask Auth0 Sample

This sample uses Auth0 along with [PyJWT](https://github.com/jpadilla/pyjwt) to protect endpoints in a Flask API server.

The `add-authorization` branch offers a working API server that exposes a public endpoint along with two protected endpoints. Each endpoint returns a different type of message: public, protected, and admin.

The `GET /api/messages/protected` and `GET /api/messages/admin` endpoints are protected against unauthorized access. Any requests that contain a valid access token in their authorization header can access the protected and admin data.

However, you should require that only access tokens that contain a `read:admin-messages` permission can access the admin data, which is referred to as [Role-Based Access Control (RBAC)](https://auth0.com/docs/authorization/rbac/).

## Get Started

### Create a virtual environment

Create a virtual environment under the root project directory:

**macOS/Linux:**

```bash
python3 -m venv venv
```

**Windows:**

```bash
py -3 -m venv venv
```

Activate the virtual environment:

**macOS/Linux:**

```bash
. venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### Install the project dependencies

Execute the following command to install the project dependencies:

```bash
pip install -r requirements.txt
```

### Register a Flask API with Auth0

- Open the [APIs](https://manage.auth0.com/#/apis) section of the Auth0 Dashboard.

- Click on the **Create API** button.

- Provide a **Name** value such as _Hello World API Server_.

- Set its **Identifier** to `https://hello-world.example.com` or any other value of your liking.

- Leave the signing algorithm as `RS256` as it's the best option from a security standpoint.

- Click on the **Create** button.

> View ["Register APIs" document](https://auth0.com/docs/get-started/set-up-apis) for more details.

### Connect Flask with Auth0

Create a `.env` file under the root project directory and populate it with the following content:

```bash
CLIENT_ORIGIN_URL=http://localhost:4040
AUTH0_AUDIENCE=https://hello-world.example.com
AUTH0_DOMAIN=
```

Get the values for `AUTH0_AUDIENCE` and `AUTH0_DOMAIN` in `.env` from your Auth0 API registration page in the Dashboard.

Head back to your Auth0 API page, and **follow these steps to get the Auth0 Audience**:

![Get the Auth0 Audience to configure an API](https://cdn.auth0.com/blog/complete-guide-to-user-authentication/get-the-auth0-audience.png)

1. Click on the **"Settings"** tab.

2. Locate the **"Identifier"** field and copy its value.

3. Paste the "Identifier" value as the value of `AUTH0_AUDIENCE` in `.env`.

Now, **follow these steps to get the Auth0 Domain value**:

![Get the Auth0 Domain to configure an API](https://cdn.auth0.com/blog/complete-guide-to-user-authentication/get-the-auth0-domain.png)

1. Click on the **"Test"** tab.
2. Locate the section called **"Asking Auth0 for tokens from my application"**.
3. Click on the **cURL** tab to show a mock `POST` request.
4. Copy your Auth0 domain, which is _part_ of the `--url` parameter value: `tenant-name.region.auth0.com`.
5. Paste the Auth0 domain value as the value of `AUTH0_DOMAIN` in `.env`.

**Tips to get the Auth0 Domain**

- The Auth0 Domain is the substring between the protocol, `https://` and the path `/oauth/token`.

- The Auth0 Domain follows this pattern: `tenant-name.region.auth0.com`.

- The `region` subdomain (`au`, `us`, or `eu`) is optional. Some Auth0 Domains don't have it.

### Run the Flask API Server

Run the project in development mode:

```bash
flask run
```

## Set Up Role-Based Access Control with Auth0

The `GET /api/messages/admin` endpoint requires the access token to contain the `read:admin-messages` permission. The best way to simulate that client-server secured request is to use any of the compatible Hello World client apps to log in as a user that has that permission.

You can use the Auth0 Dashboard to create an `admin` role and assign it the `read:admin-messages` permission. Then, you can assign the `admin` role to any user that you want to access the `/admin` endpoint.

If you need help doing so, check out the following resources:

- [Create roles](https://auth0.com/docs/authorization/rbac/roles/create-roles)

- [Create permissions](https://auth0.com/docs/get-started/dashboard/add-api-permissions)

- [Add permissions to roles](https://auth0.com/docs/authorization/rbac/roles/add-permissions-to-roles)

- [Assign roles to users](https://auth0.com/docs/users/assign-roles-to-users)

## API Endpoints

The API server defines the following endpoints:

### 🔓 Get public message

```bash
GET /api/messages/public
```

#### Response

```bash
Status: 200 OK
```

```json
{
  "message": "The API doesn't require an access token to share this message."
}
```

### 🔓 Get protected message

> You need to protect this endpoint using Auth0.

```bash
GET /api/messages/protected
```

#### Response

```bash
Status: 200 OK
```

```json
{
  "message": "The API successfully validated your access token."
}
```

### 🔓 Get admin message

> You need to protect this endpoint using Auth0 and Role-Based Access Control (RBAC).

```bash
GET /api/messages/admin
```

#### Response

```bash
Status: 200 OK
```

```json
{
  "message": "The API successfully recognized you as an admin."
}
```

## Error Handling

### 400s errors

#### Response

```bash
Status: Corresponding 400 status code
```

```json
{
  "message": "Message that describes the error that took place."
}
```

### 500s errors

#### Response

```bash
Status: 500 Internal Server Error
```

```json
{
  "message": "Message that describes the error that took place."
}
```