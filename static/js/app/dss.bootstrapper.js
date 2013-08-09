requirejs.config({
    baseUrl: com.podnoms.settings.staticUrl + 'js',
    urlArgs: com.podnoms.settings.urlArgs,
    waitSeconds: 200,
    paths: {
        jquery: 'libs/jquery',
        'jquery.ui.widget': 'libs/jquery.ui.widget',
        backbone: 'libs/backbone/backbone',
        'backbone.babysitter': 'libs/backbone/backbone.babysitter',
        'backbone.relational': 'libs/backbone/backbone.relational',
        marionette: 'libs/backbone/backbone.marionette',
        'backbone.wreqr': 'libs/backbone/backbone.wreqr',
        ich: 'libs/ICanHaz',
        bootstrap: 'libs/bootstrap/bootstrap',
        typeahead: 'libs/bootstrap/bootstrap-typeahead',
        underscore: 'libs/backbone/underscore',
        bootpag: 'libs/bootstrap/bootpag',
        text: 'libs/text',
        templates: '/templates',
        app: 'app/appv2',
        utils: 'app/lib/utils',
        vent: 'app/lib/eventAggregator',
        views: 'app/views',
        models: 'app/models',
        'app.lib': 'app/lib',
        moment: 'libs/moment',

        'tmpl': 'libs/upload/tmpl',
        'jquery.fileupload': 'libs/upload/jquery.fileupload',
        'jquery.fileupload-ui': 'libs/upload/jquery.fileupload-ui',
        'jquery.fileupload-image': 'libs/upload/jquery.fileupload-image',
        'jquery.fileupload-video': 'libs/upload/jquery.fileupload-video',
        'jquery.fileupload-validate': 'libs/upload/jquery.fileupload-validate',
        'jquery.fileupload-process': 'libs/upload/jquery.fileupload-process',
        'jquery.fileupload-audio': 'libs/upload/jquery.fileupload-audio',
        'jquery.iframe-transport': 'libs/jquery.iframe-transport',
        'load-image': 'libs/upload/load-image',
        'load-image-meta': 'libs/upload/load-image-meta',
        'load-image-exif': 'libs/upload/load-image-exif',
        'load-image-ios': 'libs/upload/load-image-ios',
        'canvas-to-blob': 'libs/canvas-to-blob',

        toastr: 'libs/toastr',
        'socket.io': [
            com.podnoms.settings.SOCKET_IO_JS_URL,
            'libs/socket.io'
        ]
    },
    shim: {
        jquery: {
            exports: '$'
        },
        'jquery.ui.widget': {
            deps: ['jquery']
        },
        backbone: {
            exports: 'Backbone',
            deps: ['jquery', 'underscore']
        },
        bootstrap: {
            exports: 'bootstrap',
            deps: ['jquery']
        },
        /*
        fileupload:{
            deps: ['iframe-transport', 'fileupload-process', 'fileupload-audio', 'fileupload-video', 'fileupload-validate', 'fileupload-ui'],
            deps: ['jquery.iframe-transport', 'jquery.ui.widget', 'fileupload-ui'],
            exports: '$.fileupload'
        },*/
        typeahead: {
            deps: ['jquery', 'bootstrap']
        },
        bootpag: {
            exports: 'bootpag',
            deps: ['jquery', 'bootstrap']
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
