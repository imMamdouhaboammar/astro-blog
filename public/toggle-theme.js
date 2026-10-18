// Light-only Arabic reading interface: enforce light mode and prevent stored dark theme
try {
  localStorage.removeItem("theme");
} catch (_) {}
document.documentElement.setAttribute("data-theme", "light");
