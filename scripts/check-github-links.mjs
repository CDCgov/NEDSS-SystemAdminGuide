#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const root = process.cwd();
const args = process.argv.slice(2);

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

function getChangedMarkdownFiles() {
  const output = execSync('git diff --name-only --diff-filter=ACMRTUXB HEAD', {
    cwd: root,
    encoding: 'utf8',
  }).trim();

  if (!output) return [];

  return output
    .split('\n')
    .map((p) => p.trim())
    .filter((p) => p.endsWith('.md'))
    .map((p) => path.join(root, p))
    .filter((p) => fs.existsSync(p));
}

function collectMarkdownFiles() {
  const hasChangedFlag = args.includes('--changed');
  const explicitFiles = args
    .filter((a) => a !== '--changed')
    .map((a) => path.resolve(root, a))
    .filter((p) => p.endsWith('.md') && fs.existsSync(p));

  if (explicitFiles.length > 0) return explicitFiles;
  if (hasChangedFlag) return getChangedMarkdownFiles();

  const files = walkMarkdownFiles(path.join(root, 'docs'));
  const topLevel = [
    'index.md',
    'ACCESSIBILITY.md',
    'FRONT-MATTER.md',
    'STYLES.md',
    'CONTRIBUTING.md',
    'WORKFLOW.md',
    'README.md',
  ]
    .map((f) => path.join(root, f))
    .filter((f) => fs.existsSync(f));

  return files.concat(topLevel);
}

function extractGitHubUrls(text) {
  const urls = new Set();
  const re = /https:\/\/github\.com\/[^\s)\]>]+/g;
  let match;

  while ((match = re.exec(text)) !== null) {
    const raw = match[0].replace(/[>.,;:]+$/g, '');
    urls.add(raw);
  }

  return [...urls];
}

async function checkUrl(url) {
  const maxAttempts = 3;
  let lastStatus = 0;
  let lastError = null;

  for (let i = 0; i < maxAttempts; i++) {
    try {
      const res = await fetch(url, {
        method: 'GET',
        redirect: 'follow',
        headers: {
          'User-Agent': 'NEDSS-link-checker/1.0',
          Accept: 'text/html',
        },
      });

      lastStatus = res.status;

      if (res.status === 429 || res.status >= 500) {
        await new Promise((r) => setTimeout(r, 500 * (i + 1)));
        continue;
      }

      return { ok: res.status >= 200 && res.status < 400, status: res.status };
    } catch (err) {
      lastError = err;
      await new Promise((r) => setTimeout(r, 500 * (i + 1)));
    }
  }

  if (lastStatus > 0) {
    return { ok: false, status: lastStatus };
  }

  return { ok: false, status: 0, error: lastError?.message || 'request failed' };
}

async function main() {
  const files = collectMarkdownFiles();
  if (files.length === 0) {
    console.log('No markdown files to check.');
    return;
  }

  const urlToFiles = new Map();

  for (const file of files) {
    const text = fs.readFileSync(file, 'utf8');
    const urls = extractGitHubUrls(text);
    for (const url of urls) {
      if (!urlToFiles.has(url)) urlToFiles.set(url, new Set());
      urlToFiles.get(url).add(path.relative(root, file));
    }
  }

  const urls = [...urlToFiles.keys()];
  if (urls.length === 0) {
    console.log('No GitHub links found in selected files.');
    return;
  }

  const failures = [];
  for (const url of urls) {
    const result = await checkUrl(url);
    if (!result.ok) {
      failures.push({
        url,
        status: result.status,
        error: result.error,
        files: [...urlToFiles.get(url)],
      });
    }
  }

  if (failures.length === 0) {
    console.log(`GitHub link check passed: ${urls.length} URL(s) checked, 0 broken.`);
    return;
  }

  console.log(`GitHub link check found ${failures.length} broken URL(s):`);
  for (const failure of failures) {
    const statusText = failure.status ? `HTTP ${failure.status}` : failure.error;
    console.log(`- ${failure.url} (${statusText})`);
    for (const file of failure.files) {
      console.log(`  referenced in: ${file}`);
    }
  }

  process.exitCode = 1;
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
