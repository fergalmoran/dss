requirejs.config({
    baseUrl: com.podnoms.settings.staticUrl + 'js',
    urlArgs: com.podnoms.settings.urlArgs,
    waitSeconds: 200,
    paths: {
        site: 'app/site',
        jquery: 'lib/jquery',
        backbone: 'lib/backbone',
        'backbone.relational': 'lib/backbone.relational',
        'backbone.syphon': 'lib/backbone.syphon',
        marionette: 'lib/backbone.marionette',
        bootstrap: 'lib/bootstrap',
        underscore: 'lib/underscore',
        text: 'lib/text',
        templates: '/templates',
        app: 'app/appv2',
        utils: 'app/lib/utils',
        vent: 'app/lib/eventAggregator',
        views: 'app/views',
        models: 'app/models',
        'app.lib': 'app/lib',
        moment: 'lib/moment',
        ace: 'lib/ace',
        wysiwyg: 'lib/bootstrap-wysiwyg',
        'ace-editable': 'lib/ace-editable',
        'facebook': '//connect.facebook.net/en_US/all',

        /*File upload */
        /*TOOD: Move this to a shim */
        'jquery.fileupload': 'lib/jquery.fileupload',
        'jquery.fileupload-audio': 'lib/jquery.fileupload-audio',
        'jquery.fileupload-video': 'lib/jquery.fileupload-video',
        'jquery.fileupload-validate': 'lib/jquery.fileupload-validate',
        'jquery.fileupload-process': 'lib/jquery.fileupload-process',
        'jquery.fileupload-ui': 'lib/jquery.fileupload-ui',
        'jquery.fileupload-image': 'lib/jquery.fileupload-image',
        'jquery.iframe-transport': 'lib/jquery.iframe-transport',
        'jquery.ui.widget': 'lib/jquery.ui.widget',
        'load-image': 'lib/load-image',
        'load-image-meta': 'lib/load-image-meta',
        'load-image-exif': 'lib/load-image-exif',
        'load-image-ios': 'lib/load-image-ios',
        'load-image-blob': 'lib/load-image-blob',
        'canvas-to-blob': 'lib/canvas-to-blob',
        /*End file upload */

        'tmpl': 'lib/tmpl',
        toastr: 'lib/toastr',
        'socket.io': [
            com.podnoms.settings.SOCKET_IO_JS_URL,
            'lib/socket.io'
        ]
    },
    shim: {
        jquery: {
            exports: '$'
        },
        backbone: {
            exports: 'Backbone',
            deps: ['jquery', 'underscore']
        },
        bootstrap: {
            exports: 'bootstrap',
            deps: ['jquery']
        },
        'facebook': {
            export: 'FB'
        },
        'ace': {
            exports: 'ace',
            deps: ['jquery', 'lib/ace-elements', 'lib/ace-extra']
        },
        'ace-editable': {
            exports: 'editable',
            deps: ['jquery', 'ace', 'lib/bootstrap-editable']
        },
        'wysiwyg': {
            exports: 'wysiwyg',
            deps: ['ace-editable', 'lib/jquery.hotkeys']
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

requirejs(['site', 'toastr', 'underscore', 'backbone', 'app'], function (site, toastr, _, Backbone, App) {
    'use strict'

    console.log('Dss.Bootstrapper: primed');
    App.start();
});
