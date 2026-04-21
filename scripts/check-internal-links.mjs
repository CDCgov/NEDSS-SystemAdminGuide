#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

const root = process.cwd();
const docsRoot = path.join(root, 'docs');
const topLevelFiles = [
  'index.md',
  'ACCESSIBILITY.md',
  'FRONT-MATTER.md',
  'STYLES.md',
  'CONTRIBUTING.md',
  'WORKFLOW.md',
  'README.md',
];

function walkMarkdownFiles(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (['.git', 'node_modules', '_site', 'vendor', '_guide_preview'].includes(entry.name)) {
      continue;
    }

    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkMarkdownFiles(fullPath, out);
    } else if (entry.isFile() && fullPath.endsWith('.md')) {
      out.push(fullPath);
    }
  }

  return out;
}

function stripFencedCodeBlocks(text) {
  const lines = text.split('\n');
  const out = [];
  let inFence = false;

  for (const line of lines) {
    const trimmed = line.trimStart();
    if (trimmed.startsWith('```') || trimmed.startsWith('~~~')) {
      inFence = !inFence;
      out.push('');
      continue;
    }

    out.push(inFence ? '' : line);
  }

  return out.join('\n');
}

function stripHtmlComments(text) {
  return text.replace(/<!--[\s\S]*?-->/g, '');
}

function collectHeadingAnchors(mdText) {
  const lines = mdText.split('\n');
  const anchors = new Set();
  const counts = new Map();

  for (const rawLine of lines) {
    const line = rawLine.trim();
    const match = /^(#{1,6})\s+(.*)$/.exec(line);
    if (!match) continue;

    const heading = match[2].trim();
    const base = slugifyHeading(heading);
    if (!base) continue;

    const n = counts.get(base) || 0;
    counts.set(base, n + 1);

    anchors.add(n === 0 ? base : `${base}-${n}`);
  }

  return anchors;
}

function slugifyHeading(text) {
  // Roughly matches kramdown/gh-style IDs used in this repo.
  let s = text.toLowerCase().trim();
  s = s.replace(/`/g, '');
  s = s.replace(/\\/g, '');
  s = s.replace(/<[^>]+>/g, '');
  s = s.replace(/[\"'.,!?():;\[\]{}]/g, '');
  s = s.replace(/\s+/g, '-');
  s = s.replace(/-+/g, '-');
  s = s.replace(/^-|-$/g, '');
  return s;
}

function isExternal(link) {
  return (
    link.startsWith('http://') ||
    link.startsWith('https://') ||
    link.startsWith('mailto:') ||
    link.startsWith('tel:') ||
    link.startsWith('#')
  );
}

function resolveTargetPath(sourceFile, hrefPath) {
  // Repo convention often uses ../../docs/.../*.html from pages under docs/*.
  // Normalize any link containing /docs/ to workspace-root docs/ resolution.
  const docsIdx = hrefPath.indexOf('/docs/');
  if (docsIdx >= 0) {
    const fromDocs = hrefPath.slice(docsIdx).replace(/^\/+/, '');
    return path.join(root, fromDocs);
  }

  if (hrefPath.startsWith('/docs/')) {
    return path.join(root, hrefPath.slice(1));
  }

  if (hrefPath.startsWith('/')) {
    // Keep old absolute site paths ignored here; external checker handles/ignores these.
    return null;
  }

  return path.resolve(path.dirname(sourceFile), hrefPath);
}

const allFiles = walkMarkdownFiles(docsRoot);
for (const file of topLevelFiles) {
  const full = path.join(root, file);
  if (fs.existsSync(full)) allFiles.push(full);
}

const headingCache = new Map();
const errors = [];
const linkRegex = /!?\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g;

for (const sourceFile of allFiles) {
  const raw = fs.readFileSync(sourceFile, 'utf8');
  const text = stripHtmlComments(stripFencedCodeBlocks(raw));

  let match;
  while ((match = linkRegex.exec(text)) !== null) {
    let target = match[1];
    if (target.startsWith('<') && target.endsWith('>')) {
      target = target.slice(1, -1);
    }

    if (isExternal(target)) continue;

    const [hrefPath, fragment] = target.split('#');
    if (!hrefPath) continue;

    const resolved = resolveTargetPath(sourceFile, hrefPath);
    if (!resolved) continue;

    let existenceTarget = resolved;
    if (hrefPath.endsWith('.html')) {
      existenceTarget = resolved.replace(/\.html$/i, '.md');
    }

    // Markdown links frequently URL-encode spaces in asset names.
    existenceTarget = decodeURIComponent(existenceTarget);

    const exists = fs.existsSync(existenceTarget);
    if (!exists) {
      errors.push({
        source: sourceFile,
        target,
        reason: `Missing target file: ${path.relative(root, existenceTarget)}`,
      });
      continue;
    }

    if (fragment && hrefPath.endsWith('.html')) {
      const targetFile = existenceTarget;
      let anchors = headingCache.get(targetFile);
      if (!anchors) {
        anchors = collectHeadingAnchors(fs.readFileSync(targetFile, 'utf8'));
        headingCache.set(targetFile, anchors);
      }

      if (!anchors.has(fragment)) {
        errors.push({
          source: sourceFile,
          target,
          reason: `Missing anchor '#${fragment}' in ${path.relative(root, targetFile)}`,
        });
      }
    }
  }
}

if (errors.length === 0) {
  console.log('Internal link audit passed: 0 issues found.');
  process.exit(0);
}

console.log('Internal link audit found issues:');
for (const e of errors) {
  console.log(`- ${path.relative(root, e.source)} -> ${e.target}`);
  console.log(`  ${e.reason}`);
}
console.log(`\nTotal issues: ${errors.length}`);
process.exit(1);
