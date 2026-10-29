const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../docs/language.js'), 'utf8');

function view(href, lang = 'en') {
  const current = new URL(href);
  const handlers = {};
  const select = { value: '', addEventListener: (name, callback) => { handlers.change = callback; } };
  const gallery = { href: new URL('./themes.html', current).href, addEventListener: (name, callback) => { handlers.gallery = callback; } };
  const root = { lang, dataset: { theme: 'iris-light' } };
  let navigation;
  const location = { href, search: current.search, hash: current.hash, assign: value => { navigation = new URL(value); } };
  vm.runInNewContext(source, { URL, window: { location }, document: { documentElement: root, querySelector: selector => selector === '#language-select' ? select : gallery } });
  return { select, root, gallery, handlers, next: () => navigation };
}

for (const href of ['https://example.com/portfolio/index.html?ref=cv&theme=azure-dark#work', 'file:///C:/portfolio/index.html?ref=cv#work']) {
  const page = view(href);
  assert.equal(page.select.value, 'en');
  page.select.value = 'es';
  page.handlers.change();
  const target = page.next();
  assert.ok(target.pathname.endsWith('/portfolio/es.html'));
  assert.equal(target.searchParams.get('theme'), 'iris-light');
  assert.equal(target.searchParams.get('ref'), 'cv');
  assert.equal(target.hash, '#work');
  page.root.dataset.theme = 'titanium-dark';
  page.handlers.gallery();
  assert.equal(new URL(page.gallery.href).searchParams.get('theme'), 'titanium-dark');
  assert.equal(new URL(page.gallery.href).searchParams.get('lang'), 'en');
}
const spanish = view('https://example.com/project/es.html#experience', 'es');
assert.equal(spanish.select.value, 'es');
spanish.select.value = 'en';
spanish.handlers.change();
assert.equal(spanish.next().pathname, '/project/index.html');
assert.equal(spanish.next().hash, '#experience');
const invalid = view('https://example.com/index.html');
invalid.select.value = 'constructor';
invalid.handlers.change();
assert.equal(invalid.next(), undefined);
console.log('PASS: EN/ES switching, theme/query/anchor preservation, project Pages and file paths, gallery language, invalid values.');
