# 🌐 SDN Playground

> A containerized software-defined networking lab built with Ryu, OpenFlow 1.3, Mininet, and Open vSwitch.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?logo=python&logoColor=fff)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ed?logo=docker&logoColor=fff)
![OpenFlow](https://img.shields.io/badge/OpenFlow-1.3-orange)
![License](https://img.shields.io/badge/license-see%20LICENSE-blue)

## 🧭 Overview

This project provides a small, reproducible SDN playground:

- A Ryu controller implements an OpenFlow 1.3 learning switch.
- Mininet creates three hosts connected to one Open vSwitch.
- Docker Compose isolates the controller and network emulator.
- The topology runs `pingAll` automatically and then opens the Mininet CLI.

The original Electron/Vue visual interface described by the repository metadata is not included in the current source tree; this version focuses on the controller and network lab.

## 🏗️ Architecture

```text
┌──────────────────────┐        OpenFlow 1.3        ┌─────────────────────┐
│ controller           │◄───────────────────────────│ mininet             │
│ Ryu / TCP 6633      │                             │ OVSwitch s1         │
└──────────────────────┘                             │ h1  h2  h3          │
                                                     └─────────────────────┘
```

The controller learns source MAC addresses and installs forwarding flows for known destinations. Unknown destinations are flooded through the switch.

## 📁 Project layout

```text
.
├── controller/
│   ├── Dockerfile       # Ryu runtime image
│   └── app.py           # OpenFlow 1.3 learning switch
├── mininet/
│   ├── Dockerfile       # Mininet runtime image
│   └── topology.py      # Three-host topology and CLI
├── docker-compose.yml   # Multi-container lab definition
└── LICENSE
```

## ✅ Requirements

- Docker 24 or newer
- Docker Compose v2
- Linux host recommended
- A host capable of running privileged containers

Mininet creates network namespaces and virtual switches, so the emulator container requires `privileged: true`. Run this project only in a trusted local or disposable environment.

## 🚀 Start the lab

```bash
git clone https://github.com/MitNak25/sdn-playground.git
cd sdn-playground
docker compose up --build
```

The controller is published on TCP port `6633`. The Mininet container connects to the Compose service name `controller`, runs an initial `pingAll`, and opens the CLI.

Useful commands inside the Mininet CLI:

```text
nodes
net
pingall
h1 ping h2
sh ovs-ofctl -O OpenFlow13 dump-flows s1
exit
```

Stop and remove the lab:

```bash
docker compose down
```

If a previous Mininet run left namespaces or switches behind, stop the containers and clean the host according to your Mininet installation before retrying.

## 🔍 How the controller works

1. When a switch connects, the controller installs a table-miss flow that sends packets to the controller.
2. On each packet-in event, the source MAC address is associated with the ingress port.
3. Known destination MAC addresses are forwarded directly and a flow is installed.
4. Unknown destinations use OpenFlow flooding until the destination is learned.

This is an educational learning switch, not a production controller. It does not provide authentication, persistence, multi-switch coordination, or production-grade policy enforcement.

## 🛡️ Safety and troubleshooting

- `privileged: true` is required for Mininet networking and has security implications.
- Port `6633` must be available on the host if you want to connect from outside the Compose network.
- The controller service is reachable from Mininet as `controller`; do not replace it with `localhost` inside the container.
- Use `docker compose logs controller` to inspect Ryu startup messages.
- Use `docker compose logs mininet` to inspect topology and CLI startup.

## 📄 License

See [LICENSE](LICENSE).
