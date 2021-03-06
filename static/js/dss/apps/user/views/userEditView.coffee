@Dss.module "UserApp.Views", (Views, App, Backbone, Marionette, $    ) ->
    class Views.UserEditView extends App.Lib.EditableView
        template: "usereditview"
        events:
            "click #save-changes": "saveChanges",
            "change input[type=radio]": "selectAvatar"

        onRender: ->
            console.log("MixEditView: onRender")
            avatarType = @model.get('avatar_type')
            $('#avatar_' + avatarType, @el).attr('checked', true);
            if avatarType is "custom"
                $("#div_avatar_image_upload", @el).show()
                #$("#file_upload").uploadifive uploadScript: "ajax/upload_avatar_image/"
            else
                $("#div_avatar_image_upload", this.el).hide();

            true

        selectAvatar: (evt) ->
            type = $(evt.currentTarget).val()
            @model.set "avatar_type", type
            if type is "custom"
                $("#custom_avatar_helptext", @el).show()
            else
                $("#custom_avatar_helptext", @el).hide()

        saveChanges: ->
            data = Backbone.Syphon.serialize(this)
            @model.set data
            ref = this
            @_saveChanges
                success: ->
                    """
                    if ref.model.get('avatar_type') is "custom"
                        $.ajaxFileUpload
                            url: "ajax/upload_avatar_image/"
                            secureuri: false
                            fileElementId: "mix_image"
                            success: (data, status) =>
                                unless typeof (data.error) is "undefined"
                                    unless data.error is ""
                                        alert data.error
                                    else
                                        alert data.msg
                                else
                                    $("#mix-details", @el).hide()
                                    Backbone.history.navigate "/",
                                        trigger: true

                            error: (data, status, e) ->
                                utils.showError e

                    else
                    """
                    toastr.info "Successfully updated yourself"
                    true
                error: ->
                    toastr.error "There was an error updating your info. Please try again later."
                    true
            true

        false

    Views.UserEditView