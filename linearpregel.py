from langgraph.pregel import Pregel, NodeBuilder
from langgraph.channels.binop import BinaryOperatorAggregate
from langgraph.channels.topic import Topic

# Step C: The Gatekeeper (Reducer)
def gatekeeper(current: int, new: int) -> int:
    c = current if isinstance(current, int) else 0
    n = new if isinstance(new, int) else 0
    return max(c, n)

# Define separate channels to avoid the loop
channels = {
    "inbox": Topic(int),              # Trigger channel
    "counter": BinaryOperatorAggregate(int, gatekeeper) # State channel
}

# Step C: Execute Phase
def worker1(input_data):
    # We read from 'inbox' (the list of inputs)
    print(f"Worker1 running...")
    return {"counter": 10}

def worker2(input_data):
    print(f"Worker2 running...")
    return {"counter": 5}

# Step C: Plan Phase (Subscribe to 'inbox' instead of 'counter')
node1 = NodeBuilder().subscribe_to("inbox").do(worker1).write_to("counter").build()
node2 = NodeBuilder().subscribe_to("inbox").do(worker2).write_to("counter").build()

app = Pregel(
    nodes={"w1": node1, "w2": node2},
    channels=channels,
    input_channels="inbox",        # Start here
    output_channels=["counter"]    # End here
)

config = {"recursion_limit": 5}

# Invoke with a list because 'inbox' is a Topic channel
result = app.invoke([0], config=config)
print(f"\nFinal State (Max Value): {result}")