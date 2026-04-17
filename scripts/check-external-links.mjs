#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const root = process.cwd();

function walkMarkdownFiles(dir, out = []) {
  if (!fs.existsSync(dir)) return out;

  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === '.git' || entry.name === 'node_modules' || entry.name === '_site') {
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

function runMarkdownLinkCheck(filePath) {
  const relativePath = path.relative(root, filePath);
  const command = `npx markdown-link-check --config .markdown-link-check.json "${relativePath}"`;

  try {
    return execSync(command, {
      cwd: root,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      env: { ...process.env, FORCE_COLOR: '1' },
    });
  } catch (error) {
    const stdout = typeof error.stdout === 'string' ? error.stdout : '';
    const stderr = typeof error.stderr === 'string' ? error.stderr : '';
    return `${stdout}${stderr}`;
  }
}

function main() {
  const docsFiles = walkMarkdownFiles(path.join(root, 'docs')).sort();
  const topLevelFiles = [
    'index.md',
    'ACCESSIBILITY.md',
    'FRONT-MATTER.md',
    'STYLES.md',
    'CONTRIBUTING.md',
    'WORKFLOW.md',
    'README.md',
  ]
    .map((file) => path.join(root, file))
    .filter((file) => fs.existsSync(file));

  const files = docsFiles.concat(topLevelFiles);
  let allOutput = '';

  for (const file of files) {
    const output = runMarkdownLinkCheck(file);
    allOutput += output;
    process.stdout.write(output);
  }

  fs.writeFileSync('/tmp/link-check-out.txt', allOutput);

  console.log('');
  console.log('=== BROKEN LINKS SUMMARY ===');

  const brokenLines = allOutput.match(/^.*(✖|ERROR).*$/gim) || [];
  if (brokenLines.length > 0) {
    for (const line of brokenLines) {
      console.log(line);
    }
  } else {
    console.log('No broken links found.');
  }

  console.log('');
  console.log('Key: [✓] checked and alive  [/] skipped (ignored pattern)  [✖] dead link');
}

main();