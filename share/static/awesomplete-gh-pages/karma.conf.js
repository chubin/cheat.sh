module.exports = function(config) {
 	config.set({
		// base path that will be used to resolve all patterns (eg. files, exclude)
		basePath: '',

		// frameworks to use
		// available frameworks: https://npmjs.org/browse/keyword/karma-adapter
		frameworks: ['jasmine', 'jasmine-def', 'fixture'],

		// list of files / patterns to load in the browser
		files: [
			'awesomplete.js',
			'test/specHelper.js',
			{
				pattern: 'test/fixtures/**/*.html',
				watched: true, included: true, served: true
			},
			'test/**/*Spec.js'
		],

		// list of files to exclude
		exclude: [
			'**/*.swp'
		],

		// preprocess matching files before serving them to the browser
		// available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
		preprocessors: {
			'awesomplete.js': ['coverage'],
			'**/*.html' : ['html2js']
		},

		// test results reporter to use
		// possible values: 'dots', 'progress'
		// available reporters: https://npmjs.org/browse/keyword/karma-reporter
		reporters: ['dots', 'coverage'],
		coverageReporter: {
			type: 'lcov',
			subdir: '.'
		},
		// web server port
		port: 9876,

		// enable / disable colors in the output (reporters and logs)
		colors: true,

		// level of logging
		// possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
		logLevel: config.LOG_INFO,

		// enable / disable watching file and executing tests whenever any file changes
		autoWatch: true,

		// start these browsers
		// available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
		browsers: process.env.TRAVIS ? ['ChromeTravisCI'] : ['Chrome'],

		// need this to run Chrome on Travis CI
		customLaunchers: {
			ChromeTravisCI: {
				base: 'Chrome',
				flags: ['--no-sandbox']
			}
		},

		// Continuous Integration mode
		// if true, Karma captures browsers, runs the tests and exits
		singleRun: false
	});
};
