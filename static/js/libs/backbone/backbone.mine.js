Backbone.Validate = function (model, changedAttributes) {

    return (function () {
        this.errors = {};
        this.attributes = _.clone(model.attributes);
        _.extend(this.attributes, changedAttributes);
        _.each(model.validates, function (value, rule) {
            this.validators[rule](value);
        });

        this.validators = {
            required:function (fields) {
                _.each(fields, function (field) {
                    if (_.isEmpty(this.attributes[field]) === true) {
                        this.addError(field, I18n.t('errors.form.required'));
                    }
                });
            }
        };

        this.addError = function (field, message) {
            if (_.isUndefined(this.errors[field])) {
                this.errors[field] = [];
            }
            this.errors[field].push(message);
        };

        return this.errors;
    })();
};

window.TastypieModel = Backbone.Model.extend({
    base_url:function () {
        var temp_url = Backbone.Model.prototype.url.call(this);
        return (temp_url.charAt(temp_url.length - 1) == '/' ? temp_url : temp_url + '/');
    },
    url:function () {
        return this.base_url();
    }
});

window.TastypieCollection = Backbone.Collection.extend({
    parse:function (response) {
        this.recent_meta = response.meta || {};
        return response.objects || response;
    }
});

window.DSSModel = window.TastypieModel.extend({
    addError:function (field, message) {
        if (_.isUndefined(this.errors[field])) {
            this.errors[field] = [];
        }
        this.errors[field].push(message);
        return field;
    }
});

window.DSSEditableView = Backbone.View.extend({
    events:{
        "change input":"changed",
        "change textarea":"changed"
    },
    changed:function (evt) {
        var changed = evt.currentTarget;
        var value = $("#" + changed.id).val();
        var obj = "{\"" + changed.id + "\":\"" + value + "\"}";
        var objInst = JSON.parse(obj);
        this.model.set(objInst);
    },
    _bakeForm:function (el, lookups) {
        //TODO extend lookups to be a list
        //TODO this way we can initialise more than one lookup per page
        var model = this.model;
        var labels, mapped;

        $('.typeahead', el).typeahead({
            source:function (query, process) {
                $.get(
                    '/ajax/lookup/' + lookups + '/',
                    { query:query },
                    function (data) {
                        labels = []
                        mapped = {}
                        $.each(data, function (i, item) {
                            mapped[item.fields.name] = item;
                            labels.push(item.fields.name);
                        });
                        process(labels);
                    }, 'json');
            },
            updater:function (item) {
                $('#release_label_id', el).val(mapped[item].pk);
                model.set('release_label_id', mapped[item].pk);
                return item;
            }
        });
        $('.datepicker', el).datepicker(
            {
                'format':'dd/mm/yyyy'
            }
        );
        $('.timepicker', this.el).timepicker();
        $('textarea.tinymce', el).tinymce({
            script_url:"/static/js/libs/tiny_mce/tiny_mce.js",
            mode:"textareas",
            theme:"advanced",
            theme_advanced_toolbar_location:"top",
            theme_advanced_toolbar_align:"left",
            theme_advanced_buttons1:"fullscreen,separator,preview,separator,bold,italic,underline,strikethrough,separator,bullist,numlist,outdent,indent,separator,undo,redo,separator,link,unlink,anchor,separator,image,cleanup,help,separator,code",
            theme_advanced_buttons2:"",
            theme_advanced_buttons3:"",
            auto_cleanup_word:true,
            plugins:"table,save,advhr,advimage,advlink,emotions,iespell,insertdatetime,print,contextmenu,fullscreen,preview,searchreplace",
            plugin_insertdate_dateFormat:"%m/%d/%Y",
            plugin_insertdate_timeFormat:"%H:%M:%S",
            extended_valid_elements:"a[name|href|target=_blank|title|onclick],img[class|src|border=0|alt|title|hspace|vspace|width|height|align|onmouseover|onmouseout|name],hr[class|width|size|noshade],font[face|size|color|style],span[class|align|style]",
            fullscreen_settings:{
                theme_advanced_path_location:"top",
                theme_advanced_buttons1:"fullscreen,separator,preview,separator,cut,copy,paste,separator,undo,redo,separator,search,replace,separator,code,separator,cleanup,separator,bold,italic,underline,strikethrough,separator,forecolor,backcolor,separator,justifyleft,justifycenter,justifyright,justifyfull,separator,help",
                theme_advanced_buttons2:"removeformat,styleselect,formatselect,fontselect,fontsizeselect,separator,bullist,numlist,outdent,indent,separator,link,unlink,anchor",
                theme_advanced_buttons3:"sub,sup,separator,image,insertdate,inserttime,separator,tablecontrols,separator,hr,advhr,visualaid,separator,charmap,emotions,iespell,flash,separator,print"
            }
        });
    }
});