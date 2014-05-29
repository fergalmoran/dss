PIPELINE_TEMPLATE_FUNC = "_.template"

PIPELINE_COMPILERS = (
    'pipeline.compilers.coffee.CoffeeScriptCompiler',
)

PIPELINE_JS = {
    'templates': {
        'source_filenames': (
            'js/dss/templates/*.jst',
        ),
        'output_filename': 'js/templates.jst',
    },
    'backbone': {
        'source_filenames': (
            'js/lib/underscore.js',
            'js/lib/underscore.templatehelpers.js',
            'js/lib/backbone.js',
            'js/lib/backbone.syphon.js',
            'js/lib/backbone.associations.js',
            'js/lib/backbone.marionette.js',
        ),
        'output_filename': 'js/backbone.js',
    },
    'lib': {
        'source_filenames': (
            'js/lib/ace/uncompressed/jquery.js',
            'js/lib/ace/uncompressed/jquery-ui.js',
            'js/lib/ace/uncompressed/bootstrap.js',
            'js/lib/moment.js',
            'js/lib/ajaxfileupload.js',
            'js/lib/ace/uncompressed/ace.js',
            'js/lib/ace/uncompressed/ace-elements.js',
            'js/lib/ace/uncompressed/select2.js',
            'js/lib/ace/uncompressed/fuelux/fuelux.wizard.js',
            'js/lib/ace/ace/elements.wizard.js',
            'js/lib/typeahead.js',

            'js/lib/ace/uncompressed/bootstrap-wysiwyg.js',
            'js/lib/ace/uncompressed/fuelux/fuelux.wizard.js',
            'js/lib/ace/uncompressed/dropzone.js',
            'js/lib/ace/uncompressed/fullcalendar.js',
            'js/lib/ace/uncompressed/x-editable/bootstrap-editable.js',
            'js/lib/ace/uncompressed/x-editable/ace-editable.js',

            'js/lib/sm/soundmanager2.js',

            'js/lib/jasny.fileinput.js',
            'js/lib/jquery.fileupload.js',
            'js/lib/jquery.fileupload-process.js',
            'js/lib/jquery.fileupload-audio.js',
            'js/lib/jquery.fileupload-video.js',
            'js/lib/jquery.fileupload-validate.js',
            'js/lib/jquery.fileupload-ui.js',
            'js/lib/jquery.fileupload-image.js',
            'js/lib/jquery.iframe-transport.js',
            'js/lib/jquery.ui.widget.js',
            'js/lib/toastr.js',
        ),
        'output_filename': 'js/lib.js',
    },
    'site': {
        'source_filenames': (
            'js/dss/*.coffee',
            'js/dss/**/*.coffee',
            'js/dss/apps/**/**/*.coffee',
        ),
        'output_filename': 'js/site.js',
    }
}
