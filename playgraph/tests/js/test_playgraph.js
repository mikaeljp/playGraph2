describe('requestService', function () {
    'use strict';

    var RequestService;

    beforeEach(function () {
        module('PlayGraph');
        inject(function (_RequestService_) {
            RequestService = _RequestService_;
        });
    });

    it('initializes', function () {
        expect(RequestService.get).toBeDefined();
    })
});