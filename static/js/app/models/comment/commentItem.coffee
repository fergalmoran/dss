define ['app.lib/backbone.dss.model'], \
    (DSSModel) ->
        class CommentItem extends DSSModel
            urlRoot:    com.podnoms.settings.urlRoot + "comments/"
            defaults:
                avatar_image: com.podnoms.settings.avatarImage
                user_name: com.podnoms.settings.userName
                user_url: com.podnoms.settings.userUrl
                date_created: ""

        CommentItem