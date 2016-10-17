(function main($angular) {

    // Бог тро́ицу лю́бит...
    $angular.module('donutApp', ['ngDonut']).controller('DonutController', function DonutController($scope, $timeout) {

        /**
         * @property selectedModel
         * @type {Object}
         */
        $scope.selectedModel = {};

        /**
         * @method random
         * @return {Number}
         */
        var random = function random() {
            return Math.round(Math.random() * 100);
        };

        /**
         * @method setValues
         * @return {void}
         */
        $scope.setValues = function setValues() {

            $scope.donutModel = [
                { name: 'Adam', value: random() },
                { name: 'Maria', value: random() },
                { name: 'Jonathan', value: random() },
                { name: 'Gabriele', value: random() },
                { name: 'Artem', value: random() }
            ];

        };
        
        /**
         * @property donutModel
         * @type {Array}
         */
        $scope.donutModel = [];

        $timeout(function timeout() {

            // Initialise after a second to simulate an AJAX request.
            $scope.setValues();

        }, 1000);

        /**
         * @method openTooltip
         * @param model {Object}
         * @return {void}
         */
        $scope.openTooltip = function openTooltip(model) {
            $scope.selectedModel = model;
        };

        /**
         * @method closeTooltip
         * @return {void}
         */
        $scope.closeTooltip = function closeTooltip() {
            $scope.selectedModel = {};
        };

        /**
         * @property donutColours
         * @type {String[]}
         */
        // $scope.donutColours = ['red', 'green', 'blue', 'yellow', 'orange'];

    }).directive('tooltip', function tooltipDirective() {

        return {

            /**
             * @property restrict
             * @type {String}
             */
            restrict: 'EA',

            /**
             * @property model
             * @type {Object}
             */
            scope: {
                model: '=ngModel'
            },

            /**
             * @property require
             * @type {String}
             */
            require: 'ngModel',

            /**
             * @property template
             * @type {String}
             */
            templateUrl: 'partials/tooltip.html'

        };

    });

})(window.angular);