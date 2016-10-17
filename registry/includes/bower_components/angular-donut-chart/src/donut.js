// Take a <chart-donut title="Foo" data="obj.percentage" color="#fff"></chart-donut>
// and transform it into a d3-d svg chart like:
// <svg>
//   <g>
//     <path d="" transform="translate(to center)" />
//   </g>
// </svg>

angular.module('chart.donut', [])

.constant('chartDonutConfig', {
    pathColor: '5a8e2f',
    strokeColor: '#a39d8c',
    bgFillColor: '#f2f0d6',
    punchoutFillColor: '#f1e0af',
    punchoutStrokeColor: '#d2c194'
})

.directive('chartDonut', ['chartDonutConfig', function(config) {
    'use strict';
    return {
        restrict: 'EA',
        scope: {
            data: '=',
            title: '@',
            color: '@',
            size: '@',
            symbol: '@'
        },
        link: function(scope, element, attrs) {
            var symbol = attrs.symbol || '%';
            var size = attrs.size || element[0].clientWidth;
            var color = attrs.color || config.pathColor;
            var ringSize = size / 20;
            var outer = size / 4;

            var transform = function(x, y) {
                return 'translate('+x+','+y+')';
            };

            if (typeof d3 !== 'object') {
                throw new Error('"chart.donut" requires a global d3 object');
            }
            var scale = d3.scale.linear().domain([0, 100]).range([0, 2 * Math.PI]);

            var transformDown = (size / 4) + ringSize + 1;
            var centerTransform = transform(transformDown, transformDown);

            var width = transformDown * 2;
            var height = scope.title ? size : width;
            var svg = d3.select(element[0])
                .append('svg')
                .style({
                    height: size,
                    width: transformDown * 2
                });

            var drawArc = function(inner, outer, start, end) {
                var a =  d3.svg.arc()
                    .innerRadius(inner).outerRadius(outer)
                    .startAngle(scale(start));
                if (typeof end !== 'undefined') {
                    a.endAngle(end);
                }
                return a;
            };

            var outerBounds = outer + ringSize;

            var background = svg.append('circle').attr({
                'class': 'background',
                fill: config.bgFillColor,
                stroke: config.strokeColor,
                r: config.outerBounds,
                transform: config.centerTransform
            });

            var middleLayer = svg.append('g').attr({transform: centerTransform});
            var topLayer = svg.append('g').attr({transform: centerTransform});

            var punchOut = middleLayer.append('path').attr({
                'class': 'punch-out',
                fill: config.punchoutFillColor,
                stroke: config.punchoutStrokeColor,
                d: drawArc(outer - ringSize, outer, 0, 100)
            });

            if (scope.title) {
                var dropPin = svg.append('g').attr({
                    transform: centerTransform,
                    'class': 'drop-pin'
                });
                var cy = outerBounds * 1.3;
                var r = outerBounds / 20;
                dropPin.append('line').attr({
                    x1: 0,
                    y1: outerBounds,
                    x2: 0,
                    y2: cy,
                    stroke: config.strokeColor
                });
                dropPin.append('circle').attr({
                    fill: config.strokeColor,
                    cx: 0,
                    cy: cy,
                    r: r
                });
                dropPin.append('text').attr({
                    y: cy + r,
                    'alignment-baseline': 'hanging',
                    'text-anchor': 'middle'
                }).text(scope.title);
            }

            topLayer.append('circle').attr({
                fill: config.bgFillColor,
                stroke: '#f9f9ec',
                r: outer - ringSize
            });

            var textLabel = topLayer.append('text').attr({
                transform: transform(0, 5),
                'text-anchor': 'middle'
            });


            var arc = drawArc(outer - ringSize, outer - 0.5, 0);
            var path = middleLayer.append('path')
                .datum({endAngle: 0})
                .attr({
                    fill: '#' + color,
                    d: arc
                });

            var arcTween = function(transition, newAngle) {
                transition.attrTween('d', function(d) {
                    var interpolate = d3.interpolate(d.endAngle, scale(newAngle));
                    return function(t) {
                        d.endAngle = interpolate(t);
                        return arc(d);
                    };
                });
            };

            scope.render = function(data, tweenTime) {
                path.transition()
                    .duration(tweenTime || 750)
                    .call(arcTween, data);
                textLabel.text(data + symbol);
            };

            scope.$watch('data', function(newVal, oldVal) {
                if (newVal !== oldVal) {
                    scope.render(newVal);
                }
            });

            if (scope.data) scope.render(scope.data, 250);
        }
    };
}]);
