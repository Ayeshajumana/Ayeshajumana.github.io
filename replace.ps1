$content = [IO.File]::ReadAllText("index.html")

# 1. Replace CSS
$css_old = [IO.File]::ReadAllText("css_old.txt")
$css_new = [IO.File]::ReadAllText("css_new.txt")
$content = $content.Replace($css_old, $css_new)

# 2. Replace MQ
$mq_old = [IO.File]::ReadAllText("mq_old.txt")
$mq_new = [IO.File]::ReadAllText("mq_new.txt")
$content = $content.Replace($mq_old, $mq_new)

# 3. Replace HTML
$html_old = [IO.File]::ReadAllText("html_old.txt")
$html_new = [IO.File]::ReadAllText("html_new.txt")
$content = $content.Replace($html_old, $html_new)

# 4. Replace JS
$js_old = [IO.File]::ReadAllText("js_old.txt")
$js_new = [IO.File]::ReadAllText("js_new.txt")
$content = $content.Replace($js_old, $js_new)

[IO.File]::WriteAllText("index.html", $content)
Write-Host "Done"
