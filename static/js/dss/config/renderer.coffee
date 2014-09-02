Backbone.Marionette.Renderer.render = (template, data) ->
    throw "Template '" + template + "' not found!"  unless JST[template]
    JST[template] data

_.addTemplateHelpers
    renderCheckbox: (value) ->
        return (if value then "checked" else "")

    renderOptionList: (list) ->

        """
            TODO: Won't get this working without sending the field label down in the REST api
                  Pretty sure I don't really want to do that
        """
        tpl = """
                <div class="checkbox">
                    <label>
                        <input type="checkbox" name="||PROPERTY||[||ITEM||]" class="ace"
                               id="||PROPERTY||[||ITEM||]" <%= renderCheckbox(||PROPERTY||.||ITEM||) %>>
                        <span class="lbl"> Plays</span>
                    </label>
                </div>
            """
        optionList = ""
        _.each list, (item)->
            optionList += tpl.replace("||PROPERTY||", "property").replace("||ITEM||", "item")

        optionList

    isMe: (id) ->
        return utils.isMe(id)

    humanise: (date)->
        moment(date).fromNow()

    secondsToHms: (d) ->
        utils.secondsToHms d

    canHomepage: () ->
        return com.podnoms.settings.canHomepage
