(function () {
  const vscode = acquireVsCodeApi();
  const roots = document.getElementById("roots");
  const featureHint = document.getElementById("feature-hint");
  const output = document.getElementById("forge-output");
  let lastPlan = "";

  document.getElementById("add-workspace").addEventListener("click", () => {
    vscode.postMessage({ type: "addWorkspace" });
  });

  document.getElementById("scan-inspiration").addEventListener("click", () => {
    vscode.postMessage({
      type: "scan",
      roots: roots.value,
      feature: featureHint.value.trim(),
    });
  });

  document.getElementById("send-plan").addEventListener("click", () => {
    if (!lastPlan) {
      output.textContent = "Run Scan & Plan first.";
      return;
    }
    vscode.postMessage({ type: "sendPlan", plan: lastPlan });
  });

  document.getElementById("evolve-folder").addEventListener("click", () => {
    vscode.postMessage({ type: "evolve", roots: roots.value.split("\n")[0] || "" });
  });

  window.addEventListener("message", (e) => {
    if (e.data.type === "appendRoot" && e.data.path) {
      const lines = roots.value.trim();
      roots.value = lines ? lines + "\n" + e.data.path : e.data.path;
    }
    if (e.data.type === "forgeResult") {
      lastPlan = e.data.text;
      output.textContent = e.data.text;
    }
    if (e.data.type === "log") output.textContent = e.data.text;
  });
})();
