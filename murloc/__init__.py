"""
Murloc is an extensible api server.

The Murloc api follows the following conventions:

Request:  {"method": String, "params": Object}
Response: {"error": Number, "data": Object}

To define api methods, you can include them as a dict() during init:

```python
# file: main.py
from murloc import Murloc

def hello_world():
    return "hello, world!"

def echo_args(args):
    return args

app = Murloc(methods={"hello":hello_world,"echo":echo_args})
```

Or, optionally, you can also use the route decorator like so:

```python
# file: main.py
from murloc import Murloc

app = Murloc()

@app.route("hello")
def hello_world():
    return "hello, world!"

@app.route("echo")
def echo_args(args):
    return args
```

In either case, you can run murloc with uvicorn like so:

$ uvicorn main:app

Note: This assumes main.py and the Murloc variable to be `app`.
"""
from .murloc import Murloc
