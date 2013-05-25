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
        views: 'app/views',
        models: 'app/models',
        app: 'app/appv2',
        'app.lib': 'app/lib',
        moment: 'libs/moment'
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
        }
    }
});

requirejs(['backbone', 'app'], function (Backbone, App) {
    console.log("Dss.Bootstrapper: primed");
    App.start();
});
