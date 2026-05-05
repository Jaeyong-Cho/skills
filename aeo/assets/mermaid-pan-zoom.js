(function () {
    function initMermaidPanZoom() {
        document.querySelectorAll('.mermaid').forEach(function (el) {
            if (el.dataset.panzoom) return;
            el.dataset.panzoom = '1';

            var wrapper = document.createElement('div');
            wrapper.className = 'mermaid-wrapper';
            wrapper.style.width = '100%';

            var inner = document.createElement('div');
            inner.className = 'mermaid-inner';

            el.parentNode.insertBefore(wrapper, el);
            inner.appendChild(el);
            wrapper.appendChild(inner);

            var controls = document.createElement('div');
            controls.className = 'mermaid-controls';
            controls.innerHTML =
                '<button title="Zoom in">+</button>' +
                '<button title="Zoom out">−</button>' +
                '<button title="Reset">⊙</button>';
            wrapper.appendChild(controls);

            var scale = 1, tx = 0, ty = 0;
            var minScale = 0.2, maxScale = 5;
            var dragging = false, startX, startY, startTx, startTy;

            function applyTransform() {
                inner.style.transform = 'translate(' + tx + 'px, ' + ty + 'px) scale(' + scale + ')';
            }

            // Wheel to zoom
            wrapper.addEventListener('wheel', function (e) {
                e.preventDefault();
                var rect = wrapper.getBoundingClientRect();
                var mx = e.clientX - rect.left;
                var my = e.clientY - rect.top;
                var delta = e.deltaY < 0 ? 1.1 : 0.9;
                var newScale = Math.min(maxScale, Math.max(minScale, scale * delta));
                tx = mx - (mx - tx) * (newScale / scale);
                ty = my - (my - ty) * (newScale / scale);
                scale = newScale;
                applyTransform();
            }, { passive: false });

            // Pan
            wrapper.addEventListener('mousedown', function (e) {
                dragging = true;
                startX = e.clientX;
                startY = e.clientY;
                startTx = tx;
                startTy = ty;
                wrapper.classList.add('grabbing');
            });

            window.addEventListener('mousemove', function (e) {
                if (!dragging) return;
                tx = startTx + (e.clientX - startX);
                ty = startTy + (e.clientY - startY);
                applyTransform();
            });

            window.addEventListener('mouseup', function () {
                dragging = false;
                wrapper.classList.remove('grabbing');
            });

            // Buttons
            var buttons = controls.querySelectorAll('button');
            buttons[0].addEventListener('click', function () {
                scale = Math.min(maxScale, scale * 1.2);
                applyTransform();
            });
            buttons[1].addEventListener('click', function () {
                scale = Math.max(minScale, scale * 0.8);
                applyTransform();
            });
            buttons[2].addEventListener('click', function () {
                scale = 1; tx = 0; ty = 0;
                applyTransform();
            });
        });
    }

    // Run after mermaid renders (which happens asynchronously)
    function tryInit() {
        if (document.querySelectorAll('.mermaid svg').length > 0) {
            initMermaidPanZoom();
        } else {
            setTimeout(tryInit, 200);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', tryInit);
    } else {
        tryInit();
    }
})();
