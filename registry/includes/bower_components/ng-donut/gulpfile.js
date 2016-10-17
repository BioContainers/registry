(function() {

    var mainModule = 'components/ngDonut.js',
        vendorDest = 'example/vendor/ng-donut',
        devDist    = 'ng-donut.js',
        minDist    = 'ng-donut.min.js';

    var gulp   = require('gulp'),
        uglify = require('gulp-uglify'),
        rename = require('gulp-rename'),
        karma  = require('gulp-karma'),
        jshint = require('gulp-jshint'),
        watch  = require('gulp-watch');

    gulp.task('build', function gulpBuild(){
        gulp.src(mainModule)
            .pipe(rename(devDist))
            .pipe(gulp.dest('dist'))
            .pipe(gulp.dest(vendorDest))
            .pipe(rename(minDist))
            .pipe(uglify())
            .pipe(gulp.dest('dist'))
    });

    gulp.task('karma', function gulpKarma() {

        var testFiles = [
            'example/vendor/d3/d3.js',
            'example/vendor/angular/angular.js',
            'example/vendor/angular-mocks/angular-mocks.js',
            'tests/spec.js',
            mainModule
        ];

        return gulp.src(testFiles).pipe(karma({
                configFile: 'karma.conf.js',
                action: 'run'
            })).on('error', function onError(error) {
                throw error;
            });
    });

    gulp.task('hint', function gulpHint() {

        return gulp.src(mainModule)
            .pipe(jshint('.jshintrc'))
            .pipe(jshint.reporter('default'));
    });

    gulp.task('test', ['hint', 'karma']);
    gulp.task('default', ['hint', 'test']);
    gulp.task('watch', ['build'], function() {
        gulp.watch(mainModule, ['build']);
    });

})();