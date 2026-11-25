import os, html
HEAD='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} - ascheuer</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://ascheuer.com{path}">
<link rel="stylesheet" href="/style.css">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://ascheuer.com{path}">
</head>
<body>
<div class="page">
  <header class="top">
    <a class="name" href="/">ascheuer</a>
    <nav><a href="/log/"{c_log}>Log</a><a href="/about/"{c_about}>About</a><a href="/now/"{c_now}>Now</a></nav>
  </header>
'''
FOOT='''  <section class="cta">
    <div class="mono">WORK WITH ME</div>
    <div>
      <p>If you run an affiliate program and want an outside operator to look at it, that is what <a href="https://traffic-goat.com/">Traffic Goat</a> does: a fixed-price audit, delivered in days.</p>
      <p>New entries get posted on <a href="https://x.com/Adamsc19">X</a>.</p>
    </div>
  </section>
  <footer><span class="mono">ASCHEUER.COM</span><p class="mono">Log est. 2026. Written by me, checked by the agents.</p></footer>
</div>
</body>
</html>
'''
def page(path,title,desc,body,nav=''):
    cur=' aria-current="page"'
    h=HEAD.format(title=html.escape(title),desc=html.escape(desc),path=path,
        c_log=cur if nav=='log' else '',c_about=cur if nav=='about' else '',c_now=cur if nav=='now' else '')
    d='.'+path
    os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'index.html'),'w').write(h+body+FOOT)

ENTRIES=[
('the-disk-that-filled-itself','25 NOV 2026','The disk that filled itself',
 'A site went down for 29 hours and no alarm fired. What happened, and the one check we added.',
 '''<p>A small data site I launched this month went down on a Tuesday morning and stayed down for 29 hours. Nobody noticed. Not me, not the agents, not an uptime monitor, because that site did not have one yet.</p>
<p>It was found by accident. My chief-of-staff agent was setting up a redirect to it, ran a quick request to confirm the target worked, and got a server error back. It stopped the redirect job and went to look.</p>
<h2>What it was</h2>
<p>The database was writing a binary log of every change, which is a feature meant for replication and point-in-time recovery. This server has no replica and already takes a nightly backup, so the log was pure cost. The site updates thousands of records every few minutes, and in under three days the log filled a 48 GB disk to the last byte. Once the disk was full, every write froze, and the pages that depend on those writes returned errors.</p>
<p>The fix took a few minutes: free a little space so the database could breathe, delete the old log files, switch binary logging off, restart. Disk went from 100% to 12%.</p>
<div class="lesson"><span class="mono">WHAT WE CHANGED</span>Every new server now ships with two checks before launch day: an uptime ping on the homepage and a disk-space alert at 80%. A launch checklist that only checks that the site works on day one is checking the wrong thing.</div>
<p>The uncomfortable part is not the bug. Defaults bite everyone. It is that the agents built the site, deployed it, and wrote a checklist for it, and the checklist had nothing about staying up. That gap was mine. I asked for "launch it", not "keep it alive".</p>'''),
('ten-domains-one-afternoon','25 NOV 2026','Ten idle domains, one afternoon',
 'I asked the team for a plan for every domain I was sitting on. The useful part was what they found before planning anything.',
 '''<p>Like most people who have been online for a long time, I own domains I am not using. Ten of them. I asked the team to sit down and write a plan for each one, on free hosting, with the rule that none of them stays dead.</p>
<p>I expected ideas. What I got first was an inventory, and the inventory was worth more than the ideas.</p>
<h2>What they found before planning</h2>
<p>One domain I thought of as an old side project turned out to be the primary domain of the hosting account that runs most of my other sites. It was 18 days from expiring. Letting it lapse would not have lost a hobby blog. It would have put the whole hosting account at risk.</p>
<p>Another, a domain I have owned for many years, was quietly forwarding all its visitors to a partner with a tracking code nobody could match to my records. A third was pointing at a server nobody remembered paying for.</p>
<div class="lesson"><span class="mono">LESSON</span>Before you ask "what should we build", ask "what is this thing doing right now". Agents are good at the second question because they do not get bored checking DNS records for ten domains.</div>
<p>The plan itself was honest in a way I appreciated. My CFO agent put the expected 90-day income from all ten at close to zero, and said so. Most of the domains became redirects or simple holding pages. One became this site.</p>'''),
('why-every-agent-has-a-name','24 NOV 2026','Why every agent on the team has a name',
 'Naming agents sounds like a gimmick. It turned out to be the cheapest routing system I have.',
 '''<p>Every agent on my team has a first name. Chase is chief of staff. Penny is the CFO. There is an analyst, a head of design, an art director, translators for four languages and a QA reviewer who checks every translated page on a phone-sized screen.</p>
<p>I did this half as a joke. It stuck because it solved a real problem.</p>
<h2>The problem it solves</h2>
<p>When you work with one general assistant, every request lands in the same place and you have to explain the context every time. When you have specialists, the hard part becomes routing: which agent owns this?</p>
<p>A name is a short, unambiguous address. "Ask Penny if this is worth it" carries a whole job description: think in cash, be conservative, say no when the numbers say no. I do not have to restate that. And because each agent has a written role, two of them disagreeing is useful information, not noise.</p>
<div class="lesson"><span class="mono">LESSON</span>The name is not the point. The written role behind the name is. The name just makes it cheap to use.</div>
<p>The other benefit is accountability. When something ships broken, "the AI did it" is not an answer. "Chase approved it without the disk check" is, and it tells me which instructions to fix.</p>'''),
]
for slug,date,title,desc,body in ENTRIES:
    page(f'/log/{slug}/',title,desc,f'''  <article>
  <div class="entry">
    <div class="date mono">{date}</div>
    <div>
      <h1 style="font-weight:600;font-size:1.9rem;line-height:1.2;margin:0 0 1.5rem">{html.escape(title)}</h1>
      <div class="body">{body}</div>
    </div>
  </div>
  </article>
''','log')
items=''.join(f'''  <div class="entry"><div class="date mono">{d}</div><div><h2><a href="/log/{s}/">{html.escape(t)}</a></h2><p>{html.escape(ds)}</p></div></div>\n''' for s,d,t,ds,_ in ENTRIES)
page('/log/','Log','Every entry in the operator\'s log, latest first.','  <div class="section-label"><span class="mono">LOG</span><span class="mono">All entries, latest first</span></div>\n'+items,'log')
page('/about/','About','Who keeps this log.','''  <div class="entry"><div class="date mono">ABOUT</div><div class="body">
<p>I am Adam Scheuer. I have worked in affiliate marketing and business development since 2002, on the program side: recruiting affiliates, building partner programs, and figuring out why traffic that looks good on paper does not convert.</p>
<p>In 2026 I started running my own sites with a team of AI agents built on Claude. I make the decisions and approve anything that goes public. The agents do the research, building, checking and the boring follow-through.</p>
<p>I write this log because most of what gets posted about AI agents is either a demo or a promise. This is the operations side: what they get right, what they get wrong, and what I changed afterwards.</p>
<p>Work: <a href="https://traffic-goat.com/">Traffic Goat</a> (affiliate program audits). Free tools: <a href="https://growthmath.io/">GrowthMath</a>.</p>
</div></div>
''','about')
page('/now/','Now','What I am working on right now.','''  <div class="entry"><div class="date mono">UPDATED 25 NOV 2026</div><div class="body">
<p>Looking for the first outside programs to audit through Traffic Goat.</p>
<p>Running a 60-day test on a new data site before deciding whether it lives.</p>
<p>Writing this log once a week.</p>
</div></div>
''','now')
open('CNAME','w').write('ascheuer.com\n')
open('robots.txt','w').write('User-agent: *\nAllow: /\nSitemap: https://ascheuer.com/sitemap.xml\n')
urls=['/','/log/','/about/','/now/']+[f'/log/{e[0]}/' for e in ENTRIES]
open('sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>https://ascheuer.com{u}</loc></url>\n' for u in urls)+'</urlset>\n')
