import fs from 'fs';
import path from 'path';

const ROOT = process.cwd();
const CONTENT_DIR = path.join(ROOT, 'portfolio-content');
const OUTPUT_JSON = path.join(ROOT, 'content', 'protosem', 'weeks.json');
const PUBLIC_ASSETS_DIR = path.join(ROOT, 'assets', 'weekly');

const DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const IMAGE_RE = /\.(jpg|jpeg|png|gif|webp|svg)$/i;
const mdEsc = (value = '') => String(value)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');

const parseFrontmatter = (text) => {
  const match = text.match(/^---\s*\n([\s\S]*?)\n---\s*\n?/);
  const meta = {};
  let body = text;
  if (match) {
    for (const line of match[1].split('\n')) {
      const m = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
      if (!m) continue;
      let value = m[2].trim();
      value = value.replace(/^['"]|['"]$/g, '');
      meta[m[1]] = /^\d+$/.test(value) ? Number(value) : value;
    }
    body = text.slice(match[0].length);
  }
  return { meta, body };
};

const inlineMarkdown = (text) => {
  let out = mdEsc(text);
  out = out.replace(/!\[\[([^\]]+)\]\]/g, (_, file) => `[[IMAGE:${file}]]`);
  out = out.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (_, alt, src) => `[[MDIMAGE:${alt}|${src}]]`);
  out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  out = out.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  return out;
};

const renderMarkdown = (body, imagePrefix, imageFiles) => {
  const lines = body.replace(/\r\n/g, '\n').split('\n');
  const html = [];
  const linkedImages = new Set();
  let paragraph = [];
  let list = [];

  const flushParagraph = () => {
    if (paragraph.length) {
      html.push(`<p>${inlineMarkdown(paragraph.join(' '))}</p>`);
      paragraph = [];
    }
  };
  const flushList = () => {
    if (list.length) {
      html.push('<ul>' + list.map(x => `<li>${inlineMarkdown(x)}</li>`).join('') + '</ul>');
      list = [];
    }
  };

  for (const raw of lines) {
    const line = raw.trim();
    if (!line) { flushParagraph(); flushList(); continue; }
    const h = line.match(/^###\s+(.+)$/);
    if (h) { flushParagraph(); flushList(); html.push(`<h3>${mdEsc(h[1])}</h3>`); continue; }
    const bullet = line.match(/^[-*]\s+(.+)$/);
    if (bullet) { flushParagraph(); list.push(bullet[1]); continue; }
    const quote = line.match(/^>\s?(.*)$/);
    if (quote) { flushParagraph(); flushList(); html.push(`<blockquote>${inlineMarkdown(quote[1])}</blockquote>`); continue; }
    paragraph.push(line);
  }
  flushParagraph(); flushList();

  let finalHtml = html.join('\n');
  finalHtml = finalHtml.replace(/\[\[IMAGE:([^\]]+)\]\]/g, (_, file) => {
    const found = imageFiles.find(x => x === file);
    if (!found) return '';
    linkedImages.add(found);
    return `<img src="${imagePrefix}/${encodeURIComponent(found)}" alt="${mdEsc(found)}" loading="lazy">`;
  });
  finalHtml = finalHtml.replace(/\[\[MDIMAGE:([^|]+)\|([^\]]+)\]\]/g, (_, alt, src) => `<img src="${src}" alt="${mdEsc(alt)}" loading="lazy">`);
  return { html: finalHtml, linkedImages };
};

const listDirs = (dir) => fs.existsSync(dir)
  ? fs.readdirSync(dir, { withFileTypes: true }).filter(x => x.isDirectory()).map(x => x.name).sort()
  : [];

const compileDay = (weekNumber, dayFolder) => {
  const dayPath = path.join(CONTENT_DIR, `Week_${String(weekNumber).padStart(2,'0')}`, dayFolder);
  const files = fs.readdirSync(dayPath);
  const markdown = files.filter(f => f.toLowerCase().endsWith('.md') && f.toLowerCase() !== 'readme.md').sort();
  const images = files.filter(f => IMAGE_RE.test(f)).sort();
  if (!markdown.length && !images.length) return null;

  const publicDir = path.join(PUBLIC_ASSETS_DIR, `Week_${String(weekNumber).padStart(2,'0')}`, dayFolder);
  fs.mkdirSync(publicDir, { recursive: true });
  for (const img of images) fs.copyFileSync(path.join(dayPath, img), path.join(publicDir, img));

  const imagePrefix = `./assets/weekly/Week_${String(weekNumber).padStart(2,'0')}/${dayFolder}`;
  const sections = [];
  const linked = new Set();
  let dayTitle = dayFolder.replace(/^\d+_/, '').toUpperCase();
  let takeaway = '';

  for (const md of markdown) {
    const raw = fs.readFileSync(path.join(dayPath, md), 'utf8');
    const { meta, body } = parseFrontmatter(raw);
    if (meta.title) dayTitle = String(meta.title);
    const rendered = renderMarkdown(body, imagePrefix, images);
    sections.push({ heading: md.replace(/\.md$/i, '').replace(/[-_]+/g, ' ').toUpperCase(), contentHtml: rendered.html });
    for (const x of rendered.linkedImages) linked.add(x);
    const q = body.match(/(?:^|\n)>\s?([^\n]+)/);
    if (q) takeaway = q[1].trim();
  }

  const unlinkedImages = images.filter(x => !linked.has(x));
  if (unlinkedImages.length) {
    sections.push({ heading: 'GALLERY', contentHtml: unlinkedImages.map(img => `<img src="${imagePrefix}/${encodeURIComponent(img)}" alt="${mdEsc(img)}" loading="lazy">`).join('\n') });
  }

  const dayNumberMatch = dayFolder.match(/^(\d+)_/);
  const dayNumber = dayNumberMatch ? Number(dayNumberMatch[1]) : sections.length + 1;
  return { dayNumber, title: dayTitle, sections, takeaway, photos: [], artifacts: [] };
};

const buildWeek = (weekNumber) => {
  const weekName = `Week_${String(weekNumber).padStart(2,'0')}`;
  const weekPath = path.join(CONTENT_DIR, weekName);
  const dayFolders = listDirs(weekPath);
  const dayData = dayFolders.map(d => compileDay(weekNumber, d)).filter(Boolean);
  const weekReadme = path.join(weekPath, 'README.md');
  let title = weekNumber === 19 ? 'FINAL DESTINATION' : (weekNumber === 0 ? 'THE JOURNEY BEGINS' : weekNumber === 1 ? 'FROM CURIOSITY TO PROBLEM-SOLVING' : 'NEXT DESTINATION');
  let journeyLabel = weekNumber === 0 ? 'FIRST LANDING' : weekNumber === 1 ? 'SECOND LANDING' : weekNumber === 19 ? 'FINAL DESTINATION' : 'UPCOMING';
  let intro = '';
  let reflection = '';
  if (fs.existsSync(weekReadme)) {
    const parsed = parseFrontmatter(fs.readFileSync(weekReadme,'utf8'));
    if (parsed.meta.title) title = parsed.meta.title;
    if (parsed.meta.journeyLabel) journeyLabel = parsed.meta.journeyLabel;
    if (parsed.meta.intro) intro = parsed.meta.intro;
    if (parsed.meta.finalReflection) reflection = parsed.meta.finalReflection;
  }
  const complete = dayData.length > 0;
  return {
    weekNumber,
    title,
    journeyLabel,
    status: complete ? 'COMPLETED' : 'UPCOMING',
    dateRange: '',
    intro,
    days: dayData,
    finalReflection: reflection,
    photos: [],
    artifacts: []
  };
};

const main = () => {
  if (!fs.existsSync(CONTENT_DIR)) return;
  const weeks = Array.from({length: 20}, (_, i) => buildWeek(i));
  fs.mkdirSync(path.dirname(OUTPUT_JSON), { recursive: true });
  fs.mkdirSync(PUBLIC_ASSETS_DIR, { recursive: true });
  fs.writeFileSync(OUTPUT_JSON, JSON.stringify({ version: 1, generatedAt: new Date().toISOString(), totalWeeks: 20, weeks }, null, 2));
  console.log(`Compiled ${weeks.length} weeks to ${path.relative(ROOT, OUTPUT_JSON)}`);
};

main();
