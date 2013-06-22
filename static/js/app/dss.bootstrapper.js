requirejs.config({
    baseUrl: 'static/js',
    urlArgs: com.podnoms.settings.urlArgs,
    waitSeconds: 200,
    paths: {
        jquery: 'libs/jquery',
        backbone: 'libs/backbone/backbone',
        'backbone.babysitter': 'libs/backbone/backbone.babysitter',
        marionette: 'libs/backbone/backbone.marionette',
        'backbone.wreqr': 'libs/backbone/backbone.wreqr',
        ich: 'libs/ICanHaz',
        bootstrap: 'libs/bootstrap/bootstrap',
        underscore: 'libs/backbone/underscore',
        text: 'libs/text',
        templates: '/templates',
        app: 'app/appv2',
        utils: 'app/lib/utils',
        vent: 'app/lib/eventAggregator',
        views: 'app/views',
        models: 'app/models',
        'app.lib': 'app/lib',
        moment: 'libs/moment',
        toastr: 'libs/toastr'
    },
    shim: {
        jquery: {
            exports: 'jQuery'
        },
        backbone: {
            exports: 'Backbone',
            deps: ['jquery', 'underscore']
        },
        bootstrap: {
            exports: 'bootstrap',
            deps: ['jquery']
        },
        marionette: {
            exports: 'Marionette',
            deps: ['jquery', 'backbone']
        },
        underscore: {
            exports: '_'
        },
        utils: {
            deps: ['jquery', 'bootstrap']
        }
    }
});

requirejs(['toastr', 'underscore', 'backbone', 'app'], function (toastr, _, Backbone, App) {
    'use strict'

    console.log('Dss.Bootstrapper: primed');
    App.start();
});
