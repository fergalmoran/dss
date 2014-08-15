@Dss.module "MixApp.Models", (Models, App, Backbone) ->

    class Models.MixCollection extends Backbone.Collection
        model: Models.MixItem
        url:com.podnoms.settings.urlRoot + "mix/?limit=20"

    Models.MixCollection