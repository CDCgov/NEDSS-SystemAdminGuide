function isAbsoluteOrSpecialUrl(value) {
  return (
    value.startsWith('/') ||
    value.startsWith('#') ||
    value.startsWith('http://') ||
    value.startsWith('https://') ||
    value.startsWith('mailto:') ||
    value.startsWith('tel:') ||
    value.startsWith('data:')
  );
}

function rewriteRelativeAssetUrls(root, sourcePageUrl) {
  const sourceUrl = new URL(sourcePageUrl, window.location.origin);

  root.querySelectorAll('[src],[href]').forEach((node) => {
    ['src', 'href'].forEach((attr) => {
      const original = node.getAttribute(attr);

      if (!original || isAbsoluteOrSpecialUrl(original)) {
        return;
      }

      node.setAttribute(attr, new URL(original, sourceUrl).pathname);
    });
  });
}

function stripNonContentElements(root) {
  root
    .querySelectorAll('.site-footer, .site-header, .side-bar, nav, script')
    .forEach((el) => el.remove());
}

function stripParentTocSection(root, isParentPage) {
  if (!isParentPage) {
    return;
  }

  const tocHeadings = Array.from(root.querySelectorAll('h1, h2, h3, h4, h5, h6')).filter((heading) => {
    const text = (heading.textContent || '').trim().toLowerCase();
    return text === 'table of contents' || text === 'on this page';
  });

  tocHeadings.forEach((heading) => {
    let node = heading;

    while (node) {
      const next = node.nextElementSibling;
      node.remove();

      if (!next || /^H[1-6]$/.test(next.tagName)) {
        break;
      }

      node = next;
    }
  });
}

async function renderPrintGuideContent() {
  const rawNodes = Array.from(document.querySelectorAll('#print-guide-sources > li[data-url]'));
  const target = document.getElementById('print-guide-content');
  const status = document.getElementById('print-guide-status');
  const printButton = document.getElementById('print-guide-trigger');

  const seen = new Set();
  const sourceNodes = rawNodes.filter((item) => {
    const kind = (item.dataset.kind || '').trim();
    const published = (item.dataset.published || 'true').trim().toLowerCase();
    const title = (item.dataset.title || '').trim();
    const url = (item.dataset.url || '').trim();
    const isDocsUrl = url.includes('/docs/') && url.endsWith('.html');
    const isIntroUrl = kind === 'intro' && (url.endsWith('/') || url.endsWith('/index.html'));

    if (!title || !url || published === 'false' || (!isDocsUrl && !isIntroUrl)) {
      return false;
    }

    if (seen.has(url)) {
      return false;
    }

    seen.add(url);
    return true;
  });

  if (!target || !status || sourceNodes.length === 0) {
    return;
  }

  if (sourceNodes.length > 1000) {
    status.textContent = `Unexpected source count (${sourceNodes.length}). Check print source filtering.`;
    return;
  }

  printButton?.addEventListener('click', () => window.print());
  status.textContent = `Loading ${sourceNodes.length} pages for print...`;

  for (let i = 0; i < sourceNodes.length; i += 1) {
    const item = sourceNodes[i];
    const level = item.dataset.level || '1';
    const isParentPage = (item.dataset.hasChildren || 'false').trim().toLowerCase() === 'true';
    const url = item.dataset.url;

    if (!url) {
      continue;
    }

    const section = document.createElement('section');
    section.className = `printable-page-section level-${level}`;

    try {
      const response = await fetch(url, { credentials: 'same-origin' });
      const html = await response.text();
      const parsed = new DOMParser().parseFromString(html, 'text/html');
      const contentRoot = parsed.querySelector('.main-content-wrap') || parsed.querySelector('main') || parsed.body;

      const body = document.createElement('div');
      body.className = 'printable-page-body';
      body.innerHTML = contentRoot ? contentRoot.innerHTML : '';
      stripNonContentElements(body);
      stripParentTocSection(body, isParentPage);
      rewriteRelativeAssetUrls(body, url);

      section.appendChild(body);
    } catch (error) {
      const note = document.createElement('p');
      note.textContent = `Unable to load content from ${url}`;
      section.appendChild(note);
    }

    target.appendChild(section);

    if (i < sourceNodes.length - 1) {
      const pageBreak = document.createElement('div');
      pageBreak.className = 'page-break';
      target.appendChild(pageBreak);
    }

    status.textContent = `Loaded ${i + 1} of ${sourceNodes.length} pages...`;
  }

  status.textContent = `Ready. Loaded ${sourceNodes.length} pages.`;
}

window.addEventListener('DOMContentLoaded', async () => {
  if (!window.location.pathname.includes('print-guide')) {
    return;
  }

  await renderPrintGuideContent();
});
