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
    ]).factory('SummaryService', [
        function () {
            function byElementQuantity(left, right) {
                return right.quantity - left.quantity;
            }
            function setArrayRank(items, limit) {
                // given a sorted list of items that have a quantity attribute
                // set the rank attribute of each element to its position in the list according to its quantity
                // in the event of a tie the rank is the same for all tied items
                // ex: [qty: 10, qty: 9, qty: 9, qty: 4] -> [rank: 1, rank: 2, rank: 2, rank: 4]
                var rank = 1,
                    position,
                    last = items[0].quantity + 1,
                    ranked = [],
                    item;
                for (position = 0; position < items.length; position += 1) {
                    item = items[position]
                    if (last != item.quantity) {
                        // the quantity of this item does not match the previous item, set rank to the position
                        rank = position + 1;
                    }
                    if (rank > limit) break;
                    last = item.quantity;
                    item.rank = rank;
                    ranked.push(item);
                }
                console.log(ranked);
                return ranked;
            }
            return {
                frequencyArray(plays, limit) {
                    // Condense the items into an array without duplicates, order by quantity then return an array
                    // with the most frequent elements up to the limit number of elements
                    var games = {},
                        summary = [];
                    plays.forEach(function (play) {
                        if (games.hasOwnProperty(play.name)) {
                            games[play.name].quantity += play.quantity;
                        } else {
                            games[play.name] = play;
                        }
                    });
                    // Take the condensed dictionary of games and set the values in a list then sort by quantity
                    for (var key in games) { summary.push(games[key]); }
                    summary.sort(byElementQuantity);

                    return setArrayRank(summary, limit);
                }
            }
        }
    ]).controller('BGGRequestController', [
        'RequestService',
        'SummaryService',
        function (RequestService, SummaryService) {
            var vm = this;
            vm.bggUsername = 'mikaeljp';
            vm.submitRequest = submitRequest;

            function updateBggUserData(data) {
                vm.user = data;
                vm.playSummary = SummaryService.frequencyArray(data.plays, 10);
            }

            function submitRequest(refresh) {
                if (vm.bggUsername) {
                    RequestService.get(vm.bggUsername, refresh, updateBggUserData);
                }
            }

        }
    ])
})();