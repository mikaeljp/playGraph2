(function () {
    'use strict';
    angular.module('PlayGraph', []).config(function ($interpolateProvider, $httpProvider) {
        // Change symbols from {{  }} -> [[  ]]
        $interpolateProvider.startSymbol('[[').endSymbol(']]');

        // Provide support for Django's csrf form security
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }).factory('RequestService', [
        '$http',
        function ($http) {
            return {
                get: function (username, refresh, callback, errback) {
                    var url = username;
                    if (refresh) { url = url + '?refresh=1'; }
                    $http.get(url)
                        .success(function (response) { callback(response); })
                        .error(function (response) { console.log(response); });
                }
            }
        }
    ]).controller('BGGRequestController', [
        'RequestService',
        function (RequestService) {
            var vm = this;
            vm.bggUsername = 'mikaeljp';
            vm.submitRequest = submitRequest;

            function updateBggUserData(data) {
            console.log(data)
                vm.user = data;
            }

            function submitRequest(refresh) {
                if (vm.bggUsername) {
                    RequestService.get(vm.bggUsername, refresh, updateBggUserData);
                }
            }

        }
    ])
})();