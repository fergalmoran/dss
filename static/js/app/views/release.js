var ReleaseListItemView = Backbone.View.extend({
    tagName:"tr",
    initialize:function () {
        $(this.el).addClass("rowlink");
        $(this.el).data("id", this.model.get("id"));
        this.render();
    },
    render:function () {
        $(this.el).html(this.template({"item":this.model.toJSON()}));
        return this;
    }
});
var ReleaseListView = Backbone.View.extend({
    events:{
        "click tr":"showDetails"
    },
    initialize:function () {
        this.render();
    },
    render:function () {
        $(this.el).html(this.template());
        var el = this.el;
        this.collection.each(function (item) {
            $('#release-list-container', el).append(new ReleaseListItemView({model:item}).render().el);
        });
        $("#release-table", this.el).tablesorter({
            sortList:[
                [0, 0],
                [1, 0]
            ]
        });
        $('tr.rowlink', this.el).rowlink();
        $('#tablesorter-fix', this.el).hide();
        return this;
    },
    showDetails:function (row) {
        window.app.navigate('#/release/' + $(row.currentTarget).data("id"), true);
    }
});
var ReleaseItemView = Backbone.View.extend({
    tagName:"li",
    initialize:function () {
        this.render();
    },
    render:function () {
        $(this.el).html(this.template({"item":this.model.toJSON()}));
        return this;
    }
});
var ReleaseView = Backbone.View.extend({
    initialize:function () {
        this.render();
    },
    render:function () {
        $(this.el).html(this.template());
        var item = new ReleaseItemView({model:this.model}).render();
        $('.release-listing', this.el).append(item.el);
        $('#release-description', this.el).html(this.model.get("description"));
        return this;
    }
});
var ReleaseCreateView = Backbone.View.extend({
    events:{
        "click #save-changes":"saveChanges",
        "change input":"changed",
        "change textarea":"changed"
    },
    initialize:function () {
        this.render();
    },
    render:function () {
        $(this.el).html(this.template({"item":this.model.toJSON()}));
        var el = this.el;
        var model = this.model;
        var labels, mapped;
        $('.typeahead', this.el).typeahead({
            source:function (query, process) {
                $.get(
                    '/ajax/lookup/',
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
        $('.datepicker', this.el).datepicker(
            {
                'format':'dd/mm/yyyy'
            }
        );
        $('textarea.tinymce', this.el).tinymce({
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
    },
    saveChanges:function () {
        var model = this.model;
        var el = this.el;
        var parent = this;

        this.model.set('release_description', $('#release-description', this.el).html());
        this.model.set('release_date', $('#release_date', this.el).val());
        this.model.set('embed_code', $('#embed_code', this.el).val());
        if (this.model.isValid() != "") {
            if (this.model.errors){
                for (var error in this.model.errors){
                    $('#group-' + error, this.el).addClass('error');
                    $('#error-' + error, this.el).text(this.model.errors[error]);
                }
            }
        } else {
            this.model.save(
                null, {
                    success:function () {
                        $.ajaxFileUpload({
                            url:'ajax/upload_release_image/' + model.get('id') + '/',
                            secureuri:false,
                            fileElementId:'release_image',
                            success:function (data, status) {
                                if (typeof(data.error) != 'undefined') {
                                    if (data.error != '') {
                                        alert(data.error);
                                    } else {
                                        alert(data.msg);
                                    }
                                } else {
                                    window.utils.showAlert("Success", "Release successfully added", "alert-info", true);
                                    app.navigate('#/release/' + model.get('id'));
                                }
                            },
                            error:function (data, status, e) {
                                alert(e);
                            }
                        });
                    },
                    error:function () {
                        alert("Error saving release");
                    }
                });
        }
        return false;
    },
    changed:function (evt) {
        var changed = evt.currentTarget;
        var value = $("#" + changed.id).val();
        var obj = "{\"" + changed.id + "\":\"" + value + "\"}";
        var objInst = JSON.parse(obj);
        this.model.set(objInst);
    }
});