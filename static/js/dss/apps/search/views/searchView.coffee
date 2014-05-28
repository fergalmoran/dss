@Dss.module "SearchApp.Views", (Views, App, Backbone, Marionette, $, _, vent) ->
    class Views.SearchView extends Marionette.CompositeView
        template: "search"

        itemView: Views.SearchItemView
        itemViewEl: "#search-results"

        ui:
            searchText: '#search-text'

        events:
            'keyup #search-text': 'doSearch'
            'blur #search-text': 'closeSearch'

        engine:
            compile: (template) ->
                compiled = _.template(template)
                render: (context) ->
                    compiled context

        closeSearch: () ->
            $(@itemViewEl).fadeOut()

        appendHtml: ->
            console.log("Appending html")

        doSearch: () ->
            inputString = @ui.searchText.val()
            if inputString.length is 0
                $(@itemViewEl).fadeOut()
            else
                results = new App.MixApp.Models.MixCollection()
                results.fetch
                    data: $.param(
                        limit: "4"
                        title__icontains: inputString
                    )
                    success: (data) =>
                        $(@itemViewEl).find("li:gt(0)").remove()
                        $(@itemViewEl).fadeIn()
                        results.each (item)=>
                            view = new Views.SearchItemView({model: item})
                            data = view.serializeData();
                            data = view.mixinTemplateHelpers(data);

                            template = view.getTemplate();
                            html = Marionette.Renderer.render(template, data);
                            $(@itemViewEl).append html
                        return

    Views.SearchView