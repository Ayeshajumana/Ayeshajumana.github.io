$lines = [IO.File]::ReadAllLines("index.html")

$part1 = $lines[0..1765]
$part2 = [IO.File]::ReadAllLines("css_new.txt")
$part3 = $lines[1949..2144]
$part4 = [IO.File]::ReadAllLines("mq_new.txt")
$part5 = $lines[2156..2684]
$part6 = [IO.File]::ReadAllLines("html_new.txt")
$part7 = $lines[2718..3598]
$part8 = [IO.File]::ReadAllLines("js_new.txt")
$part9 = $lines[3667..($lines.Length-1)]

$newLines = $part1 + $part2 + $part3 + $part4 + $part5 + $part6 + $part7 + $part8 + $part9

[IO.File]::WriteAllLines("index.html", $newLines)
Write-Host "Replacement complete!"
