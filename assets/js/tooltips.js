document.addEventListener('DOMContentLoaded', function () {
  var roots = Array.from(document.querySelectorAll('[data-tooltip-root]'));
  if (!roots.length) {
    return;
  }

  function setOpen(root, open) {
    var trigger = root.querySelector('[data-tooltip-trigger]');
    var content = root.querySelector('[data-tooltip-content]');
    if (!trigger || !content) {
      return;
    }

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

    trigger.addEventListener('focus', function () {
      setOpen(root, true);
    });

    root.addEventListener('mouseleave', function () {
      if (!root.matches(':focus-within')) {
        setOpen(root, false);
      }
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
