import fs from 'fs';
import path from 'path';

const CONTENT_DIR = path.join(process.cwd(), 'portfolio-content');
const PUBLIC_ASSETS_DIR = path.join(process.cwd(), 'public', 'assets', 'weekly');
const COMPILED_DIR = path.join(process.cwd(), 'src', 'content', 'blogs');

if (!fs.existsSync(PUBLIC_ASSETS_DIR)) fs.mkdirSync(PUBLIC_ASSETS_DIR, { recursive: true });
if (!fs.existsSync(COMPILED_DIR)) fs.mkdirSync(COMPILED_DIR, { recursive: true });

const isImage = (filename) => /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(filename);

const processMarkdown = (content, publicPathPrefix) => {
  return content.replace(/!\[\[(.*?)\]\]/g, (match, filename) => `![${filename}](${publicPathPrefix}/${filename})`);
};

const buildTemplates = () => {
  if (!fs.existsSync(CONTENT_DIR)) return;

  for (let i = 0; i <= 19; i++) {
    const weekNum = i.toString().padStart(2, '0');
    const weekFolderName = `Week_${weekNum}`;
    const weekFolderPath = path.join(CONTENT_DIR, weekFolderName);

    if (!fs.existsSync(weekFolderPath)) continue;
    
    // Sort day folders (handled by 01_ numeric prefix)
    const dayFolders = fs.readdirSync(weekFolderPath, { withFileTypes: true })
      .filter(dirent => dirent.isDirectory())
      .map(dirent => dirent.name)
      .sort();

    let compiledMarkdown = `---\ntitle: "Week ${weekNum} Review"\ndate: "${new Date().toISOString().split('T')[0]}"\nweek: ${i}\n---\n\n# Week ${weekNum}\n\n`;
    let hasContent = false;

    for (const dayFolder of dayFolders) {
      const dayFolderPath = path.join(weekFolderPath, dayFolder);
      const files = fs.readdirSync(dayFolderPath);

      const markdownFiles = files.filter(f => f.endsWith('.md'));
      const imageFiles = files.filter(isImage);

      // Skip empty days
      if (markdownFiles.length === 0 && imageFiles.length === 0) continue;
      hasContent = true;

      const dayPublicAssetDir = path.join(PUBLIC_ASSETS_DIR, weekFolderName, dayFolder);
      if (!fs.existsSync(dayPublicAssetDir)) fs.mkdirSync(dayPublicAssetDir, { recursive: true });

      for (const img of imageFiles) {
        fs.copyFileSync(path.join(dayFolderPath, img), path.join(dayPublicAssetDir, img));
      }

      const publicPathPrefix = `/assets/weekly/${weekFolderName}/${dayFolder}`;
      const displayDayName = dayFolder.replace(/^\d+_/, '');
      compiledMarkdown += `## ${displayDayName}\n\n`;

      let dayText = '';
      const linkedImages = new Set();

      for (const mdFile of markdownFiles) {
        let rawContent = fs.readFileSync(path.join(dayFolderPath, mdFile), 'utf-8');
        const wikilinkRegex = /!\[\[(.*?)\]\]/g;
        let match;
        while ((match = wikilinkRegex.exec(rawContent)) !== null) linkedImages.add(match[1]);

        rawContent = processMarkdown(rawContent, publicPathPrefix);
        dayText += rawContent + '\n\n';
      }

      compiledMarkdown += dayText;

      const unlinkedImages = imageFiles.filter(img => !linkedImages.has(img));
      if (unlinkedImages.length > 0) {
        compiledMarkdown += `\n### Gallery\n\n`;
        for (const unlinkedImg of unlinkedImages) {
          compiledMarkdown += `![${unlinkedImg}](${publicPathPrefix}/${unlinkedImg})\n\n`;
        }
      }
      compiledMarkdown += `---\n\n`;
    }

    if (hasContent) {
      fs.writeFileSync(path.join(COMPILED_DIR, `${weekFolderName}.md`), compiledMarkdown, 'utf-8');
    }
  }
};

buildTemplates();
