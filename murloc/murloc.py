# MIT License
#
# Copyright (c) 2023 Chris Varga
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json


class Murloc:
    def __init__(self, methods=dict()):
        self.methods = methods

    async def __call__(self, scope, receive, send):
        async def read_body(receive):
            """
            Read and return the entire body from an incoming ASGI message.
            """
            body = b""
            more_body = True
            while more_body:
                message = await receive()
                body += message.get("body", b"")
                more_body = message.get("more_body", False)
            return body

        async def handle_request(method, data):
            """
            Call method if defined. Handle optional data.
            """
            if method not in self.methods:
                return "Method not defined"
            if data:
                # We assume data will be parsable as JSON.
                return self.methods[method](json.loads(data))
            else:
                return self.methods[method]()

        # Main logic begins here.
        assert scope["type"] == "http"
        body = await read_body(receive)
        res = await handle_request(scope["path"], body.decode())
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    (b"content-type", b"text/plain"),
                ],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": str(res).encode(),
            }
        )

    def route(self, rule, **params):
        """
        This is a convenience decorator provided for easy route definitions.
        See help(murloc) for more info on how to use.
        """

        def decorator(func):
            self.methods[rule] = func
            return func

        return decorator
