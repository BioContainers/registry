/*
 * Copyright 2014 Works Applications Co., Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

var DOCKERHUB_ORGANIZATION = "https://hub.docker.com/v2/repositories/biocontainers/";
var CROSS_PROXY            = "https://crossorigin.me/";
var QUAY_ORGANIZATION      = "https://quay.io/api/v1/repository?namespace=biocontainers&popularity=true&last_modified=true";
var QUAY_REOPSITORY_URL    = "https://quay.io/api/v1/repository/";
var QUAY_REPOSITORY        = "biocontainers/";
var BIO_TOOLS_URL          = "https://dev.bio.tools/api/tool/";
var GITHUB_ACTIVITY_URL    = "https://api.github.com/repos/";
var ANNOTATIONS_TOKEN      = "6879-29624520768d1f0c9fff7fc901f453f2";
var ANNOTATIONS            = "https://hypothes.is/api/search";


var app = angular.module('DockerWebUI', ['ngCookies','ngRoute', 'siTable','ngDonut', 'hljs', 'ngProgress', 'calHeatmap', 'angularMoment', 'ngSocial']);

angular.module('DockerWebUI')
    .factory('timeoutHttpIntercept', function ($rootScope, $q) {
        return {
            'request': function(config) {
                config.timeout = 100000;
                return config;
            }
        }})
    .filter('jsonDate',['$filter', function ($filter){
        return function (input, format){ return (input) ? $filter('date')(input, format):'';};
    }]);

// app.config(['ngClipProvider', function(ngClipProvider) { ngClipProvider.setPath("includes/bower_components/zeroclipboard/dist/ZeroClipboard.swf"); }]);

app.config(function($httpProvider){
	delete $httpProvider.defaults.headers.common['X-Requested-With'];
});

app.config(function (hljsServiceProvider) {
    hljsServiceProvider.setOptions({
        // replace tab with 4 spaces
        tabReplace: '    '
    });
});

app.config(function($routeProvider) {
	$routeProvider
		.when('/showImages', {
			templateUrl : 'pages/showImages.html',
			controller  : 'ImagesController'
		})
        .when('/', {
            templateUrl : 'pages/showNamespaces.html',
            controller  : 'MainController'
        });
});

app.controller('MainController', ['$scope','$route','$window','$cookies','$location', '$http','$filter','ngProgressFactory', '$q',function($scope,$route,$window,$cookies,$location, $http, $filter,ngProgressFactory , $q) {
    $scope.dates = {};

    if(DOCKERHUB_ORGANIZATION === undefined) {
        $window.location.href="#";
        $route.reload();
    } else {
        console.log('the ip is ' + DOCKERHUB_ORGANIZATION);
        $scope.IP = DOCKERHUB_ORGANIZATION;
        $scope.num_results=0;
        $scope.dictionary={};
        $scope.namespacesList=[];
        results=[];
        $scope.num_results = 0;
        urls  = [GITHUB_ACTIVITY_URL + "biocontainers/containers/issues?state=all&per_page=100",
                 GITHUB_ACTIVITY_URL + "biocontainers/specs/issues?state=all&per_page=100",
                 GITHUB_ACTIVITY_URL + "biocontainers/specs/issues/comments?per_page=100",
                 GITHUB_ACTIVITY_URL + "biocontainers/containers/issues/comments?per_page=100"];
        retrieveDockerHub(CROSS_PROXY + DOCKERHUB_ORGANIZATION, $http, $scope, $filter);
        retrieveQuayIO(  QUAY_ORGANIZATION, $http, $scope, $filter);
        retrieveGitHubIssues( urls, $http, $scope, $filter, $q);
        console.log($scope.num_results)
    }
    $scope.progressbar = ngProgressFactory.createInstance();
    $scope.progressbar.start();
}]);

function retrieveGitHubIssues(url, $http, $scope, $filter, $q){
    var deferred = $q.defer();
    var urlCalls = [];
    angular.forEach(urls, function(url) {
        urlCalls.push($http({method:"GET", url: url}));
    });
    $q.all(urlCalls).then(
        function(results) {
            //deferred.resolve(JSON.stringify(results))
            $scope.githubdates = []
            angular.forEach(results, function(result){
                angular.forEach(result.data, function(issue){
                    createAt   = $filter('jsonDate')(issue.created_at,'dd/MM/yyyy');
                    modifiedAt = $filter('jsonDate')(issue.updated_at,'dd/MM/yyyy');
                    closeAt    = $filter('jsonDate')(issue.close_at,'dd/MM/yyyy');
                    $scope.githubdates.push(createAt);
                    $scope.githubdates.push(modifiedAt);
                    $scope.githubdates.push(closeAt);

                })
            });
            $scope.githubDatesMap = {};
            for(var i = 0; i< $scope.githubdates.length; i++) {
                var parts =$scope.githubdates[i].split('/');
                var dateNumber = new Date(parts[2]+"-"+parts[1]+"-"+parts[0]).getTime()/1000;
                var num = Math.floor(dateNumber);
                if(!isNaN(num)) {
                    $scope.githubDatesMap[num.toString()] = $scope.githubDatesMap[num.toString()] ? $scope.githubDatesMap[num.toString()]+1 : 1;
                }
            }
            $scope.githubheatmap = {};
            $scope.githubheatmap.config = {
                displayLegend: false,
                domain: "year", //hour|day|week|month|year
                range:1,
                colLimit: 4,
                cellSize:20,
                itemName: "Number of Issues and Comment",
                data: $scope.githubDatesMap,
                subDomainTextFormat: null
            };
            $scope.githubheatmap.showDataDensity = true

        },
        function(errors) {
            deferred.reject(errors);
        },
        function(updates) {
            deferred.update(updates);
        });
    return deferred.promise;
}

function retrieveDockerHub( url , $http, $scope, $filter){
	$http({method: "GET", url: url}).success(function(data){
		$scope.num_results= $scope.num_results + data.count;
		angular.forEach(data.results, function(result){
		    starred = false;
		    if(result.star_count > 0){
		       starred = true
            }
            dateM = $filter('jsonDate')(result.last_updated,'dd/MM/yyyy');
			$scope.dictionary["biocontainers/" + result.name] = {domain: "biocontainers/", name: result.name, description: result.description, lastModified: dateM, number_pull: [result.pull_count, 15000], start_count:starred}
			$scope.namespacesList.push({domain: "biocontainers/", name: result.name, description: result.description, lastModified: dateM, number_pull: [result.pull_count, 15000], start_count:starred})
		});
		if(data.next != null){
			retrieveDockerHub(CROSS_PROXY + data.next, $http, $scope, $filter)
		}
	}).error(function(data){console.log("Unable to request the data")});
}

function retrieveQuayIO( url , $http, $scope, $filter){
	$http({method: "GET", url: url, headers: {
        'Authorization': "Bearer "+ "XRYLsxvQqmQLpP7RrajpFdiZntveNEyiffXyibK0"}}).success(function(data){
		$scope.num_results= $scope.num_results + data.repositories.length;
		angular.forEach(data.repositories, function(result){
		    dateM = $filter('jsonDate')(result.last_modified * 1000,'dd/MM/yyyy');
			$scope.dictionary["quay.io/biocontainers/" + result.name] = {domain: "quay.io/biocontainers/", name: result.name, description: result.description, lastModified: dateM, number_pull: [result.popularity, 50], start_count:result.is_starred}
			$scope.namespacesList.push({domain: "quay.io/biocontainers/", name: result.name, description: result.description, lastModified: dateM, number_pull: [result.popularity, 50], start_count:result.is_starred})
        });

        for(var i = 0; i< $scope.namespacesList.length; i++) {
            var parts =$scope.namespacesList[i].lastModified.split('/');
            var dateNumber = new Date(parts[2]+"-"+parts[1]+"-"+parts[0]).getTime()/1000;
            //var dateNumber = new Date($scope.namespacesList[i].lastModified).getTime()/1000;
            var num = Math.floor(dateNumber);
            if(!isNaN(num)) {
                $scope.dates[num.toString()] = $scope.dates[num.toString()] ? $scope.dates[num.toString()]+1 : 1;
            }
        }
        $scope.heatmap = {};
        $scope.heatmap.config = {
            displayLegend: false,
            domain: "year", //hour|day|week|month|year
            range:1,
            colLimit: 4,
            cellSize:20,
            itemName: "Container Update",
            data: $scope.dates,
            subDomainTextFormat: null
        };
        $scope.progressbar.complete();
        $scope.heatmap.showDataDensity = true

	});
}


app.controller('ImagesController', function($scope,$http,$location,$window,$cookies,$route) {

    $scope.domain=$location.search()['domain'];
    $scope.repository=$location.search()['repository'];
    $scope.repo = {};
    $scope.repo.starred = $location.search()['starred'];
    $scope.repo.last_updated = $location.search()['modified'];

    if($scope.domain == "dockerhub"){
        repoURL    = CROSS_PROXY + DOCKERHUB_ORGANIZATION + $scope.repository;
        imagesURL  = repoURL + "/tags/";
        dockerFile = repoURL + "/dockerfile/";
        $http({method: "GET", url: repoURL}).success(function(data){
            $scope.repo.starred = $location.search()['starred'];
            $scope.repo.repoName     = data.name;
            $scope.repo.description  = data.description;
            $scope.repo.star_count   = data.star_count;
            $scope.repo.pull_count   = data.pull_count;
            $scope.repo.last_updated = data.last_updated;
            $scope.repo.dockerFile   = "";
            $scope.repo.imagesList   = [];
            $scope.repo.domain       = "docker";
            $scope.repo.command      = "docker pull biocontainers/" + $scope.repository;
            $scope.repo.url          = "https://hub.docker.com/r/biocontainers/" + $scope.repository;
            $scope.repo.typeDockerFile = "DockerFile";

            $http({method: "GET", url: dockerFile}).success(function(data){
                $scope.repo.dockerFile = data.contents;});
            $http({method: "GET", url: imagesURL}).success(function(data){
                angular.forEach(data.results, function(result){
                    $scope.repo.imagesList.push({tag: result.name, last_updated: result.last_updated, size: result.full_size})
                })
            });

        }).error(function(data){console.log("Unable to request the data")})
    }
    if($scope.domain == "quay"){

        repoURL    = QUAY_REOPSITORY_URL + QUAY_REPOSITORY + $scope.repository;
        $http({method: "GET", url: repoURL, headers: {
            'Authorization': "Bearer "+ "XRYLsxvQqmQLpP7RrajpFdiZntveNEyiffXyibK0"}}).success(function(data){
            $scope.repo.repoName     = $scope.repository;
            $scope.repo.description  = data.description;
            $scope.repo.imagesList   = [];
            $scope.repo.domain       = "quay";
            $scope.repo.url          = "https://quay.io/repository/biocontainers/" + $scope.repository;
            $scope.repo.command      = "docker pull quay.io/biocontainers/" + $scope.repository;
            githubYaml               = "";
            $scope.repo.typeDockerFile = "Yaml";

            githubAPIYaml             = "https://api.github.com/repos/bioconda/bioconda-recipes/contents/recipes/" + $scope.repository;

            $http({method: "GET", url: githubAPIYaml}).success(function(data){
                angular.forEach(data, function(value){
                   if(value.name == "meta.yaml"){
                       githubYaml = value.download_url
                   }
                });
                if(githubYaml == ""){
                    angular.forEach(data, function(value){
                        if(value.type == "dir"){
                            githubYaml = "https://raw.githubusercontent.com/bioconda/bioconda-recipes/master/recipes/" + $scope.repository +"/" + value.name + "/meta.yaml";
                        }
                    });
                }
                $http({method: "GET", url: githubYaml}).success(function(data){
                    $scope.repo.dockerFile = data});
            });
            angular.forEach(data.tags, function(key, value){
                    $scope.repo.imagesList.push({tag: key.name, last_updated: key.last_modified, size: key.size})
                })
            });
    }

    $http({method: "GET", url: BIO_TOOLS_URL + $scope.repository}).success(function(data){
        if(data.id != null){
            $scope.repo.toolTags = [];
            angular.forEach(data.topic, function(value){
                if ($scope.repo.toolTags.indexOf(value.term) == -1) {
                    $scope.repo.toolTags.push(value.term)
                }
            })
        }else{
            $scope.repo.toolTags = null;
        }

    });
});


function parseDate(dateString, moment) {
    var m = moment(dateString, 'DD/MM/YYYY', true);
    return m.isValid() ? m.toDate() : new Date(NaN);
}