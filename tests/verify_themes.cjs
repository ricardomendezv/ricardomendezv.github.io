// Check theme precedence and controls with the Node standard library.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../docs/theme.js'), 'utf8');
function page({ search = '', saved, blocked = false, embedded = false } = {}) {
  const root = { dataset: {} };
  const meta = { content: '' };
  const browserColor = { content: '' };
  const bar = { hidden: true };
  const handlers = {};
  const select = { options: ['azure', 'silver', 'titanium', 'iris', 'arctic'].map(value => ({ value })), addEventListener: (name, fn) => { handlers.select = fn; } };
  const buttons = ['dark', 'light'].map(mode => ({ dataset: { mode }, setAttribute: (name, value) => { handlers[mode + name] = value; }, addEventListener: (name, fn) => { handlers[mode] = fn; } }));
  let ready, stored = saved, history;
  const window = {
    location: { search, href: `https://example.com/portfolio/index.html${search}#work` },
    localStorage: { getItem: () => { if (blocked) throw Error('Unavailable'); return stored; }, setItem: (key, value) => { if (blocked) throw Error('Unavailable'); stored = value; } },
    history: { replaceState: (state, title, url) => { if (blocked) throw Error('Unavailable'); history = String(url); } }
  };
  window.self = window;
  window.top = embedded ? {} : window;
  const document = {
    documentElement: root,
    querySelector: selector => selector === '.appearance-bar' ? bar : selector === '#theme-select' ? select : selector.includes('theme-color') ? browserColor : meta,
    querySelectorAll: () => buttons,
    addEventListener: (name, fn) => { ready = fn; }
  };
  vm.runInNewContext(source, { URL, URLSearchParams, window, document, getComputedStyle: () => ({ getPropertyValue: () => ' #123456 ' }) });
  ready();
  assert.equal(browserColor.content, '#123456');
  return { root, meta, bar, select, handlers, stored: () => stored, history: () => history };
}

for (const theme of ['silver', 'azure', 'titanium', 'iris', 'arctic'].flatMap(name => [`${name}-light`, `${name}-dark`])) {
  const view = page({ search: `?theme=${theme}`, saved: 'iris-dark' });
  assert.equal(view.root.dataset.theme, theme);
  assert.equal(view.select.value, theme.split('-')[0]);
  assert.equal(view.meta.content, theme.endsWith('dark') ? 'dark' : 'light');
  assert.equal(view.bar.hidden, false);
}

for (const search of ['', '?theme=unknown', '?theme=silver-dark-extra', '?theme=%3Cscript%3E']) {
  assert.equal(page({ search }).root.dataset.theme, 'azure-dark');
}
assert.equal(page({ saved: 'titanium-light' }).root.dataset.theme, 'titanium-light');
assert.equal(page({ saved: 'unknown' }).root.dataset.theme, 'azure-dark');
assert.equal(page({ embedded: true }).bar.hidden, true);
const view = page({ search: '?ref=portfolio' });
assert.equal(view.select.options[0].textContent, 'Midnight');
view.handlers.light();
assert.equal(view.root.dataset.theme, 'azure-light');
assert.equal(view.select.options[0].textContent, 'Azure');
assert.equal(view.handlers['lightaria-pressed'], 'true');
view.select.value = 'iris';
view.handlers.select();
assert.equal(view.root.dataset.theme, 'iris-light');
view.handlers.dark();
assert.equal(view.root.dataset.theme, 'iris-dark');
assert.equal(view.stored(), 'iris-dark');
assert.match(view.history(), /ref=portfolio&theme=iris-dark#work$/);
const offline = page({ blocked: true });
offline.handlers.light();
assert.equal(offline.root.dataset.theme, 'azure-light');
console.log('PASS: 10 theme URLs, Midnight default, saved preference, mode/palette controls, metadata, hash preservation and unavailable storage.');
