

\### \*\*3. ONNX Model Challenge\*\* (`ONNX\_CHALLENGE.md`)



```markdown

\# Challenge: Suspicious ONNX Model



\## 🔍 Description

Our ML team received this machine learning model from an untrusted source. We need to inspect it for any hidden data or backdoors. Can you find what's hidden inside this ONNX model?



\*\*Difficulty\*\*: Easy-Medium  

\*\*Category\*\*: Reverse Engineering / Forensics  

\*\*Author\*\*: ClawCTF Team  

\*\*Flag Format\*\*: `ClawCTF{...}`



\## 📁 Files Provided

\- `suspicious\_model.onnx` - The machine learning model file



\## 🚀 How to Start

```bash

\# Install required tools

pip install onnx onnxruntime netron



\# View the model structure

netron suspicious\_model.onnx



\# Or inspect with Python

python inspect\_model.py

