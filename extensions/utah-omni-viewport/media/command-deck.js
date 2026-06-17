(function () {
  const vscode = acquireVsCodeApi();
  const input = document.getElementById("protocol-input");
  const output = document.getElementById("output");

  document.querySelectorAll(".proto-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const protocol = btn.dataset.protocol;
      const needsInput = btn.dataset.needsInput === "true";
      let value = input.value.trim();
      if (needsInput && !value) {
        value = prompt("Intent for " + btn.textContent + ":") || "";
      }
      vscode.postMessage({ type: "dispatch", protocol, input: value });
    });
  });

  document.getElementById("kernel-health").addEventListener("click", () => {
    vscode.postMessage({ type: "kernelHealth" });
  });

  document.getElementById("entropy-scan").addEventListener("click", () => {
    vscode.postMessage({ type: "entropyScan" });
  });

  window.addEventListener("message", (e) => {
    if (e.data.type === "log") output.textContent = e.data.text;
  });
})();
