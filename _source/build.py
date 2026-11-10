"""Builds the Civic Leaders Lab static site.
Usage: python3 build.py <out_dir> [--preview]
--preview writes index.html without the <!doctype>/<html>/<head> shell (the Artifact viewer adds its own)."""
import sys, os, shutil

OUT = sys.argv[1]
PREVIEW = "--preview" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
ORG = "Civic Leaders Lab"
EMAIL = "ilan@civicleaderslab.org"

NAV = [("index.html", "Home"), ("about.html", "About"), ("manifesto.html", "Manifesto"),
       ("fellowship.html", "Fellowship"), ("work.html", "Our work"), ("contact.html", "Contact")]

MARK = """<svg class="brand-mark" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="48" fill="#1b2f5e" stroke="#2c4174" stroke-width="2"/><path d="M50 13 L54.2 35.8 L70 40 L54.2 44.2 L50 60 L45.8 44.2 L30 40 L45.8 35.8Z" fill="#e2b85a"/><rect x="12" y="66" width="76" height="3" fill="#e2b85a"/><rect x="22" y="74" width="56" height="2.2" fill="#eef0f6" opacity=".45"/><rect x="32" y="81" width="36" height="2.2" fill="#eef0f6" opacity=".3"/></svg>"""

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
<link rel="icon" href="favicon.svg" type="image/svg+xml">
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
    '<div class="btns"><a class="btn btn-gold" href="fellowship.html">Explore the Fellowship</a><a class="btn btn-ghost" href="manifesto.html">Get the manifesto</a></div>',
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
SIGNUP_FORM = """<form class="form signup-card" id="manifesto-form" name="manifesto" method="POST" action="manifesto-thanks.html" data-netlify="true" netlify-honeypot="bot-field">
<input type="hidden" name="form-name" value="manifesto">
<p hidden><label>Leave empty <input name="bot-field"></label></p>
<div><p class="eyebrow" style="margin-bottom:6px">Free &middot; Sent by email</p><h3 style="margin:0">Get the full manifesto</h3></div>
<div class="field"><label for="m-name">Your name</label><input id="m-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="m-email">Email</label><input id="m-email" name="email" type="email" autocomplete="email" required></div>
<div><button class="btn btn-gold" type="submit">Send me the manifesto</button></div>
<p class="form-note">We will send it to your inbox personally. No spam, and we never share your email.</p>
<p class="form-done" id="manifesto-done" hidden>Thanks. This is a preview, so nothing was sent. The form goes live once the site is online.</p>
</form>"""

man = hero("The manifesto", "We have a vision for <span class=\"gold\">America&rsquo;s cities.</span>",
           "We would love to share it with you. Leave your name and email, and we will send you the full Civic Leaders Lab manifesto.",
           '<div class="btns"><a class="btn btn-gold" href="#get-it">Send me the manifesto</a></div>')
man += f"""
<section class="band"><div class="wrap split">
<div><p class="eyebrow">Why we wrote it</p><h2>People have not stopped caring. <span class="gold">They have stopped believing.</span></h2></div>
<div class="stack"><div class="prose">
<p>People are tired of politics without leadership. They want vision. They want trust. They want character. They want to be heard, and to feel safe in the hands of those who lead them.</p>
<p>We believe that can change, and that it starts in our cities. Not with anger, and not with another party, but with a new generation of leaders who serve before they rule, mean what they say, and deliver results people can see on their own street.</p>
<p>The manifesto is our promise of what that leadership looks like, and our invitation to build it together.</p></div>
<p class="pull">Better leaders. Better systems. <span class="gold">Better cities.</span></p></div>
</div></section>

<section class="band on-navy"><div class="wrap">
<div class="split" style="margin-bottom:36px"><div><p class="eyebrow">Inside the manifesto</p><h2>A new standard for <span class="gold">civic leadership.</span></h2></div>
<p class="lede" style="margin-top:0">A short, honest read about where America&rsquo;s cities are, and where we believe they can go.</p></div>
<div class="grid-3">
<div class="cell"><span class="k">The moment</span><p>Why so many people have stopped believing in politics, and why that silence is an opening, not an ending.</p></div>
<div class="cell"><span class="k">What is at stake</span><p>What America risks losing if we do not act boldly now, and what we will do to protect it.</p></div>
<div class="cell"><span class="k">Our values</span><p>Nonpartisan, but never without values: love of country, freedom of faith, justice under law, and leading with honor.</p></div>
<div class="cell"><span class="k">Flip the ratio</span><p>Leadership first, politics second. Why the leaders we need should spend 80% of their energy on vision, people and results.</p></div>
<div class="cell"><span class="k">Leadership for the age of AI</span><p>How cities can know every resident, see problems early, and solve them in days instead of months.</p></div>
<div class="cell"><span class="k">The New Standard</span><p>The commitments that define the leaders we will raise, and the city pilots we will test, measure and share.</p></div>
</div>
</div></section>

<section class="band paper" id="get-it"><div class="wrap split">
<div class="stack"><div><p class="eyebrow">Join us</p><h2>Be one of the first to read it.</h2></div>
<div class="prose"><p>This vision belongs to everyone who wants their city to rise: residents, future leaders, and partners who believe America&rsquo;s best days can still be ahead.</p>
<p>Tell us where to send it, and the manifesto will arrive in your inbox from our founder, Ilan Gelberg.</p></div>
<p class="callout">The future of our cities will be shaped by the people willing to lead them. <span class="gold">Let&rsquo;s build that future together.</span></p></div>
{SIGNUP_FORM}
</div></section>
<script>
(function () {{
  var live = /(civicleaderslab\\.org|netlify\\.app)$/.test(location.hostname);
  document.getElementById('manifesto-form').addEventListener('submit', function (e) {{
    if (live) return;
    e.preventDefault();
    document.getElementById('manifesto-done').hidden = false;
  }});
}})();
</script>
"""

thanks = hero("Thank you", "The manifesto is <span class=\"gold\">on its way.</span>",
              "Thank you for wanting to be part of this. We will email the full Civic Leaders Lab manifesto to you shortly.")
thanks += f"""
<section class="band"><div class="wrap split">
<div><p class="eyebrow">While you wait</p><h2>See how the vision becomes real.</h2></div>
<div class="stack"><div class="prose"><p>The manifesto is where it starts. The Fellowship is how we turn it into leaders, and the city pilots are how we prove it works.</p>
<p>Did not get it within a day? Check your spam folder, or write to us at {EMAIL}.</p></div>
<div class="btns" style="margin-top:0"><a class="btn btn-navy" href="fellowship.html">Explore the Fellowship</a><a class="btn btn-ghost" href="about.html">Meet the founder</a></div></div>
</div></section>
"""
thanks += cta("Want to help launch the first Fellowship?", "Join the small circle of founding partners building this from day one.")

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
page("manifesto.html", f"Manifesto | {ORG}", "We have a vision for America's cities. Get the Civic Leaders Lab manifesto by email.", man)
page("manifesto-thanks.html", f"Thank you | {ORG}", "The Civic Leaders Lab manifesto is on its way.", thanks)
page("fellowship.html", f"The Fellowship | {ORG}", "A twelve-month program that turns potential into civic leadership.", fel)
page("work.html", f"Our work | {ORG}", "What Civic Leaders Lab will build: a leadership model, a fellowship, an innovation lab, and open playbooks.", work)
page("support.html", f"Founding partners | {ORG}", "Help launch the first year of Civic Leaders Lab in Las Vegas.", sup)
page("contact.html", f"Contact | {ORG}", "Get in touch with Civic Leaders Lab.", con)
shutil.copy(os.path.join(HERE, "styles.css"), OUT)
shutil.copy(os.path.join(HERE, "founder.jpg"), OUT)
print("built", OUT, "preview" if PREVIEW else "")
