#!/usr/bin/env python3
"""
UtahMosphere Operating System Kernel - Omega-Build v33.0
Omni-Compiler agentic mesh, MCP context bridge, Utah-Omni-Mind sovereign inference.
"""

import os
import sys
import json
import time
import hmac
import hashlib
import socket
import threading
import http.server
import socketserver
import subprocess
import urllib.parse
from typing import Dict, Any, Optional

from utah_lazarus import LazarusEngine
from utah_s3_mesh import get_object, put_object, verify_signature, list_objects, S3_ROOT
from utah_rds_ledger import read as rds_read, write as rds_write
from utah_lambda_engine import invoke as lambda_invoke, register_function
from utah_container_runtime import start_container_server, stop_all_containers
from utahx_proxy import proxy_request
from utah_mesh_engine import UtahNetesMesh, derive_node_hash, MASTER_REGISTRY_FILE

try:
    from quantum_ledger import ledger_guard
    from utah_swarm_protocol import UtahSwarmNode
    from utah_tycoon import tycoon_engine
    from nonce_guard import nonce_guard
    from attestation_guard import HardwareAttestation
    from tpm_lock import TPMLocker
    from ra_tls_attest import RATLSAttestation
    from quote_registry import quote_registry
    from ra_tls_guard import RATLSGuard, ra_tls_guard
    from dht_quote_registry import dht_quote_registry
    from dht_consensus_engine import dht_consensus_engine
    from drift_detector import drift_detector
    from quorum_witness import quorum_witness
    from lazarus_restore import LazarusRestore
    from state_diff_engine import encode_delta, apply_state_delta, state_hash, should_use_delta
    from omni_compiler import SovereignOmniCompiler
    from mcp_omni_bridge import mcp_omni_compiler
    from utah_omni_mind import omni_mind
    from omni_glass import omni_glass
except ImportError:
    print("[Critical] Sovereign modules missing. Ensure all .py components are present.")
    ledger_guard = None
    UtahSwarmNode = None
    tycoon_engine = None
    nonce_guard = None
    HardwareAttestation = None
    TPMLocker = None
    RATLSAttestation = None
    quote_registry = None
    RATLSGuard = None
    ra_tls_guard = None
    dht_quote_registry = None
    dht_consensus_engine = None
    drift_detector = None
    quorum_witness = None
    LazarusRestore = None
    encode_delta = None  # type: ignore
    apply_state_delta = None  # type: ignore
    state_hash = None  # type: ignore
    should_use_delta = None  # type: ignore
    SovereignOmniCompiler = None  # type: ignore
    mcp_omni_compiler = None  # type: ignore
    omni_mind = None  # type: ignore
    omni_glass = None  # type: ignore

UTAH_DATA_DIR = os.environ.get("UTAH_DATA_DIR", "/var/lib/utahmosphere")
UTAHX_CONF_ROOT = os.path.join(UTAH_DATA_DIR, "utahx_mesh")
CONTAINER_DATA_DIR = os.path.join(UTAH_DATA_DIR, "containers")
LAMBDA_ROOT = os.path.join(UTAH_DATA_DIR, "lambda")
RDS_ROOT = os.path.join(UTAH_DATA_DIR, "rds")
SYSTEM_STATE_LOG = os.path.join(UTAH_DATA_DIR, "secure_registry.json")

SYSTEM_INGRESS_PORT = 8999


class UtahmosphereSovereignKernel:
    def __init__(self):
        self.node_identity = socket.gethostname()
        self.system_vector = os.environ.get(
            "UTAH_SECRET_VECTOR", "utah_akashic_sovereign_perimeter_authorization_vector"
        ).encode("utf-8")

        self.ui_state = {
            "node_status": "Active [Omega-Build v33.0 Omni-Mind]",
            "active_workloads": 0,
            "last_voice_command": "Omega-Genesis Protocol Initialized",
            "cluster_health": "Resilient",
            "mutation_count": 0,
            "swarm_peers": 0,
            "tycoon_pending": 0,
            "authorized_nodes": [],
        }

        self._bootstrap_sovereign_paths()
        self._load_cluster_registry()
        self._sync_authorized_nodes_to_registry()

        self.root_vibe = None
        self.swarm_router = None
        self.mesh_engine = None
        self._init_swarm_and_mesh()

        if tycoon_engine:
            tycoon_engine.register_settlement_callback(self._on_tycoon_settlement)

        threading.Thread(target=self._initiate_predictive_janitor, daemon=True).start()
        if drift_detector:
            drift_detector.monitor(self)

        print(f"[{self.node_identity}] Omega-Build v33.0 omni-mind kernel online. World-A excised.")

    def _node_hash(self) -> str:
        if ledger_guard and ledger_guard.ledger.get("root_vibe_hash"):
            return ledger_guard.ledger["root_vibe_hash"]
        return derive_node_hash(self.node_identity)

    def _init_swarm_and_mesh(self):
        if UtahSwarmNode is None:
            return
        node_hash = self._node_hash()
        self.root_vibe = node_hash if ledger_guard and ledger_guard.ledger.get("root_vibe_hash") else None
        auth_guard = ledger_guard.auth_guard if ledger_guard else None
        self.swarm_router = UtahSwarmNode(
            node_hash,
            on_ledger_sync=self._on_swarm_ledger_sync,
            on_attestation=self._on_swarm_attestation,
        )
        self.mesh_engine = UtahNetesMesh(
            node_id=self.node_identity,
            get_registry=lambda: self.cluster_registry,
            apply_registry=self._apply_remote_registry,
            swarm_broadcast=self._broadcast_to_swarm,
            auth_guard=auth_guard,
            node_hash=node_hash,
            vibe_hash=self.root_vibe,
        )
        self._sync_authorized_nodes_to_registry()

        if LazarusRestore:
            LazarusRestore.save_checkpoint(self)

    def get_golden_master(self) -> dict:
        if LazarusRestore:
            return LazarusRestore.get_golden_master(self)
        return {"registry": dict(self.cluster_registry)}

    def apply_state(self, golden_state: dict):
        """Re-apply verified Golden Master state after Lazarus auto-restore."""
        registry = golden_state.get("registry", {})
        if registry:
            self._apply_remote_registry(registry)
        self.cluster_registry.pop("quarantined", None)
        self.cluster_registry.pop("quarantine_reason", None)
        if golden_state.get("quorum_consensus") and dht_consensus_engine:
            dht_consensus_engine.merge_quorum_votes(golden_state["quorum_consensus"])
        if golden_state.get("dht_golden_registry") and dht_quote_registry:
            dht_quote_registry.merge_dht_consensus(golden_state["dht_golden_registry"])
        if drift_detector:
            drift_detector.anchor_golden()
        self._save_registry_unlocked()
        self.trigger_flux_ui_render()

    def _broadcast_to_swarm(self, payload: dict):
        if self.swarm_router:
            if dht_consensus_engine:
                payload["quorum_consensus"] = dht_consensus_engine.export_consensus()
            if dht_quote_registry:
                payload["dht_golden_registry"] = dht_quote_registry.export_golden()
            if state_hash and quorum_witness:
                sh = state_hash(self.cluster_registry)
                payload["state_hash"] = sh
                quorum_witness.record_local_witness(sh)
            if RATLSAttestation:
                vibe = ledger_guard.ledger.get("root_vibe_hash") if ledger_guard else None
                payload = RATLSAttestation.attach_to_message(payload, self.node_identity, vibe_hash=vibe)
            with self.swarm_router._lock:
                for peer_hash in list(self.swarm_router.routing_table.keys())[:8]:
                    self.swarm_router.route_payload_deterministic(peer_hash, payload)

    def _on_swarm_ledger_sync(self, payload: dict):
        if payload.get("type") == "DHT_GOLDEN_SYNC":
            if dht_quote_registry and payload.get("dht_golden_registry"):
                dht_quote_registry.merge_dht_consensus(payload["dht_golden_registry"])
                self.cluster_registry["dht_golden_registry"] = dht_quote_registry.export_golden()
                self._save_registry_unlocked()
            return
        if RATLSAttestation and not RATLSAttestation.verify_mesh_message(payload):
            print("[Swarm Link] RA-TLS rejected DHT ledger sync")
            return
        if ledger_guard and payload.get("mesh_signature"):
            if not ledger_guard.auth_guard.verify_message(payload):
                print("[Swarm Link] Rejected unsigned DHT ledger sync")
                return
        registry = payload.get("registry", {})
        if dht_consensus_engine and payload.get("quorum_consensus"):
            dht_consensus_engine.merge_quorum_votes(payload["quorum_consensus"])
        origin = payload.get("origin_node", "unknown")
        sh = payload.get("state_hash", "")
        if sh and quorum_witness and not quorum_witness.get_consensus(sh):
            print(f"[Witness] Multi-region quorum rejected state sync from {origin}")
            return
        if payload.get("registry_delta") and apply_state_delta:
            delta_pkg = payload["registry_delta"]
            delta = delta_pkg.get("delta", {})
            merged = apply_state_delta(self.cluster_registry, delta)
            self._apply_remote_registry(merged)
        else:
            self._apply_remote_registry(registry)
        print(f"[Swarm Link] DHT state sync from {origin}")

    def _on_swarm_attestation(self, payload: dict, source_hash: str, addr: tuple):
        ptype = payload.get("type")
        if ptype == "ATTESTATION_CHALLENGE" and RATLSAttestation and self.swarm_router:
            quote = RATLSAttestation.generate_quote(
                self.node_identity, vibe_hash=self.root_vibe
            )
            self.swarm_router._send_to(addr[0], addr[1], {
                "type": "ATTESTATION_RESPONSE",
                "quote": quote,
                "peer_id": self.node_identity,
                "hardware_id": self.cluster_registry.get("hardware_id"),
            })
            return
        if ptype == "ATTESTATION_RESPONSE":
            quote = payload.get("quote")
            peer_id = payload.get("peer_id") or source_hash
            if dht_consensus_engine and quote:
                dht_consensus_engine.record_vote(peer_id, quote, self.node_identity)
            if dht_consensus_engine and quote and not dht_consensus_engine.verify_against_quorum(peer_id, quote):
                print(f"[Quorum] Peer {peer_id[:12]} failed majority consensus.")
                hw = payload.get("hardware_id")
                if quote_registry and hw:
                    quote_registry.purge_node(hw, "quorum_mismatch")
                if dht_consensus_engine:
                    dht_consensus_engine.purge_peer(peer_id, "quorum_mismatch")
                elif dht_quote_registry:
                    dht_quote_registry.purge_peer(peer_id, "quorum_mismatch")
            return
        if ptype == "QUARANTINE_NOTICE":
            hw = payload.get("hardware_id")
            peer = payload.get("peer_id", source_hash)
            if quote_registry and hw:
                quote_registry.purge_node(hw, payload.get("reason", "remote_quarantine"))
            if dht_consensus_engine:
                dht_consensus_engine.purge_peer(peer, payload.get("reason", "remote_quarantine"))
            elif dht_quote_registry:
                dht_quote_registry.purge_peer(peer, payload.get("reason", "remote_quarantine"))
            print(f"[DHT-Federation] Swarm quarantine notice for peer {peer[:12]}")

    def emergency_quarantine(self, reason: str = "pcr_drift"):
        """Forces all containers into cryo-stasis upon attestation failure."""
        stopped = stop_all_containers()
        for app in list(self.cluster_registry.get("tenants", {}).keys()):
            tenant = self.cluster_registry["tenants"][app]
            tenant["status"] = "quarantined"
            tenant["quarantine_reason"] = reason
        hw_id = self.cluster_registry.get("hardware_id")
        if quote_registry and hw_id:
            quote_registry.purge_node(hw_id, reason)
        if dht_consensus_engine:
            dht_consensus_engine.purge_peer(self.node_identity, reason)
        elif dht_quote_registry:
            dht_quote_registry.purge_peer(self.node_identity, reason)
        self.cluster_registry["quarantined"] = True
        self.cluster_registry["quarantine_reason"] = reason
        if quote_registry:
            self.cluster_registry["quote_registry"] = quote_registry.export_nodes()
        if dht_consensus_engine:
            self.cluster_registry["quorum_consensus"] = dht_consensus_engine.export_consensus()
        if dht_quote_registry:
            self.cluster_registry["dht_golden_registry"] = dht_quote_registry.export_golden()
        if reason in ("pcr_drift", "quorum_mismatch"):
            status_label = "QUARANTINED: PCR DRIFT / QUORUM MISMATCH"
        else:
            status_label = f"QUARANTINED: {reason.upper()}"
        self.ui_state["node_status"] = status_label
        self.ui_state["cluster_health"] = "Quarantined"
        self._save_registry_unlocked()
        self.trigger_flux_ui_render()
        if self.swarm_router:
            notice = {
                "type": "QUARANTINE_NOTICE",
                "peer_id": self.node_identity,
                "hardware_id": hw_id,
                "reason": reason,
            }
            with self.swarm_router._lock:
                for peer_hash in list(self.swarm_router.routing_table.keys())[:8]:
                    self.swarm_router.route_payload_deterministic(peer_hash, notice)
        print(f"[Kernel] Emergency quarantine ({reason}). Stopped {stopped} container(s).")
        if LazarusRestore:
            LazarusRestore.schedule_auto_restore(self)

    def _sync_authorized_nodes_to_registry(self):
        if not ledger_guard:
            return
        nodes = ledger_guard.get_authorized_nodes()
        self.cluster_registry["authorized_nodes"] = nodes
        self.ui_state["authorized_nodes"] = nodes
        self._save_registry_unlocked()

    def revoke_node(self, node_hash: str) -> bool:
        if not ledger_guard:
            return False
        if not ledger_guard.revoke_node(node_hash):
            return False
        self._sync_authorized_nodes_to_registry()
        if self.mesh_engine:
            self.mesh_engine._auth_guard = ledger_guard.auth_guard
        print(f"[AuthGuard] Node {node_hash[:12]} revoked. Gossip mesh pruned.")
        self.trigger_flux_ui_render()
        return True

    @staticmethod
    def _attestation_snapshot() -> dict:
        snap = HardwareAttestation.status() if HardwareAttestation else {}
        if TPMLocker:
            snap["tpm_lock"] = TPMLocker.status()
        if RATLSAttestation:
            snap["ra_tls"] = RATLSAttestation.status()
        if quote_registry:
            snap["quote_registry"] = quote_registry.stats()
        if dht_consensus_engine:
            snap["quorum"] = dht_consensus_engine.stats()
        if dht_quote_registry:
            snap["dht_federation"] = dht_quote_registry.stats()
        if drift_detector:
            snap["pcr_drift"] = drift_detector.status()
        if quorum_witness:
            snap["witness"] = quorum_witness.stats()
        if LazarusRestore:
            snap["lazarus"] = LazarusRestore.status()
        if omni_glass:
            snap["omni_glass"] = omni_glass.stats()
        if omni_mind:
            snap["omni_mind"] = omni_mind.status()
        return snap

    def _register_hardware_quote(self, acoustic_hash: str):
        if not RATLSAttestation or not quote_registry:
            return
        quote = RATLSAttestation.generate_quote(
            self.node_identity, vibe_hash=acoustic_hash
        )
        try:
            body = json.loads(quote["body"])
        except json.JSONDecodeError:
            return
        hw_id = body.get("hardware_id")
        if not hw_id:
            return
        quote_registry.register_node(
            hw_id,
            json.dumps(quote),
            vibe_hash=acoustic_hash,
            pcr_digest=body.get("pcr0_digest"),
            node_id=self.node_identity,
        )
        if dht_consensus_engine:
            dht_consensus_engine.record_golden(
                self.node_identity,
                quote,
                voter_id=self.node_identity,
            )
        elif dht_quote_registry:
            dht_quote_registry.record_golden(
                self.node_identity,
                quote,
                pcr_digest=body.get("pcr0_digest"),
                hardware_id=hw_id,
            )
        if drift_detector:
            drift_detector.anchor_golden()
        self.cluster_registry["hardware_id"] = hw_id
        self.cluster_registry["quote_registry"] = quote_registry.export_nodes()
        self.cluster_registry["dht_golden_registry"] = (
            dht_quote_registry.export_golden() if dht_quote_registry else {}
        )
        self.cluster_registry["quorum_consensus"] = (
            dht_consensus_engine.export_consensus() if dht_consensus_engine else {}
        )
        self._save_registry_unlocked()
        if LazarusRestore:
            LazarusRestore.save_checkpoint(self)
        print(f"[RA-TLS] Hardware quote registered globally: {hw_id[:16]}...")

    def save_registry(self):
        self._save_registry_unlocked()

    def _apply_remote_registry(self, remote: dict):
        if not remote:
            return
        for key, val in remote.get("tenants", {}).items():
            local = self.cluster_registry.get("tenants", {}).get(key, {})
            if key not in self.cluster_registry.get("tenants", {}) or val.get("epoch", 0) > local.get("epoch", 0):
                self.cluster_registry.setdefault("tenants", {})[key] = val
        if quote_registry and remote.get("quote_registry"):
            quote_registry.merge_remote(remote["quote_registry"])
            self.cluster_registry["quote_registry"] = quote_registry.export_nodes()
        if dht_consensus_engine and remote.get("quorum_consensus"):
            dht_consensus_engine.merge_quorum_votes(remote["quorum_consensus"])
            self.cluster_registry["quorum_consensus"] = dht_consensus_engine.export_consensus()
        if dht_quote_registry and remote.get("dht_golden_registry"):
            dht_quote_registry.merge_dht_consensus(remote["dht_golden_registry"])
            self.cluster_registry["dht_golden_registry"] = dht_quote_registry.export_golden()
        self._save_registry_unlocked()
        if self.swarm_router:
            self.ui_state["swarm_peers"] = self.swarm_router.peer_count()

    def _on_tycoon_settlement(self, tx_id: str, record: dict):
        app_name = record.get("app_target")
        if app_name:
            self.activate_tenant(app_name)
            print(f"[Tycoon] Tenant {app_name} -> active-compute after settlement {tx_id[:8]}")
        self.trigger_flux_ui_render()

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
        claimed = bool(ledger_guard and ledger_guard.ledger.get("root_vibe_hash"))

        if ledger_guard:
            if "claim node" in transcript:
                response = ledger_guard.anchor_root_vibe(acoustic_hash)
                if "mapped" in response and UtahSwarmNode:
                    self.root_vibe = acoustic_hash
                    self._register_hardware_quote(acoustic_hash)
                    self.swarm_router = UtahSwarmNode(
                        acoustic_hash,
                        on_ledger_sync=self._on_swarm_ledger_sync,
                        on_attestation=self._on_swarm_attestation,
                    )
                    self._sync_authorized_nodes_to_registry()
                    if self.mesh_engine:
                        self.mesh_engine.node_hash = acoustic_hash
                        self.mesh_engine._auth_guard = ledger_guard.auth_guard
                return response

            if "authorize node" in transcript:
                parts = transcript.split()
                try:
                    idx = parts.index("node") + 1
                    node_hash = parts[idx]
                    if ledger_guard.authorize_node(node_hash):
                        self._sync_authorized_nodes_to_registry()
                        return f"Node {node_hash[:8]} authorized for mesh gossip."
                    return "Invalid node hash. Expected 64-char vibe-print."
                except Exception:
                    return "Usage: authorize node <64-char-vibe-hash>"

            if nonce_guard and nonce_guard.enforcement_required(claimed) and "claim node" not in transcript:
                nonce = payload.get("nonce")
                command_signature = (
                    payload.get("command_signature")
                    or payload.get("signature", "")
                )
                if nonce is None or not command_signature:
                    return "Access Denied. Fresh nonce and command_signature required (GET /nonce)."
                try:
                    nonce_int = int(nonce)
                except (TypeError, ValueError):
                    return "Access Denied. Invalid nonce format."
                if not nonce_guard.validate_and_process(
                    transcript, nonce_int, command_signature, acoustic_hash
                ):
                    self.ui_state["node_status"] = "SECURITY LOCKDOWN: REPLAY DETECTED"
                    self.trigger_flux_ui_render()
                    return "Access Denied. Nonce replay or signature invalid."

            request_sig = payload.get("request_signature", "")
            if request_sig and not ledger_guard.verify_request_signature(request_sig, transcript):
                self.ui_state["node_status"] = "SECURITY LOCKDOWN: INVALID SIGNATURE"
                self.trigger_flux_ui_render()
                return "Access Denied. Request signature failed AuthGuard validation."

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

        elif "compile" in tokens or "omni" in transcript.lower():
            intent_str = transcript
            for marker in ("compile", "build", "create", "give me"):
                if marker in transcript.lower():
                    intent_str = transcript.lower().split(marker, 1)[-1].strip(" :")
                    break
            if SovereignOmniCompiler is None:
                return "Omni-Compiler unavailable."
            if os.environ.get("UTAH_OMNI_MCP_ENFORCE", "1") != "0" and mcp_omni_compiler:
                result = mcp_omni_compiler.execute_intent_sync(intent_str, kernel_ref=self)
            else:
                result = SovereignOmniCompiler.process_developer_intent(intent_str, kernel_ref=self)
            if result.get("ok"):
                self.ui_state["active_workloads"] = len(self.cluster_registry["tenants"])
                self.ui_state["mutation_count"] += 1
                self.trigger_flux_ui_render()
                return result.get("message", f"Omni-compiled {result.get('app_name')}")
            return f"Omni-Compiler error: {result.get('error', 'unknown')}"

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

        if path == "/app/unlock":
            data = json.loads(body.decode("utf-8")) if body else {}
            app_name = data.get("app_name") or data.get("app", "")
            client_id = data.get("client_id") or self.client_address[0]
            if not app_name:
                self._json_response(400, {"error": "app_name required"})
                return
            if tycoon_engine is None:
                self._json_response(503, {"error": "Tycoon engine unavailable"})
                return
            result = tycoon_engine.submit_unlock_request(
                app_name, client_id, data.get("payment_tx"), data.get("amount_sats", 5000)
            )
            self.send_response(202)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "pending",
                "message": "Payment required. Awaiting ledger consensus.",
                "tx_id": result["tx_id"],
                "payment_address": result["invoice"]["payment_address"],
                "amount_sats": result["invoice"]["amount_sats"],
            }).encode())
            return

        if path == "/admin/revoke-node":
            data = json.loads(body.decode("utf-8")) if body else {}
            node_hash = data.get("node_hash", "")
            acoustic_hash = data.get("acoustic_hash", "")
            if not node_hash or not acoustic_hash:
                self._json_response(400, {"error": "node_hash and acoustic_hash required"})
                return
            if ledger_guard is None:
                self._json_response(503, {"error": "Ledger guard unavailable"})
                return
            root = ledger_guard.ledger.get("root_vibe_hash")
            if not root or not hmac.compare_digest(root, acoustic_hash):
                self._json_response(403, {"error": "Root vibe required for revocation"})
                return
            if self.core_engine.revoke_node(node_hash):
                self._json_response(200, {"status": "revoked", "node_hash": node_hash})
            else:
                self._json_response(404, {"error": "Node not found or cannot revoke root"})
            return

        if path == "/registry/purge":
            data = json.loads(body.decode("utf-8")) if body else {}
            hardware_id = data.get("hardware_id", "")
            acoustic_hash = data.get("acoustic_hash", "")
            if not hardware_id or not acoustic_hash:
                self._json_response(400, {"error": "hardware_id and acoustic_hash required"})
                return
            if ledger_guard is None or quote_registry is None:
                self._json_response(503, {"error": "Registry unavailable"})
                return
            root = ledger_guard.ledger.get("root_vibe_hash")
            if not root or not hmac.compare_digest(root, acoustic_hash):
                self._json_response(403, {"error": "Root vibe required for purge"})
                return
            if quote_registry.purge_node(hardware_id, data.get("reason", "compromised")):
                self.core_engine.cluster_registry["quote_registry"] = quote_registry.export_nodes()
                self.core_engine.save_registry()
                self._json_response(200, {"status": "purged", "hardware_id": hardware_id})
            else:
                self._json_response(404, {"error": "Hardware ID not found"})
            return

        if path == "/omni/compile":
            data = json.loads(body.decode("utf-8")) if body else {}
            intent = data.get("intent") or data.get("transcript", "")
            if not intent or SovereignOmniCompiler is None:
                self._json_response(400, {"error": "intent required and Omni-Compiler must be online"})
                return
            use_mcp = data.get("mcp", True) and mcp_omni_compiler is not None
            if use_mcp:
                mcp_cmd = data.get("mcp_server_command")
                result = mcp_omni_compiler.execute_intent_sync(intent, mcp_cmd, self.core_engine)
            else:
                result = SovereignOmniCompiler.process_developer_intent(intent, self.core_engine)
            self._json_response(200 if result.get("ok") else 422, result)
            return

        if path == "/lazarus/restore":
            if LazarusRestore is None:
                self._json_response(503, {"error": "Lazarus restore unavailable"})
                return
            ok = LazarusRestore.auto_restore(self.core_engine)
            self._json_response(200 if ok else 503, {
                "status": "restored" if ok else "restore_failed",
            })
            return

        if path == "/dht/challenge":
            data = json.loads(body.decode("utf-8")) if body else {}
            peer_hash = data.get("peer_hash", "")
            if not peer_hash or not self.core_engine.swarm_router:
                self._json_response(400, {"error": "peer_hash required and swarm must be online"})
                return
            ok = self.core_engine.swarm_router.challenge_peer_attestation(peer_hash)
            self._json_response(202 if ok else 503, {
                "status": "challenge_sent" if ok else "challenge_failed",
                "peer_hash": peer_hash,
            })
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
                "version": "33.0",
                "build": "omega-build-v33-omni-mind",
                "attestation": self.core_engine._attestation_snapshot(),
            })
            return

        if path == "/registry/quotes":
            if quote_registry is None:
                self._json_response(503, {"error": "Quote registry unavailable"})
                return
            self._json_response(200, {
                "nodes": quote_registry.export_nodes(),
                "stats": quote_registry.stats(),
            })
            return

        if path == "/dht/consensus":
            if dht_quote_registry is None:
                self._json_response(503, {"error": "DHT federation unavailable"})
                return
            body = {
                "golden": dht_quote_registry.export_golden(),
                "stats": dht_quote_registry.stats(),
            }
            if dht_consensus_engine:
                body["quorum"] = dht_consensus_engine.export_consensus()
                body["quorum_stats"] = dht_consensus_engine.stats()
            self._json_response(200, body)
            return

        if path == "/quorum/consensus":
            if dht_consensus_engine is None:
                self._json_response(503, {"error": "Quorum engine unavailable"})
                return
            self._json_response(200, {
                "consensus": dht_consensus_engine.export_consensus(),
                "stats": dht_consensus_engine.stats(),
            })
            return

        if path == "/witness/status":
            if quorum_witness is None:
                self._json_response(503, {"error": "Witness layer unavailable"})
                return
            self._json_response(200, {
                "witnesses": quorum_witness.export_witnesses(),
                "stats": quorum_witness.stats(),
            })
            return

        if path == "/omni/status":
            if omni_mind is None:
                self._json_response(503, {"error": "Omni-Mind unavailable"})
                return
            self._json_response(200, {
                "omni_mind": omni_mind.status(),
                "omni_glass": omni_glass.stats() if omni_glass else {},
            })
            return

        if path == "/omni/glass":
            if omni_glass is None:
                self._json_response(503, {"error": "Omni-Glass unavailable"})
                return
            limit = int(urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get("limit", ["50"])[0])
            self._json_response(200, {
                "events": omni_glass.export(limit=limit),
                "stats": omni_glass.stats(),
            })
            return

        if path == "/lazarus/status":
            if LazarusRestore is None:
                self._json_response(503, {"error": "Lazarus restore unavailable"})
                return
            self._json_response(200, {
                "lazarus": LazarusRestore.status(),
                "golden_master": self.core_engine.get_golden_master(),
            })
            return

        if path == "/attestation/quote":
            if RATLSAttestation is None:
                self._json_response(503, {"error": "RA-TLS unavailable"})
                return
            quote = RATLSAttestation.generate_quote(
                self.core_engine.node_identity,
                vibe_hash=self.core_engine.root_vibe,
            )
            self._json_response(200, {"ra_tls_quote": quote, "hardware_id": self.core_engine.cluster_registry.get("hardware_id")})
            return

        if path == "/nonce":
            if nonce_guard is None:
                self._json_response(503, {"error": "Nonce guard unavailable"})
                return
            issued = nonce_guard.issue_nonce()
            self._json_response(200, {
                "nonce": issued,
                "window_sec": nonce_guard.window_sec,
                "signature_hint": "HMAC-SHA256(acoustic_hash, f'{nonce}:{transcript}')",
            })
            return

        if path == "/status":
            tycoon_stats = tycoon_engine.get_stats() if tycoon_engine else {}
            swarm_peers = self.core_engine.swarm_router.peer_count() if self.core_engine.swarm_router else 0
            self._json_response(200, {
                "ui_state": self.core_engine.ui_state,
                "tenants": list(self.core_engine.cluster_registry.get("tenants", {}).keys()),
                "claimed": self.core_engine.root_vibe is not None,
                "authorized_nodes": self.core_engine.cluster_registry.get("authorized_nodes", []),
                "s3_root": S3_ROOT,
                "master_registry": MASTER_REGISTRY_FILE,
                "swarm_peers": swarm_peers,
                "tycoon": tycoon_stats,
                "attestation": self.core_engine._attestation_snapshot(),
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
                if app_name not in self.core_engine.cluster_registry.get("tenants", {}):
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Application not manifested"}).encode())
                    return
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
                ingress = {k: v for k, v in self.headers.items()}
                status, content, _ = proxy_request(
                    port, sub_path, "GET", ingress_headers=ingress
                )
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
