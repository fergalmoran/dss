var EventListItemView = Backbone.View.extend({
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
var EventListView = Backbone.View.extend({
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
            $('#event-list-container', el).append(new EventListItemView({model:item}).render().el);
        });
        $("#event-table", this.el).tablesorter({
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
        window.app.navigate('#/event/' + $(row.currentTarget).data("id"), true);
    }
});
var EventItemView = Backbone.View.extend({
    tagName:"li",
    initialize:function () {
        this.render();
    },
    render:function () {
        $(this.el).html(this.template({"item":this.model.toJSON()}));
        return this;
    }
});
var EventView = Backbone.View.extend({
    initialize:function () {
        this.render();
    },
    render:function () {
        $(this.el).html(this.template());
        var item = new EventItemView({model:this.model}).render();
        $('.event-listing', this.el).append(item.el);
        $('#event-description', this.el).html(this.model.get("description"));
        return this;
    }
});
var EventCreateView = DSSEditableView.extend({
    events:{
        "click #save-changes":"saveChanges"
    },
    initialize:function () {
        this.render();
        this._bakeForm(this.el, 'venue');
    },
    render:function () {
        $(this.el).html(this.template({"item":this.model.toJSON()}));
        return this;
    },
    saveChanges:function () {
        this.model.set('event_description', $('#event-description', this.el).html());
        this.model.set('event_date', $('#event_date', this.el).val());
        this._saveChanges({
            success:function () {
                com.podnoms.utils.showAlert("Success", "Event successfully added", "alert-info", true);
            }
        });
        return false;
    }
});