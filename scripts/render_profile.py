#!/usr/bin/env python3
from __future__ import annotations
import json, os, urllib.request, datetime as dt, html
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ASSETS,DATA=ROOT/"assets",ROOT/"data"
USER=os.getenv("GITHUB_USERNAME","ShreyanshJain105")
TOKEN=os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
NOW=dt.datetime.now(dt.timezone.utc)

def e(x): return html.escape(str(x or ""),quote=True)
def api(path,method="GET",payload=None):
    h={"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28","User-Agent":"profile-svg-generator"}
    if TOKEN: h["Authorization"]="Bearer "+TOKEN
    body=json.dumps(payload).encode() if payload is not None else None
    req=urllib.request.Request("https://api.github.com"+path,data=body,headers=h,method=method)
    with urllib.request.urlopen(req,timeout=25) as r: return json.loads(r.read().decode())
def tx(x,y,s,size=16,color="#e6edf7",weight="400",font="monospace"):
    return '<text x="%s" y="%s" font-family="%s" font-size="%s" font-weight="%s" fill="%s">%s</text>'%(x,y,font,size,weight,color,e(s))
def doc(w,h,b,title):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s" viewBox="0 0 %s %s"><title>%s</title><defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0b1220"/><stop offset="1" stop-color="#111c32"/></linearGradient><linearGradient id="ac"><stop stop-color="#54d6ff"/><stop offset="1" stop-color="#9b8cff"/></linearGradient></defs>%s</svg>'%(w,h,w,h,e(title),b)
def base(w,h):
    return '<rect x="1" y="1" width="%s" height="%s" rx="18" fill="url(#bg)" stroke="#263750"/><circle cx="%s" cy="27" r="5" fill="#54d6ff"><animate attributeName="opacity" values=".3;1;.3" dur="2.4s" repeatCount="indefinite"/></circle>'%(w-2,h-2,w-28)
def save(n,s): (ASSETS/n).write_text(s,encoding="utf-8")

def hero(p):
    b=base(1200,310)+tx(40,52,"HELLO, WORLD / GITHUB PROFILE",13,"#7ddcff","700")
    b+=tx(40,112,p.get("name") or USER,39,"#f4f7fb","700","Arial")
    b+=tx(42,148,"SOFTWARE ENGINEERING  •  QUALITY ENGINEERING  •  AI",15,"#a8b9d1","600","Arial")
    b+=tx(42,188,"Building reliable software. Testing what matters.",15)
    b+=tx(42,230,"LIVE PROFILE METRICS • REFRESHED DAILY",13,"#70d7ff","700")
    b+=tx(42,270,"BUILD / TEST / EXPLORE",13,"#9b8cff","700")
    b+='<circle cx="900" cy="143" r="91" fill="#13243a" stroke="#54d6ff" stroke-width="2"/><clipPath id="avatarClip"><circle cx="900" cy="143" r="84"/></clipPath><image href="https://github.com/'+USER+'.png" x="816" y="59" width="168" height="168" clip-path="url(#avatarClip)" preserveAspectRatio="xMidYMid slice"/><circle cx="900" cy="143" r="91" fill="none" stroke="#54d6ff" stroke-dasharray="8 8"><animateTransform attributeName="transform" type="rotate" from="0 900 143" to="360 900 143" dur="24s" repeatCount="indefinite"/></circle>'
    b+=tx(1030,90,"$ whoami",14,"#9b8cff","700")+tx(1030,120,"Shreyansh Jain",14)+tx(1030,150,"AQA / SDET",14,"#7ddcff")+tx(1030,180,"AI explorer",14,"#7ddcff")
    b+='<rect x="1030" y="196" width="9" height="17" fill="#54d6ff"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>'
    return doc(1200,310,b,"Shreyansh Jain animated profile")
def tile(title,sub,color,num):
    b=base(390,150)+tx(26,64,num,29,color,"800","Arial")+tx(82,61,title,23,"#f4f7fb","800","Arial")+tx(27,105,sub,13,"#b5c4d8")
    b+='<path d="M26 124h330" stroke="%s" stroke-width="2"><animate attributeName="stroke-dasharray" values="0 330;330 0" dur="4s" repeatCount="indefinite"/></path>'%color
    return doc(390,150,b,title)
def contrib(calendar,events):
    b=base(1200,255)+tx(30,42,"CONTRIBUTION SIGNAL",14,"#7ddcff","700")
    if calendar:
        vals=[d["contributionCount"] for wk in calendar["weeks"] for d in wk["contributionDays"]]
        total=calendar["totalContributions"]; label="365-DAY CONTRIBUTION CALENDAR"
    else:
        vals=[events.get((NOW.date()-dt.timedelta(days=i)).isoformat(),0) for i in range(364,-1,-1)]
        total=sum(vals); label="RECENT PUBLIC EVENT ACTIVITY • APPROXIMATION"
    b+=tx(30,76,label,11,"#aabbd0")+tx(1000,52,"%s contributions"%format(total,","),17,"#f4f7fb","700")
    shades=["#17263a","#17445a","#176b83","#259caa","#68d9c8"]
    for i,c in enumerate(vals[-371:]):
        level=0 if c==0 else 1 if c==1 else 2 if c<=3 else 3 if c<=6 else 4
        b+='<rect x="%s" y="%s" width="12" height="12" rx="3" fill="%s"><title>%s contributions</title></rect>'%(30+(i//7)*17,104+(i%7)*17,shades[level],c)
    b+=tx(30,226,"LESS",10,"#8da0b8")
    for i,c in enumerate(shades): b+='<rect x="%s" y="214" width="12" height="12" rx="3" fill="%s"/>'%(78+i*20,c)
    b+=tx(190,226,"MORE",10,"#8da0b8")
    return doc(1200,255,b,"GitHub contribution activity")
def activity(events):
    b=base(1200,205)+tx(30,43,"ACTIVITY / LAST 12 WEEKS",14,"#7ddcff","700")
    vals=[]
    for i in range(12):
        d=(NOW.date()-dt.timedelta(days=(11-i)*7)).isoformat()
        vals.append(sum(v for k,v in events.items() if d<=k<=(dt.date.fromisoformat(d)+dt.timedelta(days=6)).isoformat()))
    mx=max(vals+[1])
    for i,v in enumerate(vals):
        x=38+i*92; bh=85*v/mx
        b+='<rect x="%s" y="%s" width="48" height="%s" rx="5" fill="url(#ac)"><animate attributeName="opacity" values=".65;1;.65" dur="%ss" repeatCount="indefinite"/></rect>'%(x,145-bh,bh,2.5+i*.13)
        b+=tx(x,166,v,11,"#d9e5f2","600")+tx(x-4,185,"W%s"%(i+1),9,"#8296b0")
    b+=tx(1080,65,"PUBLIC",11,"#aabbd0","700")+tx(1080,88,"EVENTS",11,"#aabbd0","700")
    return doc(1200,205,b,"Recent GitHub activity")
def daily_commits(calendar,events):
    b=base(1200,245)+tx(30,42,"DAILY CONTRIBUTION ACTIVITY / LAST 30 DAYS",14,"#7ddcff","700")
    days=[]
    if calendar:
        days=[d for wk in calendar["weeks"] for d in wk["contributionDays"]][-30:]
        label="LIVE GITHUB CONTRIBUTION CALENDAR"
    else:
        for i in range(29,-1,-1):
            day=(NOW.date()-dt.timedelta(days=i)).isoformat()
            days.append({"date":day,"contributionCount":events.get(day,0)})
        label="PUBLIC EVENT COUNTS ONLY — ADD GH_TOKEN FOR EXACT DAILY CONTRIBUTIONS"
    b+=tx(30,69,label,10,"#aabbd0")
    vals=[int(d.get("contributionCount",0)) for d in days]; maxv=max(vals+[1]); total=sum(vals)
    b+=tx(1030,52,"%s total"%format(total,","),17,"#f4f7fb","700")
    for i,d in enumerate(days):
        v=int(d.get("contributionCount",0)); x=34+i*37; h=100*v/maxv
        b+='<rect x="%s" y="%s" width="23" height="%s" rx="4" fill="url(#ac)"><title>%s: %s contributions</title></rect>'%(x,190-h,h,e(d.get("date")),v)
        if i%5==0 or i==len(days)-1: b+=tx(x-2,211,d.get("date","")[5:],9,"#8296b0")
    b+=tx(30,231,"GitHub contribution counts include commits, pull requests, issues and reviews.",10,"#8296b0")
    return doc(1200,245,b,"Daily GitHub contribution activity")

def projects(repos):
    b=base(1200,325)+tx(30,44,"SELECTED BUILDS / OPEN-SOURCE REPOSITORIES",14,"#7ddcff","700")
    selected=[("CraveBite","Food ordering app • frontend + backend","cravebite-frontend"),("JobTrek","Job portal • React UI + Spring Boot API","JobTrek-UI"),("rea","Agent-based reverse engineering • fork","rea"),("coolify","Self-hostable PaaS • fork","coolify"),("ruflo","Claude multi-agent orchestration • fork","ruflo")]
    for i,(title,desc,name) in enumerate(selected):
        r=next((x for x in repos if x["name"].lower()==name.lower()),{})
        col=i%3; row=i//3; x=30+col*385; y=72+row*112
        url=r.get("html_url","https://github.com/%s/%s"%(USER,name))
        tag="FORKED REPOSITORY" if r.get("fork") else "PROJECT"
        b+='<a href="%s" target="_blank"><rect x="%s" y="%s" width="355" height="94" rx="13" fill="#111f34" stroke="#2d4562"/><text x="%s" y="%s" font-family="Arial" font-size="19" font-weight="700" fill="#f4f7fb">%s</text><text x="%s" y="%s" font-family="Arial" font-size="11" fill="#b5c4d8">%s</text><text x="%s" y="%s" font-family="monospace" font-size="10" fill="#71d7ff">%s</text><text x="%s" y="%s" font-family="monospace" font-size="9" fill="#9b8cff">%s ↗</text></a>'%(e(url),x,y,x+17,y+27,e(title),x+17,y+49,e(desc),x+17,y+69,e(r.get("language") or "Project"),x+17,y+85,tag)
    b+=tx(30,310,"Forks are labelled transparently; original project ownership is not implied.",10,"#8296b0")
    return doc(1200,325,b,"Featured GitHub repositories and open-source forks")

def main():
    profile=api("/users/"+USER)
    repos=[]; page=1
    while page<=3:
        batch=api("/users/%s/repos?per_page=100&sort=updated&page=%s"%(USER,page))
        repos.extend(batch)
        if len(batch)<100: break
        page+=1
    raw=api("/users/%s/events/public?per_page=100"%USER)
    events={}
    for ev in raw:
        day=ev.get("created_at","")[:10]
        if day: events[day]=events.get(day,0)+1
    calendar=None
    if TOKEN:
        try:
            q='query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){contributionsCollection(from:$from,to:$to){contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}'
            start=(NOW-dt.timedelta(days=364)).replace(hour=0,minute=0,second=0,microsecond=0)
            end=NOW.replace(hour=23,minute=59,second=59,microsecond=0)
            res=api("/graphql","POST",{"query":q,"variables":{"login":USER,"from":start.isoformat(),"to":end.isoformat()}})
            calendar=res["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        except Exception as err: print("GraphQL unavailable; falling back to public events:",err)
    (DATA/"github-data.json").write_text(json.dumps({"profile":profile,"repositories":repos,"public_events_by_date":events,"contribution_calendar":calendar,"generated_at":NOW.isoformat()},indent=2),encoding="utf-8")
    save("hero.svg",hero(profile))
    save("build.svg",tile("BUILD","Java • Spring Boot • React • APIs","#54d6ff","01"))
    save("test.svg",tile("TEST","AQA • API • Regression • Automation","#ff8c9d","02"))
    save("explore.svg",tile("EXPLORE","AI Voice Agents • LLMs • RAG","#b49aff","03"))
    save("contributions.svg",contrib(calendar,events))
    save("daily-commits.svg",daily_commits(calendar,events))
    save("activity.svg",activity(events))
    save("projects.svg",projects(repos))
    print("Rendered @%s: %s public repositories"%(USER,len(repos)))
if __name__=="__main__": main()
