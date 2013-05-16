/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */

UserEditView = DSSEditableView.extend({
    events: {
        "click #save-changes": "saveChanges",
        "change input[type=radio]": "selectAvatar"
    },
    render: function () {
        ich.addTemplate('user', this.template());
        var renderedTemplate = ich.user(this.model.toJSON());
        $(this.el).html(renderedTemplate);

        $("#div_avatar_image_upload", this.el).hide();
        var avatarType = this.model.get('profile').avatar_type;
        if (!com.podnoms.utils.isEmpty(avatarType)){
            $('#avatar_' + avatarType, this.el).attr('checked', true);
            if (avatarType == 'custom') {
                $("#div_avatar_image_upload", this.el).show();
                $('#file_upload').uploadifive({
                        'uploadScript': 'ajax/upload_avatar_image/'
                });
            }
        }
        return this;
    },
    saveChanges: function () {
        var data = Backbone.Syphon.serialize(this);
        this.model.set(data);
        var ref = this;
        this._saveChanges({
            success: function () {
                if (ref.model.get('profile').avatar_type == 'custom'){
                        $.ajaxFileUpload({
                            url: '/ajax/upload_avatar_image/',
                            secureuri: false,
                            fileElementId: 'avatar_image',
                            success: function (data, status) {
                                if (typeof(data.error) != 'undefined') {
                                    if (data.error != '') {
                                        alert(data.error);
                                    } else {
                                        alert(data.msg);
                                    }
                                } else {
                                    com.podnoms.utils.showAlert("Success", "Successfully updated yourself");
                                    Backbone.history.navigate('/', {trigger:true});
                                }
                            },
                            error: function (data, status, e) {
                                alert(e);
                            }
                        });
                }else{
                        com.podnoms.utils.showAlert("Success", "Successfully updated yourself");
                        Backbone.history.navigate('/', {trigger:true});
                }
            },
            error: function () {
                com.podnoms.utils.showError("Error", "There was an error updating your info. Please try again later.");
            }
        });
        return false;
    },

    selectAvatar: function (evt) {
        var type = $(evt.currentTarget).val();
        this.model.set('avatar_type', type);
        if (type == 'custom') {
            $("#div_avatar_image_upload", this.el).show();
            $('#file_upload').uploadifive({
                'uploadScript': 'ajax/upload_avatar_image/'
            });
        }else{
            $("#div_avatar_image_upload", this.el).hide();
        }
    }
});
