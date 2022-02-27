/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://coffe-shop-api:5000', // the running FLASK api server url
  auth0: {
    url: 'testmacina.eu', // the auth0 domain prefix
    audience: 'id_access', // the audience set for the auth0 app
    clientId: 'P9jUymMTPa9sfYVjpjNDUyrfYX9gVpkU', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
