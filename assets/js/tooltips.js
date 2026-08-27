function initTooltips() {
  var roots = Array.from(document.querySelectorAll('[data-tooltip-root]'));
  if (!roots.length) {
    return;
  }

  var closeDelay = 120;

  function ensureContent(root) {
    var content = root.querySelector('[data-tooltip-content]');
    if (!content) {
      return null;
    }

    if (content.dataset.tooltipHydrated === 'true') {
      return content;
    }

    var html = root.getAttribute('data-tooltip-html');
    if (html) {
      content.innerHTML = html;

      // Some browsers may return entity-encoded attribute values. If we still
      // don't have rendered elements, decode once and re-apply.
      if (!content.querySelector('*')) {
        var decoder = document.createElement('textarea');
        decoder.innerHTML = html;
        content.innerHTML = decoder.value;
      }
    }

    content.dataset.tooltipHydrated = 'true';
    return content;
  }

  function positionTooltip(root) {
    var trigger = root.querySelector('[data-tooltip-trigger]');
    var content = root.querySelector('[data-tooltip-content]');
    if (!trigger || !content || content.hidden) {
      return;
    }

    var gap = 8;
    var margin = 8;
    var rect = trigger.getBoundingClientRect();
    var viewportWidth = document.documentElement.clientWidth;
    var viewportHeight = document.documentElement.clientHeight;

    // Reset placement so the natural size can be measured.
    content.classList.remove('is-above');
    content.style.left = '0px';
    content.style.top = '0px';

    var width = content.offsetWidth;
    var height = content.offsetHeight;
    var triggerCenter = rect.left + rect.width / 2;

    // Center horizontally on the trigger, clamped to the viewport.
    var left = Math.max(margin, Math.min(triggerCenter - width / 2, viewportWidth - width - margin));

    // Prefer below the trigger; flip above if it would overflow the bottom.
    var top = rect.bottom + gap;
    if (top + height > viewportHeight - margin && rect.top - gap - height >= margin) {
      top = rect.top - gap - height;
      content.classList.add('is-above');
    }

    content.style.left = Math.round(left) + 'px';
    content.style.top = Math.round(top) + 'px';

    // Point the arrow at the trigger, kept within the tooltip's edges.
    var arrowLeft = Math.max(12, Math.min(triggerCenter - left, width - 12));
    content.style.setProperty('--tooltip-arrow-left', Math.round(arrowLeft) + 'px');
  }

  function clearCloseTimer(root) {
    if (root.tooltipCloseTimer) {
      window.clearTimeout(root.tooltipCloseTimer);
      root.tooltipCloseTimer = null;
    }
  }

  function scheduleClose(root) {
    clearCloseTimer(root);
    root.tooltipCloseTimer = window.setTimeout(function () {
      if (!root.matches(':hover') && !root.matches(':focus-within')) {
        setOpen(root, false);
      }
    }, closeDelay);
  }

  function setOpen(root, open) {
    var trigger = root.querySelector('[data-tooltip-trigger]');
    var content = ensureContent(root);
    if (!trigger || !content) {
      return;
    }

    clearCloseTimer(root);

    trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) {
      root.classList.add('is-open');
      content.hidden = false;
      content.setAttribute('aria-hidden', 'false');
      positionTooltip(root);
      return;
    }

    root.classList.remove('is-open');
    content.hidden = true;
    content.setAttribute('aria-hidden', 'true');
  }

  function closeAll(exceptRoot) {
    roots.forEach(function (root) {
      if (root !== exceptRoot) {
        setOpen(root, false);
      }
    });
  }

  roots.forEach(function (root) {
    var trigger = root.querySelector('[data-tooltip-trigger]');
    if (!trigger) {
      return;
    }

    trigger.addEventListener('mouseenter', function () {
      setOpen(root, true);
    });

    var content = root.querySelector('[data-tooltip-content]');
    if (content) {
      content.addEventListener('mouseenter', function () {
        setOpen(root, true);
      });

      content.addEventListener('mouseleave', function () {
        scheduleClose(root);
      });
    }

    trigger.addEventListener('focus', function () {
      setOpen(root, true);
    });

    root.addEventListener('mouseleave', function () {
      scheduleClose(root);
    });

    root.addEventListener('focusout', function () {
      window.setTimeout(function () {
        if (!root.matches(':focus-within')) {
          setOpen(root, false);
        }
      }, 0);
    });

    trigger.addEventListener('click', function () {
      var isExpanded = trigger.getAttribute('aria-expanded') === 'true';
      if (!isExpanded) {
        closeAll(root);
      }
      setOpen(root, !isExpanded);
    });

    trigger.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        setOpen(root, false);
        trigger.blur();
      }
    });
  });

  // A fixed tooltip is positioned to the viewport, so re-anchor it to the
  // trigger whenever the page (or an inner container) scrolls or resizes.
  function repositionOpen() {
    roots.forEach(function (root) {
      if (root.classList.contains('is-open')) {
        positionTooltip(root);
      }
    });
  }

  window.addEventListener('scroll', function () {
    window.requestAnimationFrame(repositionOpen);
  }, true);
  window.addEventListener('resize', function () {
    window.requestAnimationFrame(repositionOpen);
  });

  document.addEventListener('click', function (event) {
    roots.forEach(function (root) {
      if (!root.contains(event.target)) {
        setOpen(root, false);
      }
    });
  });

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
      closeAll();
    }
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initTooltips);
} else {
  initTooltips();
}
