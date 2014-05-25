Backbone.Marionette.Renderer.render = (template, data) ->
    throw "Template '" + template + "' not found!"  unless JST[template]
    JST[template] data

_.addTemplateHelpers
    renderCheckbox: (value) ->
        return (if value then "checked" else "")

    isMe: (id) ->
        return utils.isMe(id)

    humanise: (date)->
        moment(date).fromNow()

    secondsToHms: (d) ->
        utils.secondsToHms d
