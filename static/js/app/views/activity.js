/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
window.ActivityListItemView = Backbone.View.extend({
    tagName:"li",
    initialize:function () {
        $(this.el).data("id", this.model.get("id"));
        $(this.el).addClass("media");
    },
    render:function () {
        $(this.el).html(this.template({"item":this.model.toJSON()}));
        return this;
    }
});

window.ActivityListView = Backbone.View.extend({
    initialize:function () {
        //this.collection.bind('add', this.render);
        this.render();
    },
    render:function () {
        $(this.el).html(this.template()).append('<ul class="activity-listing media-list"></ul>');
        this.collection.each(function (item) {
            $('.activity-listing', this.el).append(new ActivityListItemView({model:item}).render().el);
        }, this);
        return this;
    }
});
