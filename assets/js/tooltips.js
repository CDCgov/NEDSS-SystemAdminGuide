document.addEventListener('DOMContentLoaded', function () {
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

    var template = root.querySelector('[data-tooltip-template]');
    if (template) {
      var decoder = document.createElement('textarea');
      decoder.innerHTML = template.innerHTML;
      content.innerHTML = decoder.value;
    }

    content.dataset.tooltipHydrated = 'true';
    return content;
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
});
