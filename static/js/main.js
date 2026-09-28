// Nivela — interações básicas de UI
// 1) Anima as barras de progresso (XP/nivelamento) do valor 0 até o alvo,
//    reaproveitando o mesmo elemento .progress-bar que já existe no Bootstrap.
// 2) Fecha alertas de mensagens (sucesso/erro) automaticamente após alguns segundos.

document.addEventListener("DOMContentLoaded", function () {
  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  // --- Animação das barras de progresso ---
  document.querySelectorAll(".progress-bar").forEach(function (bar) {
    const targetWidth = bar.style.width || bar.getAttribute("aria-valuenow") + "%";

    if (prefersReducedMotion) {
      bar.style.width = targetWidth;
      return;
    }

    bar.style.width = "0%";
    // pequeno delay para o navegador registrar o estado inicial antes de animar
    requestAnimationFrame(function () {
      bar.style.transition = "width 0.8s ease-out";
      bar.style.width = targetWidth;
    });
  });

  // --- Fecha alertas de mensagens automaticamente ---
  document.querySelectorAll(".alert").forEach(function (alertEl) {
    setTimeout(function () {
      const closeBtn = alertEl.querySelector(".btn-close");
      if (closeBtn) {
        closeBtn.click();
      }
    }, 6000);
  });
});