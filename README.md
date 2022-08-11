# Python Server

Python Server Library for NOODLES Protocol

## Description
This server library implements the NOODLES messaging protocol and provides objects for maintaining a scene in state. The server uses a websocket connection to send CBOR encoded messages. To customize its implementation, the library provides convenient interface methods to assist the user in writing their own methods for the server. The user can also add custom delegates to add additionaly functionality to any of the standard components.

## How does the server work?
The server handles incoming websocket connections and maintains a list of clients that are currently connected. After a client has sent an introductory message, they are free to invoke methods disclosed by the server. The server parses each message and attempts to invoke a corresponding message which has been injected by the user. The server calls this method and sends a reply with either a response or an exception. 

```mermaid
sequenceDiagram
    participant User
    participant Server
    participant Method
    participant Client
    User->>Method: Defines Methods and Components
    User->>Server: Starts Server with Starting State
    Client->>Server: Sends Intro Message
    Server->>Client: Updates the Client with Current State
    Client->>Server: Request to Invoke Method
    Server->>Method: Invokes Method
    Method->>Server: Creates, Updates, and Deletes Components
    Server->>Client: Broadcasts Component Changes to All Clients
    Server->>Client: Sends Method Reply with Response or Exception
```

## Getting Started
### 1. Install the server library

```pip install pyserver```

### 2. Define components to be held in the server's starting state
- Use starting component objects to help with the creation of these components
```python
pyserver.StartingComponent(Type[Component], dict[Component_Attr, Value])
```
- You can refer to the objects listed in `noodle_objects.py` to find all the available components along with their mandatory, default, and optional attributes. Additional information on NOODLE components and their attributes can be found [here](https://github.com/InsightCenterNoodles/message_spec)
- When creating methods, an additional callable object should be attached. This method will be injected onto the server object, and it will be associated with its corresponding method component.

```python
pyserver.StartingComponent(Type[Component], dict[Component_Attr, Value], Callable)
```

### 3. Start running the server

```python
asyncio.run(pyserver.start_server(port: [int], starting_state: list[StartingComponent]))
```

## More Info on Creating Methods
The majority of the user's time building a server application will be spent defining methods. To help the user with this process, this library provides several interface methods to reduce friction when interacting with state and the server object. Also it is important to note that each method is injected and called so that the first two arguments are a reference to the server object and the method invoke's context as a dict.

### Interface Methods
```python
server.create_component(comp_type: Type[Component], **kwargs)
server.delete_component(obj: Union[Component, Delegate, ID])
server.update_component(obj: Component, delta: Set[str)
server.invoke_signal(signal: ID, on_component: Component, signal_data: list[Any])
server.get_ids_by_type(component: Type[Component])
server.get_component_id(type: Type[Component], name: str)
```


## Hungry for more NOODLES?
For more information and other related repositories check out [this repository](https://github.com/InsightCenterNoodles)
