window.UserView = Backbone.View.extend({
    events:{
        "click #save-changes":"saveChanges",
        "change input" :"changed",
        "change select" :"changed"
    },
    initialize:function () {
        this.render();
    },
    render:function () {
        $(this.el).html(this.template({"item":this.model.toJSON()}));
        return this;
    },
    saveChanges: function(){
        this.model.save();
        return false;
    },
    changed:function(evt) {
        var changed = evt.currentTarget;
        var value = $("#"+changed.id).val();
        var obj = "{\""+changed.id +"\":\""+value+"\"}";
        var objInst = JSON.parse(obj);
        this.model.set(objInst);
    }
});