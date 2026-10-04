import re
import sys

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

content = read_file('index.html')

# 1. Replace CSS (.journey-dashboard to .paper-airplane closing brace)
css_pattern = re.compile(r'\.journey-dashboard\s*\{.*?\/\*\s*Journal Modal\s*\*\//', re.DOTALL)

css_replacement = """\
.journey-dashboard {
            max-width: 1300px;
            margin: 0 auto 5rem auto;
            display: grid;
            grid-template-columns: 1fr 1.3fr;
            gap: 4rem;
            position: relative;
        }

        .flight-path-svg {
            position: absolute;
            top: 50%;
            left: 20%;
            width: 80%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
            overflow: visible;
        }

        .destination-sheet {
            background: #fdf8e9;
            color: #2b1133;
            border-radius: 4px;
            padding: 4rem 3rem;
            position: relative;
            box-shadow: 10px 15px 30px rgba(0,0,0,0.4), inset 0 0 40px rgba(200, 170, 140, 0.2);
            border: 1px solid rgba(0,0,0,0.1);
            transform: rotate(-1deg);
            z-index: 2;
        }

        .destination-header {
            font-family: var(--font-body);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 3px;
            color: #8b6b72;
            margin-bottom: 2rem;
            font-weight: 600;
        }

        .current-destination-text {
            font-family: var(--font-display);
            font-size: 3.2rem;
            line-height: 1.1;
            color: #2c1236;
            margin-bottom: 2rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .current-progress-text {
            font-family: var(--font-body);
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #6a4c52;
            font-weight: 600;
        }

        .destination-annotation {
            font-family: var(--font-handwritten);
            font-size: 1.8rem;
            color: #9824d6;
            position: absolute;
            bottom: 2rem;
            right: 2rem;
            transform: rotate(-5deg);
            opacity: 0.8;
            line-height: 1;
        }

        .compass-illustration {
            position: absolute;
            bottom: 3rem;
            right: 4rem;
            width: 120px;
            height: 120px;
            opacity: 0.1;
            pointer-events: none;
            color: #2b1133;
        }

        .passport-panel {
            background: #2a0f2b;
            border-radius: 8px;
            padding: 3rem;
            position: relative;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5), inset 0 0 0 2px rgba(255,255,255,0.05);
            color: var(--color-text-main);
            z-index: 2;
        }
        
        .passport-panel::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,0.02) 10px, rgba(255,255,255,0.02) 11px);
            pointer-events: none;
            border-radius: 8px;
        }

        .passport-header {
            font-family: var(--font-display);
            font-size: 2.2rem;
            color: #fdf8e9;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            border-bottom: 2px dashed rgba(255,255,255,0.1);
            padding-bottom: 1rem;
        }

        .passport-meta {
            display: flex;
            gap: 2rem;
            font-family: var(--font-body);
            font-size: 0.85rem;
            color: rgba(253, 248, 233, 0.7);
            margin-bottom: 2.5rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            flex-wrap: wrap;
        }

        .passport-meta strong {
            color: #fdf8e9;
        }

        .passport-stamps-container {
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            position: relative;
            z-index: 2;
        }

        .passport-stamp {
            width: 100px;
            height: 100px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border: 2px solid rgba(253, 248, 233, 0.2);
            border-radius: 4px;
            padding: 0.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            background: transparent;
            position: relative;
        }

        .passport-stamp::after {
            content: '';
            position: absolute;
            inset: -4px;
            border: 1px dashed rgba(253, 248, 233, 0.15);
            border-radius: 6px;
        }

        .passport-stamp:hover {
            transform: scale(1.05) rotate(2deg);
            border-color: #9824d6;
            background: rgba(152, 36, 214, 0.1);
            z-index: 5;
        }

        .passport-stamp.completed {
            border-color: #d896ff;
            color: #d896ff;
            transform: rotate(-3deg);
        }

        .passport-stamp.completed::after {
            border-color: rgba(216, 150, 255, 0.3);
        }
        
        .passport-stamp.current {
            border-color: #ff00ff;
            color: #ff00ff;
            background: rgba(255, 0, 255, 0.08);
            transform: rotate(4deg) scale(1.1) !important;
            box-shadow: 0 0 15px rgba(255, 0, 255, 0.2);
            z-index: 10;
        }

        .passport-stamp.upcoming {
            opacity: 0.25;
            border-style: dotted;
            cursor: not-allowed;
        }
        
        .passport-stamp.upcoming:hover {
            transform: none;
            border-color: rgba(253, 248, 233, 0.3);
            background: transparent;
        }

        .passport-stamp:nth-child(3n) { transform: rotate(2deg); }
        .passport-stamp:nth-child(3n+1) { transform: rotate(-1deg); }
        .passport-stamp:nth-child(3n+2) { transform: rotate(3deg); }

        .stamp-week {
            font-family: var(--font-display);
            font-size: 1.8rem;
            line-height: 1;
            margin-bottom: 0.4rem;
        }

        .stamp-status {
            font-family: var(--font-body);
            font-size: 0.65rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-align: center;
        }

        .passport-stamp.completed .stamp-status {
            color: #d896ff;
        }

        .paper-airplane {
            position: absolute;
            z-index: 20;
            width: 45px;
            height: 45px;
            transition: all 1.2s cubic-bezier(0.34, 1.56, 0.64, 1);
            filter: drop-shadow(0 5px 10px rgba(0,0,0,0.4));
            opacity: 0;
            pointer-events: none;
        }

        /* Journal Modal */"""

i1 = content.find('.journey-dashboard {')
i2 = content.find('/* Journal Modal */', i1)
if i1 != -1 and i2 != -1:
    content = content[:i1] + css_replacement + content[i2 + 19:]
else:
    print("Failed to find CSS block")
    
# 2. Replace CSS mobile queries
mq_old = """\
            .journey-dashboard {
                grid-template-columns: 1fr;
            }
            .journey-map-container {
                flex-direction: column;
                align-items: center;
            }
            .journey-stamp {
                width: 100%;
                max-width: 320px;
            }\
"""
mq_new = """\
            .journey-dashboard {
                grid-template-columns: 1fr;
                gap: 2rem;
            }
            .passport-stamp {
                width: 80px;
                height: 80px;
            }
            .stamp-week {
                font-size: 1.4rem;
            }\
"""
content = content.replace(mq_old, mq_new)

# 3. Replace HTML Structure
html_old = """\
            <div class="journey-dashboard">
                <!-- Current Destination -->
                <div class="journey-tracker-card">
                    <div class="journey-tracker-title">CURRENT DESTINATION</div>
                    <div class="current-destination-text" id="current-destination-text">Loading...</div>
                    <div class="current-progress-text" id="current-progress-text">0 / 20 weeks completed</div>
                </div>

                <!-- Price Passport -->
                <div class="journey-tracker-card">
                    <div class="journey-tracker-title">🛂 MY PRICE PASSPORT</div>
                    <div style="display:flex; gap: 1.5rem; color: var(--color-text-secondary); font-family: var(--font-body); font-size: 0.85rem; margin-bottom: 0.5rem; flex-wrap: wrap;">
                        <div><strong style="color:var(--color-text-main)">JOURNEY:</strong> PRICE Protosem</div>
                        <div><strong style="color:var(--color-text-main)">DURATION:</strong> 20 Weeks</div>
                        <div><strong style="color:var(--color-text-main)">STATUS:</strong> In Flight <svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-left: 0.2rem;"><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon><line x1="22" y1="2" x2="11" y2="13"></line></svg></div>
                    </div>
                    <div class="passport-stamps-grid" id="passport-stamps-grid">
                        <!-- Stamps injected by JS -->
                    </div>
                </div>
            </div>

            <!-- The Map -->
            <div class="journey-map-container" id="journey-map-container">
                <div class="paper-airplane" id="paper-airplane">
                    <svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        <line x1="22" y1="2" x2="11" y2="13"></line>
                    </svg>
                </div>
                <!-- Weekly Stamps injected by JS -->
            </div>\
"""

html_new = """\
            <div class="journey-dashboard passport-redesign">
                <!-- Flight Path Background -->
                <svg class="flight-path-svg" viewBox="0 0 800 400" preserveAspectRatio="none">
                    <path d="M 200,100 Q 400,-50 600,150 T 800,50" fill="none" stroke="rgba(253, 248, 233, 0.15)" stroke-width="3" stroke-dasharray="8 8" />
                </svg>

                <!-- Current Destination -->
                <div class="destination-sheet">
                    <div class="destination-header">CURRENT DESTINATION</div>
                    <div class="current-destination-text" id="current-destination-text">Loading...</div>
                    <div class="current-progress-text" id="current-progress-text">0 / 20 weeks completed</div>
                    <div class="destination-annotation">better questions.<br>bigger possibilities.</div>
                    
                    <div class="compass-illustration">
                        <svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="50" cy="50" r="45" stroke-dasharray="4 4" />
                            <circle cx="50" cy="50" r="35" />
                            <path d="M50 15 L60 50 L50 85 L40 50 Z" fill="currentColor" />
                            <path d="M50 15 L50 85" stroke-width="1" />
                            <path d="M15 50 L85 50" stroke-width="1" stroke-dasharray="2 2" />
                            <text x="50" y="10" text-anchor="middle" font-size="10" font-family="sans-serif">N</text>
                            <text x="50" y="98" text-anchor="middle" font-size="10" font-family="sans-serif">S</text>
                            <text x="92" y="53" text-anchor="middle" font-size="10" font-family="sans-serif">E</text>
                            <text x="8" y="53" text-anchor="middle" font-size="10" font-family="sans-serif">W</text>
                        </svg>
                    </div>
                </div>

                <!-- Price Passport -->
                <div class="passport-panel">
                    <div class="passport-header">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16v16H4z"/><path d="M4 10h16"/><circle cx="12" cy="16" r="2"/></svg>
                        MY PRICE PASSPORT
                    </div>
                    <div class="passport-meta">
                        <div><strong>JOURNEY:</strong> PRICE Protosem</div>
                        <div><strong>DURATION:</strong> 20 Weeks</div>
                        <div><strong>STATUS:</strong> In Flight</div>
                    </div>
                    <div class="passport-stamps-container" id="passport-stamps-grid">
                        <!-- Stamps injected by JS -->
                    </div>
                </div>
                
                <!-- Animated Paper Airplane -->
                <div class="paper-airplane" id="paper-airplane">
                    <svg viewBox="0 0 24 24" width="100%" height="100%">
                        <polygon points="22 2 15 22 11 13 2 9 22 2" fill="#fdf8e9" stroke="#2b1133" stroke-width="1" stroke-linejoin="round"></polygon>
                        <polygon points="22 2 11 13 15 22" fill="#eaddc5" stroke="#2b1133" stroke-width="1" stroke-linejoin="round"></polygon>
                    </svg>
                </div>
            </div>
            
            <!-- Map container removed, keeping ID for compatibility if needed -->
            <div id="journey-map-container" style="display:none;"></div>\
"""

if html_old in content:
    content = content.replace(html_old, html_new)
else:
    print("Failed to find HTML block")
    
# 4. Replace JS Logic
js_old = """\
            const mapContainer = document.getElementById('journey-map-container');
            const passportGrid = document.getElementById('passport-stamps-grid');
            let completedCount = 0;
            let latestCompletedIndex = -1;

            protosemJourneyData.weeks.forEach((week, index) => {
                if (week.status === 'COMPLETED') {
                    completedCount++;
                    latestCompletedIndex = index;
                }

                // Render Stamp
                const stamp = document.createElement('div');
                stamp.className = `journey-stamp ${week.status.toLowerCase()}`;
                if (index === latestCompletedIndex) stamp.classList.add('current');
                stamp.dataset.index = index;
                stamp.id = `stamp-w${week.weekNumber}`;

                stamp.innerHTML = `
                    <div class="stamp-week">W${String(week.weekNumber).padStart(2, '0')}</div>
                    <div class="stamp-label">${week.journeyLabel || week.title}</div>
                    <div class="stamp-status">${week.status === 'COMPLETED' ? '✓ LANDED' : (week.status === 'UPCOMING' ? 'UPCOMING' : week.status)}</div>
                `;

                mapContainer.appendChild(stamp);

                // Render Passport Mini Stamp
                const miniStamp = document.createElement('div');
                miniStamp.className = `passport-mini-stamp ${week.status === 'COMPLETED' ? 'completed' : ''}`;
                miniStamp.textContent = `W${String(week.weekNumber).padStart(2, '0')}`;
                passportGrid.appendChild(miniStamp);
                
                // Click event for modal
                if (week.status !== 'UPCOMING') {
                    stamp.addEventListener('click', () => openJournalModal(week));
                }
            });

            // Update Dashboard Stats
            document.getElementById('current-progress-text').textContent = `${completedCount} / ${protosemJourneyData.totalWeeks} weeks completed`;
            if (latestCompletedIndex >= 0) {
                document.getElementById('current-destination-text').textContent = `WEEK ${String(protosemJourneyData.weeks[latestCompletedIndex].weekNumber).padStart(2, '0')} — ${protosemJourneyData.weeks[latestCompletedIndex].title}`;
            }

            // Animate Airplane
            const airplane = document.getElementById('paper-airplane');
            const positionAirplane = () => {
                if (latestCompletedIndex >= 0) {
                    const targetStamp = document.getElementById(`stamp-w${protosemJourneyData.weeks[latestCompletedIndex].weekNumber}`);
                    if (targetStamp) {
                        const containerRect = mapContainer.getBoundingClientRect();
                        const targetRect = targetStamp.getBoundingClientRect();
                        
                        // Calculate relative position to land near the stamp
                        const left = targetRect.left - containerRect.left + (targetRect.width / 2) - 20;
                        const top = targetRect.top - containerRect.top - 40;
                        
                        airplane.style.opacity = '1';
                        airplane.style.left = `${left}px`;
                        airplane.style.top = `${top}px`;
                    }
                }
            };
            
            // Wait for layout to settle before positioning
            setTimeout(positionAirplane, 500);
            window.addEventListener('resize', positionAirplane);\
"""

js_new = """\
            const passportGrid = document.getElementById('passport-stamps-grid');
            let completedCount = 0;
            let latestCompletedIndex = -1;

            if (passportGrid) passportGrid.innerHTML = '';

            protosemJourneyData.weeks.forEach((week, index) => {
                if (week.status === 'COMPLETED') {
                    completedCount++;
                    latestCompletedIndex = index;
                }

                // Render Stamp
                const stamp = document.createElement('div');
                stamp.className = `passport-stamp ${week.status.toLowerCase()}`;
                if (index === latestCompletedIndex) stamp.classList.add('current');
                stamp.dataset.index = index;
                stamp.id = `stamp-w${week.weekNumber}`;

                let statusText = week.status;
                if (week.status === 'COMPLETED') statusText = '✓ LANDED';
                else if (week.status === 'UPCOMING') {
                    statusText = (week.weekNumber === protosemJourneyData.totalWeeks) ? 'FINAL STOP' : 'NEXT STOP';
                }

                stamp.innerHTML = `
                    <div class="stamp-week">W${String(week.weekNumber).padStart(2, '0')}</div>
                    <div class="stamp-status">${statusText}</div>
                `;

                if (passportGrid) passportGrid.appendChild(stamp);
                
                // Click event for modal
                if (week.status !== 'UPCOMING') {
                    stamp.addEventListener('click', () => openJournalModal(week));
                }
            });

            // Update Dashboard Stats
            const progressEl = document.getElementById('current-progress-text');
            const destinationEl = document.getElementById('current-destination-text');
            if (progressEl) progressEl.textContent = `${completedCount} / ${protosemJourneyData.totalWeeks} WEEKS COMPLETED`;
            if (latestCompletedIndex >= 0 && destinationEl) {
                destinationEl.innerHTML = `WEEK ${String(protosemJourneyData.weeks[latestCompletedIndex].weekNumber).padStart(2, '0')} &mdash;<br>${protosemJourneyData.weeks[latestCompletedIndex].title}`;
            }

            // Animate Airplane
            const airplane = document.getElementById('paper-airplane');
            const positionAirplane = () => {
                if (latestCompletedIndex >= 0 && airplane) {
                    const targetStamp = document.getElementById(`stamp-w${protosemJourneyData.weeks[latestCompletedIndex].weekNumber}`);
                    if (targetStamp) {
                        const dashboardRect = document.querySelector('.journey-dashboard').getBoundingClientRect();
                        const targetRect = targetStamp.getBoundingClientRect();
                        
                        const left = targetRect.left - dashboardRect.left + (targetRect.width / 2) - 22;
                        const top = targetRect.top - dashboardRect.top - 22;
                        
                        airplane.style.opacity = '1';
                        airplane.style.left = `${left}px`;
                        airplane.style.top = `${top}px`;
                    }
                }
            };
            
            // Wait for layout to settle before positioning
            setTimeout(positionAirplane, 500);
            window.addEventListener('resize', positionAirplane);\
"""

# Try both exact match and a loose regex match for js since there might be encoding issues like unicode checkmarks
js_old_clean = js_old.replace('✓', '✓').replace('—', '—')
if js_old_clean in content:
    content = content.replace(js_old_clean, js_new)
else:
    # Use regex to find it
    js_pattern = re.compile(r'const mapContainer = document\.getElementById\(\'journey-map-container\'\);.*?window\.addEventListener\(\'resize\', positionAirplane\);', re.DOTALL)
    if js_pattern.search(content):
        content = js_pattern.sub(js_new, content)
    else:
        print("Failed to find JS block")

write_file('index.html', content)
print("Done")
