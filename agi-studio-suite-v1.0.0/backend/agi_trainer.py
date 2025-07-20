# FILE: agi_trainer.py
# VERSION: v1.0.0-GODCORE
# NAME: AGITrainer
# AUTHOR: Brandon "iambandobandz" Emery x Victor (Fractal Architect Mode)
# PURPOSE: Training loop, checkpointing, stat tracking, weight save/restore

import numpy as np
import os
import json
from agi_kernel import AGINodeGraph, AGINode

class AGITrainer:
    def __init__(self, graph: AGINodeGraph, loss_fn, optimizer, batch_size=32):
        self.graph = graph
        self.loss_fn = loss_fn
        self.optimizer = optimizer
        self.batch_size = batch_size
        self.epoch = 0
        self.step = 0
        self.stats = {"loss": [], "accuracy": []}

    def train(self, dataset, labels, epochs=1, checkpoint_dir="checkpoints"):
        n_samples = len(dataset)
        os.makedirs(checkpoint_dir, exist_ok=True)
        for ep in range(epochs):
            idxs = np.random.permutation(n_samples)
            for i in range(0, n_samples, self.batch_size):
                batch_idx = idxs[i:i+self.batch_size]
                x_batch = dataset[batch_idx]
                y_batch = labels[batch_idx]
                # Forward pass
                preds = self.graph.forward(x_batch)
                # Get last node's output
                out_id = list(self.graph.nodes.keys())[-1]
                pred = preds[out_id]
                # Loss and accuracy
                loss = self.loss_fn(pred, y_batch)
                acc = (np.argmax(pred, axis=1) == np.argmax(y_batch, axis=1)).mean()
                self.stats["loss"].append(float(loss))
                self.stats["accuracy"].append(float(acc))
                # Backprop (simple example: SGD)
                self.optimizer.step(self.graph, pred, y_batch)
                self.step += 1
                if self.step % 10 == 0:
                    self.save_checkpoint(checkpoint_dir)
            self.epoch += 1
            print(f"Epoch {self.epoch} done | Loss: {loss:.4f} | Acc: {acc:.4f}")

    def save_checkpoint(self, checkpoint_dir):
        ckpt = {
            "epoch": self.epoch,
            "step": self.step,
            "stats": self.stats,
            "graph": self.serialize_graph(),
        }
        ckpt_path = os.path.join(checkpoint_dir, f"ckpt_{self.epoch}_{self.step}.json")
        with open(ckpt_path, 'w') as f:
            json.dump(ckpt, f, indent=2)

    def load_checkpoint(self, path):
        with open(path, 'r') as f:
            ckpt = json.load(f)
        self.epoch = ckpt["epoch"]
        self.step = ckpt["step"]
        self.stats = ckpt["stats"]
        self.deserialize_graph(ckpt["graph"])

    def serialize_graph(self):
        # Serialize all node params (weights/biases)
        nodes = {}
        for k, node in self.graph.nodes.items():
            params = {}
            for p, v in node.params.items():
                if isinstance(v, np.ndarray):
                    params[p] = v.tolist()
                else:
                    params[p] = v
            nodes[k] = {"type": node.type, "params": params, "inputs": node.inputs, "outputs": node.outputs}
        return {"nodes": nodes, "edges": self.graph.edges}

    def deserialize_graph(self, data):
        self.graph.nodes = {}
        for nid, nd in data["nodes"].items():
            params = {}
            for p, v in nd["params"].items():
                if isinstance(v, list):
                    params[p] = np.array(v)
                else:
                    params[p] = v
            node = AGINode(nd["type"], params)
            node.inputs = nd["inputs"]
            node.outputs = nd["outputs"]
            node.id = nid
            self.graph.nodes[nid] = node
        self.graph.edges = data["edges"]

# Example optimizer: SGD
class SGD:
    def __init__(self, lr=0.01):
        self.lr = lr

    def step(self, graph, preds, targets):
        # Insert your own full backprop/weight update logic as needed
        pass  # Implement or plug in your own
