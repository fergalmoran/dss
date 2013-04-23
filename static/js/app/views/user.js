/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
window.UserView = DSSEditableView.extend({
    events:{
        "click #save-changes":"saveChanges",
        "click input[type=radio]":"selectAvatar",
        "change input":"changed",
        "change textarea":"changed",
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
        var avatarType = this.model.get('avatar_type');
        if (!com.podnoms.utils.isEmpty(avatarType))
            $('#' + this.model.get('avatar_type'), this.el).attr('checked', 'checked');

        //console.clear();
        return this;
    },
    saveChanges:function () {
        var model = this.model;
        this._saveChanges({
            success:function () {
                com.podnoms.utils.showAlert("Success", "Successfully updated yourself");
                Backbone.history.navigate('/', {trigger:true});
            },
            error:function () {
                com.podnoms.utils.showError("Error", "There was an error updating your info. Please try again later.");
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
});
