define ['marionette', 'underscore', 'vent', 'text!/tpl/MixTabHeaderView'],
(Marionette, _, vent, Template) ->

    class MixTabHeaderView extends Marionette.ItemView
        template: _.template(Template)

        initialize: ->
            @listenTo(vent, "mix:showlist", @tabChanged)

        tabChanged: (options) ->
            $('#mix-tab li[id=li-' + options.order_by + ']', @el).addClass('active')
            true


    MixTabHeaderView