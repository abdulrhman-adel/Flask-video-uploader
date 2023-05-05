# Flask Video Uploader

Flask Video Uploader is a simple Flask application that allows users to upload videos to a server using a RESTful API.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Upload videos to a server using a RESTful API
- Verify JWT tokens for authentication
- Limit file types and sizes
- Generate unique file names

## Installation

1. Clone the repository
2. Install dependencies

`$ pip install -r requirements.txt`

3. Create a `database.db` file for the SQLite database.

## Usage

1. Start the application

`$ python app.py`

2. Use the API to upload videos

### Upload a Video

```
POST /upload HTTP/1.1
Host: localhost:5000
Content-Type: multipart/form-data
Authorization: Bearer <JWT token>

<file data>
```

## JWT Authentication

The application uses JSON Web Tokens (JWTs) for authentication. To get a JWT token, send a POST request to the `/auth` endpoint with `a username` and `password` in the request body. The server will respond with a JWT token that can be used to authenticate subsequent requests.

```
POST /auth HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
    "username": "your-username",
    "password": "your-password"
}
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
