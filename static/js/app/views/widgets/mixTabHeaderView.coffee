define ['marionette', 'underscore', 'vent', 'text!/tpl/MixTabHeaderView'],
(Marionette, _, vent, Template) ->

    class MixTabHeaderView extends Marionette.ItemView
        template: _.template(Template)

    MixTabHeaderView