SockJS-tornado server
=====================

SockJS-tornado is a Python server side counterpart of [SockJS-client browser library](https://github.com/sockjs/sockjs-client)
running on top of [Tornado](http://tornadoweb.org>) framework.

Simplified echo SockJS server could look more or less like::

    from tornado import web, ioloop
    from sockjs.tornado import SockJSRouter, SockJSConnection

    class EchoConnection(SockJSConnection):
        def on_message(self, msg):
            self.send(msg)

    if __name__ == '__main__':
        EchoRouter = SockJSRouter(EchoConnection, '/echo')

        app = web.Application(EchoRouter.urls)
        app.listen(9999)
        ioloop.IOLoop.instance().start()

(Take look at [examples](https://github.com/MrJoes/sockjs-tornado/tree/master/examples>) for a complete version).

Subscribe to [SockJS mailing list](https://groups.google.com/forum/#!forum/sockjs>) for discussions and support.

SockJS-tornado API
------------------

SockJS provides slightly different API than _tornado.websocket_. Main differences are:

1.  Depending on transport, actual client connection might or might not be there. So, there is no _self.request_ and
    other _tornado.web.RequestHandler_ properties.
2.  Changed _open_ callback name to _on\_open_ to be more consistent with other callbacks.
3.  Instead of _write\_message_, all messages are sent using _send_ method. Just in case, _send_ in _tornado.web.RequestHandler_
    sends raw data over the connection, without encoding it.
4.  There is handy _broadcast_ function, which accepts list (or iterator) of clients and message to send.

Settings
--------

You can pass various settings to the _SockJSRouter_, in a dictionary::

    MyRouter = SockJSRouter(MyConnection, '/my', dict(disabled_transports=['websocket']))

Following options are supported:

<table>
    <tr>
        <td>*Name*</td>
        <td>*Description*</td>
        <td>*Default Value*</td>
    </tr>
    <tr>
        <td>session_check_interval</td>
        <td>How often sessions are verified, in seconds. Lower the value, more resources sockjs-tornado will use to drop expired sessions, but will be more precise.</td>
        <td>1</td>
    </tr>
    <tr>
        <td>disconnect_delay</td>
        <td>How long does it takes to consider session dead, in seconds.</td>
        <td>5</td>
    </tr>
    <tr>
        <td>heartbeat_delay</td>
        <td>How often sockjs-tornado should send heartbeats to the client, in seconds.</td>
        <td>25</td>
    </tr>
    <tr>
        <td>disabled_transports</td>
        <td>List of disabled transports. Possible values are: 'websocket', 'xhr', 'xhr_streaming', 'jsonp', 'eventsource' and 'htmlfile'</td>
        <td>[]</td>
    </tr>
    <tr>
        <td>sockjs_url</td>
        <td>Location of the sockjs client script. By default points to the SockJS CDN.</td>
        <td>http://cdn.sockjs.org/sockjs-0.1.2.min.js</td>
    </tr>
</table>


Deployment
----------

sockjs-tornado properly works behind haproxy and it is recommended deployment approach.

Sample configuration file can be found [here](https://raw.github.com/sockjs/sockjs-node/master/examples/haproxy.cfg).

If your log is full of "WARNING: Connection closed by the client", pass _no\_keep\_alive_ as _True_ to _HTTPServer_ constructor::

    HTTPServer(app, no_keep_alive=True).listen(port)

or::

    app.listen(port, no_keep_alive=True)

