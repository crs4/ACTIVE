/* oauth-ng - v0.3.8 - 2015-02-06 */

'use strict';

// App libraries
var app = angular.module('oauth', [
  'oauth.directive',      // login directive
  'oauth.accessToken',    // access token service
  'oauth.endpoint',       // oauth endpoint service
  'oauth.profile',        // profile model
  'oauth.interceptor'     // bearer token interceptor
]);

angular.module('oauth').config(['$locationProvider','$httpProvider',
  function($locationProvider, $httpProvider) {
    $httpProvider.interceptors.push('ExpiredInterceptor');
  }]);

'use strict';

var accessTokenService = angular.module('oauth.accessToken', ['ngStorage']);

accessTokenService.factory('AccessToken', function($rootScope, $location, $sessionStorage, $interval){

    var service = {
            token: null
        },
        oAuth2HashTokens = [ //per http://tools.ietf.org/html/rfc6749#section-4.2.2
            'access_token', 'token_type', 'expires_in', 'scope', 'state',
            'error', 'error_description'
        ];

    /**
     * Returns the access token.
     */
    service.get = function(){
        return this.token;
    };

    /**
     * Sets and returns the access token. It tries (in order) the following strategies:
     * - takes the token from the fragment URI
     * - takes the token from the sessionStorage
     */
    service.set = function(){
        this.setTokenFromString($location.hash());

        //If hash is present in URL always use it, cuz its coming from oAuth2 provider redirect
        if(null === service.token){
            setTokenFromSession();
        }

        return this.token;
    };

    /**
     * Delete the access token and remove the session.
     * @returns {null}
     */
    service.destroy = function(){
        delete $sessionStorage.token;
        this.token = null;
        return this.token;
    };


    /**
     * Tells if the access token is expired.
     */
    service.expired = function(){
        return (this.token && this.token.expires_at && this.token.expires_at<new Date());
    };


    /**
     * Get the access token from a string and save it
     * @param hash
     */
    service.setTokenFromString = function(hash){
        var params = getTokenFromString(hash);

        if(params){
            removeFragment();
            setToken(params);
            setExpiresAt();
            $rootScope.$broadcast('oauth:login', service.token);
        }
    };

   
    /* * * * * * * * * *
     * PRIVATE METHODS *
     * * * * * * * * * */
   
    /**
     * Set the access token from the sessionStorage.
     */
    var setTokenFromSession = function(){
        if($sessionStorage.token){
            var params = $sessionStorage.token;
            params.expires_at = new Date(params.expires_at);
            setToken(params);
        }
    };

    /**
     * Set the access token.
     *
     * @param params
     * @returns {*|{}}
     */
    var setToken = function(params){
        service.token = service.token || {};      // init the token
        angular.extend(service.token, params);      // set the access token params
        setTokenInSession();                // save the token into the session
        setExpiresAtEvent();                // event to fire when the token expires

        return service.token;
    };

    /**
     * Parse the fragment URI and return an object
     * @param hash
     * @returns {{}}
     */
    var getTokenFromString = function(hash){
        var params = {},
            regex = /([^&=]+)=([^&]*)/g,
            m;

        while (m = regex.exec(hash)) {
            params[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
        }

        if(params.access_token || params.error){
            return params;
        }
    };

    /**
     * Save the access token into the session
     */
    var setTokenInSession = function(){
        $sessionStorage.token = service.token;
    };

    /**
     * Set the access token expiration date (useful for refresh logics)
     */
    var setExpiresAt = function(){
        if(service.token){
            var expires_at = new Date();
            expires_at.setSeconds(expires_at.getSeconds() + parseInt(service.token.expires_in) - 60); // 60 seconds less to secure browser and response latency
            service.token.expires_at = expires_at;
        }
    };


    /**
     * Set the timeout at which the expired event is fired
     */
    var setExpiresAtEvent = function(){
        var time = (new Date(service.token.expires_at))-(new Date());
        if(time){
            $interval(function(){
                $rootScope.$broadcast('oauth:expired', service.token)
            }, time, 1)
        }
    };

    /**
     * Remove the oAuth2 pieces from the hash fragment
     */
    var removeFragment = function(){
        var curHash = $location.hash();
        angular.forEach(oAuth2HashTokens,function(hashKey){
            var re = new RegExp('&'+hashKey+'(=[^&]*)?|^'+hashKey+'(=[^&]*)?&?');
            curHash = curHash.replace(re,'');
        });

        $location.hash(curHash);
    };


    return service;
});

'use strict';

var endpointClient = angular.module('oauth.endpoint', []);

endpointClient.factory('Endpoint', function(AccessToken, $location) {

  var service = {};
  var url;


  /*
   * Defines the authorization URL
   */

  service.set = function(params) {
    var oAuthScope = (params.scope) ? params.scope : '',
        state = (params.state) ? encodeURIComponent(params.state) : '',
        authPathHasQuery = (params.authorizePath.indexOf('?') == -1) ? false : true,
        appendChar = (authPathHasQuery) ? '&' : '?';    //if authorizePath has ? already append OAuth2 params

    url = params.site +
          params.authorizePath +
          appendChar + 'response_type=' + params.responseType + '&' +
          'client_id=' + encodeURIComponent(params.clientId) + '&' +
          'redirect_uri=' + encodeURIComponent(params.redirectUri) + '&' +
          'scope=' + oAuthScope + '&' +
          'state=' + state;

    return url;
  };

  /*
   * Returns the authorization URL
   */

  service.get = function() {
    return url;
  };


  /*
   * Redirects the app to the authorization URL
   */

  service.redirect = function() {
    window.location.replace(url);
  };

  return service;
});

'use strict';

var profileClient = angular.module('oauth.profile', [])

profileClient.factory('Profile', function($http, AccessToken, $rootScope) {
  var service = {};
  var profile;

  service.find = function(uri) {
    var promise = $http.get(uri, { headers: headers() });
    promise.success(function(response) {
        profile = response;
        $rootScope.$broadcast('oauth:profile', profile);
    });
    return promise;
  };

  service.get = function(uri) {
    return profile;
  };

  service.set = function(resource) {
    profile = resource;
    return profile;
  };

  var headers = function() {
    return { Authorization: 'Bearer ' + AccessToken.get().access_token };
  };

  return service;
});

'use strict';

var interceptorService = angular.module('oauth.interceptor', []);

interceptorService.factory('ExpiredInterceptor', function ($rootScope, $q, $sessionStorage) {

  var service = {};

  service.request = function(config) {
    var token = $sessionStorage.token;

    if (token && expired(token))
      $rootScope.$broadcast('oauth:expired', token);

    return config;
  };

  var expired = function(token) {
    return (token && token.expires_at && new Date(token.expires_at) < new Date())
  };

  return service;
});

'use strict';

var directives = angular.module('oauth.directive', []);

directives.directive('oauth', function(AccessToken, Endpoint, Profile, $location, $rootScope, $compile, $http, $templateCache) {

  var definition = {
    restrict: 'AE',
    replace: true,
    scope: {
      site: '@',          // (required) set the oauth server host (e.g. http://oauth.example.com)
      clientId: '@',      // (required) client id
      redirectUri: '@',   // (required) client redirect uri
      responseType: '@',  // (optional) response type, defaults to token (use 'token' for implicit flow and 'code' for authorization code flow
      scope: '@',         // (optional) scope
      profileUri: '@',    // (optional) user profile uri (e.g http://example.com/me)
      template: '@',      // (optional) template to render (e.g bower_components/oauth-ng/dist/views/templates/default.html)
      text: '@',          // (optional) login text
      authorizePath: '@', // (optional) authorization url
      state: '@'          // (optional) An arbitrary unique string created by your app to guard against Cross-site Request Forgery
    }
  };

  definition.link = function postLink(scope, element, attrs) {
    scope.show = 'none';

    scope.$watch('clientId', function(value) { init() });

    var init = function() {
      initAttributes();          // sets defaults
      compile();                 // compiles the desired layout
      Endpoint.set(scope);       // sets the oauth authorization url
      AccessToken.set(scope);    // sets the access token object (if existing, from fragment or session)
      initProfile(scope);        // gets the profile resource (if existing the access token)
      initView();                // sets the view (logged in or out)
    };

    var initAttributes = function() {
      scope.authorizePath = scope.authorizePath || '/oauth/authorize';
      scope.tokenPath     = scope.tokenPath     || '/oauth/token';
      scope.template      = scope.template      || '/assets/js/core/views/templates/default.html';//'bower_components/oauth-ng/dist/views/templates/default.html';
      scope.responseType  = scope.responseType  || 'token';
      scope.text          = scope.text          || 'Sign In';
      scope.state         = scope.state         || undefined;
      scope.scope         = scope.scope         || undefined;
    };

    var compile = function() {
      $http.get(scope.template, { cache: $templateCache }).success(function(html) {
        element.html(html);
        $compile(element.contents())(scope);
      });
    };

    var initProfile = function(scope) {
      var token = AccessToken.get();

      if (token && token.access_token && scope.profileUri) {
        Profile.find(scope.profileUri).success(function(response) {
          scope.profile = response
        })
      }
    };

    var initView = function() {
      var token = AccessToken.get();

      if (!token)             { return loggedOut()  }  // without access token it's logged out
      if (token.access_token) { return authorized() }  // if there is the access token we are done
      if (token.error)        { return denied()     }  // if the request has been denied we fire the denied event
    };

    scope.login = function() {
      Endpoint.redirect();
    };

    scope.logout = function() {
      AccessToken.destroy(scope);
      $rootScope.$broadcast('oauth:logout');
      loggedOut();
    };

    scope.$on('oauth:expired', function() {
      AccessToken.destroy(scope);
      scope.show = 'logged-out';
    });

    // user is authorized
    var authorized = function() {
      $rootScope.$broadcast('oauth:authorized', AccessToken.get());
      scope.show = 'logged-in';
    };

    // set the oauth directive to the logged-out status
    var loggedOut = function() {
      $rootScope.$broadcast('oauth:loggedOut');
      scope.show = 'logged-out';
    };

    // set the oauth directive to the denied status
    var denied = function() {
      scope.show = 'denied';
      $rootScope.$broadcast('oauth:denied');
    };

    // Updates the template at runtime
    scope.$on('oauth:template:update', function(event, template) {
      scope.template = template;
      compile(scope);
    });

    // Hack to update the directive content on logout
    // TODO think to a cleaner solution
    scope.$on('$routeChangeSuccess', function () {
      init();
    });
  };

  return definition
});
