# Murloc
Extensible api server

## Example usage
```python
import murloc

# First, define the methods you want murloc to handle.
# They must have (self, params) as the function signature.
# `params` will be a `dict` containing the json request params.
def hello(self, params):
    print("hello, world!")
    return f"params={params}"

def command_set(self, params):
    return '{"err":0,"data":"configuration successful"}'


# Then add the methods to murloc using a `dict` like so.
myroutes = {
    "hello": hello,
    "set": command_set,
}
m = murloc.init(methods=myroutes)

# And start the server.
m.listen()
```

## Syntax
Murloc uses the following api conventions.

### Request format
```javascript
{
    "method": string,
    "params": {
        // any valid json
    }
}
```

### Success response
```javascript
{
    "err": 0,
    "data": {
        // any valid json
    }
}
```

### Error response
```javascript
{
    "err": 1,
    "data": {
        // any valid json
    }
}
```

## Examples
```bash
hero@azeroth:~$ cat test.py
import murloc

def command_equip(self, params):
    print(f"setting {params['variable']}={params['value']}")
    return '{"err":0,"data":null}'

methods = {
    "equip": command_equip,
}
m = murloc.init(methods=methods)

m.listen()
hero@azeroth:~$ python3 test.py
[2023-05-27 20:04:37] [3064]
     ___
    /\  \
   /::\  \       murloc 1.0.0
  /:/\:\  \
 /:/  \:\  \
/:/__/ \:\__\    Running in default mode
\:\  \ /:/  /    Port: 8048
 \:\  /:/  /     PID:  3064
  \:\/:/  /
   \::/  /             Aaaaaughibbrgubugbugrguburgle!
    \/__/

[2023-05-27 20:04:37] [3064] Listening at 127.0.0.1:8048
[2023-05-27 20:04:46] [3068] Connection from ('127.0.0.1', 60516)
setting class=warrior
```

```bash
hero@azeroth:~$ echo '{"method":"equip","params":{"variable":"class","value":"warrior"}}' | nc -q 0 localhost 8048
{"err":0,"data":null}
hero@azeroth:~$ echo '{"method":"dwarf","params":{"variable":"class","value":"warrior"}}' | nc -q 0 localhost 8048
{"err":1,"data":"method not defined"}
hero@azeroth:~$ echo '{"params":{"variable":"class","value":"warrior"}}' | nc -q 0 localhost 8048
{"err":1,"data":"request lacks method"}
hero@azeroth:~$ echo '{"method":"dwarf"}' | nc -q 0 localhost 8048
{"err":1,"data":"request lacks params"}
hero@azeroth:~$
```
