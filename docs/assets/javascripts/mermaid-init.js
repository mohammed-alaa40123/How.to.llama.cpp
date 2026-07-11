document$.subscribe(() => {
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "loose",
    theme: document.body.getAttribute("data-md-color-scheme") === "slate" ? "dark" : "default",
    flowchart: { curve: "basis", htmlLabels: true }
  });
  mermaid.run({ querySelector: ".mermaid" });
});
