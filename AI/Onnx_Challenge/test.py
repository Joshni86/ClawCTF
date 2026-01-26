import onnx

# Load the model
model = onnx.load('challenge.onnx')

# Extract the flag from doc_string
flag = model.graph.doc_string
print(f"Flag found: {flag}")

# You can also check other metadata
print(f"Model IR version: {model.ir_version}")
print(f"Producer name: {model.producer_name}")

# Check all graph attributes
for attr in model.graph.attribute:
    print(f"Attribute: {attr.name}")