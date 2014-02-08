requirejs.config({
    baseUrl: com.podnoms.settings.staticUrl + 'js',
    urlArgs: com.podnoms.settings.urlArgs,
    waitSeconds: 200,
    paths: {
        site: 'app/site',
        jquery: 'lib/jquery',
        backbone: 'lib/backbone',
        'backbone-associations': 'lib/backbone.associations',
        'backbone.syphon': 'lib/backbone.syphon',
        marionette: 'lib/backbone.marionette',
        bootstrap: 'lib/ace/uncompressed/bootstrap',
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
        ajaxfileupload: 'lib/ajaxfileupload',
        ace: 'lib/ace/uncompressed/ace',
        typeahead: 'lib/ace/typeahead-bs2.min',
        wysiwyg: 'lib/ace/uncompressed/bootstrap-wysiwyg',
        wizard: 'lib/ace/uncompressed/fuelux/fuelux.wizard',
        dropzone: 'lib/ace/uncompressed/dropzone',
        'ace-editable': 'lib/ace/uncompressed/x-editable/ace-editable',
        'bootstrap-editable': 'lib/ace/uncompressed/x-editable/bootstrap-editable',
        'facebook': '//connect.facebook.net/en_US/all',
        soundmanager2: 'lib/sm/soundmanager2',

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
        toastr: 'lib/toastr'
    },
    shim: {
        jquery: {
            exports: '$'
        },
        ajaxfileupload: {
            exports: '$',
            deps: ['jquery']
        },
        backbone: {
            exports: 'Backbone',
            deps: ['jquery', 'underscore']
        },
        'backbone-associations': {
            exports: 'Backbone.AssociatedModel',
            deps: ['backbone']
        },
        bootstrap: {
            exports: 'bootstrap',
            deps: ['jquery']
        },
        'facebook': {
            exports: 'FB'
        },
        'ace': {
            exports: 'ace',
            deps: ['jquery', 'lib/ace/uncompressed/ace-elements', 'lib/ace/uncompressed/ace-extra']
        },
        'ace-editable': {
            exports: 'editable',
            deps: ['jquery', 'ace', 'bootstrap-editable']
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
        },
        'soundmanager2': {
            exports: 'soundManager'
        }
    }
});

requirejs(['site', 'toastr', 'underscore', 'backbone', 'app'], function (site, toastr, _, Backbone, App) {
    'use strict'

    console.log('Dss.Bootstrapper: primed')
    if(typeof String.prototype.trim !== 'function') {
        console.log("Fucking Microsoft!");
        String.prototype.trim = function() {
            return this.replace(/^\s+|\s+$/g, '');
        }
    }
    App.start();
});
