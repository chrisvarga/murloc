"""
Murloc is an extensible API server.

To define API methods, use the `route` decorator like so:

```python
# main.py
from murloc import Murloc

app = Murloc()

@app.route("/hello")
def hello_world():
    return "hello, world!"

@app.route("/echo")
def echo_data(data):
    return data
```

You can also specify `methods` directly as a `dict()` during Murloc initialization:

```python
# main.py
from murloc import Murloc

def hello_world():
    return "hello, world!"

def echo_data(data):
    return data

app = Murloc(methods={"/hello": hello_world, "/echo": echo_data})
```

Run the murloc server with uvicorn like so:

```bash
$ uvicorn main:app
```

> Note: These examples assume main.py and the Murloc variable `app`.
"""
from .murloc import Murloc
