/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
window.CommentListItemView = Backbone.View.extend({
    tagName:"li",
    initialize:function () {
        $(this.el).data("id", this.model.get("id"));
        $(this.el).addClass("comment-entry");
    },
    render:function () {
        $(this.el).html(this.template({"item":this.model.toJSON()}));
        return this;
    }
});
window.CommentListView = Backbone.View.extend({
    initialize:function () {
        //this.collection.bind('add', this.render);
    },
    events:{
        "click #id-btn-add-comment":"addComment"
    },
    addComment:function (ev) {
        var comment = $('textarea[name=new-comment]').val();
        var view = this;
        if (comment) {
            this.collection.create({
                mix:this.collection.mix,
                comment:comment,
                time_index:15
            }, {
                success:function () {
                    view.collection.sort();
                    view.render();
                },
                error:function () {
                    com.podnoms.utils.showError("Error", "Unable to save comment");
            }});
            $('textarea[name=new-comment]').val('');
        }
        return false;
    },
    render:function () {
        $(this.el).html(this.template()).append('<ul class="comment-listing list-nostyle"></ul>');
        this.collection.each(function (item) {
            $('.comment-listing', this.el).append(new CommentListItemView({model:item}).render().el);
        }, this);
        return this;
    }
});
