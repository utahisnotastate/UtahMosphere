#!/usr/bin/env python3
"""
UtahMosphere Operating System Kernel - Golden Master Build v25.0
Unified bare-metal sovereign cloud: UtahX, UtahContainerEngine, Lazarus,
UtahNetes, Quantum Ledger, S3 Mesh, Lambda, RDS Ledger, Tycoon Finance.
Replaces Nginx, Docker, and Kubernetes with native Python-to-kernel logic gates.
"""

import os
import sys
import json
import time
import hmac
import hashlib
import socket
import struct
import threading
import http.server
import socketserver
import subprocess
import urllib.parse
from typing import Dict, Any, Optional

from utah_lazarus import LazarusEngine
from utah_s3_mesh import get_object, put_object, verify_signature, list_objects, S3_ROOT
from utah_rds_ledger import read as rds_read, write as rds_write, delete as rds_delete
from utah_lambda_engine import invoke as lambda_invoke, register_function
from utah_container_runtime import start_container_server
from utahx_proxy import proxy_request

try:
    from quantum_ledger import ledger_guard
    from utah_swarm_protocol import UtahSwarmNode
    from utah_tycoon import tycoon_engine
except ImportError:
    print("[Critical] Sovereign modules missing. Ensure all .py components are present.")
    ledger_guard = None
    UtahSwarmNode = None
    tycoon_engine = None

UTAH_DATA_DIR = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")
UTAHX_CONF_ROOT = os.path.join(UTAH_DATA_DIR, "utahx_mesh")
CONTAINER_DATA_DIR = os.path.join(UTAH_DATA_DIR, "containers")
LAMBDA_ROOT = os.path.join(UTAH_DATA_DIR, "lambda")
RDS_ROOT = os.path.join(UTAH_DATA_DIR, "rds")
SYSTEM_STATE_LOG = os.path.join(UTAH_DATA_DIR, "secure_registry.json")

SYSTEM_INGRESS_PORT = 8999
UTAHNETES_GOSSIP_PORT = 9001
MULTICAST_MESH_ADDR = "239.255.43.21"


class UtahmosphereSovereignKernel:
    def __init__(self):
        self.node_identity = socket.gethostname()
        self.system_vector = os.environ.get(
            "UTAH_SECRET_VECTOR", "utah_akashic_sovereign_perimeter_authorization_vector"
        ).encode("utf-8")

        self.ui_state = {
            "node_status": "Active [Golden Master v25.0]",
            "active_workloads": 0,
            "last_voice_command": "Omega-Genesis Protocol Initialized",
            "cluster_health": "Resilient",
            "mutation_count": 0,
        }

        self._bootstrap_sovereign_paths()
        self._load_cluster_registry()

        self.root_vibe = None
        self.swarm_router = None
        if ledger_guard:
            self.root_vibe = ledger_guard.ledger.get("root_vibe_hash")
            if not self.root_vibe:
                print("[Warning] Node unclaimed. Awaiting Biological Signature.")
            else:
                self.swarm_router = UtahSwarmNode(self.root_vibe)

        threading.Thread(target=self._utahnetes_mesh_listener, daemon=True).start()
        threading.Thread(target=self._utahnetes_mesh_broadcaster, daemon=True).start()
        threading.Thread(target=self._initiate_predictive_janitor, daemon=True).start()

        print(f"[{self.node_identity}] UtahMosphere Golden Master Kernel online. World-A excised.")

    def _bootstrap_sovereign_paths(self):
        for path in [UTAH_DATA_DIR, UTAHX_CONF_ROOT, CONTAINER_DATA_DIR, LAMBDA_ROOT, RDS_ROOT, S3_ROOT]:
            try:
                os.makedirs(path, exist_ok=True)
            except PermissionError:
                pass

    def _load_cluster_registry(self):
        default = {"tenants": {}, "ledger": {}, "storage_index": {}, "utahx_routes": {}, "lambda": {}}
        if os.path.exists(SYSTEM_STATE_LOG):
            with open(SYSTEM_STATE_LOG, "r") as f:
                try:
                    self.cluster_registry = json.load(f)
                except Exception:
                    self.cluster_registry = default
        else:
            self.cluster_registry = default
            self._save_registry_unlocked()

    def _save_registry_unlocked(self):
        try:
            with open(SYSTEM_STATE_LOG, "w") as f:
                json.dump(self.cluster_registry, f, indent=4)
        except PermissionError:
            pass

    def _tenant_port(self, app_name: str) -> Optional[int]:
        tenant = self.cluster_registry.get("tenants", {}).get(app_name, {})
        return tenant.get("execution_port") or tenant.get("port")

    def trigger_flux_ui_render(self):
        ui_manifest_path = os.path.join(UTAH_DATA_DIR, "flux_ui_manifest.json")
        try:
            with open(ui_manifest_path, "w") as f:
                json.dump(self.ui_state, f, indent=4)
        except PermissionError:
            with open("flux_ui_manifest.json", "w") as f:
                json.dump(self.ui_state, f, indent=4)

    def execute_voice_intent(self, payload: dict) -> str:
        transcript = payload.get("transcript", "").lower()
        acoustic_hash = payload.get("acoustic_hash", "")
        self.ui_state["last_voice_command"] = transcript

        if ledger_guard:
            if "claim node" in transcript:
                response = ledger_guard.anchor_root_vibe(acoustic_hash)
                if "mapped" in response and UtahSwarmNode:
                    self.swarm_router = UtahSwarmNode(acoustic_hash)
                    self.root_vibe = acoustic_hash
                return response

            if not ledger_guard.verify_vibe_signature(acoustic_hash, transcript):
                self.ui_state["node_status"] = "SECURITY LOCKDOWN: UNAUTHORIZED ENTITY"
                self.trigger_flux_ui_render()
                return "Access Denied. Biological signature does not match the Akashic Record."

        tokens = transcript.split()
        if "deploy" in tokens or "manifest" in tokens:
            try:
                app_name = tokens[tokens.index("app") + 1] if "app" in tokens else tokens[tokens.index("application") + 1]
                response = self.manifest_utah_container(app_name)
                self.ui_state["active_workloads"] = len(self.cluster_registry["tenants"])
                self.trigger_flux_ui_render()
                return response
            except Exception as e:
                return f"Structural translation exception: {str(e)}"

        elif "update" in tokens or "patch" in tokens:
            try:
                app_name = tokens[tokens.index("app") + 1]
                intent_idx = tokens.index("to") + 1
                intent_str = " ".join(tokens[intent_idx:])
                if LazarusEngine.patch_live_logic(app_name, intent_str):
                    self.ui_state["mutation_count"] += 1
                    self.trigger_flux_ui_render()
                    return f"Lazarus AST mutation applied to {app_name}."
                return f"Application {app_name} not found."
            except Exception as e:
                return f"Patch routing error: {str(e)}"

        elif "status" in tokens or "grid" in tokens:
            return json.dumps(self.cluster_registry)

        self.trigger_flux_ui_render()
        return "Linguistic instruction registered but requires additional context parameters."

    def manifest_utah_container(self, app_name: str) -> str:
        print(f"[UtahContainerEngine] Manifesting namespace: {app_name}")
        container_path = os.path.join(CONTAINER_DATA_DIR, app_name)
        os.makedirs(container_path, exist_ok=True)

        handler_path = os.path.join(container_path, "handler.py")
        if not os.path.exists(handler_path):
            with open(handler_path, "w") as f:
                f.write(
                    "def handler(event, context):\n"
                    "    return {'status': 'active', 'app': context.get('app'), 'event': event}\n"
                )

        assigned_port = 8200 + len(self.cluster_registry["tenants"])
        register_function(app_name, None)  # mirror in lambda root for invoke parity

        try:
            start_container_server(app_name, assigned_port, handler_path)
        except Exception as e:
            print(f"[UtahContainerEngine] Runtime start warning: {e}")

        self.cluster_registry["tenants"][app_name] = {
            "runtime_engine": "UtahContainerEngine",
            "execution_port": assigned_port,
            "port": assigned_port,
            "epoch": time.time(),
            "status": "cryo-stasis-ready",
        }
        self._save_registry_unlocked()
        self.apply_utahx_routing_rule(app_name, assigned_port)
        return f"Application anchored on port {assigned_port}. UtahX route manifested."

    def activate_tenant(self, app_name: str):
        if app_name in self.cluster_registry.get("tenants", {}):
            self.cluster_registry["tenants"][app_name]["status"] = "active-compute"
            self._save_registry_unlocked()

    def apply_utahx_routing_rule(self, app_name: str, port: int):
        manifest = {
            "ingress_host": f"{app_name}.utahmosphere.internal",
            "fluid_proxy_target": f"http://127.0.0.1:{port}",
            "tollbooth_cache": "cryo-stasis-active",
            "buffer_optimization": "high-throughput-ram",
        }
        dest = os.path.join(UTAHX_CONF_ROOT, f"{app_name}.utahx.json")
        try:
            with open(dest, "w") as f:
                json.dump(manifest, f, indent=4)
        except PermissionError:
            pass
        self.cluster_registry.setdefault("utahx_routes", {})[app_name] = manifest
        self._save_registry_unlocked()

    def _utahnetes_mesh_broadcaster(self):
        tx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        tx_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        while True:
            try:
                payload = json.dumps({"node": self.node_identity, "registry": self.cluster_registry}).encode()
                tx_socket.sendto(payload, (MULTICAST_MESH_ADDR, UTAHNETES_GOSSIP_PORT))
                if self.swarm_router:
                    with self.swarm_router._lock:
                        neighbors = list(self.swarm_router.routing_table.keys())
                    for neighbor in neighbors:
                        self.swarm_router.send_encrypted_payload(
                            neighbor,
                            {"type": "LEDGER_SYNC", "registry": self.cluster_registry, "origin_node": self.node_identity},
                        )
            except Exception:
                pass
            time.sleep(10)

    def _utahnetes_mesh_listener(self):
        rx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        rx_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        rx_socket.bind(("", UTAHNETES_GOSSIP_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_MESH_ADDR), socket.INADDR_ANY)
        rx_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while True:
            try:
                data, _ = rx_socket.recvfrom(65535)
                message = json.loads(data.decode("utf-8"))
                remote_node = message.get("node")
                if remote_node and remote_node != self.node_identity:
                    for key, val in message["registry"].get("tenants", {}).items():
                        local = self.cluster_registry["tenants"].get(key, {})
                        if key not in self.cluster_registry["tenants"] or val.get("epoch", 0) > local.get("epoch", 0):
                            self.cluster_registry["tenants"][key] = val
                    self._save_registry_unlocked()
            except Exception:
                pass

    def _initiate_predictive_janitor(self):
        while True:
            time.sleep(60)
            try:
                subprocess.run(["docker", "system", "prune", "-f"], capture_output=True)
            except Exception:
                pass


class SovereignIngressMultiplexer(http.server.BaseHTTPRequestHandler):
    core_engine = UtahmosphereSovereignKernel()

    def log_message(self, format, *args):
        return

    def _read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length) if length else b""

    def _json_response(self, status: int, payload: Any):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _raw_response(self, status: int, body: bytes, content_type: str = "application/octet-stream"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        body = self._read_body()

        if path == "/command":
            payload = json.loads(body.decode("utf-8"))
            result = self.core_engine.execute_voice_intent(payload)
            self._json_response(200, {"status": "manifested", "response": result})
            return

        if path == "/rds/write":
            data = json.loads(body.decode("utf-8"))
            result = rds_write(data["key"], data["value"])
            self._json_response(200, result)
            return

        if path.startswith("/lambda/") and path.endswith("/invoke"):
            fn_name = path.split("/")[2]
            event = json.loads(body.decode("utf-8")) if body else {}
            try:
                result = lambda_invoke(fn_name, event)
                self._json_response(200, {"result": result})
            except FileNotFoundError:
                self._json_response(404, {"error": f"Lambda function {fn_name} not found"})
            except Exception as e:
                self._json_response(500, {"error": str(e)})
            return

        if path.startswith("/s3/"):
            self._handle_s3_post(path, body)
            return

        self.send_response(404)
        self.end_headers()

    def do_PUT(self):
        if self.path.startswith("/s3/"):
            self._handle_s3_post(self.path, self._read_body())
            return
        self.send_response(404)
        self.end_headers()

    def _handle_s3_post(self, path: str, body: bytes):
        parts = path.strip("/").split("/", 2)
        if len(parts) < 3:
            self._json_response(400, {"error": "Use /s3/{bucket}/{key}"})
            return
        _, bucket, key = parts
        tenant = self.headers.get("X-Utah-Tenant-ID", "")
        sig = self.headers.get("X-Utah-Signature", "")
        if tenant and sig and not verify_signature(tenant, path, sig):
            self._json_response(403, {"error": "Invalid HMAC signature"})
            return
        result = put_object(bucket, key, body, tenant)
        self._json_response(200, result)

    def do_GET(self):
        client_id = self.headers.get("X-Client-ID", self.client_address[0])
        path = urllib.parse.urlparse(self.path).path

        if path == "/health":
            self._json_response(200, {
                "status": "healthy",
                "node": self.core_engine.node_identity,
                "version": "25.0",
                "build": "golden-master",
            })
            return

        if path == "/status":
            self._json_response(200, {
                "ui_state": self.core_engine.ui_state,
                "tenants": list(self.core_engine.cluster_registry.get("tenants", {}).keys()),
                "claimed": self.core_engine.root_vibe is not None,
                "s3_root": S3_ROOT,
            })
            return

        if path.startswith("/s3/"):
            self._handle_s3_get(path)
            return

        if path.startswith("/rds/read/"):
            key = path.split("/rds/read/", 1)[1]
            value = rds_read(key)
            if value is None:
                self._json_response(404, {"error": "Key not found"})
            else:
                self._json_response(200, {"key": key, "value": value})
            return

        if path.startswith("/lambda/") and not path.endswith("/invoke"):
            fn_name = path.split("/")[2]
            try:
                result = lambda_invoke(fn_name, {"path": path, "method": "GET"})
                self._json_response(200, {"result": result})
            except Exception as e:
                self._json_response(404, {"error": str(e)})
            return

        parts = path.split("/")
        if len(parts) > 2 and parts[1] == "app":
            app_name = parts[2]
            sub_path = "/" + "/".join(parts[3:]) if len(parts) > 3 else "/"

            if tycoon_engine is not None and not tycoon_engine.check_access_authorization(app_name, client_id):
                invoice = tycoon_engine.generate_tollbooth_invoice(app_name, client_id, amount_sats=5000)
                self.send_response(402)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "Payment Required",
                    "payment_address": invoice["payment_address"],
                    "amount_sats": invoice["amount_sats"],
                }).encode())
                return

            if tycoon_engine is not None:
                self.core_engine.activate_tenant(app_name)

            port = self.core_engine._tenant_port(app_name)
            if port:
                status, content, _ = proxy_request(port, sub_path, "GET")
                self._raw_response(status, content, "application/json" if content[:1] == b"{" else "text/plain")
            else:
                self._json_response(404, {"error": f"Tenant {app_name} not found"})
            return

        self.send_response(404)
        self.end_headers()

    def _handle_s3_get(self, path: str):
        parts = path.strip("/").split("/", 2)
        if len(parts) < 3:
            self._json_response(400, {"error": "Use /s3/{bucket}/{key}"})
            return
        _, bucket, key = parts
        if key.endswith("*") or key == "":
            objs = list_objects(bucket, key.rstrip("*"))
            self._json_response(200, {"bucket": bucket, "objects": objs})
            return
        data, err = get_object(bucket, key)
        if err:
            self._json_response(404, {"error": err})
        else:
            self._raw_response(200, data)


def run_master_server(port: int = SYSTEM_INGRESS_PORT):
    class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True

    with ThreadedHTTPServer(("", port), SovereignIngressMultiplexer) as server:
        print(f"[UtahMosphere] Golden Master Kernel online at port {port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == "__main__":
    run_master_server()
