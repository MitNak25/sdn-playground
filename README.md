# SDN Playground

Minimal Dockerized SDN playground with a Ryu OpenFlow 1.3 learning switch and a Mininet topology.

## Requirements

- Docker 24+
- Docker Compose v2
- Linux host recommended; Mininet requires privileged networking

## Run

```bash
docker compose up --build
```

The Mininet container runs `pingAll` and opens its CLI. Use `nodes`, `net`, or `h1 ping h2`; exit with `exit`. The controller listens on port 6633. The original Electron/Vue visual interface is not included in this repository.

## Services

- `controller`: Ryu OpenFlow 1.3 controller on TCP port 6633.
- `mininet`: three-host Mininet topology connected to one Open vSwitch.

The Mininet container runs with elevated privileges because it creates network namespaces and virtual switches. Use this demo only in a trusted local environment.
