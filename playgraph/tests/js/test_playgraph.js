describe('requestService', function () {
    'use strict';

    var RequestService, $httpBackend;
    var completeUser = {
        name: 'gamer',
        avatar_link: '//link.jpg',
        plays: [{
            name: 'some game',
            quantity: 3,
            date: '2016-01-01'
        }]
    }
    function getMockCallbacks() {
        var cbValue = undefined;
        return {
            callback: jasmine.createSpy('callback').and.callFake(function (data) { cbValue = data; }),
            errback: jasmine.createSpy('errback'),
            cbValue: function () { return cbValue; }
        };
    };

    beforeEach(function () {
        module('PlayGraph');
        inject(function (_$httpBackend_, _RequestService_) {
            RequestService = _RequestService_;
            $httpBackend = _$httpBackend_;
        });
    });

    it('initializes', function () {
        expect(RequestService.get).toBeDefined();
    });

    it('calls callback on successful call', function () {
        var callbacks = getMockCallbacks()
        $httpBackend.expectGET('plays/user').respond(completeUser);
        RequestService.get('user', undefined, callbacks.callback, callbacks.errback)
        $httpBackend.flush();
        expect(callbacks.callback).toHaveBeenCalled();
        expect(callbacks.errback).not.toHaveBeenCalled();
    });

    it('calls callback on successful refresh call', function () {
        var callbacks = getMockCallbacks()
        $httpBackend.expectGET('plays/user?refresh=1').respond(completeUser);
        RequestService.get('user', true, callbacks.callback, callbacks.errback)
        $httpBackend.flush();
        expect(callbacks.callback).toHaveBeenCalled();
        expect(callbacks.errback).not.toHaveBeenCalled();
    });
});

describe('SummaryService', function () {
    'use strict';

    var SummaryService
    beforeEach(function () {
        module('PlayGraph');
        inject(function (_SummaryService_) {
            SummaryService = _SummaryService_;
        });
    });

    it('initializes', function () {
        expect(SummaryService.frequencyArray).toBeDefined();
    });

    it('summarizes collection', function () {
        var collection = [{name: 'a', quantity: 5}, {name: 'a', quantity: 3}, {name: 'b', quantity: 6}, {name: 'c', quantity: 3}];
        var expected = [{name:'a', quantity: 8, rank: 1}, {name: 'b', quantity: 6, rank: 2}, {name: 'c', quantity: 3, rank: 3}]
        expect(SummaryService.frequencyArray(collection)).toEqual(expected);
    });

    it('assigns tie ranks', function () {
        var collection = [{name: 'a', quantity: 3}, {name: 'a', quantity: 3}, {name: 'b', quantity: 6}, {name: 'c', quantity: 3}];
        var expected = [{name:'a', quantity: 6, rank: 1}, {name: 'b', quantity: 6, rank: 1}, {name: 'c', quantity: 3, rank: 3}]
        expect(SummaryService.frequencyArray(collection)).toEqual(expected);
    })
});

describe('')