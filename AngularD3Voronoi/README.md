#AngularD3Voronoi

This project consists of a CoffeeScript-based AngularJS directive that is used
to render a ["Voronoi" tesselation](https://github.com/mbostock/d3/wiki/Voronoi-Geom)
from D3. It takes the attribute `vertices` as an input via the way the AngularJS
bindings have been specified. The following code-snippets contain potential implementation
steps to incorporate this functionality into code in the most efficient way possible.

This guide assumes that the reader has a working knowledge of AngularJS.

**A)** A sample implementation of this directive which can be used in a given view is:

```
<div>
<voronoi vertices="{{data}}" width="960" height="500"></voronoi>
</div>
```

To include this directive in an AngularJS controller, the CoffeeScript will need
to be compiled into Javascript first. `grunt` was used to compile this during
testing and development.

**B)** A sample implementation of an AngularJS application that contains this directive
would look something like:

```
'use strict';

/**
 * @ngdoc overview
 * @name AngularApp
 * @description
 * # AngularApp
 *
 * Main module of the application.
 */
angular
  .module('AngularApp', [
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'AngularD3Voronoi'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
```

**C)** The controller `MainCtrl` would be implemented similarly to this:

```
'use strict';

/**
 * @ngdoc function
 * @name AngularApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the AngularApp
 */
angular.module('AngularApp')
  .controller('MainCtrl', [ '$scope' ,  function ($scope) {
    $scope.data =  d3.range(100).map(function(d) {
    	   return [Math.random() * 960, Math.random() * 500];
     });
 }]);
```

As is apparent, the `data` variable above is set as a property of the controller's `$scope`
object. The values created via the `d3.range(100).map()` call in turn are bound to the attribute `vertices` in the directive above (ref. 'A').
