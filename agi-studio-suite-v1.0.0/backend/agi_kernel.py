# FILE: agi_kernel.py
# VERSION: v1.0.0-GODCORE
# NAME: AGIKernel
# AUTHOR: Brandon "iambandobandz" Emery x Victor (Fractal Architect Mode)
# PURPOSE: Modular, future-proof AGI kernel for node-graph, tensor ops, model runtime
import numpy as np
import json
import uuid

class AGINode:
    def __init__(self, node_type, params=None):
        self.id = str(uuid.uuid4())
        self.type = node_type
        self.params = params or {}
        self.inputs = []
        self.outputs = []
        self.data = {}

    def forward(self, *args):
        if self.type == "linear":
            x = args[0]
            w = self.params.get('weight', np.eye(x.shape[-1]))
            b = self.params.get('bias', np.zeros(w.shape[0]))
            return np.dot(x, w.T) + b
        elif self.type == "relu":
            return np.maximum(0, args[0])
        elif self.type == "tanh":
            return np.tanh(args[0])
        elif self.type == "sigmoid":
            return 1/(1+np.exp(-args[0]))
        elif self.type == "softmax":
            exps = np.exp(args[0] - np.max(args[0]))
            return exps / np.sum(exps)
        elif self.type == "add":
            return sum(args)
        elif self.type == "mul":
            out = args[0]
            for a in args[1:]:
                out = out * a
            return out
        elif self.type == "flatten":
            return args[0].reshape(args[0].shape[0], -1)
        elif self.type == "dropout":
            x = args[0]
            p = self.params.get("rate", 0.5)
            mask = np.random.binomial(1, 1-p, size=x.shape)
            return x * mask
        elif self.type == "custom" and "fn" in self.params:
            return self.params["fn"](*args)
        else:
            raise NotImplementedError(f"Node type {self.type} not implemented.")

class AGINodeGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []  # (from, to)

    def add_node(self, node_type, params=None):
        node = AGINode(node_type, params)
        self.nodes[node.id] = node
        return node.id

    def connect(self, src_id, dst_id):
        self.nodes[src_id].outputs.append(dst_id)
        self.nodes[dst_id].inputs.append(src_id)
        self.edges.append((src_id, dst_id))

    def disconnect(self, src_id, dst_id):
        self.nodes[src_id].outputs.remove(dst_id)
        self.nodes[dst_id].inputs.remove(src_id)
        self.edges = [(f, t) for (f, t) in self.edges if not (f==src_id and t==dst_id)]

    def remove_node(self, node_id):
        for src, dst in list(self.edges):
            if src == node_id or dst == node_id:
                self.disconnect(src, dst)
        del self.nodes[node_id]

    def forward(self, input_data):
        node_values = {}
        # Assume single input node(s)
        for node_id, node in self.nodes.items():
            if not node.inputs:
                node_values[node_id] = input_data
        # Traverse graph, topologically
        to_compute = set(self.nodes.keys()) - set(node_values.keys())
        while to_compute:
            progress = False
            for nid in list(to_compute):
                node = self.nodes[nid]
                if all(i in node_values for i in node.inputs):
                    node_args = [node_values[i] for i in node.inputs]
                    node_values[nid] = node.forward(*node_args)
                    to_compute.remove(nid)
                    progress = True
            if not progress:
                raise RuntimeError("Cycle detected or disconnected graph.")
        return node_values

    def save(self, path):
        nodes_serial = {
            k: dict(
                type=v.type, params=v.params, inputs=v.inputs, outputs=v.outputs
            ) for k, v in self.nodes.items()
        }
        with open(path, 'w') as f:
            json.dump({"nodes": nodes_serial, "edges": self.edges}, f, indent=2)

    def load(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        self.nodes = {}
        for nid, nd in data["nodes"].items():
            node = AGINode(nd["type"], nd["params"])
            node.inputs = nd["inputs"]
            node.outputs = nd["outputs"]
            node.id = nid
            self.nodes[nid] = node
        self.edges = data["edges"]
