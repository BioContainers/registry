module.exports = function(config) {

    config.set({
        basePath: '',
        frameworks: ['jasmine'],
        files: [
            'example/vendor/angular/angular.js',
            'example/vendor/angular-mocks/angular-mocks.js',
            'example/vendor/d3/d3.js',
            'tests/spec.js',
            'components/ngDonut.js'
        ],
        reporters: ['progress'],
        port: 9876,
        colors: true,
        logLevel: config.LOG_INFO,
        autoWatch: true,
        browsers: ['Firefox'],
        singleRun: true
    });
};