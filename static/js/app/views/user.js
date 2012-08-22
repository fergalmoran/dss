window.UserView = Backbone.View.extend({
    events:{
        "click #save-changes":"saveChanges",
        "click input[type=radio]":"selectAvatar",
        "change input":"changed",
        "change select":"changed",
        "change .switch":"changeSwitch"
    },
    initialize:function () {
        this.render();
    },
    render:function () {
        var model = this.model;
        $(this.el).html(this.template({"item":this.model.toJSON()}));
        $('.switch', this.el).each(function (item) {
            var val = model.get(this.id) ? "on" : "off";
            $(this).attr('checked', val == "on");
            $(this).iphoneSwitch(
                val,
                function (obj) {
                },
                function (obj) {
                },
                {
                    speed:250,
                    use_images:true,
                    track_bg_color:'#333',
                    sync_checkbox:true
                }
            );
        });
        $("#div_avatar_image", this.el).hide();
        $('#' + this.model.get('avatar_type'), this.el).attr('checked', 'checked');
        //console.clear();
        return this;
    },
    saveChanges:function () {
        this.model.save(
            null, {
                success:function () {
                    window.utils.showAlert("Success", "Successfully updated yourself", "alert-info", true);
                    window.history.back();
                },
                error:function () {
                    window.utils.showAlert("Success", "Successfully updated yourself", "alert-info", false);
                    alert("Error");
                }
            });
        return false;
    },
    changeSwitch:function (evt) {
        var bit = $(evt.currentTarget).data('bitflag');
        var coalesce = $(evt.currentTarget).data('coalesce');
        if ($(evt.currentTarget).attr('checked')) {
            this.model.set(coalesce, this.model.get(coalesce) | bit);
        } else {
            this.model.set(coalesce, this.model.get(coalesce) & ~bit);
        }
        this.model.save();
    },
    changed:function (evt) {
        var changed = evt.currentTarget;
        var value = $("#" + changed.id).val();
        var obj = "{\"" + changed.id + "\":\"" + value + "\"}";
        var objInst = JSON.parse(obj);
        this.model.set(objInst);
    },
    selectAvatar:function (evt) {
        var type = $(evt.currentTarget).val();
        this.model.set('avatar_type', type);
        if (type == 'custom') {
            $("#div_avatar_image", this.el).show();
            $('#file_upload').uploadifive({
                'uploadScript':'ajax/upload_avatar_image/'
            });
        }
    }
})
