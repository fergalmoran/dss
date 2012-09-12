/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
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
var ReleaseCreateView = DSSEditableView.extend({
    events:{
        "click #save-changes":"saveChanges"
    },
    initialize:function () {
        this.render();
    },
    render:function () {
        $(this.el).html(this.template({"item":this.model.toJSON()}));
        this._bakeForm(this.el, 'release');
    },
    saveChanges:function () {
        var model = this.model;
        var el = this.el;
        var parent = this;

        this.model.set('release_description', $('#release-description', this.el).html());
        this.model.set('release_date', $('#release_date', this.el).val());
        this.model.set('embed_code', $('#embed_code', this.el).val());

        this._saveChanges({
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
                            com.podnoms.utils.showAlert("Success", "Release successfully added", "alert-info", true);
                            app.navigate('#/release/' + model.get('id'));
                        }
                    },
                    error:function (data, status, e) {
                        alert(e);
                    }
                });
            }
        });
        return false;
    }
});