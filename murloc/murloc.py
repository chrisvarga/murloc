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
    """
    Murloc is an extensible api server. See help(murloc) for more info.
    """

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

        async def parse(req):
            """
            Parse a json request for `method` and `params` and call handle().
            """
            err = {"error": 1, "data": None}
            try:
                js = json.loads(req)
            except Exception as e:
                err["data"] = "Invalid json request"
                return json.dumps(err)
            try:
                method = js["method"]
            except:
                err["data"] = "Request missing method"
                return json.dumps(err)
            try:
                params = js["params"]
            except:
                params = None
            return await handle(method, params)

        async def handle(method, params):
            """
            Call method if defined. Handle optional and missing `params` cases.
            """
            if method not in self.methods:
                return json.dumps({"error": 1, "data": "Method not defined"})
            # We could just raise an exception here if they passed params
            # to a method not expecting them. Then they would just get an
            # Internal Error response. But why not handle it gracefully?
            # Similarly for if they don't pass params when they should.
            if params:
                try:
                    return self.methods[method](params)
                except:
                    # If we fail even after giving a second chance, let it die.
                    return self.methods[method]()
            else:
                try:
                    return self.methods[method]()
                except:
                    return json.dumps({"error": 1, "data": "Method expected params"})

        # Main logic begins here.
        assert scope["type"] == "http"
        body = await read_body(receive)
        res = await parse(body)
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
        See help(murloc) for more info.
        """

        def decorator(func):
            self.methods[rule] = func
            return func

        return decorator
