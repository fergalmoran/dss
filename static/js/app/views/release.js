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
    events: {
        "click tr" : "showDetails"
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
            sortList: [[0,0],[1,0]]
        });
        $('tr.rowlink', this.el).rowlink();

        return this;
    },
    showDetails: function(row){
        window.app.navigate('#/release/' + $(row.currentTarget).data("id"), true);
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