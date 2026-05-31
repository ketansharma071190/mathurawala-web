const header = document.querySelector("[data-header]");

const setHeader = () => {
  header.classList.toggle("is-scrolled", window.scrollY > 24);
};

setHeader();
window.addEventListener("scroll", setHeader, { passive: true });

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener("click", () => {
    document.activeElement?.blur();
  });
});
