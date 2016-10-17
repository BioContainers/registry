// =====================================================================
// Percent Display Directive
//
// Por Walter Staeblein - 2015
// =====================================================================
(function() {

    var pd_app = angular.module('ngPercentDisplay', []);

    pd_app.directive('percentDisplay', function () {       
        return {
            restrict: 'E',
            template:  '<div class="ngpercentdisplay" data-percent="{{ percent }}">' +
                            '<div class="ngperdispleft">' +
                                '<span></span>' +
                            '</div>' +
                            '<div class="ngperdispright">' +
                                '<span></span>' +
                           '</div>' +
                        '</div>',
            scope: { percent: '=' },
            link: function($scope, element, attrs) {  

                var jEle = $(element);
                var leftSide = jEle.find(".ngperdispleft span"),
                    rightSide = jEle.find(".ngperdispright span"),
                    side = attrs.side || 50,
                    fontSize = Math.floor(side / 5);
                    colors = attrs.colors.split(' ');
                var deg, strdeg;

                if (!colors[0]) { colors[0] = '#DADADA'; }
                if (!colors[1]) { colors[1] = '#606060'; }
                if (!colors[2]) { colors[2] = '#FFFFFF'; }

                jEle.find('.ngpercentdisplay').css({ 'width': side, 'height': side, 'font-size': fontSize, 'background-color': colors[0], 'color': colors[1] });
                jEle.find('.ngpercentdisplay span').css({ 'background-color': colors[1] });
                jEle.find('.ngpercentdisplay:before').css({ 'background-color': colors[2] });

                $scope.$watch('percent', function(newvalue, oldvalue){

                    if (newvalue > -1 && newvalue < 101) {
                        if(newvalue <= 50) {
                            // Hide left
                            leftSide.hide();
                            
                            // Adjust right
                            deg = 180 - (newvalue / 100 * 360);
                           	strdeg = "rotateZ(-" + deg + "deg)";
                            rightSide.css({ "transform": strdeg, "-webkit-transform": strdeg, "-moz-transform": strdeg, "msTransform": "rotate(-" + deg + "deg)" });
                        } else {
                            // Adjust left
                            leftSide.show();
                            deg = 180 - ((newvalue - 50) / 100 * 360);
                            strdeg = "rotateZ(-" + deg + "deg)";
                            leftSide.css({ "transform": strdeg, "-webkit-transform": strdeg, "-moz-transform": strdeg, "msTransform": "rotate(-" + deg + "deg)" });
                            rightSide.css({ "transform": "rotateZ(0deg)", "-webkit-transform": "rotateZ(0deg)", "-moz-transform": "rotateZ(0deg)", "msTransform": "rotate(0deg)"  });
                        }
                    }
                });
            }
        }
    });
} ());
