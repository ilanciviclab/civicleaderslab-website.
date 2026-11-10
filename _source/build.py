"""Builds the Civic Leaders Lab static site.
Usage: python3 build.py <out_dir> [--preview]
--preview writes index.html without the <!doctype>/<html>/<head> shell (the Artifact viewer adds its own)."""
import sys, os, shutil

OUT = sys.argv[1]
PREVIEW = "--preview" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
ORG = "Civic Leaders Lab"
EMAIL = "hello@civicleaderslab.org"

NAV = [("index.html", "Home"), ("about.html", "About"), ("manifesto.html", "Manifesto"),
       ("fellowship.html", "Fellowship"), ("work.html", "Our work"), ("contact.html", "Contact")]

MARK = """<svg class="brand-mark" viewBox="0 0 30 30" aria-hidden="true"><rect width="30" height="30" rx="2" fill="#1b2f5e"/><polyline points="4,23 9,17 12,20 15,8 18,19 21,14 26,23" fill="none" stroke="#e2b85a" stroke-width="2" stroke-linejoin="round"/><circle cx="15" cy="8" r="2" fill="#e2b85a"/></svg>"""

SKYLINE = """<svg class="skyline" viewBox="0 0 1440 220" preserveAspectRatio="none" aria-hidden="true">
<line class="grid" x1="900" y1="40" x2="900" y2="220"/><line class="grid" x1="960" y1="10" x2="960" y2="220"/><line class="grid" x1="1010" y1="60" x2="1010" y2="220"/><line class="grid" x1="1090" y1="30" x2="1090" y2="220"/><line class="grid" x1="1180" y1="80" x2="1180" y2="220"/>
<polyline class="line" points="0,200 120,170 220,190 340,150 430,180 560,120 650,160 760,110 850,150 900,90 960,40 1010,100 1090,60 1180,120 1270,100 1340,150 1440,130"/>
<circle class="dot" cx="960" cy="40" r="4"/><circle class="dot" cx="1090" cy="60" r="3"/><circle class="dot" cx="900" cy="90" r="3"/><circle class="dot" cx="1010" cy="100" r="2.5"/><circle class="dot" cx="1180" cy="120" r="2.5"/>
</svg>"""


CUR = ' aria-current="page"'


def header(current):
    links = "".join(
        f'<a href="{h}"{CUR if h == current else ""}>{t}</a>' for h, t in NAV)
    return f"""<header class="site-header"><div class="wrap">
<a class="brand" href="index.html">{MARK}<span>Civic Leaders <b>Lab</b></span></a>
<nav class="nav" aria-label="Main">{links}<a class="nav-cta" href="support.html">Founding partners</a></nav>
</div></header>"""


FOOTER = f"""<footer class="site-footer"><div class="wrap">
<div><a class="brand" href="index.html">{MARK}<span style="color:#eef0f6">Civic Leaders <b>Lab</b></span></a>
<p class="foot-tag">Better leaders. Better systems. Better cities.</p></div>
<div><h4>Explore</h4><ul><li><a href="about.html">About</a></li><li><a href="manifesto.html">Manifesto</a></li><li><a href="fellowship.html">The Fellowship</a></li><li><a href="work.html">Our work</a></li></ul></div>
<div><h4>Get involved</h4><ul><li><a href="support.html">Become a founding partner</a></li><li><a href="contact.html#fellowship">Apply to the Fellowship</a></li><li><a href="contact.html">Contact us</a></li><li>{EMAIL}</li></ul></div>
<p class="legal">{ORG} is a nonpartisan educational organization. It does not support or oppose any candidate or campaign for public office. Candidate-specific campaign work for participants who later seek office will be handled separately under applicable nonprofit and election laws.<br>&copy; 2026 {ORG}. Las Vegas, Nevada.</p>
</div></footer>"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap">'


def page(fname, title, desc, body):
    head = f"""<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="claude:viewport-fit-sides" content="cover">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
{FONTS}
<link rel="stylesheet" href="styles.css">"""
    content = header(fname) + "<main>" + body + "</main>" + FOOTER
    if PREVIEW and fname == "index.html":
        html = head + "\n" + content
    else:
        html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head}
</head><body>
{content}
</body></html>"""
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(html)


def hero(eyebrow, h1, lede, extra="", cls="page-hero"):
    return f"""<section class="hero {cls}"><div class="wrap">
<p class="eyebrow">{eyebrow}</p><h1>{h1}</h1>{f'<p class="lede">{lede}</p>' if lede else ''}{extra}
</div>{SKYLINE}</section>"""


def rows(items, label_cls="gold-label"):
    return '<div class="rows">' + "".join(
        f'<div class="row"><h3 class="{label_cls}">{k}</h3><p>{v}</p></div>' for k, v in items) + "</div>"


def cta(h, p, btn_href="support.html", btn="Become a founding partner"):
    return f"""<section class="cta-band"><div class="wrap">
<div><p class="eyebrow">Get involved</p><h2>{h}</h2><p class="lede" style="color:var(--on-navy-muted)">{p}</p></div>
<div class="btns" style="margin-top:0"><a class="btn btn-gold" href="{btn_href}">{btn}</a><a class="btn btn-ghost" href="contact.html">Contact us</a></div>
</div></section>"""


QUARTERS = [("Months 1–3", "The Inner Core", "Who they are"), ("Months 4–6", "The Voice", "How they are heard"),
            ("Months 7–9", "The Strategist", "How they plan"), ("Months 10–12", "The Builder", "What they build")]


def quarters():
    return '<div class="quarters">' + "".join(
        f'<div class="quarter"><span class="months">{m}</span><h3>{t}</h3><p>{s}</p></div>' for m, t, s in QUARTERS) + "</div>"


RATIO = """<div class="ratio">
<div class="donut-box"><span class="cap">Today</span><div class="donut today"><div class="donut-inner"><b>80%</b><small>politics</small></div></div><span class="ratio-foot">20% leadership</span></div>
<span class="ratio-arrow" aria-hidden="true">&rarr;</span>
<div class="donut-box new"><span class="cap">The new standard</span><div class="donut new"><div class="donut-inner"><b>80%</b><small>leadership</small></div></div><span class="ratio-foot">20% politics</span></div>
</div>
<div class="grid-2" style="margin-top:40px">
<div class="cell"><span class="k">Leadership leads</span><div class="chips" style="justify-content:flex-start"><span class="chip">Vision</span><span class="chip">Service</span><span class="chip">People</span><span class="chip">Culture</span><span class="chip">Execution</span><span class="chip">Results</span></div></div>
<div class="cell"><span class="k">Politics supports</span><div class="chips" style="justify-content:flex-start"><span class="chip outline">Coalition</span><span class="chip outline">Process</span><span class="chip outline">Negotiation</span></div></div>
</div>"""

# ------------------------------------------------------------------ HOME
home = hero(
    "An institute for a new era of leadership",
    'Setting the new standard for <span class="gold">civic leadership.</span>',
    "We find natural leaders, prepare them to lead America&rsquo;s cities, and share what works so every city can rise.",
    '<div class="btns"><a class="btn btn-gold" href="fellowship.html">Explore the Fellowship</a><a class="btn btn-ghost" href="manifesto.html">Read the manifesto</a></div>',
    cls="")
home += f"""
<section class="band"><div class="wrap split">
<div><p class="eyebrow">Who we are</p><h2>A leadership institute.</h2><hr class="short-rule">
<p class="muted">{ORG} is where the future of civic leadership is built. We bring together the best minds, resources, and visions, and turn them into a living plan for how cities should be led, and the leaders ready to lead them.</p></div>
<ul class="statements">
<li>We gather the best minds and the boldest ideas on civic leadership.</li>
<li>We define the future of city leadership, and turn it into a real plan.</li>
<li>We discover natural leaders, and we develop them.</li>
<li>We give them the knowledge, skills, and network to lead.</li>
<li>And we share what works, so every city can rise.</li>
</ul></div></section>

<section class="band paper"><div class="wrap">
<p class="eyebrow">The moment</p><h2>People are tired of politics without leadership.</h2>
<p class="lede">They want vision. They want trust. They want character. They want to be heard, and to feel safe in the hands of those who lead them.</p>
<div class="stats">
<div><div class="stat-num dim">42%</div><p class="stat-cap">trust the people who hold or run for public office.</p></div>
<div><div class="stat-num">67%</div><p class="stat-cap">trust their local government&rsquo;s ability to handle local problems.</p></div>
</div>
<p class="pull" style="margin-top:36px">People have lost faith in politicians, <span class="gold">not in the power of their city.</span></p>
<p class="source">Source: Gallup Governance poll, September 2026</p>
</div></section>

<section class="band on-navy"><div class="wrap">
<p class="eyebrow">The new standard</p><h2>Flip the ratio.</h2>
<p class="lede">Politics is part of governing. It should never become its purpose. Yet today, too much of civic life is run the other way around.</p>
{RATIO}
<p class="pull" style="margin-top:40px;color:var(--on-navy)">Both matter. <span class="gold">Only one should lead.</span></p>
</div></section>

<section class="band"><div class="wrap">
<p class="eyebrow">The leadership program</p><h2>The Fellowship: built to lead.</h2>
<p class="lede">The heart of {ORG}. We find people with the right profile and take them through twelve months that turn potential into leadership.</p>
{quarters()}
<div class="btns"><a class="btn btn-navy" href="fellowship.html">See the full program</a></div>
</div></section>

<section class="band paper"><div class="wrap">
<p class="eyebrow">Why cities</p><h2>Cities are the laboratories of the future.</h2>
<div class="grid-2" style="margin-top:36px">
<div class="cell"><span class="k">Highest impact</span><h3>No level of government touches residents&rsquo; daily lives more directly.</h3></div>
<div class="cell"><span class="k">Lowest barrier to entry</span><h3>No level of government is more open to new leaders.</h3></div>
</div>
<div class="process"><span>DECISION</span><i>&rarr;</i><span>ACTION</span><i>&rarr;</i><span>RESULT</span></div>
</div></section>
"""
home += cta("Not a donation. An investment in a legacy.",
            "We are raising $1.8 million to launch the first Fellowship class and city pilots in Las Vegas.")

# ------------------------------------------------------------------ ABOUT
about = hero("About us", "Better leaders. Better systems. <span class=\"gold\">Better cities.</span>",
             f"{ORG} is a nonpartisan leadership institute building a new model of civic leadership, and the leaders ready to carry it.")
about += f"""
<section class="band"><div class="wrap split">
<div><p class="eyebrow">Our goals</p><h2>What we are here to do.</h2></div>
{rows([("A new model.", "Create a new model of civic leadership, built by the best minds, tested in real cities, and ready to lead in a new era."),
       ("New leaders.", "Identify, attract, and prepare natural leaders, then train them, educate them, and make them ready to serve in city leadership."),
       ("An American future.", "Build an innovative movement for the benefit of America that stops the dangerous expansion of radical Islam in the United States, and ensures that America&rsquo;s future remains American, rooted in Western values.")])}
</div></section>

<section class="band paper"><div class="wrap">
<p class="eyebrow">How we work</p><h2>Research the present. Create the future. Share what works.</h2>
<div class="prose" style="margin-top:24px">
<p>We study what actually works, around the world. We bring exceptional minds together to challenge old assumptions and design new models. We turn ideas into pilots, measure results with data and AI, and learn directly from residents and city teams.</p>
<p>We publish what we learn, openly. And we help cities, institutions, and leaders adapt what works, feeding every lesson back into the model.</p>
</div>
<div class="process"><span>RESEARCH</span><i>&rarr;</i><span>CREATE</span><i>&rarr;</i><span>TEST</span><i>&rarr;</i><span>PUBLISH</span><i>&rarr;</i><span>IMPLEMENT</span><i>&#8635; and repeat</i></div>
</div></section>

<section class="band on-navy" id="founder"><div class="wrap founder">
<img src="founder.jpg" alt="Ilan Gelberg, founder of {ORG}" width="340" height="510" loading="lazy">
<div><p class="eyebrow">From the founder</p><h2>Cities are where leadership becomes visible.</h2>
<div class="prose" style="margin-top:24px;color:var(--on-navy-muted)">
<p>I believe people want more than politics. They want leaders they can trust: leaders with vision, character, courage, competence, and the ability to produce real results.</p>
<p>Many of the people capable of that leadership are outside public life today. They are building companies, technologies, organizations, teams, and communities, because they do not yet see civic leadership as a place where they can thrive.</p>
<p style="color:var(--on-navy)">{ORG} exists to change that.</p>
</div>
<div class="sig"><b>Ilan Gelberg</b><small>Founder, {ORG}</small></div>
</div></div></section>
"""
about += cta("Help set a new standard of leadership.", "Join the small circle of founding partners launching the first Fellowship.")

# ------------------------------------------------------------------ MANIFESTO
man = hero("The manifesto", "A new standard for <span class=\"gold\">civic leadership.</span>",
           "The world has changed. The way we lead our cities must change with it.")
man += f"""
<section class="band"><div class="wrap split">
<div><p class="eyebrow">The moment</p><h2>People are tired of politics without leadership.</h2></div>
<div class="prose"><p>They want vision. They want trust. They want character. They want to be heard, and to feel safe in the hands of those who lead them.</p>
<p>That is where a new kind of leadership can start. Most of today&rsquo;s civic leadership systems were built for another era. They are run by political habit rather than leadership, and they are not keeping pace with the fast-moving human challenges of our age.</p></div>
</div></section>

<section class="band on-navy"><div class="wrap split">
<div><p class="eyebrow">What is at stake</p><h2>A worrying trend.</h2></div>
<div class="stack"><div class="prose" style="color:var(--on-navy-muted)">
<p>Over the past four years, radical left socialist movements have been gaining ground in city halls across America, through well-funded, highly organized efforts that most residents never see.</p>
<p>Much of that funding moves quietly, and some of it originates outside the United States. Its aim is to place city leaders who would change what America is, one city at a time.</p></div>
<div><p class="eyebrow" style="margin-bottom:6px">What they push</p><ul class="bullets">
<li>Confusion over the most basic truths about gender.</li><li>Weakening the family as the foundation of American life.</li>
<li>An economy of dependency, asking for money instead of earning it.</li><li>Open-border policies that reward illegal immigration.</li></ul></div>
<p class="pull">If we do not act boldly now, we risk losing what makes America, America. Our answer is not anger. <span class="gold">It is a new generation of leaders.</span></p>
</div></div></section>

<section class="band"><div class="wrap">
<div class="split" style="margin-bottom:36px"><div><p class="eyebrow">Our values</p><h2>Nonpartisan. <span class="gold">Not without values.</span></h2></div>
<p class="lede" style="margin-top:0">We do not serve a party. Our vision is rooted in the American and Western values that made this country extraordinary, and every leader we develop will carry them.</p></div>
{rows([("True leadership", "Leaders who serve before they rule, act with character, and deliver real results."),
       ("Lead with honor", "We build our message on our strength, not on our opponents&rsquo; weakness. No insults, no humiliation, no celebrating others&rsquo; failures. We are honest about our competitors&rsquo; strengths and weaknesses, and we prove why our vision is better."),
       ("A purpose for every person", "We build the next generation of humanity by leading people to their purpose path."),
       ("Love of country", "Pride in America&rsquo;s founding principles, and the duty to pass them on stronger than we found them."),
       ("Love of people and community", "Every resident matters. A city is only as strong as the bonds between its people."),
       ("Man and woman", "We recognize two sexes, male and female, and honor the dignity of every person."),
       ("Freedom of faith", "Every person is free to believe, worship, and live by their faith without interference."),
       ("Prosperity through free enterprise", "Wealth is built by people free to create, compete, and keep the fruits of their work."),
       ("Equal rights for all", "One standard of rights and opportunity for every citizen, with no exceptions and no favorites."),
       ("Justice under law", "Laws applied fairly, safe streets, and accountability for everyone, including those in power."),
       ("Innovation and adaptation", "Embracing new technologies, new ways of thinking, and new ways of living.")])}
<p class="pull" style="margin-top:36px">We will raise leaders who keep America, America, <span class="gold">and build its future.</span></p>
</div></section>

<section class="band paper"><div class="wrap split">
<div><p class="eyebrow">Our vision</p><h2>New standards for civic leadership.</h2></div>
<div class="stack">{rows([("Leaders, not politicians.", "We believe cities should be led by people with natural leadership ability, ambition, creativity, courage, and a genuine desire to serve."),
       ("An entrepreneurial spirit.", "Cities should run with efficiency, speed, creativity, critical thinking, and strong growth, always grounded in what residents truly need and want."),
       ("At the speed of life.", "A city leader&rsquo;s decision can change residents&rsquo; lives within a week. The world is moving forward faster than ever. Leadership and governance must move with it.")])}
<p class="callout">The standard of public leadership can be raised: <span class="gold">deliberately, visibly, and for good.</span></p></div>
</div></section>

<section class="band on-navy"><div class="wrap">
<p class="eyebrow">The new standard</p><h2>Flip the ratio.</h2>
<p class="lede">Politics is part of governing. It should never become its purpose.</p>
{RATIO}
</div></section>

<section class="band"><div class="wrap split">
<div><p class="eyebrow">Authenticity over political correctness</p><h2>Mean what you say. <span class="gold">Say what you mean.</span></h2></div>
<div class="stack"><div class="prose">
<p>Political correctness began as a tool of politics: a way to communicate, negotiate, and keep tensions low. Over time it became a norm, and then an expectation. Rules about what you can and cannot say, whether you mean it or not, just to avoid offending the other side or inflaming the moment.</p>
<p>That is the opposite of authenticity. It is the opposite of integrity. Leaders who weigh every word to avoid offense slowly stop telling people the truth, and people can feel it.</p>
<p>Diplomacy has its place at the negotiating table. It cannot be our vision, our public policy, or the standard for our society.</p></div>
<p class="callout" style="font-style:normal;font-family:var(--display);font-weight:600">Honesty and respect are not opposites.<br><span class="gold">We will lead with both, never with scripts.</span></p></div>
</div></section>

<section class="band paper"><div class="wrap split">
<div><p class="eyebrow">Why cities</p><h2>Cities are the laboratories of the future.</h2></div>
<div class="stack"><div class="prose">
<p>At the city level, leadership becomes visible. Residents see it in the park, the street, the permit process, the neighborhood, the public space, and the quality of everyday government. They can trace the line from a decision, to an action, to a result.</p>
<p>That is why residents should never simply receive government decisions. They deserve to understand them, feel their impact, influence them, and help shape what comes next.</p></div>
<div class="process" style="margin-top:0"><span>DECISION</span><i>&rarr;</i><span>ACTION</span><i>&rarr;</i><span>RESULT</span></div>
<p class="pull">Cities can become places where ideas are tested quickly, results are measured clearly, mistakes are corrected honestly, and successful models are shared openly.</p></div>
</div></section>

<section class="band"><div class="wrap split">
<div><p class="eyebrow">Why now</p><h2>People have not stopped caring. <span class="gold">They have stopped believing.</span></h2></div>
<div class="stack">
<div><div class="stat-num" style="color:var(--navy)">72,000</div><p class="stat-cap">votes cast in the June 2024 Las Vegas mayoral primary, in a city of more than 640,000 residents.</p></div>
<div class="prose"><p>People don&rsquo;t believe in politics, so they don&rsquo;t show up. Across America&rsquo;s largest cities, the typical mayoral voter is close to 60 years old, and voters over 65 are about ten times more likely to vote than those aged 18 to 34.</p>
<p>That silence is not apathy. It is an opening. It means a new vision can reach the people politics has never reached, especially voters between 18 and 40, who vote least and have the most future at stake.</p></div>
<p class="callout">We will engage a new generation of voters with new ideas, <span class="gold">fitted to who they are, and to where the world is going.</span></p></div>
</div></section>

<section class="band on-navy"><div class="wrap">
<p class="eyebrow">The AI revolution</p><h2>Leadership for the <span class="gold">age of AI.</span></h2>
<p class="lede">The world is moving into the AI revolution. In every area of city life, it opens a new opportunity: to know residents better, understand their struggles, and shape solutions around each of them.</p>
<div class="grid-3" style="margin-top:36px">
<div class="cell"><h4>Know every resident</h4><p>Understand the needs, wants, struggles, and problems of the people we serve.</p></div>
<div class="cell"><h4>Personal service</h4><p>Treat every resident like a valued customer, with help tailored to them.</p></div>
<div class="cell"><h4>See problems early</h4><p>Identify problems before they happen, and act before they grow.</p></div>
<div class="cell"><h4>Faster, better solutions</h4><p>Solve problems in days, not months, with answers that fit each case.</p></div>
<div class="cell"><h4>A more efficient city</h4><p>Less waste, less bureaucracy, more results for every dollar.</p></div>
<div class="cell"><h4>Growth for every adult</h4><p>Personal programs for adults who truly want to change their lives.</p></div>
</div>
<p class="pull" style="margin-top:36px;color:var(--on-navy)">AI can be a powerful force for good. <span class="gold">We will master it, and keep it working for people, always.</span></p>
</div></section>

<section class="band"><div class="wrap">
<div class="split" style="margin-bottom:36px"><div><p class="eyebrow">Our commitments</p><h2>The New Standard.</h2></div>
<p class="lede" style="margin-top:0">The commitments that define the leadership we will build, test, and share.</p></div>
{rows([("Leadership before politics.", "Politics is part of governing. It must never become its purpose. Vision, people, responsibility, and results come first."),
       ("Residents first.", "Every system is measured by the quality of life it creates for the people it serves."),
       ("An entrepreneurial spirit.", "Government does not need to become a business. But it can ask what great entrepreneurs ask: What problem are we solving? Who are we serving? Can this be simpler? How do we measure success?"),
       ("Public value is the return.", "In business, the return may be profit. In public service, it is a better quality of life, greater opportunity, stronger communities, and greater trust."),
       ("The right people in the right roles.", "Better systems begin with people who know where they are strongest, placed where their strengths create the greatest value."),
       ("Test, measure, improve.", "Ideas become pilots. Pilots become evidence, measured with data and AI. Evidence becomes the model."),
       ("Share openly.", "If a solution works, it should not belong to one city. What works is shared. What fails is documented. What can be improved invites collaboration.")])}
</div></section>
"""
man += cta("The future of our cities will be shaped by the people willing to lead them.", "Let&rsquo;s build that future together.")

# ------------------------------------------------------------------ FELLOWSHIP
def phase(m, t, tag, text, tags, alt=False):
    return f"""<div class="phase"><div><p class="months">{m}</p><h2>{t}</h2></div>
<div><p class="tagline">{tag}</p><p>{text}</p><div class="tags">{''.join(f'<span class="tag">{x}</span>' for x in tags)}</div></div></div>"""

fel = hero("The leadership program", "The Fellowship: <span class=\"gold\">built to lead.</span>",
           "Twelve months that transform potential into leadership, designed by the best minds we can bring together.",
           '<div class="btns"><a class="btn btn-gold" href="contact.html#fellowship">Express interest</a></div>')
fel += f"""
<section class="band"><div class="wrap">
<p class="eyebrow">Who we prepare</p><h2>Every office that shapes a city.</h2>
<p class="lede">Elected and appointed.</p>
<div class="grid-2" style="margin-top:32px">
<div class="cell"><span class="k">Elected</span><div class="tags" style="margin-top:4px">{''.join(f'<span class="tag">{x}</span>' for x in ["Mayor","City council","Ward leadership","City attorney","City auditor","City clerk","Municipal judge","School board","County commission"])}</div></div>
<div class="cell"><span class="k">Appointed</span><div class="tags" style="margin-top:4px">{''.join(f'<span class="tag">{x}</span>' for x in ["City manager","Department directors","Planning commissions","City boards"])}</div></div>
</div>
<h3 style="margin-top:56px">The year at a glance</h3>
{quarters()}
</div></section>

<section class="band paper"><div class="wrap">
{phase("Months 1–3", "The Inner Core", "Every leader begins with themselves.",
       "In the first three months, each fellow does the deep work of self-awareness: discovering their natural gifts, facing their strengths and weaknesses honestly, and defining their true purpose. Their why must be strong, and it will be challenged again and again through personal coaching, retreats, and intensive seminars. This is also where we learn whether a fellow is real, and leading for the right reasons.",
       ["Personal coaching", "Purpose and values work", "Opening retreat", "Breakthrough seminars"])}
{phase("Months 4–6", "The Voice", "A leader who cannot be heard cannot lead.",
       "Fellows learn to speak with power and authenticity: on a stage, in front of a camera, in a council chamber, or across a kitchen table. They master public speaking, presence, storytelling, media, and social media, and they practice in front of real audiences until their message is clear, confident, and unmistakably their own.",
       ["Public speaking", "Body language and presence", "Storytelling", "Media and public relations", "Social media mastery"])}
{phase("Months 7–9", "The Strategist", "Vision needs a map.",
       "Fellows learn how cities really work: how budgets are built, how decisions are made, how institutions move, and which civic models succeed or fail, and why. They study political science and public policy, social and development strategy, fundraising, negotiation, and coalition building, so they can turn a vision into a plan that earns support and delivers results.",
       ["Civic systems and policy", "Political science", "Social strategy", "Development strategy", "Fundraising", "Negotiation and coalitions"])}
{phase("Months 10–12", "The Builder", "Ideas are only real when they are built.",
       "In the final quarter, each fellow takes on a real problem facing a real city and designs the solution, with a team, a budget, a timeline, and measurable results. They learn to attract top talent, build systems that scale, leverage their connections, and lead with AI and data. The year ends at Civic Demo Day, where fellows present their plans to partners, experts, and the public.",
       ["Attracting top talent", "Systems that scale", "Leveraging connections", "Leading with AI and data", "Civic Demo Day"])}
<p class="callout" style="margin-top:24px">After twelve months, every graduate is ready to carry the message into any city: <span class="gold">to put these qualities into action, create change, and spread the movement.</span></p>
</div></section>

<section class="band on-navy"><div class="wrap">
<p class="eyebrow">Throughout the year</p><h2>Support at every step.</h2>
<div class="grid-4" style="margin-top:36px">
<div class="cell"><h4>A mentor for every fellow</h4><p>A current or former mayor, council member, or city manager.</p></div>
<div class="cell"><h4>A cohort</h4><p>Fellows learn, challenge, and hold each other accountable.</p></div>
<div class="cell"><h4>Study tours</h4><p>Visits to the cities doing it best.</p></div>
<div class="cell"><h4>Certification</h4><p>Graduates become {ORG} Fellows.</p></div>
</div>
<p class="lede" style="margin-top:36px">Delivered through personal and group learning, inside and outside the classroom: private coaching, university and college courses, online education, group learning, seminars and events.</p>
</div></section>

<section class="band"><div class="wrap split">
<div><p class="eyebrow">Partner programs</p><h2>Open-enrollment courses.</h2><p class="lede">Courses fellows can join with no prerequisites.</p></div>
{rows([("Negotiation and Leadership", "Program on Negotiation at Harvard Law School"),
       ("Principles and Techniques of Fundraising", "The Fund Raising School, Indiana University. Online, with certificate."),
       ("Google AI Essentials", "Online, self-paced, with certificate."),
       ("Political science and public policy", "Open online courses from leading universities, with certificates."),
       ("Public speaking", "Dale Carnegie and Toastmasters.")])}
</div></section>

<section class="band paper"><div class="wrap">
<p class="eyebrow">After the program</p><h2>The leader we build.</h2>
<p class="lede" style="margin-bottom:36px">Character first. Purpose always. Vision ahead. Results that prove it.</p>
<div class="virtues">
<article class="virtue"><header><h3>Character</h3><small>Who the leader is</small></header><dl>
<div><dt>Integrity</dt><dd>Says what they mean, does what they say, in private as in public.</dd></div>
<div><dt>Courage</dt><dd>Makes the hard call and stands behind it.</dd></div>
<div><dt>Humility</dt><dd>Strong enough to say &ldquo;I was wrong,&rdquo; and to learn from anyone.</dd></div>
<div><dt>Honor</dt><dd>Builds on their own strength, never on an opponent&rsquo;s weakness.</dd></div></dl></article>
<article class="virtue"><header><h3>Purpose</h3><small>Why they lead</small></header><dl>
<div><dt>Service</dt><dd>Leadership is a duty to people, not a reward.</dd></div>
<div><dt>Purpose-driven</dt><dd>Leads from their true self and core values, not from polls or pressure.</dd></div>
<div><dt>Love of country and community</dt><dd>Leads out of care for America and for the people of their city.</dd></div></dl></article>
<article class="virtue"><header><h3>Vision</h3><small>Where they lead</small></header><dl>
<div><dt>Vision</dt><dd>Sees the future first, and gives people a clear picture of where they are going.</dd></div>
<div><dt>Curiosity</dt><dd>Always asks why, explores the new, and learns from every source.</dd></div>
<div><dt>Inspiration</dt><dd>Moves people to believe again, and calls out the best in every resident.</dd></div></dl></article>
<article class="virtue"><header><h3>Execution</h3><small>How they lead</small></header><dl>
<div><dt>Ownership</dt><dd>Full responsibility for results. No excuses, no blaming.</dd></div>
<div><dt>Entrepreneurial drive</dt><dd>Fast, creative, efficient: ideas turned into results.</dd></div>
<div><dt>Growth</dt><dd>Never stops learning, adapting, and becoming a better version of themselves.</dd></div></dl></article>
</div>
<p class="prose" style="margin-top:36px">Beyond these virtues, every graduate will be ready: ready to lead, to innovate, to change the status quo, to disrupt, and to build things as they should be. Confident, connected, and fully equipped, they will have everything they need to start.</p>
</div></section>
"""
fel += cta("Know someone who should lead their city?", "We do not wait for great leaders to find public service. We go find them.",
           "contact.html#fellowship", "Recommend or apply")

# ------------------------------------------------------------------ WORK
work = hero("Our work", "What we <span class=\"gold\">will build.</span>",
            "Five programs that turn a new standard of leadership into tested, shareable practice.")
work += f"""
<section class="band"><div class="wrap">
{rows([("The Future City Leadership Model", "A practical operating system for modern civic leadership: vision, decision-making, accountability, culture, resident experience, performance, and technology."),
       ("The Future City Leadership Fellowship", "Do not wait for great leaders to find public service. Go find them. We will recruit high-potential people from technology, business, sports, education, entrepreneurship, nonprofits, and community life, and teach them how cities work, how decisions are made, how to build teams, and how to turn vision into implementation. <a href=\"fellowship.html\">See the Fellowship</a>."),
       ("The City Innovation Lab", "The best minds from entrepreneurship, technology, design, academia, psychology, and public administration, designing and testing practical solutions, from permitting and resident services to AI, transparency, and small-business support."),
       ("Civic Performance and Human Potential", "Helping civic institutions move beyond filling positions, and place people where their strengths, skills, and motivation create the greatest value."),
       ("The Publishing Engine", "Tested knowledge, not opinions: playbooks, case studies, scorecards, tools, and an honest record of what worked and what did not.")])}
</div></section>

<section class="band on-navy"><div class="wrap">
<p class="eyebrow">How we work</p><h2>Research the present. Create the future. <span class="gold">Share what works.</span></h2>
<div class="process"><span>RESEARCH</span><i>&rarr;</i><span>CREATE</span><i>&rarr;</i><span>TEST</span><i>&rarr;</i><span>PUBLISH</span><i>&rarr;</i><span>IMPLEMENT</span><i>&#8635; and repeat</i></div>
<p class="lede" style="margin-top:28px">We turn ideas into pilots, measure results with data and AI, and learn directly from residents and city teams. Then we publish what we learn, openly.</p>
</div></section>
"""
work += cta("Help us build the first model city.", "Founding partners launch the first Fellowship, the first city pilots in Las Vegas, and the first open playbooks.")

# ------------------------------------------------------------------ SUPPORT
sup = hero("The invitation", "Not a donation. <span class=\"gold\">An investment in a legacy.</span>",
           f"{ORG} is a nonprofit. But supporting it is not just another way to give back. It is an opportunity to help set a new standard of leadership, and a new future for our cities.")
sup += f"""
<section class="band on-navy" style="padding-top:24px"><div class="wrap split">
<div><p class="eyebrow">The first year</p><div class="big">$1.8M</div><p class="lede">to launch the first year in Las Vegas.</p></div>
{rows([("The first class", "Prepare our first class of leaders in Las Vegas, ready to serve as mayor and as city council members."),
       ("The hub", "Establish a center of leadership: offices, meeting rooms, a media room, a social media center, and a podcast studio. A place where people come to bring ideas and think big together."),
       ("The team", "Build a core team of seven exceptional minds to run the operation."),
       ("The model", "Within one year, deliver a complete model of how the future city should look and be led.")])}
</div></section>

<section class="band"><div class="wrap split">
<div><p class="eyebrow">Founding partners</p><h2>Join a small circle of founding partners.</h2></div>
<div class="stack"><div class="prose">
<p>We are inviting a small circle of founding partners to help launch the first Fellowship, the first city pilots in Las Vegas, and the first open playbooks for a new era of civic leadership.</p>
<p>A detailed budget and program plan is available to founding partners.</p></div>
<p class="callout">The future of our cities will be shaped by the quality of the people willing to lead them. <span class="gold">Let&rsquo;s build that future together.</span></p>
<div class="btns" style="margin-top:0"><a class="btn btn-navy" href="contact.html#partner">Request the partner plan</a></div></div>
</div></section>
"""

# ------------------------------------------------------------------ CONTACT
con = hero("Contact", "Let&rsquo;s build that future <span class=\"gold\">together.</span>",
           "Whether you want to become a founding partner, join the Fellowship, or recommend a natural leader, we would like to hear from you.")
con += f"""
<section class="band"><div class="wrap split">
<div class="stack">
<div><p class="eyebrow">Email</p><div class="copy-line"><code id="email">{EMAIL}</code><button class="copy-btn" type="button" id="copy-email">Copy</button></div></div>
<div id="partner"><h3>Founding partners</h3><p class="muted" style="margin-top:6px">Ask for the detailed budget and program plan.</p></div>
<div id="fellowship"><h3>The Fellowship</h3><p class="muted" style="margin-top:6px">Tell us about yourself, or about someone you believe should lead their city.</p></div>
<div><h3>Based in</h3><p class="muted" style="margin-top:6px">Las Vegas, Nevada</p></div>
</div>
<form class="form" id="contact-form" name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field">
<input type="hidden" name="form-name" value="contact">
<p hidden><label>Leave empty <input name="bot-field"></label></p>
<div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="f-topic">I&rsquo;m interested in</label><select id="f-topic" name="topic">
<option>Becoming a founding partner</option><option>Joining the Fellowship</option><option>Recommending a leader</option><option>Something else</option></select></div>
<div class="field"><label for="f-msg">Message</label><textarea id="f-msg" name="message"></textarea></div>
<div><button class="btn btn-navy" type="submit">Send message</button></div>
<p class="form-done" id="form-done" hidden>Thanks. This is a preview, so nothing was sent. The form goes live once the site is online at civicleaderslab.org.</p>
</form>
</div></section>
<script>
(function () {{
  var live = /civicleaderslab\\.org$/.test(location.hostname);
  var form = document.getElementById('contact-form');
  form.addEventListener('submit', function (e) {{
    if (live) return;
    e.preventDefault();
    document.getElementById('form-done').hidden = false;
  }});
  var btn = document.getElementById('copy-email');
  btn.addEventListener('click', function () {{
    var t = document.getElementById('email').textContent;
    var done = function () {{ btn.textContent = 'Copied'; }};
    var fallback = function () {{ var r = document.createRange(); r.selectNodeContents(document.getElementById('email')); var s = getSelection(); s.removeAllRanges(); s.addRange(r); }};
    try {{ navigator.clipboard.writeText(t).then(done, fallback); }} catch (err) {{ fallback(); }}
  }});
}})();
</script>
"""

os.makedirs(OUT, exist_ok=True)
D = "Civic Leaders Lab is a nonpartisan leadership institute that finds natural leaders and prepares them to lead America's cities."
page("index.html", ORG, D, home)
page("about.html", f"About | {ORG}", D, about)
page("manifesto.html", f"Manifesto | {ORG}", "A new standard for civic leadership: the Civic Leaders Lab manifesto.", man)
page("fellowship.html", f"The Fellowship | {ORG}", "A twelve-month program that turns potential into civic leadership.", fel)
page("work.html", f"Our work | {ORG}", "What Civic Leaders Lab will build: a leadership model, a fellowship, an innovation lab, and open playbooks.", work)
page("support.html", f"Founding partners | {ORG}", "Help launch the first year of Civic Leaders Lab in Las Vegas.", sup)
page("contact.html", f"Contact | {ORG}", "Get in touch with Civic Leaders Lab.", con)
shutil.copy(os.path.join(HERE, "styles.css"), OUT)
shutil.copy(os.path.join(HERE, "founder.jpg"), OUT)
print("built", OUT, "preview" if PREVIEW else "")
