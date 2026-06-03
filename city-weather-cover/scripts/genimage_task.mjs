#!/usr/bin/env node

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';

const TERMINAL = new Set(['SUCCEEDED', 'FAILED', 'VIOLATION']);

function parseArgs(argv) {
  const opts = {};
  const positional = [];
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith('--')) {
        opts[key] = true;
      } else {
        opts[key] = next;
        i += 1;
      }
    } else {
      positional.push(arg);
    }
  }
  return { command: positional[0] || 'help', opts };
}

function normalizeBaseUrl(baseUrl) {
  const value = String(baseUrl || '').trim().replace(/\/+$/, '');
  if (!value) throw new Error('Missing base URL');
  return value.endsWith('/api') ? value : `${value}/api`;
}

async function loadJson(filePath) {
  try {
    return JSON.parse(await readFile(filePath, 'utf8'));
  } catch {
    return null;
  }
}

async function loadSession(authFile) {
  const candidates = [];
  if (authFile) candidates.push(authFile);
  candidates.push(path.join(process.cwd(), '.genimage', 'session.json'));
  candidates.push(path.join(process.env.HOME || '', '.genimage', 'session.json'));
  for (const candidate of candidates) {
    const data = await loadJson(candidate);
    if (data) return data;
  }
  return null;
}

async function saveSession(session, authFile) {
  const filePath = authFile || path.join(process.cwd(), '.genimage', 'session.json');
  await mkdir(path.dirname(filePath), { recursive: true });
  await writeFile(filePath, `${JSON.stringify(session, null, 2)}\n`, 'utf8');
}

async function requestJson(url, { method = 'GET', token, body } = {}) {
  const headers = {};
  if (token) headers.Authorization = `Bearer ${token}`;
  let payload;
  if (body !== undefined) {
    headers['Content-Type'] = 'application/json';
    payload = JSON.stringify(body);
  }
  const res = await fetch(url, { method, headers, body: payload });
  const text = await res.text();
  let data;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }
  if (!res.ok) {
    const message = data?.msg || data?.message || res.statusText || 'Request failed';
    const error = new Error(message);
    error.status = res.status;
    error.body = data;
    throw error;
  }
  return data;
}

async function ensureToken(opts) {
  const session = await loadSession(opts['auth-file'] || process.env.GENIMAGE_AUTH_FILE);
  const baseUrl = normalizeBaseUrl(opts['base-url'] || process.env.GENIMAGE_BASE_URL || session?.baseUrl);
  let token = opts.token || process.env.GENIMAGE_TOKEN || session?.token;
  if (!token) {
    const username = opts.username || process.env.GENIMAGE_USERNAME;
    const password = opts.password || process.env.GENIMAGE_PASSWORD;
    if (!username || !password) throw new Error('Missing token and no username/password available');
    const login = await requestJson(`${baseUrl}/auth/login`, {
      method: 'POST',
      body: { username, password },
    });
    token = login?.data?.token;
    if (!token) throw new Error('Login returned no token');
    await saveSession(
      {
        baseUrl,
        token,
        user: login?.data?.user || null,
        savedAt: new Date().toISOString(),
      },
      opts['auth-file'] || process.env.GENIMAGE_AUTH_FILE,
    );
  }
  return { baseUrl, token };
}

async function pollTask(baseUrl, token, id, intervalMs) {
  for (;;) {
    const envelope = await requestJson(`${baseUrl}/tasks/${id}/poll`, {
      method: 'POST',
      token,
    });
    const status = envelope?.data?.status;
    if (TERMINAL.has(status)) return envelope;
    await new Promise((resolve) => setTimeout(resolve, intervalMs));
  }
}

async function main() {
  const { command, opts } = parseArgs(process.argv.slice(2));
  if (command !== 'generate') {
    console.error('Usage: genimage_task.mjs generate --base-url URL --prompt TEXT [--ratio 3:4] [--resolution 4k] [--wait]');
    process.exit(1);
  }
  const { baseUrl, token } = await ensureToken(opts);
  const prompt = opts.prompt;
  if (!prompt) throw new Error('Missing --prompt');
  const envelope = await requestJson(`${baseUrl}/tasks/generate`, {
    method: 'POST',
    token,
    body: {
      prompt,
      ratio: opts.ratio || '3:4',
      resolution: opts.resolution || '4k',
    },
  });
  const result = { task_create: envelope };
  const taskId = envelope?.data?.id;
  if (opts.wait && taskId) {
    result.task_poll = await pollTask(baseUrl, token, taskId, Number(opts['poll-interval'] || 10000));
  }
  console.log(JSON.stringify(result, null, 2));
}

main().catch((error) => {
  console.error(
    JSON.stringify(
      {
        error: error.message,
        status: error.status,
        body: error.body,
      },
      null,
      2,
    ),
  );
  process.exit(1);
});
