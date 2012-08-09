var ReleaseItemView = Backbone.View.extend({
    tagName:"li",
    initialize:function () {
        /*$(this.el).attr("id", "releaseitem-" + this.model.get("id"));
        $(this.el).addClass("release-listing-item");
        $(this.el).data("id", this.model.get("id"));*/
    },
    render:function () {
        $(this.el).html(this.template({"item":this.model.toJSON()}));
        return this;
    }
});
var ReleaseListView = Backbone.View.extend({
    initialize:function () {
        this.render();
    },
    render:function () {
        $(this.el).html(this.template()).append('<ul class="release-listing audio-listing"></ul>');
        var el = this.el;
        this.collection.each(function (item) {
            $('.release-listing', el).append(new ReleaseItemView({model:item}).render().el);
        });
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