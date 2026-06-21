// Apply highlight.js to inline <code> elements (not inside <pre>)
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('code:not(pre code)').forEach(function (el) {
    hljs.highlightElement(el);
  });
});
