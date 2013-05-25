requirejs.config({
    baseUrl: "static/js",
    paths: {
        jquery: 'libs/jquery',
        backbone: 'libs/backbone/backbone',
        marionette: 'libs/backbone/backbone.marionette',
        ich: 'libs/ICanHaz',
        underscore: 'libs/backbone/underscore',
        text: 'libs/text',
        templates: '/templates',
        app: 'app/appv2',
        views: 'app/views',
        models: 'app/models',
        'app.lib': 'app/lib',
        moment: 'libs/moment',
        toastr: 'libs/toastr'
    },
    shim: {
        backbone: {
            exports: 'Backbone',
            deps: ['underscore']
        },
        marionette: {
            exports: 'Marionette',
            deps: ['backbone']
        },
        underscore: {
            exports: '_'
        },
		'toastr': {
			deps: ['jquery'],
			exports: 'toastr'
		}
    }
});

requirejs(['toastr', 'underscore', 'backbone', 'app'], function (toastr, _, Backbone, App) {
    "require strict"

    console.log("Dss.Bootstrapper: primed");
    App.start();
});
