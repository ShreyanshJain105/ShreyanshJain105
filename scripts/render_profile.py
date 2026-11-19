#!/usr/bin/env python3
from __future__ import annotations
import json, os, urllib.request, datetime as dt, html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS, DATA = ROOT / "assets", ROOT / "data"
USER = os.getenv("GITHUB_USERNAME", "ShreyanshJain105")
TOKEN = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
NOW = dt.datetime.now(dt.timezone.utc)

def e(x):
    return html.escape(str(x or ""), quote=True)

def api(path, method="GET", payload=None):
    h = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "profile-svg-generator"
    }
    if TOKEN:
        h["Authorization"] = "Bearer " + TOKEN
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request("https://api.github.com" + path, data=body, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode())

def tx(x, y, s, size=14, color="#e2e8f0", weight="400", font="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{color}">{e(s)}</text>'

def doc(w, h, b, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<title>{e(title)}</title>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#060a12"/>
    <stop offset="50%" stop-color="#0b1324"/>
    <stop offset="100%" stop-color="#101c36"/>
  </linearGradient>
  <linearGradient id="panelBg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#091222"/>
    <stop offset="100%" stop-color="#0d1b33"/>
  </linearGradient>
  <linearGradient id="borderGlow" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8"/>
    <stop offset="50%" stop-color="#1e3a5f" stop-opacity="0.35"/>
    <stop offset="100%" stop-color="#6366f1" stop-opacity="0.75"/>
  </linearGradient>
  <linearGradient id="cyanGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#38bdf8"/>
    <stop offset="100%" stop-color="#0284c7"/>
  </linearGradient>
  <linearGradient id="emeraldGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#34d399"/>
    <stop offset="100%" stop-color="#059669"/>
  </linearGradient>
  <linearGradient id="violetGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#a78bfa"/>
    <stop offset="100%" stop-color="#6366f1"/>
  </linearGradient>
  <linearGradient id="ac" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#38bdf8"/>
    <stop offset="100%" stop-color="#818cf8"/>
  </linearGradient>
  <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
    <path d="M 28 0 L 0 0 0 28" fill="none" stroke="#172844" stroke-width="0.6" stroke-opacity="0.32"/>
  </pattern>
</defs>
{b}
</svg>'''

def base(w, h, show_status=True):
    s = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="url(#bg)"/>'
    s += f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="url(#grid)"/>'
    s += f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="none" stroke="url(#borderGlow)" stroke-width="1.2"/>'
    
    if show_status and w >= 600:
        pill_w, pill_h = 220, 26
        px = w - pill_w - 24
        py = 18
        s += f'<rect x="{px}" y="{py}" width="{pill_w}" height="{pill_h}" rx="6" fill="#091426" stroke="#1e3a5f" stroke-width="1"/>'
        s += f'<circle cx="{px+14}" cy="{py+13}" r="4" fill="#10b981"/>'
        s += f'<circle cx="{px+14}" cy="{py+13}" r="8" fill="none" stroke="#10b981" opacity="0.6"><animate attributeName="r" values="4;10;4" dur="2.4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.8;0.1;0.8" dur="2.4s" repeatCount="indefinite"/></circle>'
        s += f'<text x="{px+28}" y="{py+17}" font-family="monospace" font-size="11" font-weight="700" fill="#38bdf8" letter-spacing="1">SYSTEM : PROD_ONLINE</text>'
    elif w < 600:
        px = w - 24
        py = 28
        s += f'<circle cx="{px}" cy="{py}" r="3.5" fill="#10b981"/>'
        s += f'<circle cx="{px}" cy="{py}" r="7" fill="none" stroke="#10b981" opacity="0.6"><animate attributeName="r" values="3.5;8;3.5" dur="2.4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.8;0.1;0.8" dur="2.4s" repeatCount="indefinite"/></circle>'
    return s

def save(n, s):
    (ASSETS / n).write_text(s, encoding="utf-8")

def hero(p):
    b = base(1200, 310, show_status=True)
    
    # Left Section: Professional Identity & Enterprise Role
    b += '<rect x="36" y="24" width="310" height="24" rx="4" fill="#0c192e" stroke="#1e3a5f" stroke-width="0.8"/>'
    b += '<circle cx="48" cy="36" r="3.5" fill="#38bdf8"><animate attributeName="opacity" values="0.4;1;0.4" dur="2s" repeatCount="indefinite"/></circle>'
    b += tx(58, 40, "ENTERPRISE SYSTEMS // QUALITY ENGINEERING", 10.5, "#7dd3fc", "700", "monospace")
    
    b += tx(36, 88, "Shreyansh Jain", 35, "#f8fafc", "800")
    b += tx(38, 118, "SOFTWARE DEVELOPMENT ENGINEER IN TEST (SDET) • QUALITY ARCHITECT", 13.5, "#38bdf8", "700", "monospace")
    b += tx(38, 146, "Architecting resilient test automation, continuous quality gates, and high-scale API validation.", 13, "#94a3b8", "400")
    
    # Capability indicators
    b += tx(38, 180, "● CORE TECH : Java · Spring Boot · Selenium · Postman · REST Assured · SQL", 12, "#cbd5e1", "500", "monospace")
    b += tx(38, 204, "● DOMAINS   : Shift-Left QA · Microservices Reliability · End-to-End Test Automation", 12, "#cbd5e1", "500", "monospace")
    b += tx(38, 228, "● DEVOPS    : Resilient CI/CD Pipelines · Automated Sanity & Regression Gates · Docker", 12, "#cbd5e1", "500", "monospace")
    
    # Metric badges row
    badges = [
        ("CI/CD: AUTOMATED", "#10b981", 38),
        ("COVERAGE: HIGH-RELIABILITY", "#38bdf8", 205),
        ("ZERO-DEFECT MINDSET", "#818cf8", 435)
    ]
    for label, col, bx in badges:
        bw = len(label) * 7.5 + 24
        b += f'<rect x="{bx}" y="254" width="{bw}" height="24" rx="5" fill="#091426" stroke="{col}" stroke-opacity="0.4" stroke-width="1"/>'
        b += f'<circle cx="{bx+10}" cy="{266}" r="3" fill="{col}"/>'
        b += tx(bx + 18, 270, label, 10, col, "700", "monospace")
    
    # Right Section: Enterprise Automation HUD & Live Telemetry Console (NO Personal Image)
    hud_x, hud_y, hud_w, hud_h = 675, 28, 490, 256
    b += f'<rect x="{hud_x}" y="{hud_y}" width="{hud_w}" height="{hud_h}" rx="10" fill="#08101e" stroke="#1e385c" stroke-width="1.2"/>'
    b += f'<rect x="{hud_x}" y="{hud_y}" width="{hud_w}" height="28" rx="10" fill="#0e1b30"/>'
    b += f'<rect x="{hud_x}" y="{hud_y+20}" width="{hud_w}" height="8" fill="#0e1b30"/>'
    
    # Terminal control dots
    b += f'<circle cx="{hud_x+16}" cy="{hud_y+14}" r="4" fill="#ef4444"/>'
    b += f'<circle cx="{hud_x+30}" cy="{hud_y+14}" r="4" fill="#f59e0b"/>'
    b += f'<circle cx="{hud_x+44}" cy="{hud_y+14}" r="4" fill="#10b981"/>'
    b += tx(hud_x + 60, hud_y + 18, "sys://sdet-telemetry.mnc-core.v3", 10.5, "#7dd3fc", "700", "monospace")
    
    # Radar Scanner Widget (Left inside HUD)
    rx, ry, rr = hud_x + 68, hud_y + 120, 52
    b += f'<circle cx="{rx}" cy="{ry}" r="{rr}" fill="#060c18" stroke="#162942" stroke-width="1.2"/>'
    b += f'<circle cx="{rx}" cy="{ry}" r="{rr*0.68}" fill="none" stroke="#1b3354" stroke-width="0.8" stroke-dasharray="3 3"/>'
    b += f'<circle cx="{rx}" cy="{ry}" r="{rr*0.35}" fill="none" stroke="#254875" stroke-width="0.8"/>'
    b += f'<line x1="{rx-rr}" y1="{ry}" x2="{rx+rr}" y2="{ry}" stroke="#1b3354" stroke-width="0.8"/>'
    b += f'<line x1="{rx}" y1="{ry-rr}" x2="{rx}" y2="{ry+rr}" stroke="#1b3354" stroke-width="0.8"/>'
    
    # Animated Radar Sweep Line
    b += f'''<line x1="{rx}" y1="{ry}" x2="{rx+rr}" y2="{ry}" stroke="#38bdf8" stroke-width="1.8" opacity="0.85">
      <animateTransform attributeName="transform" type="rotate" from="0 {rx} {ry}" to="360 {rx} {ry}" dur="4s" repeatCount="indefinite"/>
    </line>'''
    
    # Radar blips
    b += f'<circle cx="{rx+22}" cy="{ry-18}" r="3" fill="#10b981"><animate attributeName="opacity" values="0.2;1;0.2" dur="2s" repeatCount="indefinite"/></circle>'
    b += f'<circle cx="{rx-18}" cy="{ry+20}" r="2.5" fill="#38bdf8"><animate attributeName="opacity" values="1;0.2;1" dur="2.4s" repeatCount="indefinite"/></circle>'
    b += tx(rx - 48, ry + rr + 18, "RADAR: AUTOMATION HEALTH 100%", 8.5, "#34d399", "700", "monospace")
    
    # Monospace Live Telemetry Stream (Right inside HUD)
    lx = hud_x + 148
    lines = [
        ("$ sys.role     -> SDET / Software Engineer", "#cbd5e1"),
        ("$ env.tier     -> Enterprise Tier (MNC)", "#7dd3fc"),
        ("$ test.gate    -> [PASS] Zero-Critical Defect", "#34d399"),
        ("$ api.status   -> 200 OK / Automated Suites", "#cbd5e1"),
        ("$ suite.cov    -> Regression & E2E Active", "#a78bfa"),
        ("$ cicd.cadence -> Automated Daily Releases", "#38bdf8")
    ]
    for i, (ln, col) in enumerate(lines):
        b += tx(lx, hud_y + 56 + i * 24, ln, 11, col, "600", "monospace")
    
    # Blinking prompt cursor
    cur_y = hud_y + 56 + len(lines) * 24
    b += tx(lx, cur_y, "$ telemetry_stream: ACTIVE", 11, "#94a3b8", "600", "monospace")
    b += f'<rect x="{lx+185}" y="{cur_y-10}" width="8" height="12" fill="#38bdf8"><animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite"/></rect>'
    
    return doc(1200, 310, b, "Shreyansh Jain — Enterprise SDET Profile")

def tile(title, sub, color, num, tag):
    w, h = 385, 155
    b = base(w, h, show_status=False)
    
    # Number badge
    b += f'<rect x="20" y="20" width="38" height="38" rx="8" fill="#0b172a" stroke="{color}" stroke-opacity="0.5" stroke-width="1.2"/>'
    b += tx(29, 45, num, 18, color, "800", "monospace")
    
    # Title & Tag
    b += tx(68, 36, title, 16, "#f8fafc", "800")
    b += tx(68, 52, tag, 9.5, color, "700", "monospace")
    
    # Description
    b += tx(20, 88, sub, 12, "#94a3b8", "500")
    
    # Animated bottom data stream line
    b += f'''<path d="M20 128 h{w-40}" stroke="{color}" stroke-width="1.5" stroke-opacity="0.3"/>
    <path d="M20 128 h{w-40}" stroke="{color}" stroke-width="2" stroke-dasharray="30 200">
      <animate attributeName="stroke-dashoffset" values="230;0" dur="3s" repeatCount="indefinite"/>
    </path>'''
    
    return doc(w, h, b, title)

def contrib(calendar, events):
    b = base(1200, 260, show_status=True)
    
    b += '<rect x="30" y="22" width="290" height="22" rx="4" fill="#0c192e" stroke="#1e3a5f" stroke-width="0.8"/>'
    b += tx(40, 37, "CONTINUOUS INTEGRATION // CONTRIBUTION SIGNAL", 10.5, "#7dd3fc", "700", "monospace")
    
    if calendar:
        vals = [d["contributionCount"] for wk in calendar["weeks"] for d in wk["contributionDays"]]
        total = calendar["totalContributions"]
        label = "365-DAY ENTERPRISE CONTRIBUTION CALENDAR (GRAPHQL VERIFIED)"
    else:
        vals = [events.get((NOW.date() - dt.timedelta(days=i)).isoformat(), 0) for i in range(364, -1, -1)]
        total = sum(vals)
        label = "PUBLIC REPOSITORY EVENT ACTIVITY (SYNC WITH GH_TOKEN FOR COMPLETE CALENDAR)"
        
    b += tx(30, 68, label, 10.5, "#94a3b8", "600", "monospace")
    b += tx(960, 46, f"{total:,} CONTRIBUTIONS", 17, "#38bdf8", "800", "monospace")
    b += tx(960, 66, "STATUS : VERIFIED", 10, "#34d399", "700", "monospace")
    
    shades = ["#0e1726", "#064e6b", "#0284c7", "#38bdf8", "#10b981"]
    for i, c in enumerate(vals[-371:]):
        level = 0 if c == 0 else 1 if c == 1 else 2 if c <= 3 else 3 if c <= 6 else 4
        x = 30 + (i // 7) * 16.5
        y = 96 + (i % 7) * 16.5
        b += f'<rect x="{x}" y="{y}" width="12" height="12" rx="2.5" fill="{shades[level]}"><title>{c} contributions</title></rect>'
        
    # Legend
    b += tx(30, 236, "LESS", 9.5, "#64748b", "600", "monospace")
    for i, c in enumerate(shades):
        b += f'<rect x="{72+i*18}" y="{226}" width="11" height="11" rx="2.5" fill="{c}"/>'
    b += tx(174, 236, "MORE", 9.5, "#64748b", "600", "monospace")
    b += tx(350, 236, "Automated daily ingestion tracks enterprise commits, pull requests, issues & code reviews.", 10, "#64748b")
    
    return doc(1200, 260, b, "GitHub Contribution Signal")

def daily_commits(calendar, events):
    b = base(1200, 250, show_status=True)
    
    b += '<rect x="30" y="22" width="280" height="22" rx="4" fill="#0c192e" stroke="#1e3a5f" stroke-width="0.8"/>'
    b += tx(40, 37, "SPRINT VELOCITY & COMMIT CADENCE // 30-DAY WINDOW", 10.5, "#7dd3fc", "700", "monospace")
    
    days = []
    if calendar:
        days = [d for wk in calendar["weeks"] for d in wk["contributionDays"]][-30:]
        label = "VERIFIED GITHUB GRAPHQL DAILY ACTIVITY"
    else:
        for i in range(29, -1, -1):
            day = (NOW.date() - dt.timedelta(days=i)).isoformat()
            days.append({"date": day, "contributionCount": events.get(day, 0)})
        label = "PUBLIC REPOSITORY EVENTS (CONFIGURE GH_TOKEN FOR FULL METRICS)"
        
    b += tx(30, 68, label, 10, "#94a3b8", "600", "monospace")
    vals = [int(d.get("contributionCount", 0)) for d in days]
    maxv = max(vals + [1])
    total = sum(vals)
    
    b += tx(980, 46, f"{total:,} TOTAL IN 30D", 17, "#38bdf8", "800", "monospace")
    
    for i, d in enumerate(days):
        v = int(d.get("contributionCount", 0))
        x = 34 + i * 37.5
        h = max(4, int(105 * v / maxv))
        y = 192 - h
        
        # Bar with animated pulse on non-zero
        color = "url(#ac)" if v > 0 else "#14243b"
        b += f'<rect x="{x}" y="{y}" width="24" height="{h}" rx="4" fill="{color}"><title>{e(d.get("date"))}: {v} contributions</title></rect>'
        if v > 0:
            b += f'<circle cx="{x+12}" cy="{y}" r="2" fill="#38bdf8"/>'
            
        if i % 5 == 0 or i == len(days) - 1:
            b += tx(x - 2, 212, d.get("date", "")[5:], 9, "#64748b", "500", "monospace")
            
    b += tx(30, 235, "Daily sprint velocity reflects continuous quality automation, test refactoring, and feature validation.", 10, "#64748b")
    return doc(1200, 250, b, "Daily Commit Velocity")

def activity(events):
    b = base(1200, 215, show_status=True)
    
    b += '<rect x="30" y="22" width="270" height="22" rx="4" fill="#0c192e" stroke="#1e3a5f" stroke-width="0.8"/>'
    b += tx(40, 37, "RELEASE CADENCE & SPRINT WORKFLOW // 12 WEEKS", 10.5, "#7dd3fc", "700", "monospace")
    
    vals = []
    for i in range(12):
        d = (NOW.date() - dt.timedelta(days=(11 - i) * 7)).isoformat()
        end_d = (dt.date.fromisoformat(d) + dt.timedelta(days=6)).isoformat()
        vals.append(sum(v for k, v in events.items() if d <= k <= end_d))
    mx = max(vals + [1])
    
    for i, v in enumerate(vals):
        x = 38 + i * 92
        bh = max(6, int(88 * v / mx))
        y = 150 - bh
        b += f'''<rect x="{x}" y="{y}" width="52" height="{bh}" rx="6" fill="url(#ac)">
          <animate attributeName="opacity" values="0.75;1;0.75" dur="{2.2 + i*0.12}s" repeatCount="indefinite"/>
        </rect>'''
        b += tx(x + 14, 172, str(v), 11, "#e2e8f0", "700", "monospace")
        b += tx(x + 12, 192, f"W{i+1}", 9.5, "#64748b", "600", "monospace")
        
    b += tx(1030, 52, "ENTERPRISE", 12, "#38bdf8", "800", "monospace")
    b += tx(1030, 70, "CADENCE", 12, "#34d399", "800", "monospace")
    return doc(1200, 215, b, "Recent Public Release Cadence")

def projects(repos):
    b = base(1200, 335, show_status=True)
    
    b += '<rect x="30" y="22" width="370" height="22" rx="4" fill="#0c192e" stroke="#1e3a5f" stroke-width="0.8"/>'
    b += tx(40, 37, "FEATURED ENTERPRISE SYSTEMS & OPEN-SOURCE ARCHITECTURES", 10.5, "#7dd3fc", "700", "monospace")
    
    selected = [
        ("CraveBite", "Distributed food ordering platform • REST APIs", "cravebite-frontend", "ENTERPRISE BUILD", "#38bdf8"),
        ("JobTrek", "Enterprise recruitment portal • React + Spring Boot", "JobTrek-UI", "ENTERPRISE BUILD", "#38bdf8"),
        ("coolify", "Self-hosted PaaS & Cloud Container Engine", "coolify", "OPEN-SOURCE // FORK", "#a78bfa"),
        ("rea", "Agent-based reverse engineering & binary analysis", "rea", "OPEN-SOURCE // FORK", "#a78bfa"),
        ("ruflo", "Claude multi-agent orchestration architecture", "ruflo", "OPEN-SOURCE // FORK", "#a78bfa")
    ]
    
    lang_map = {
        "cravebite-frontend": "JavaScript / React",
        "jobtrek-ui": "TypeScript / React",
        "coolify": "PHP / PaaS Engine",
        "rea": "TypeScript / Binary",
        "ruflo": "Python / AI Agents"
    }
    
    for i, (title, desc, name, tag, tag_col) in enumerate(selected):
        r = next((x for x in repos if x["name"].lower() == name.lower()), {})
        col = i % 3
        row = i // 3
        x = 30 + col * 385
        y = 68 + row * 118
        url = r.get("html_url", f"https://github.com/{USER}/{name}")
        lang = r.get("language") or lang_map.get(name.lower(), "Full-Stack")
        
        b += f'''<a href="{e(url)}" target="_blank">
          <rect x="{x}" y="{y}" width="365" height="98" rx="10" fill="#0c182c" stroke="#1f3757" stroke-width="1"/>
          <text x="{x+16}" y="{y+26}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-size="17" font-weight="800" fill="#f8fafc">{e(title)}</text>
          <text x="{x+16}" y="{y+48}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-size="11" fill="#94a3b8">{e(desc)}</text>
          <rect x="{x+16}" y="{y+62}" width="95" height="18" rx="4" fill="#08101e"/>
          <text x="{x+22}" y="{y+75}" font-family="monospace" font-size="9" font-weight="700" fill="#38bdf8">{e(lang)}</text>
          <text x="{x+120}" y="{y+75}" font-family="monospace" font-size="8.5" font-weight="700" fill="{tag_col}">{tag} ↗</text>
        </a>'''
        
    b += tx(30, 318, "Open-source repositories represent technical exploration and architectural analysis; forks are transparently identified.", 10, "#64748b")
    return doc(1200, 335, b, "Featured Enterprise Systems and Open-Source Architectures")

def main():
    profile = api("/users/" + USER)
    repos = []
    page = 1
    while page <= 3:
        batch = api(f"/users/{USER}/repos?per_page=100&sort=updated&page={page}")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
        
    raw = api(f"/users/{USER}/events/public?per_page=100")
    events = {}
    for ev in raw:
        day = ev.get("created_at", "")[:10]
        if day:
            events[day] = events.get(day, 0) + 1
            
    calendar = None
    if TOKEN:
        try:
            q = 'query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){contributionsCollection(from:$from,to:$to){contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}'
            start = (NOW - dt.timedelta(days=364)).replace(hour=0, minute=0, second=0, microsecond=0)
            end = NOW.replace(hour=23, minute=59, second=59, microsecond=0)
            res = api("/graphql", "POST", {"query": q, "variables": {"login": USER, "from": start.isoformat(), "to": end.isoformat()}})
            calendar = res["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        except Exception as err:
            print("GraphQL unavailable; falling back to public events:", err)
            
    (DATA / "github-data.json").write_text(json.dumps({
        "profile": profile,
        "repositories": repos,
        "public_events_by_date": events,
        "contribution_calendar": calendar,
        "generated_at": NOW.isoformat()
    }, indent=2), encoding="utf-8")
    
    save("hero.svg", hero(profile))
    save("build.svg", tile("ARCHITECTURE", "Java • Spring Boot • Microservices • REST APIs", "#38bdf8", "01", "ENTERPRISE CORE"))
    save("test.svg", tile("QUALITY ENGINEERING", "Selenium • TestNG • Postman • Shift-Left QA", "#10b981", "02", "ZERO-DEFECT GATES"))
    save("explore.svg", tile("CLOUD & AI DEVOPS", "Docker • CI/CD Automation • Multi-Agent Systems", "#a78bfa", "03", "RELIABILITY ENGINES"))
    save("contributions.svg", contrib(calendar, events))
    save("daily-commits.svg", daily_commits(calendar, events))
    save("activity.svg", activity(events))
    save("projects.svg", projects(repos))
    print(f"Rendered Enterprise Profile for @{USER}: {len(repos)} repositories processed.")

if __name__ == "__main__":
    main()
