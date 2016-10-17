(function main($angular, $d3) {

	"use strict";

	/**
	 * @method throwException
	 * @param message {String}
	 * @return {void}
	 */
	var throwException = function throwException(message) {
		throw "ngDonut: " + message;
	};

	if (typeof $angular === 'undefined') {
		throwException('Angular is a required library: https://angularjs.org/');
	}

	if (typeof $d3 === 'undefined') {
		throwException('D3 is a required library: http://d3js.org/');
	}

	/**
	 * @module ngDonut
	 * @author Adam Timberlake
	 * @link https://github.com/Wildhoney/ngDonut
	 */
	$angular.module('ngDonut', []).directive('donut', function ngDonut() {

		return {

			/**
			 * @property restrict
			 * @type {String}
			 */
			restrict: 'EA',

			/**
			 * @property require
			 * @type {String}
			 */
			require: 'ngModel',

			/**
			 * @property scope
			 * @type {Object}
			 */
			scope: {
				dataset: '=ngModel',
				height: '=',
				width: '=',
				radius: '=',
				colours: '=',
				property: '=',
				stroke: '=',
				strokeWidth: '=',
				mousemove: '&',
				mouseleave: '&'
			},

			/**
			 * @property controller
			 * @type {Array}
			 */
			controller: ['$scope', function controller($scope) {

				/**
				 * @property colour
				 * @type {Function}
				 */
				var colour = $d3.scale.category20();

				/**
				 * @property currentAngles
				 * @type {Object}
				 */
				$scope.currentAngles = {};

				/**
				 * @method getColour
				 * @param colourIndex {Number}
				 * @return {String}
				 */
				$scope.getColour = function getColour(colourIndex) {

					// Use the user defined colours if the developer has defined them, and the current index
					// is available.
					if ($scope.colours && $scope.colours.length > colourIndex) {
						return $scope.colours[colourIndex];
					}

					// ...Otherwise we'll fallback to using the D3 category 20 colours.
					return colour(colourIndex);

				};

				/**
				 * @method getTranslate
				 * @return {String}
				 */
				$scope.getTranslate = function getTranslate() {
					return 'translate(' + $scope.getWidth() / 2 + ',' + $scope.getHeight() / 2 + ')';
				};

				/**
				 * @method getWidth
				 * @return {Number}
				 */
				$scope.getWidth = function getWidth() {
					return $scope.width || 400;
				};

				/**
				 * @method getHeight
				 * @return {Number}
				 */
				$scope.getHeight = function getHeight() {
					return $scope.height || 400;
				};

				/**
				 * @method getRadius
				 * @return {Number}
				 */
				$scope.getRadius = function getRadius() {
					return $scope.radius || (Math.min($scope.getWidth(), $scope.getHeight()) / 2);
				};

				/**
				 * @method clean
				 * @param dataset {Array}
				 * @return {Array}
				 */
				$scope.clean = function clean(dataset) {

					return dataset.map(function map(value) {

						if ($scope.property) {

							if (isNaN(Number(value[$scope.property]))) {
								value[$scope.property] = 0;
							} else {
								value[$scope.property] = Number(value[$scope.property]);
							}

							return value;

						}

						if (isNaN(Number(value))) {
							return 0;
						}

						return Number(value);

					});

				};

				/**
				 * @method tweenArc
				 * @param a
				 * @return {Function}
				 */
				$scope.tweenArc = function tweenArc(a) {

					var arc = d3.svg.arc().innerRadius($scope.getRadius() - 100).outerRadius($scope.getRadius() - 20),
						i   = d3.interpolate(this._current, a);

					this._current = i(0);

					return function donutTween(t) {
						return arc(i(t));
					};

				};

				/**
				 * Computes the pointer relative to the container, rather than D3's approach of being
				 * relative to the centre point of the container.
				 *
				 * @method computePointer
				 * @param context {Object}
				 * @return {Array}
				 */
				$scope.computePointer = function computePointer(context) {

					var mouse = $d3.mouse(context);

					var x = mouse[0] + ($scope.getWidth() / 2),
						y = mouse[1] + ($scope.getHeight() / 2);

					return [x, y];

				};

				/**
				 * @method listenForEvents
				 * @param path {Object}
				 * @return {void}
				 */
				$scope.listenForEvents = function listenForEvents(path) {

					if ($scope.mousemove) {

						path.on('mousemove', function onMouseMove(event) {

							var model     = event.data;
							model.pointer = $scope.computePointer(this);

							// Listen for the user hovering over the arcs.
							$scope.mousemove({ model: event.data });
							$scope.$apply();

						});

					}

					if ($scope.mouseleave) {

						path.on('mouseleave', function onMouseLeave() {

							// Listen for when the user leaves the arcs.
							$scope.mouseleave({ pointer: $scope.computePointer(this) });
							$scope.$apply();

						});

					}

				};

			}],

			/**
			 * @method link
			 * @param scope {Object}
			 * @param element {angular.element}
			 * @return {void}
			 */
			link: function link(scope, element) {

				var radius, pie, arc, svg, path;

				/**
				 * @method createDonut
				 * @return {void}
				 */
				scope.createDonut = function createDonut() {

					radius = Math.min(scope.getWidth(), scope.getHeight()) / 2;
					pie    = $d3.layout.pie().sort(null).value(function value(model) {
							return scope.property ? model[scope.property] : model;
					});
					arc    = $d3.svg.arc().innerRadius(radius).outerRadius(radius - scope.getRadius());
					svg    = $d3.select(element[0]).append('svg')
							.attr('width', scope.getWidth())
							.attr('height', scope.getHeight())
							.append('g')
							.attr('transform', scope.getTranslate());
					path = svg.selectAll('path')
							.data(pie(scope.clean(scope.dataset)))
							.enter().append('path')
							.attr('fill', function(d, i) { return scope.getColour(i); })
							.attr('d', arc)
							.each(function(d) { this._current = d; });

					// Listen for the mouse events!
					scope.listenForEvents(path);

					if (scope.stroke) {
						path.attr('stroke', scope.stroke);
					}

					if (scope.strokeWidth) {
						path.attr('stroke-width', scope.strokeWidth)
					}

				};

				/**
				 * @method tweenArc
				 * @param arcModel {Object}
				 * @return {Function}
				 */
				scope.tweenArc = function tweenArc(arcModel) {

					var i = $d3.interpolate(this._current, arcModel);
					this._current = i(0);
					return function(t) {
						return arc(i(t));
					};

				};

				// Listen for any changes to the dataset...
				scope.$watch('dataset', function datasetChanged() {

					if (scope.dataset.length === 0) {
						return;
					}

					if (!pie) {

						// Create the donut shape as we have the data.
						scope.createDonut();
						return;

					}

					// Otherwise it's an update as we have an existing donut.
					path.data(pie(scope.clean(scope.dataset)));
					path.transition().duration(750).attrTween('d', scope.tweenArc);

				}, true);

			}

		};

	});

})(window.angular, window.d3);