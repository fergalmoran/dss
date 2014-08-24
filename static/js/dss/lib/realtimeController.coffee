@Dss.module "Lib", (Lib, App, Backbone, Marionette, $    ) ->
    class Lib.RealtimeController
        startSocketIO: ->
            console.log("RealtimeController: SocketIO starting on " + com.podnoms.settings.REALTIME_HOST)
            if (io?)
                @socket = io.connect(com.podnoms.settings.REALTIME_HOST);

                @socket.on "connect", ->
                    console.log("RealtimeController: Socket connected")

                @socket.on "notification", (data) =>
                    console.log("RealtimeController: notification " + data['message'])
                    utils.showRichMessage("New activity", data['image'], data['message'])
                    App.vent.trigger("model:notification:new", data['message'])
            else
                console.log("Realtime server unavailable")

        registerSessionWithServer: (sessionId) ->
            console.log("Registering session: " + sessionId)

        sendMessage: (message) ->
            console.log("RealtimeController: sendMessage")
            console.log(message)
