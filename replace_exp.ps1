$content = [IO.File]::ReadAllText("index.html")

# 1. Replace CSS
$css_pattern = '(?s)/\*\s*EXPERIENCE SECTION STYLES\s*\*/.*?(?=\s*/\*\s*==========================================\s*\*/\s*/\*\s*RESEARCH & PROJECTS SECTION)'
$new_css = [IO.File]::ReadAllText("new_css.txt")
$content = $content -replace $css_pattern, $new_css

# 2. Replace HTML
$html_pattern = '(?s)<section id="experience".*?</section>'
$new_html = [IO.File]::ReadAllText("new_html.txt")
$content = $content -replace $html_pattern, $new_html

# 3. Replace Data
$data_pattern = '(?s)experiences:\s*\[.*?\],(?=\s*// ==========================================\s*// RESEARCH & PROJECTS DATA)'
$new_data = [IO.File]::ReadAllText("new_data.txt")
$content = $content -replace $data_pattern, $new_data

# 4. Replace JS Logic
$js_pattern = '(?s)// 9\. Render Experience Timeline.*?\}\);.*?(?=\s*// 10\. Render Research & Projects Section)'
$new_js = [IO.File]::ReadAllText("new_js.txt")
$content = $content -replace $js_pattern, $new_js

[IO.File]::WriteAllText("index.html", $content)
Write-Host "Replacement Complete."
