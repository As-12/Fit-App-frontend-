# FitApp API Front End

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Description

This is a simple implementation of a Fitness tracking application, a tool that helps visualize and track your weight loss progress.

## API Documentation can be accessed here

[https://fit-app-tc.herokuapp.com](https://fit-app-tc.herokuapp.com/)

![FitApp](banner.gif)

# Technology Stack

- Angular 9
- Chartist + Bootstrap Material Design

## Getting Started

### Installing Dependencies

#### NPM

Follow instructions to install the latest version of npm package manager for your platform in the [npm docs](https://docs.npmjs.com/cli/install)

#### NPM Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
npm install
```

This will install all of the required packages we selected within the `package.json` file.

### Setting environment variables

For production deployment, please ensure that you set the backend API to your deployed API server

```
src/environments/environment.prod.ts
```

```
export const environment = {
  production: true,
  AppUrl: "https://my-api-server.com",
};
```

If the front-end is served on a different domain, ensure that you have a CORS configuration set correctly in the API server.

### Auth setup

Since the endpoints are secured by using Auth0 as an identity provider. The front-end must authenticate the user and attach bearer token to every request through Angular HTTP interceptor.

The Auth can be configured by setting the client id and API audience accordingly in

```
/src/app/auth/AuthService.tx
```

```
auth0Client$ = (from(
    createAuth0Client({
      domain: "{AUTH0_PREFIX}.auth0.com",
      client_id: "{CLIENT_ID}",
      redirect_uri: `${window.location.origin}`,
      audience: "{API_AUDIENCE}",
    })
```

```
logout() {
    // Ensure Auth0 client instance exists
    this.auth0Client$.subscribe((client: Auth0Client) => {
      // Call method to log out
      client.logout({
        client_id: "{CLIENT_ID}",
        returnTo: window.location.origin,
      });
    });
  }
```

### Running the server

The server can be executed by running this command.

```bash
ng serve
```

By default the application should be listening for request on localhost:4200

Please refers to Angular documentation for other operating system configuration. The environment variable should be set accordingly.

## License

MIT License. See [LICENSE.md](LICENSE.md)

## Attribution

https://freeicons.io/ - for various royalty free SVG icons

https://www.videvo.net/video/young-boxer-training-with-coach-2/452776 - Homepage Boxing video

https://www.creative-tim.com/ - Free Angular UI Themes
