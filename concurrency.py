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
    count= len(messages)
    print(f"Processing node counted {count} messages.")
    return {"counter": count}

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
     checkpointer=memory,
)
# config which has both recursion limit and thread_id for checkpointing
config = {"configurable": {"thread_id": "history_demo"}, "recursion_limit": 10}
app.invoke(["msg1", "msg2", "msg3"], config=config)

history =list(app.get_state_history(config))

for snapshot in history:
    step =snapshot.metadata.get("step")
    values =snapshot.values
    print(f"past checkpoint, steps {step}, values: {values}")

print("\n updating the past values")
app.update_state(config, {"counter": 50}, as_node="processor")
final_state =app.get_state(config)

print(f"the new current state is {final_state.values}")
print("\n lesssgo")
