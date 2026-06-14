# OTA Lazarus Channel

Over-The-Air (OTA) updates push Golden Master kernel patches to swarm nodes via the deterministic DHT routing layer.

## Push to Swarm Nodes

```python
from utah_swarm_protocol import UtahSwarmNode
from utah_ota_lazarus import push_kernel_to_node

node = UtahSwarmNode("your_node_hash")
push_kernel_to_node(node, "target_peer_hash", "utahmosphere_master.py", version="25.0")
```

## Pull and Verify on Target Node

```python
from utah_ota_lazarus import pull_and_verify, apply_ota_patch

pull_and_verify("/opt/utahmosphere/utahmosphere_master.py", expected_hash, url)
apply_ota_patch({"version": "25.0", "artifact": "utahmosphere_master.py"})
sudo systemctl restart utahmosphere
```

## Environment

| Variable | Purpose |
|----------|---------|
| `UTAH_OTA_KERNEL_URL` | URL to fetch signed kernel artifact |
| `UTAH_INSTALL_DIR` | Install path (default `/opt/utahmosphere`) |

## Swarm Packet Type

OTA manifests use payload type `OTA_LAZARUS` in the Global Swarm DHT. Nodes record metadata in `{UTAH_DATA_DIR}/ota/last_patch.json`.

See [Omega-Build Golden Master](OMEGA_BUILD.md).
