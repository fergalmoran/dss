@Dss.module "UserApp.Views", (Views, App, Backbone, Marionette, $    ) ->
    class Views.UserProfileView extends App.Lib.EditableView
        template: "userprofileview"

        events:
            "click #follow-button": -> App.vent.trigger("user:follow", @model)
            "click #follow-button-login": -> App.vent.trigger("app:login", @model)

        initialize: =>
            @listenTo(@model, 'change:is_following', @render)

        onDomRefresh: ->
            console.log("UserProfileView: initialize")

            $.fn.editable.defaults.mode = "inline"
            $.fn.editableform.loading = "<div class='editableform-loading'><i class='light-blue icon-2x icon-spinner icon-spin'></i></div>"
            $.fn.editableform.buttons = "<button type=\"submit\" class=\"btn btn-info editable-submit\"><i class=\"fa fa-check fa-white\"></i></button>" + "<button type=\"button\" class=\"btn editable-cancel\"><i class=\"fa fa-times fa-white\"></i></button>"

            #editables
            if utils.isMe(@model.get("id"))
                @setupImageEditable
                    el: $("#avatar", @el)
                    url: "/ajax/upload_avatar_image/"
                    chooseMessage: "Choose profile image"

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

            if location.hash != ''
                $('a[href="'+location.hash+'"]', @el).tab('show')

            $('a[data-toggle="tab"]', @el).on 'shown.bs.tab', (e) ->
                location.hash = $(e.target).attr('href').substr(1)
                e.preventDefault()

        onRender: ->
            window.scrollTo 0, 0

    Views.UserProfileView


