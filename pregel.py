from langgraph.pregel import Pregel, NodeBuilder
from langgraph.channels.last_value import LastValue
from langgraph.channels.topic import Topic
from langgraph.checkpoint.memory import InMemorySaver

#define the channels(where current update is stored)
channels ={ 
    "inbox": Topic(str), #a topic channel to broadcast messages to all neighbors
    "counter":LastValue(int)  # only the most recent value is stored
}

def process(input_data):
    messages =input_data.get("inbox",[])
    return {"counter": len(messages)}

def log(input_data):
    messages =input_data.get("inbox", [])
    print(f"Node received {messages}")
    return {}

#now convert the above functions into Pregel nodes using the NodeBuilder
#node1 processor which will subscribe to inbox and write to "counter" to update the state

processor_node = (
    NodeBuilder()
    .subscribe_to("inbox")
    .do(process)
    .write_to("counter")
    .build()
)
logger_node = (
    NodeBuilder()
    .subscribe_to("inbox")
    .do(log)
    .build()
)

memory=InMemorySaver()

#define the Pregel application
app=Pregel(
    nodes={ 
        "processor": processor_node,
        "logger": logger_node
    },
    channels=channels,
    input_channels ="inbox", # here the initial .invoke() data goes
    output_channels= ["counter"], # what .invoke() returns at the end 
    #we will define whcih nodes run after which channel updates
    stream_channels=['inbox']
)
# config which has both recursion limit and thread_id for checkpointing
config={
    "recursion_limit":50,
    "configurable":{"thread_id": "user_session_1"}
}

# The default is usually 25. If your graph is complex, you might need more.
result = app.invoke(["pregel"], config=config) # step control 
print(f"\n output counter: {result}")
