requirejs.config({
    baseUrl: "static/js",
    paths: {
        jquery: 'libs/jquery',
        backbone: 'libs/backbone/backbone',
        'backbone.babysitter': 'libs/backbone/backbone.babysitter',
        marionette: 'libs/backbone/backbone.marionette',
        'backbone.wreqr': 'libs/backbone/backbone.wreqr',
        ich: 'libs/ICanHaz',
        underscore: 'libs/backbone/underscore',
        text: 'libs/text',
        templates: '/templates',
        app: 'app/appv2',
        vent: 'app/lib/eventAggregator',
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
    "use strict"

    console.log("Dss.Bootstrapper: primed");
    App.start();
});
