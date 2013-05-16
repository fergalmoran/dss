requirejs.config({
    baseUrl: "static/js",
    paths: {
        backbone: 'libs/backbone/backbone',
        marionette: 'libs/backbone/backbone.marionette',
        underscore: 'libs/backbone/underscore',
        jquery: 'libs/jquery',
        templates: '/templates',
        views: 'app/views',
        models: 'app/models',
        moment: 'libs/moment'
    },
    shim: {
        backbone: {
            exports: 'Backbone',
            deps: ['jquery', 'underscore']
        },
        marionette: {
            exports: 'Backbone.Marionette',
            deps: ['backbone']
        }
    }
});

requirejs(['backbone'], function(Backbone){
    console.log("RequireJS primed");
});