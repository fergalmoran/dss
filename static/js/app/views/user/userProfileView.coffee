define ['app', 'utils', 'moment', 'marionette', 'vent', 'app.lib/editableView', 'models/user/userItem',
        'text!/tpl/UserProfileView', 'ace-editable', 'wysiwyg'],
(App, utils, moment, Marionette, vent, EditableView, UserItem, Template)->
    class UserProfileView extends EditableView
        template: _.template(Template)

        events:
            "click #follow-button": -> vent.trigger("user:follow", @model)
            "click #follow-button-login": -> vent.trigger("app:login", @model)

        initialize: =>
            @listenTo(@model, 'change:is_following', @render)

        templateHelpers:
            humanise: (date)->
                moment(date).fromNow()

        onDomRefresh: ->
            console.log("UserProfileView: initialize")
            @setupImageEditable
                el: $("#avatar", @el)
                url: "/ajax/upload_avatar_image/"
                chooseMessage: "Choose profile image"

            $.fn.editable.defaults.mode = "inline"
            $.fn.editableform.loading = "<div class='editableform-loading'><i class='light-blue icon-2x icon-spinner icon-spin'></i></div>"
            $.fn.editableform.buttons = "<button type=\"submit\" class=\"btn btn-info editable-submit\"><i class=\"icon-ok icon-white\"></i></button>" + "<button type=\"button\" class=\"btn editable-cancel\"><i class=\"icon-remove\"></i></button>"

            #editables
            if utils.isMe(@model.get("id"))
                $("#about", @el).editable
                    mode: "inline"
                    type: "wysiwyg"
                    name: "about"
                    wysiwyg: {}
                    css: {'max-width': '300px'}
                    success: (response, newValue) =>
                        console.log("Update model with new value")
                        @model.save 'description', newValue, patch: true

            $(".usereditable").attr('class', if utils.isMe(@model.get("id")) then "editable editable-click" else "user-info")

        onRender: ->
            window.scrollTo 0, 0

    UserProfileView


