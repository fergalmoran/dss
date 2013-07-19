define ['app', 'toastr', 'app.lib/editableView', 'moment', 'libs/backbone/backbone.syphon', 'text!/tpl/UserEditView'],
(App, toastr, EditableView, moment, Syphon, Template) ->
    class UserEditView extends EditableView
        template: _.template(Template)
        events:
            "click #save-changes": "saveChanges",
            "change input[type=radio]": "selectAvatar"

        onRender: ->
            console.log("MixEditView: onRender")
            avatarType = @model.get('avatar_type')
            $('#avatar_' + avatarType, @el).attr('checked', true);
            if avatarType is "custom"
                $("#div_avatar_image_upload", @el).show()
                $("#file_upload").uploadifive uploadScript: "ajax/upload_avatar_image/"
            else
                $("#div_avatar_image_upload", this.el).hide();

            true
        selectAvatar: (evt) ->
            type = $(evt.currentTarget).val()
            @model.set "avatar_type", type
            if type is "custom"
                $("#div_avatar_image_upload", @el).show()
                $("#file_upload").uploadifive uploadScript: "ajax/upload_avatar_image/"
            else
                $("#div_avatar_image_upload", @el).hide()

        saveChanges: ->
            data = Backbone.Syphon.serialize(this)
            @model.set data
            ref = this
            @_saveChanges
                success: ->
                    if ref.model.get('avatar_type') is "custom"
                        $.ajaxFileUpload
                            url: "/ajax/upload_avatar_image/"
                            secureuri: false
                            fileElementId: "avatar_image"
                            success: (data, status) ->
                                unless typeof (data.error) is "undefined"
                                    unless data.error is ""
                                        alert data.error
                                    else
                                        alert data.msg
                                else
                                    toastr.info "Successfully updated yourself"
                                    Backbone.history.navigate "/",
                                        trigger: true


                            error: (data, status, e) ->
                                alert e

                    else
                        toastr.info "Successfully updated yourself"
                        Backbone.history.navigate "/",
                            trigger: true
                    true
                error: ->
                    toastr.error "There was an error updating your info. Please try again later."
                    true
            true

        false

    UserEditView