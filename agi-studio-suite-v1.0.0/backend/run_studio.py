# FILE: run_studio.py
# VERSION: v1.0.0-GODCORE
# NAME: AGIStudioRunner
# AUTHOR: Brandon "iambandobandz" Emery x Victor (Fractal Architect Mode)
# PURPOSE: Standalone entrypoint—brings up AGI kernel, trainer, fileops, session, config, utils, launches interactive CLI

from agi_kernel import AGINodeGraph
from agi_trainer import AGITrainer, SGD
from agi_fileops import AGIFileOps
from agi_utils import AGIUtils
from agi_session import AGISession
from agi_config import AGIConfig
import numpy as np

def main():
    AGIUtils.setup_logging()
    AGIUtils.log("Starting AGI Studio Suite GODCORE Edition")
    config = AGIConfig()
    config.load()
    session = AGISession()
    session.load()
    graph = AGINodeGraph()
    loss_fn = lambda pred, target: np.mean((pred - target) ** 2)
    optimizer = SGD(lr=0.01)
    trainer = AGITrainer(graph, loss_fn, optimizer)
    print("AGI Studio is READY. Enter commands (type 'help'):")

    while True:
        cmd = input(">> ").strip().lower()
        if cmd == "help":
            print("""
commands:
  newgraph                - start a new graph
  loadgraph [path]        - load graph from file
  savegraph [path]        - save current graph
  addnode [type]          - add node to graph
  connect [src] [dst]     - connect nodes
  train [epochs]          - train for N epochs (dummy data)
  checkpoint              - save checkpoint
  stats                   - show training stats
  quit/exit               - save session & exit
""")
        elif cmd.startswith("newgraph"):
            graph = AGINodeGraph()
            AGIUtils.log("New graph started")
        elif cmd.startswith("loadgraph"):
            _, path = cmd.split(maxsplit=1)
            graph.load(path)
            AGIUtils.log(f"Graph loaded from {path}")
        elif cmd.startswith("savegraph"):
            _, path = cmd.split(maxsplit=1)
            graph.save(path)
            AGIUtils.log(f"Graph saved to {path}")
        elif cmd.startswith("addnode"):
            _, ntype = cmd.split(maxsplit=1)
            nid = graph.add_node(ntype)
            AGIUtils.log(f"Added node {nid} of type {ntype}")
        elif cmd.startswith("connect"):
            _, src, dst = cmd.split()
            graph.connect(src, dst)
            AGIUtils.log(f"Connected {src} -> {dst}")
        elif cmd.startswith("train"):
            _, epochs = cmd.split()
            epochs = int(epochs)
            # Dummy dataset for demo; replace with real
            X = np.random.randn(100, 4)
            Y = np.eye(4)[np.random.randint(0, 4, size=100)]
            trainer.graph = graph
            trainer.train(X, Y, epochs=epochs)
        elif cmd == "checkpoint":
            trainer.save_checkpoint("checkpoints")
            AGIUtils.log("Checkpoint saved")
        elif cmd == "stats":
            print("Loss history:", trainer.stats["loss"])
            print("Acc history:", trainer.stats["accuracy"])
        elif cmd in {"quit", "exit"}:
            session.set_last_graph("latest_graph.json")
            graph.save("latest_graph.json")
            session.save()
            AGIUtils.log("Session saved. Bye.")
            break
        else:
            print("Unknown command. Type 'help'.")

if __name__ == "__main__":
    main()
