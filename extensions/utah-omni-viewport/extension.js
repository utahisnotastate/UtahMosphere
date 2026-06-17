const vscode = require("vscode");
const { execFile } = require("child_process");
const path = require("path");
const http = require("http");
const https = require("https");

/** @type {Map<string, vscode.WebviewView>} */
const views = new Map();

const PROTOCOLS = {
  cascade: {
    title: "Cascade Sync",
    build: (input) =>
      `[PROTOCOL: CASCADE]\nHolographic Sync. Trace this change across the entire UtahMosphere stack (kernel routes, RDS, S3, Flux UI, docs, verify script). Use utah_godeye MCP before editing.\n\nIntent: ${input || "Describe the schema or model change"}`,
  },
  absorb: {
    title: "Absorb",
    build: (input) =>
      `[PROTOCOL: ABSORB]\nAssimilate the provided foreign code into UtahMosphere native stack per .cursor/memory.md.\n\nTarget: ${input || "paste snippet or repo path"}`,
  },
  voidfill: {
    title: "Void Fill",
    build: (input) =>
      `[PROTOCOL: VOID-FILL]\nDo not write code yet. Use utahclaw_ambient_mesh MCP to research, then synthesize MCP tool.\n\nConcept: ${input || "unknown API or library"}`,
  },
  chronofix: {
    title: "Chrono Fix",
    build: () =>
      `[PROTOCOL: CHRONO-FIX]\nTime-Reversal Debugging. Read last terminal error, revert paradox, apply structural fix, re-run. Use chrono_state patterns if post-deploy failed.`,
  },
  entropypurge: {
    title: "Entropy Purge",
    build: () =>
      `[PROTOCOL: ENTROPY-PURGE]\nRun zeo_entropy.suggest_collapse_targets. Rewrite top 3 hotspots. Log to .cursor/memory.md. ADR if systemic.`,
  },
  schism: {
    title: "Schism",
    build: (input) =>
      `[PROTOCOL: SCHISM]\nDecouple module into UtahContainerEngine microservice. God-Eye blast radius, rewrite imports, log_schism_decision ADR.\n\nModule: ${input || "module_name"}`,
  },
  vibeshift: {
    title: "Vibe Shift",
    build: (input) =>
      `[PROTOCOL: VIBE-SHIFT]\nRestyle flux_gui.py / UI only. DO NOT change state logic. Aesthetic: ${input || "describe aesthetic"}`,
  },
  immortalize: {
    title: "Immortalize",
    build: () =>
      `[PROTOCOL: IMMORTALIZE]\nGenerate edge-case tests, log_architectural_decision ADR, output semantic git commit command. Do not commit unless user asks.`,
  },
  evolve: {
    title: "Evolve Folder",
    build: (input) =>
      `[PROTOCOL: EVOLVE-FOLDER]\nAutonomously evolve this project folder: prune debt, sync docs/locales, update capability matrix, run verify.\n\nFolder scope: ${input || "current workspace"}`,
  },
};

function getWorkspaceRoot() {
  const folders = vscode.workspace.workspaceFolders;
  return folders?.[0]?.uri.fsPath || "";
}

function getConfig() {
  const cfg = vscode.workspace.getConfiguration("utahOmniViewport");
  return {
    kernelBase: cfg.get("kernelBase", "http://127.0.0.1:8999"),
    pythonPath: cfg.get("pythonPath", "py"),
    inspirationRoots: cfg.get("inspirationRoots", []),
  };
}

function httpGet(url) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith("https") ? https : http;
    lib
      .get(url, (res) => {
        let data = "";
        res.on("data", (c) => (data += c));
        res.on("end", () => resolve({ status: res.statusCode, body: data }));
      })
      .on("error", reject);
  });
}

async function dispatchToComposer(prompt) {
  await vscode.env.clipboard.writeText(prompt);
  const commands = [
    "composer.createNew",
    "aichat.newchataction",
    "workbench.action.chat.open",
  ];
  for (const cmd of commands) {
    try {
      await vscode.commands.executeCommand(cmd);
      break;
    } catch (_) {
      /* Cursor/VS Code command availability varies */
    }
  }
  vscode.window.showInformationMessage(
    "Omni-Viewport: protocol prompt copied. Open Composer (Ctrl+I) and paste."
  );
}

function runPythonScript(args) {
  const root = getWorkspaceRoot();
  const script = path.join(root, "scripts", "inspiration_scanner.py");
  const { pythonPath } = getConfig();
  return new Promise((resolve, reject) => {
    execFile(pythonPath, [script, ...args, "--json"], { cwd: root, maxBuffer: 8 * 1024 * 1024 }, (err, stdout, stderr) => {
      if (err) return reject(new Error(stderr || err.message));
      try {
        resolve(JSON.parse(stdout));
      } catch {
        resolve({ ok: true, raw: stdout });
      }
    });
  });
}

function getWebviewHtml(webview, extensionUri, panel) {
  const scriptUri = webview.asWebviewUri(
    vscode.Uri.joinPath(extensionUri, "media", panel === "deck" ? "command-deck.js" : "inspiration-forge.js")
  );
  const styleUri = webview.asWebviewUri(
    vscode.Uri.joinPath(extensionUri, "media", "omni-viewport.css")
  );
  const csp = `default-src 'none'; style-src ${webview.cspSource} 'unsafe-inline'; script-src ${webview.cspSource};`;
  const body = panel === "deck" ? getDeckBody() : getForgeBody();
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="Content-Security-Policy" content="${csp}">
  <link rel="stylesheet" href="${styleUri}">
</head>
<body>${body}<script src="${scriptUri}"></script></body>
</html>`;
}

function getDeckBody() {
  const buttons = Object.entries(PROTOCOLS)
    .map(([id, p]) => {
      const needsInput = !["chronofix", "entropypurge", "immortalize"].includes(id);
      return `<button class="proto-btn" data-protocol="${id}" data-needs-input="${needsInput}">${p.title}</button>`;
    })
    .join("\n");
  return `
    <div class="panel">
      <h1>Command Deck</h1>
      <p class="sub">Press a button — no slash commands. Prompt ships to Composer.</p>
      <input id="protocol-input" class="input" placeholder="Optional intent (module, feature, aesthetic…)" />
      <div class="grid">${buttons}</div>
      <div class="row">
        <button id="kernel-health" class="secondary">Kernel Health</button>
        <button id="entropy-scan" class="secondary">Entropy Scan</button>
      </div>
      <pre id="output" class="output"></pre>
    </div>`;
}

function getForgeBody() {
  return `
    <div class="panel">
      <h1>Inspiration Forge</h1>
      <p class="sub">Select codebases, mine patterns, plan new features.</p>
      <textarea id="roots" class="textarea" placeholder="One folder per line&#10;C:\\code\\OldProject&#10;C:\\code\\AnotherRepo"></textarea>
      <input id="feature-hint" class="input" placeholder="New feature to plan (e.g. real-time chat WebSocket)" />
      <div class="row">
        <button id="add-workspace" class="secondary">+ Workspace</button>
        <button id="scan-inspiration" class="primary">Scan &amp; Plan</button>
        <button id="send-plan" class="primary">Send Plan to Composer</button>
      </div>
      <button id="evolve-folder" class="proto-btn full">Evolve Project Folder</button>
      <pre id="forge-output" class="output"></pre>
    </div>`;
}

function setupDeckWebview(webviewView, extensionUri) {
  webviewView.webview.options = { enableScripts: true };
  webviewView.webview.html = getWebviewHtml(webviewView.webview, extensionUri, "deck");

  webviewView.webview.onDidReceiveMessage(async (msg) => {
    const out = webviewView.webview;
    try {
      if (msg.type === "dispatch") {
        const proto = PROTOCOLS[msg.protocol];
        if (!proto) return;
        const prompt = proto.build(msg.input || "");
        await dispatchToComposer(prompt);
        out.postMessage({ type: "log", text: `Dispatched: ${proto.title}` });
      } else if (msg.type === "kernelHealth") {
        const { kernelBase } = getConfig();
        const res = await httpGet(`${kernelBase}/health`);
        out.postMessage({ type: "log", text: res.body.slice(0, 800) });
      } else if (msg.type === "entropyScan") {
        const root = getWorkspaceRoot();
        const script = path.join(root, "scripts", "mcp_zeo_entropy.py");
        const { pythonPath } = getConfig();
        execFile(
          pythonPath,
          ["-c", `import sys; sys.path.insert(0,'scripts'); from mcp_zeo_entropy import scan_project_entropy; print(scan_project_entropy('.'))`],
          { cwd: root },
          (err, stdout) => {
            out.postMessage({ type: "log", text: err ? String(err) : stdout });
          }
        );
      }
    } catch (e) {
      out.postMessage({ type: "log", text: String(e) });
    }
  });
}

function setupForgeWebview(webviewView, extensionUri) {
  webviewView.webview.options = { enableScripts: true };
  webviewView.webview.html = getWebviewHtml(webviewView.webview, extensionUri, "forge");

  webviewView.webview.onDidReceiveMessage(async (msg) => {
    const out = webviewView.webview;
    const root = getWorkspaceRoot();
    try {
      if (msg.type === "addWorkspace") {
        out.postMessage({ type: "appendRoot", path: root });
      } else if (msg.type === "scan") {
        const dirs = (msg.roots || "").split("\n").map((s) => s.trim()).filter(Boolean);
        const result = await runPythonScript([...dirs, "--feature", msg.feature || ""]);
        const text = result.feature_plan_markdown || JSON.stringify(result.tag_index, null, 2);
        out.postMessage({ type: "forgeResult", text, raw: result });
      } else if (msg.type === "sendPlan") {
        const prompt = `[PROTOCOL: INSPIRATION-PLAN]\nUse this cross-codebase analysis to plan and implement the feature. Read .cursor/memory.md first.\n\n${msg.plan}`;
        await dispatchToComposer(prompt);
      } else if (msg.type === "evolve") {
        const prompt = PROTOCOLS.evolve.build(msg.roots || root);
        await dispatchToComposer(prompt);
      }
    } catch (e) {
      out.postMessage({ type: "log", text: String(e) });
    }
  });
}

function activate(context) {
  const extensionUri = context.extensionUri;

  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider("utahOmniViewport.commandDeck", {
      resolveWebviewView(webviewView) {
        setupDeckWebview(webviewView, extensionUri);
      },
    })
  );

  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider("utahOmniViewport.inspirationForge", {
      resolveWebviewView(webviewView) {
        setupForgeWebview(webviewView, extensionUri);
      },
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("utahOmniViewport.openCommandDeck", () => {
      vscode.commands.executeCommand("utahOmniViewport.commandDeck.focus");
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("utahOmniViewport.openInspirationForge", () => {
      vscode.commands.executeCommand("utahOmniViewport.inspirationForge.focus");
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("utahOmniViewport.dispatchCascade", async () => {
      const input = await vscode.window.showInputBox({ prompt: "Cascade intent" });
      await dispatchToComposer(PROTOCOLS.cascade.build(input || ""));
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("utahOmniViewport.dispatchEntropyPurge", async () => {
      await dispatchToComposer(PROTOCOLS.entropypurge.build());
    })
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
