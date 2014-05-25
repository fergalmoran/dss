@Dss.module "UserApp.Models", (Models, App, Backbone, Marionette, $    ) ->
    class Models.UserCollection extends Backbone.Collection
        model: Models.UserItem
        page: 0
        limit: 20
        url: ->
            com.podnoms.settings.urlRoot + "user/?limit=" + @limit + "&offset=" + Math.max(@page-1, 0) * @limit

