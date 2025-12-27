from langgraph.pregel import Pregel, NodeBuilder
from langgraph.channels.binop import BinaryOperatorAggregate

# 1. The Gatekeeper (Reducer)
def gatekeeper(current: int, new: any) -> int:
    # Ensure we extract the int from potential dict input
    new_val = new.get("counter", 0) if isinstance(new, dict) else new
    
    # If the new value is None or we are just starting
    if new_val is None: return current or 0
    
    current_val = current if isinstance(current, int) else 0
    return max(current_val, new_val)

channels = {
    "counter": BinaryOperatorAggregate(int, gatekeeper)
}

# 2. The Workers
def worker1(input_data):
    val = input_data.get("counter", 0) if isinstance(input_data, dict) else input_data
    if val < 10:
        print(f"Worker1 updating {val} -> 10")
        return {"counter": 10} # Explicitly return a dict for the write
    return {} # Returning EMPTY dict tells Pregel NOT to write anything

def worker2(input_data):
    val = input_data.get("counter", 0) if isinstance(input_data, dict) else input_data
    if val < 5:
        print(f"Worker2 updating {val} -> 5")
        return {"counter": 5}
    return {}

# 3. Building the Graph
# Remove the .write_to("counter") from the builder because 
# the workers are now returning the channel name in a dict
node1 = (
    NodeBuilder()
    .subscribe_to("counter")
    .do(worker1)
    .build()
)

node2 = (
    NodeBuilder()
    .subscribe_to("counter")
    .do(worker2)
    .build()
)

app = Pregel(
    nodes={"w1": node1, "w2": node2},
    channels=channels,
    input_channels="counter",
    output_channels=["counter"]
)

# 4. Run it
config = {"recursion_limit": 50}

# Step-by-step logic:
# 1. Starts at 0. Workers return {'counter': 10} and {'counter': 5}.
# 2. Gatekeeper resolves to 10.
# 3. Workers trigger again. This time they return {}.
# 4. Pregel sees no writes. THE LOOP STOPS.
result = app.invoke({"counter": 0}, config=config)
print(f"Final State: {result}")