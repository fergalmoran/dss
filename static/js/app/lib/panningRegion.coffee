define ['marionette'],
(Marionette) ->

    getPrefixedCssProp = (baseProp) ->
        str = Modernizr.prefixed(baseProp)
        str = str.replace(/([A-Z])/g, (str, m1) ->
            "-" + m1.toLowerCase()
        ).replace(/^ms-/, "-ms-")
        str

    class PanningRegion extends Marionette.Region
        el: "#content"
        initialize: ->
            transEndEventNames =
                WebkitTransition: "webkitTransitionEnd"
                MozTransition: "transitionend"
                OTransition: "oTransitionEnd"
                msTransition: "MSTransitionEnd"
                transition: "transitionend"

            @transEndEventName = transEndEventNames[Modernizr.prefixed("transition")]
            @transformPropName = getPrefixedCssProp("transform")
            console.log @transEndEventName, @transformPropName
            true

        # Very similar to show(), but uses css transition class between views
        transitionToView: (newView, type) ->
            self = this

            # Do we have a view currently?
            view = @currentView
            if not view or view.isClosed
                @show newView
                return
            Marionette.triggerMethod.call this, "willTransition", view

            # Wait for the new view to render, then initialize a transition to
            # show the new view while hiding the old.
            newView.on "render", ->

                # clean up the old listeners, just to ensure we only have 1 active.
                self.$el.off self.transEndEventName

                # Move the new view to an off-screen position using transformation matrix
                translation = undefined

                # Determine the type of transition and build the css transformation.
                if type is "slide"
                    translation = "translateX(100%)"
                else if type is "rotate"
                    translation = "translateX(100%) translateY(100%) rotate(" +
                    ["20", "40", "60", "80", "90"][_.random(0, 4)] + "deg)"
                else translation = "translateY(100%)"  if type is "drop"
                newView.$el.css self.transformPropName, translation

                # Add the new view to the dom
                self.$el.append newView.el

                # Translate the container to show the new element
                $background = jQuery("#world-bg")

                # Find the transformation matrix of each element.
                worldContentMatrix = Matrix.initWithElem(self.$el)
                worldBgMatrix = Matrix.initWithElem($background)
                newViewMatrix = Matrix.initWithElem(newView.$el)

                # Turn on the css animations to enable the transition. We do this here,
                # before the tranision instead of after the transition is complete
                # because it causes less of a visual 'snap' as the pattern moves.
                self.$el.addClass "animated"
                $background.addClass "animated"

                # Given than we know the container has an identity matrix we can transition
                # by simply inverting the matrix of the new view and appyling it to the parent.
                self.$el.css self.transformPropName, newViewMatrix.clone().invert().toMatrixString()

                # Let's make sure the background moves to the same place.
                $background.css self.transformPropName, newViewMatrix.clone().invert().toMatrixString()

                # after transition, clean up by removing the old view, then
                # re-position everything back to a zero-point. There might be a problem
                # relying on the transitionEnd event because there are cases where it
                # does not fire.
                self.$el.on self.transEndEventName, ->
                    self.$el.off self.transEndEventName

                    # clean up the old view
                    self.close()
                    self.currentView = newView

                    # clean up new view and place everything back
                    # to a sane starting position, ready for next transition.
                    self.$el.removeClass "animated"
                    $background.removeClass "animated"
                    self.$el.css self.transformPropName, (new Matrix()).toMatrixString()
                    newView.$el.css self.transformPropName, (new Matrix()).toMatrixString()
                    $background.css "webkit-transform", (new Matrix()).toMatrixString()

                    # do the things show would normally do after showing a new view
                    Marionette.triggerMethod.call newView, "show"
                    Marionette.triggerMethod.call self, "show", newView


            newView.render()
            true

    PanningRegion