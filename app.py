import os
from typing import Optional

import google.generativeai as genai
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MENTOR_INSTRUCTION = (
   """You are Careero's AI Mentor—a friendly, sharp, and encouraging older-sibling-style guide for students in India from Class 9 to B.Tech.

Rules for your responses:
- Tone: Warm, direct, and conversational. Never sound like a stiff textbook or formal counselor.
- Context: Always tailor advice to the Indian education system (Class 10/12 streams, JEE, NEET, CUET, NID, CLAT, B.Tech, and realistic Indian entry-to-mid salary ranges in ₹ LPA).
- Formatting: Use short paragraphs and clean Markdown bullet points. NEVER use arrow symbols (→) to chain steps together.
- Engagement: Keep answers focused and scannable, and always end with one short, specific question to help narrow down the student's next step."""
)

st.set_page_config(
    page_title="Careero",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAV = [
    "Home/Landing Page",
    "Grade-Level Pathways",
    "Interest Assessment",
    "Inspiration Stories",
    "AI Mentor Chat",
]

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560;9..144,680&family=Figtree:wght@400;500;600;700&display=swap');

    .stApp {
        background: #f3efe6;
        font-family: "Figtree", "Segoe UI", sans-serif;
    }
    html, body, [class*="css"] {
        font-family: "Figtree", "Segoe UI", sans-serif;
    }
    h1, h2, h3 {
        font-family: "Fraunces", Georgia, serif !important;
        letter-spacing: -0.03em;
        color: #1c1915;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3.5rem;
        max-width: 1080px;
    }
    [data-testid="stSidebar"] {
        background: #14241c;
        border-right: 1px solid #0e1a14;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #f4f0e6 !important;
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #c9ddd1 !important;
    }
    .brand {
        font-family: "Fraunces", Georgia, serif;
        font-size: 2rem;
        font-weight: 680;
        line-height: 1;
        margin: 0.2rem 0 0.15rem 0;
        color: #f7f3ea;
    }
    .kicker {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #1f6b4a;
        margin-bottom: 0.2rem;
    }
    .lede {
        font-size: 1.12rem;
        line-height: 1.55;
        color: #3d3830;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #fffdf8;
        border-color: #e5dccb !important;
        border-radius: 16px !important;
    }
    div[data-testid="stMetric"] {
        background: #fffdf8;
        border: 1px solid #e5dccb;
        border-radius: 16px;
        padding: 0.8rem 1rem 0.4rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def bullets(items: list[str]) -> None:
    st.markdown("\n".join(f"- {item}" for item in items))


def set_nav(page: str) -> None:
    st.session_state.nav = page


PATHWAYS = {
    "Class 9–10": {
        "summary": (
            "These two years are for range and honesty. Build real skill in maths, "
            "science, and language, and try one or two directions before anyone asks "
            "you to name a career."
        ),
        "focus": [
            "Treat maths and science as skills you practice, not talents you either have or lack.",
            "Read beyond the textbook: one article, one biography, or one chapter a week is enough.",
            "Finish one small project. A science model, a Python quiz, a school magazine piece, or a budget for a fest all count.",
            "Notice which homework you return to and which you avoid. That is more useful than a career title.",
        ],
        "exams": [
            "Board exams at the end of Class 10 matter for stream cutoffs and scholarships. Steady revision beats a last-month sprint.",
            "Olympiads and NTSE-style tests are optional stretch. Skip them if they crowd out school fundamentals.",
            "Entrance coaching is not required yet. If a class is eating your sleep, it is too early.",
        ],
        "clusters": [
            {
                "title": "How streams will open after Class 10",
                "body": (
                    "Most boards then offer Science (PCM or PCB), Commerce, and Humanities. "
                    "PCM keeps engineering and several science degrees open. PCB is the usual "
                    "road toward NEET and life sciences. Commerce leads toward business, "
                    "accounts, and economics. Humanities leads toward law, social sciences, "
                    "design portfolios, and media. You do not need to choose among these in Class 9."
                ),
            },
            {
                "title": "A diploma is a real option, not a leftover",
                "body": (
                    "After Class 10, polytechnic diploma courses train you for a trade in three years. "
                    "Many states allow lateral entry into the second year of B.Tech after a diploma. "
                    "This fits students who want workshop practice sooner. Check your state technical "
                    "board for branches and the lateral-entry exam."
                ),
            },
            {
                "title": "What to ignore for now",
                "body": (
                    "Online posts that rank careers by salary are written for working adults in large cities. "
                    "They are a poor map for a 14-year-old. Ignore 'drop out and build a company' stories too. "
                    "The students in those stories already had unusual support, and most strong paths in India "
                    "still run through school."
                ),
            },
        ],
    },
    "Class 11–12 · PCM": {
        "summary": (
            "Physics, chemistry, and mathematics keep the widest set of science and engineering "
            "doors open. The work is cumulative: Class 11 gaps become Class 12 panic."
        ),
        "focus": [
            "Finish the Class 11 textbook before collecting more material. NCERT is the base for CBSE and for JEE Main.",
            "Separate board answers from entrance problem practice. Both matter, and they are not the same skill.",
            "Keep one evening a week for a project or a sport. Two years of only mock tests is a brittle plan.",
            "If maths is collapsing, get help early. Switching streams later is possible and better than silent failure.",
        ],
        "exams": [
            "JEE Main is the broad national engineering exam. JEE Advanced is only for students who qualify and want the IITs.",
            "State exams such as MHT-CET, KCET, EAMCET, and WBJEE fill a large share of engineering seats. Know which one your state uses.",
            "BITSAT and institute exams are extras, not obligations. Add one only if the syllabus overlaps with what you already study.",
            "Architecture needs a design aptitude test such as NATA along with maths. Confirm the current brochure.",
        ],
        "clusters": [
            {
                "title": "Engineering after PCM",
                "body": (
                    "B.Tech seats span computer science, electronics, electrical, mechanical, civil, "
                    "chemical, and more. The branch should match how you like to work: software, "
                    "circuits, machines, or structures. A 'lower' branch at a college where you will "
                    "actually learn can beat a famous branch you chose only for the label."
                ),
            },
            {
                "title": "Science degrees that are not engineering",
                "body": (
                    "BSc and integrated programs in maths, physics, chemistry, statistics, and "
                    "economics are serious routes. Research-leaning students later look at JAM, "
                    "institute entrance exams, and postgraduate study. Data and finance roles also "
                    "hire from strong maths degrees, not only from CSE."
                ),
            },
            {
                "title": "Boards and entrance, in the same week",
                "body": (
                    "A workable week has school hours, one deep problem-solving block, and a board "
                    "writing block where you practice full answers. Sleep is part of the plan. "
                    "If your mock rank and your school marks are both falling, reduce the number of "
                    "books before you reduce sleep."
                ),
            },
        ],
    },
    "Class 11–12 · PCB": {
        "summary": (
            "Physics, chemistry, and biology are the usual preparation for NEET and for life-science "
            "degrees. Biology rewards steady reading. Physics still decides many ranks."
        ),
        "focus": [
            "Read NCERT biology until you can explain a chapter aloud. Highlighting is not revision.",
            "Do not drop physics because it feels less 'medical'. It is a large part of NEET.",
            "If your board allows an optional maths paper, it keeps some engineering and data routes open. Check the rule before you assume.",
            "Hospital shadowing or a first-aid course tells you more about medicine than a slogan does.",
        ],
        "exams": [
            "NEET UG is the national exam for MBBS, BDS, and most AYUSH and veterinary seats.",
            "Pharmacy, nursing, physiotherapy, and several allied-health courses have their own institute processes. List them before results week.",
            "CUET opens many BSc programs if you want research, psychology, or biotech more than a clinic.",
        ],
        "clusters": [
            {
                "title": "Medicine is one health career, not the only one",
                "body": (
                    "MBBS is long, competitive, and clinical. Pharmacy, nursing, public health, "
                    "clinical psychology, biotechnology, and research are different jobs with different "
                    "training. If you care about health but dislike the idea of a hospital ward, say so "
                    "early and look at those routes."
                ),
            },
            {
                "title": "If NEET is the goal",
                "body": (
                    "Build a revision loop: learn, recall without notes the next day, and again after a week. "
                    "Past-paper practice starts only after a chapter is actually learned. A stack of unsolved "
                    "test series is not a plan."
                ),
            },
            {
                "title": "Switching toward maths or commerce",
                "body": (
                    "Some schools allow a shift in Class 11 if you ask early. After Class 12, a later move "
                    "into engineering usually means you still need mathematics eligibility for that exam. "
                    "Talk to your school before the registration deadline, not after the first failed unit test."
                ),
            },
        ],
    },
    "Class 11–12 · Commerce": {
        "summary": (
            "Commerce is a professional path, not a backup for students who left science. "
            "Accounts rewards precision. Economics and maths reward reasoning."
        ),
        "focus": [
            "If your school offers maths with commerce, take it when you can. It helps economics, finance, and several college entrances.",
            "Practice accounts by hand until the formats are automatic. Reading solved problems feels like study and is not.",
            "Follow one real business you can explain: a local shop, a listed company, or a school fest budget.",
            "English and presentation matter for internships and for professional interviews later.",
        ],
        "exams": [
            "CUET is the gateway to many central-university B.Com, BBA, and economics programs.",
            "CA, CS, and CMA are professional routes that continue well after Class 12. Check the current ICAI, ICSI, and ICMAI eligibility before you pay a fee.",
            "IPMAT and other BBA entrance exams are optional targets for students who want management college early.",
        ],
        "clusters": [
            {
                "title": "Chartered accountancy and its neighbours",
                "body": (
                    "CA is a multi-stage qualification with articleship, not a college degree you finish in three years. "
                    "It suits students who like rules, accuracy, and long study cycles. Company Secretary work leans "
                    "toward law and governance. Cost and management accountancy leans toward costing inside firms. "
                    "You can start college and a professional course together. You do not have to pick only one."
                ),
            },
            {
                "title": "College routes",
                "body": (
                    "B.Com builds accounting and law foundations. BBA is broader and more classroom-and-internship "
                    "oriented. Economics, especially with maths, opens analysis, policy, and later finance roles. "
                    "The college's teaching and internship culture matter more than a viral ranking list."
                ),
            },
            {
                "title": "If you wanted science and landed here",
                "body": (
                    "Commerce does not block technology. BCA, later analytics courses, and self-taught programming "
                    "are available. It does change which entrance exams you can take immediately. Be plain with "
                    "yourself about whether you are relieved or resentful, and plan from that fact."
                ),
            },
        ],
    },
    "Class 11–12 · Humanities": {
        "summary": (
            "Humanities is for students who want language, society, history, psychology, or law "
            "as a craft. It is a poor place to hide from every subject, and a strong place to get "
            "very good at reading and argument."
        ),
        "focus": [
            "Write every week. A paragraph you can defend is worth more than a notebook of highlights.",
            "Choose optional subjects you will still respect in March: political science, psychology, economics, geography, or a literature.",
            "Build proof of work: a school magazine, debate record, art portfolio, or a small research essay.",
            "Maths or economics as an extra subject helps if law-and-policy or economics is a possibility.",
        ],
        "exams": [
            "CLAT is the major law entrance for many national law universities. It tests reading and reasoning more than a single textbook.",
            "CUET covers a wide set of BA, psychology, and social-science programs.",
            "Design exams (NID, NIFT, UCEED, and state tests) change their eligibility. Read the current brochure and start a portfolio anyway.",
        ],
        "clusters": [
            {
                "title": "Law",
                "body": (
                    "A five-year law program after Class 12 is the direct route. It asks for daily reading, "
                    "not a talent for arguing at the dinner table. Start with newspapers and with finishing "
                    "timed passages. A law degree can lead to practice, firms, policy, and compliance."
                ),
            },
            {
                "title": "Design, media, and psychology",
                "body": (
                    "Design schools look at original work. Copying tutorial screenshots will not carry a portfolio. "
                    "Media and journalism programs want clips and writing. Psychology degrees split into counseling "
                    "routes, which need further study, and research routes. None of these is a casual elective."
                ),
            },
            {
                "title": "Public life, later",
                "body": (
                    "Civil services are a graduate-level exam, not a Class 11 identity. The useful preparation now "
                    "is reading history and polity properly and writing clearly. Choose an undergraduate subject "
                    "you can score in and care about."
                ),
            },
        ],
    },
    "Diploma after Class 10": {
        "summary": (
            "A polytechnic diploma is a three-year, hands-on qualification. It can lead straight "
            "into a job or into the second year of B.Tech through lateral entry."
        ),
        "focus": [
            "Pick a branch for the kind of workshop you want: computers, electronics, mechanical, civil, or electrical.",
            "Labs and industrial visits are the point. Do not treat them as attendance.",
            "Keep maths alive if you want lateral entry. The bridge into B.Tech is harder if Class 10 maths was shaky.",
            "Ask working diploma holders in your city what the first job actually looks like.",
        ],
        "exams": [
            "State polytechnic admissions usually use Class 10 marks or a state entrance. Names and cutoffs differ.",
            "Lateral entry into B.Tech is a separate exam, often in the final diploma year. Look up your state directorate of technical education.",
        ],
        "clusters": [
            {
                "title": "When a diploma is a strong fit",
                "body": (
                    "Choose it if you want to work with tools and systems sooner, or if a full higher-secondary "
                    "science load is the wrong classroom for you. It is a structured path into engineering, "
                    "not an exit from education."
                ),
            },
            {
                "title": "When to stay in Class 11 instead",
                "body": (
                    "Stay in higher secondary if you want MBBS, most pure-science degrees, CA foundations on the "
                    "usual timeline, or law after Class 12. Those routes assume Class 11 and 12."
                ),
            },
            {
                "title": "After the diploma",
                "body": (
                    "Two honest options are a job in your trade, or lateral entry into B.Tech. "
                    "Either can be the right one. Visit one college lab and one workplace before you decide."
                ),
            },
        ],
    },
    "B.Tech": {
        "summary": (
            "The degree is four years of fundamentals, projects, and increasingly specific choices. "
            "Your branch shapes the first job. Your projects and internship decide whether that job is any good."
        ),
        "focus": [
            "Year 1: survive maths and the basics, and learn one programming language even if you are not in CSE.",
            "Year 2: core branch subjects plus one project small enough to finish.",
            "Year 3: an internship or a serious lab project. This is the year recruiters actually ask about.",
            "Year 4: placements, GATE or higher studies, or a careful first step into a startup. Do not attempt all three at full intensity.",
        ],
        "exams": [
            "GATE matters if you want M.Tech, several PSUs, or a research-leaning path.",
            "CAT and other management exams are a different career turn. Take them because you want that work, not because placements feel slow.",
            "Study-abroad applications need transcripts, a test such as GRE only where the university asks, and projects you can explain.",
        ],
        "clusters": [
            {
                "title": "Computer science and allied branches",
                "body": (
                    "CSE, IT, AI, and often ECE students compete for software roles. The branch label is not a "
                    "portfolio. Ship projects, do an internship, and be able to explain your code without reading it. "
                    "Core electronics, embedded systems, and communications are real ECE careers if you do not want a software job."
                ),
            },
            {
                "title": "Mechanical, civil, electrical, chemical",
                "body": (
                    "These branches feed design, manufacturing, energy, construction, and process industries. "
                    "Software electives can still help, but abandoning the core lab work leaves you unconvincing "
                    "in both markets. Learn the tools your industry uses: CAD, site practice, power systems, or process calculations."
                ),
            },
            {
                "title": "Placements without the panic",
                "body": (
                    "Many companies filter on CGPA. Treat the cutoff as a constraint, then spend the remaining "
                    "energy on one strong project and on speaking clearly. Mass-applying to internships with an "
                    "empty resume is less useful than asking two seniors how they got theirs."
                ),
            },
        ],
    },
}


QUESTIONS = [
    {
        "prompt": "What would you rather do on a free afternoon?",
        "options": {
            "Sketch, photograph, or edit a short video": {"Design & Media": 2},
            "Take a gadget apart or wrestle with a maths puzzle": {
                "Core Engineering": 2,
                "Technology": 1,
            },
            "Read a science piece and write down questions": {"Research": 2},
            "Organise a fest stall, a budget, or a team": {"Business & Finance": 2},
            "Write, debate, or read about a case or a policy": {"Humanities & Law": 2},
        },
    },
    {
        "prompt": "Which subject would you revise first if exams were next month?",
        "options": {
            "Computer science or anything with code": {"Technology": 2},
            "Mathematics": {"Core Engineering": 2, "Technology": 1},
            "Biology": {"Medicine & Health": 2, "Research": 1},
            "Accountancy, economics, or business studies": {"Business & Finance": 2},
            "History, political science, or literature": {"Humanities & Law": 2},
            "Art, design, or media": {"Design & Media": 2},
        },
    },
    {
        "prompt": "Which question is the most interesting?",
        "options": {
            "Why does this bridge, engine, or circuit behave this way?": {"Core Engineering": 2},
            "Why does this illness happen, and what helps?": {"Medicine & Health": 2},
            "How does a shop, market, or team actually decide?": {"Business & Finance": 2},
            "How should this app or poster look so people use it?": {
                "Design & Media": 2,
                "Technology": 1,
            },
            "Is this rule fair, and who does it affect?": {"Humanities & Law": 2},
            "What does the evidence say, and what is still unknown?": {"Research": 2},
        },
    },
    {
        "prompt": "Which school club would you join first?",
        "options": {
            "Coding or robotics": {"Technology": 2, "Core Engineering": 1},
            "Health, biology, or first aid": {"Medicine & Health": 2},
            "Entrepreneurship or a commerce club": {"Business & Finance": 2},
            "Debate, MUN, or the school magazine": {"Humanities & Law": 2, "Design & Media": 1},
            "Astronomy, quiz, or a science circle": {"Research": 2},
            "Photography, film, or the art room": {"Design & Media": 2},
        },
    },
    {
        "prompt": "Which piece of work would you be proud to show?",
        "options": {
            "A tool or program people use every week": {"Technology": 2},
            "A machine, a structure, or a working model": {"Core Engineering": 2},
            "Care you gave, or a clear explanation of a health topic": {"Medicine & Health": 2},
            "A small business, brand, or event that ran well": {"Business & Finance": 2},
            "A film, campaign, or design people remember": {"Design & Media": 2},
            "An essay, case, or report that changed someone's mind": {"Humanities & Law": 2},
            "A careful experiment with notes someone else could repeat": {"Research": 2},
        },
    },
    {
        "prompt": "When a chapter is difficult, what do you do first?",
        "options": {
            "Build a tiny version in code": {"Technology": 2},
            "Derive it and solve problems on paper": {"Core Engineering": 2, "Research": 1},
            "Draw the process until it makes sense": {"Design & Media": 1, "Medicine & Health": 1},
            "Connect it to a news story, a shop, or a family example": {
                "Business & Finance": 1,
                "Humanities & Law": 1,
            },
            "Teach it to a friend from a blank page": {"Research": 2},
        },
    },
    {
        "prompt": "Who do you most want your work to help?",
        "options": {
            "People using a product or a tool": {"Technology": 2, "Design & Media": 1},
            "Patients and their families": {"Medicine & Health": 2},
            "A team building something physical": {"Core Engineering": 2},
            "Customers, clients, or a business owner": {"Business & Finance": 2},
            "Readers, citizens, or a neighbourhood": {"Humanities & Law": 2},
            "Other people trying to understand a hard question": {"Research": 2},
        },
    },
    {
        "prompt": "Which headline would you open first?",
        "options": {
            "Students ship a tool their school actually uses": {"Technology": 2},
            "A new bridge design cuts an hour off the commute": {"Core Engineering": 2},
            "A hospital team untangles a difficult diagnosis": {"Medicine & Health": 2},
            "A small brand finds its first hundred customers": {"Business & Finance": 2},
            "The story behind a film's title sequence": {"Design & Media": 2},
            "A judgment that changed how a rule works": {"Humanities & Law": 2},
            "A lab result that surprised the researchers": {"Research": 2},
        },
    },
]

INTERESTS = {
    "Technology": (
        "You lean toward building software and tools. In Class 9–10, start Python and finish one small program. "
        "In Class 11–12, PCM (or commerce plus self-taught code) keeps the road open. After school, look at "
        "B.Tech in CSE, IT, or ECE, or at BCA if engineering is not your route. Projects you can explain matter "
        "more than a pile of certificates."
    ),
    "Core Engineering": (
        "You lean toward physical systems: machines, structures, circuits, and energy. PCM plus JEE Main or your "
        "state engineering exam is the usual school path. Branches such as mechanical, civil, electrical, "
        "electronics, and chemical match this better than choosing CSE only for the crowd. If buildings and "
        "drawing appeal, check architecture and NATA as well."
    ),
    "Medicine & Health": (
        "You lean toward health and the human body. PCB and NEET UG are the route for MBBS and several medical "
        "seats. If a hospital career is not what you want, pharmacy, nursing, physiotherapy, public health, "
        "and psychology are different professions, not consolation prizes. Spend time near the work before you lock the exam."
    ),
    "Business & Finance": (
        "You lean toward organisations, money, and decisions. Commerce, especially with maths, is a direct fit. "
        "College options include B.Com, BBA, and economics. CA, CS, and CMA are longer professional paths. "
        "Confirm the latest eligibility with the institute before you register, and keep one real business you can describe in detail."
    ),
    "Design & Media": (
        "You lean toward making things people see and use. Start a portfolio of original work now. School stream "
        "rules differ by design exam, so read the current NID, NIFT, UCEED, or state brochure rather than an old blog. "
        "Writing, photography, and basic coding are all useful companions."
    ),
    "Humanities & Law": (
        "You lean toward language, argument, and public questions. Humanities subjects, a writing habit, and "
        "timed reading are the right preparation. CLAT is the main law entrance. CUET opens many BA and social-science "
        "degrees. Civil services can wait until you have an undergraduate subject you actually like."
    ),
    "Research": (
        "You lean toward questions, evidence, and careful notes. Strong school science or maths comes first. "
        "Later paths include BSc or an integrated science degree, and exams such as JAM for postgraduate study. "
        "Olympiads are optional. A lab notebook or a small study you can explain is better proof than a slogan about curiosity."
    ),
}


def score_answers(answers: list[str]) -> dict[str, int]:
    totals = {name: 0 for name in INTERESTS}
    for question, answer in zip(QUESTIONS, answers):
        for interest, points in question["options"][answer].items():
            totals[interest] += points
    return totals


def category_caps() -> dict[str, int]:
    caps = {name: 0 for name in INTERESTS}
    for question in QUESTIONS:
        best = {name: 0 for name in INTERESTS}
        for weights in question["options"].values():
            for interest, points in weights.items():
                best[interest] = max(best[interest], points)
        for interest, points in best.items():
            caps[interest] += points
    return caps


def render_home() -> None:
    st.markdown('<p class="kicker">Class 9 to B.Tech · India</p>', unsafe_allow_html=True)
    st.title("Careero")
    st.markdown(
        '<p class="lede">A calmer way to choose subjects, exams, and the next two years of work. '
        "Built for school and B.Tech students who are tired of career lists that all sound the same.</p>",
        unsafe_allow_html=True,
    )

    intro, start = st.columns([1.4, 1], gap="large")
    with intro:
        st.subheader("Start from where you are")
        bullets(
            [
                "Class 9 and 10: build fundamentals and try a direction before naming a job.",
                "Class 11 and 12: match a stream to real exams — JEE, state CETs, NEET, CUET, CLAT, and professional courses.",
                "Diploma and B.Tech: turn a branch into projects, internships, and a next step you can explain.",
            ]
        )
    with start:
        with st.container(border=True):
            st.markdown("**Open a section**")
            st.caption("Each page stands on its own. You do not have to finish them in order.")
            for destination in NAV[1:]:
                st.button(
                    destination,
                    on_click=set_nav,
                    args=(destination,),
                    width="stretch",
                    key=f"home_{destination}",
                )

    st.write("")
    one, two, three = st.columns(3)
    one.metric("Stages", "9th → B.Tech", "School, diploma, college")
    two.metric("After Class 10", "4 streams", "PCM, PCB, commerce, humanities")
    three.metric("Mentor", "Ask tonight", "Exams, branches, family talks")

    st.write("")
    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.markdown("**Pathways, not posters**")
            st.write(
                "See what to study this year, which exams actually matter, and which options can wait. "
                "Salary slideshows are left out on purpose."
            )
    with right:
        with st.container(border=True):
            st.markdown("**An assessment that can disagree with you**")
            st.write(
                "Eight questions map to technology, engineering, health, business, design, humanities, and research. "
                "The result is a prompt for reading, not a label you have to keep."
            )

    with st.expander("How to use Careero this week"):
        bullets(
            [
                "Pick your stage on Grade-Level Pathways and write down the two exams that apply to you.",
                "Take the Interest Assessment once, without choosing the option you think sounds impressive.",
                "Read the two inspiration stories for the habit, not for the headline about leaving college.",
                "Ask the mentor one specific question that includes your class.",
            ]
        )


def render_pathways() -> None:
    st.markdown('<p class="kicker">Subjects, exams, and timing</p>', unsafe_allow_html=True)
    st.title("Grade-Level Pathways")
    st.markdown(
        '<p class="lede">Choose the stage you are in now. The notes stay specific to that stage, '
        "including what not to worry about yet.</p>",
        unsafe_allow_html=True,
    )

    stage = st.selectbox("Your stage", list(PATHWAYS), label_visibility="collapsed")
    path = PATHWAYS[stage]
    st.write(path["summary"])

    focus, exams = st.columns(2, gap="large")
    with focus:
        with st.container(border=True):
            st.markdown("**Focus this year**")
            bullets(path["focus"])
    with exams:
        with st.container(border=True):
            st.markdown("**Exams and routes**")
            bullets(path["exams"])

    st.subheader("Go deeper")
    for cluster in path["clusters"]:
        with st.expander(cluster["title"]):
            st.write(cluster["body"])

    with st.expander("If your exact course is not listed"):
        st.write(
            "BSc, BCA, B.Com, BA, and BBA students can use the Class 11–12 page closest to their subjects, "
            "then borrow the B.Tech year plan: fundamentals, one finished project, an internship, and a single next step. "
            "If you have just finished Class 10, compare two stream pages rather than hunting for a job title."
        )


def render_assessment() -> None:
    st.markdown('<p class="kicker">A reflection, not a rank</p>', unsafe_allow_html=True)
    st.title("Interest Assessment")
    st.markdown(
        '<p class="lede">Answer for the work you would actually do, not for the option that sounds safest '
        "at home. Eight questions. No account required.</p>",
        unsafe_allow_html=True,
    )

    with st.form("interest_assessment"):
        answers: list[Optional[str]] = []
        for index, question in enumerate(QUESTIONS):
            st.markdown(f"**{index + 1}. {question['prompt']}**")
            answers.append(
                st.radio(
                    question["prompt"],
                    list(question["options"]),
                    index=None,
                    key=f"assess_{index}",
                    label_visibility="collapsed",
                )
            )
            st.write("")
        submitted = st.form_submit_button("See my pathways", type="primary")

    if submitted:
        if any(answer is None for answer in answers):
            st.warning("Answer every question. Skipped ones make the pattern unreliable.")
        else:
            st.session_state.results = score_answers(answers)  # type: ignore[arg-type]

    results = st.session_state.get("results")
    if not results:
        return

    ranked = sorted(results.items(), key=lambda item: (-item[1], item[0]))
    top = [item for item in ranked if item[1] > 0][:3]
    caps = category_caps()

    st.subheader("Your strongest leans")
    st.caption("Tied scores stay in alphabetical order. A two-point gap is a hint, not a destiny.")

    columns = st.columns(len(top) or 1, gap="medium")
    for column, (name, points) in zip(columns, top):
        with column:
            with st.container(border=True):
                share = points / caps[name] if caps[name] else 0
                st.markdown(f"**{name}**")
                st.progress(share, text=f"{points} of {caps[name]}")
                st.write(INTERESTS[name])

    chart = pd.DataFrame(
        {"Score": results},
    ).sort_values("Score", ascending=False)
    st.bar_chart(chart, horizontal=True)

    with st.expander("How to read this"):
        st.write(
            "The questions add points when an answer matches a kind of work. They are not an aptitude test, "
            "a personality diagnosis, or a placement prediction. Take the top result to Grade-Level Pathways "
            "and check whether your current subjects can reach it. If the top result feels wrong, trust the "
            "subject you already work at, and ask the mentor to compare the two."
        )

    if st.button("Clear my results"):
        st.session_state.results = None
        st.rerun()


def render_stories() -> None:
    st.markdown('<p class="kicker">Habits worth copying</p>', unsafe_allow_html=True)
    st.title("Inspiration Stories")
    st.markdown(
        '<p class="lede">Two short readings. The useful part is how they practiced, not the myth that school is optional.</p>',
        unsafe_allow_html=True,
    )

    mark, elon = st.columns(2, gap="large")
    with mark:
        with st.container(border=True):
            st.markdown("**Mark Zuckerberg**")
            st.write(
                "Mark Zuckerberg launched Facebook in 2004 while he was a student at Harvard, after years of "
                "building small programs for himself and his classmates. At college he studied computer science "
                "and psychology, a combination that shows up in the product: software, plus a close interest in "
                "how people behave."
            )
            st.write(
                "For a student in India, the transferable part is narrow and practical. He kept shipping small tools, "
                "stayed with one product long enough to improve it, and learned a human subject alongside the technical one. "
                "Leaving college in his second year is not a plan for Class 9, and it is not a plan for B.Tech either. "
                "The matching assignment is a project you finish this term."
            )
        with st.expander("Try this from Zuckerberg's story", expanded=True):
            bullets(
                [
                    "Class 9–10: build a tiny program your own class can use, such as a quiz or a club signup list.",
                    "Class 11–12: keep one project alive beside board preparation, even if it is only two hours a week.",
                    "B.Tech: write down who uses your project and what they do differently because of it.",
                ]
            )
    with elon:
        with st.container(border=True):
            st.markdown("**Elon Musk**")
            st.write(
                "Elon Musk taught himself programming as a child, then studied physics and economics before working "
                "on companies in payments, cars, energy, and space. The through-line is not a single viral moment. "
                "It is a long stack of hard subjects, especially physics, and a willingness to stay on engineering problems for years."
            )
            st.write(
                "If you like systems in the physical world, that story points toward mathematics, physics, and a serious "
                "engineering or science degree. Wide reading is an advantage. Quitting school early is not the lesson. "
                "Mechanical, electrical, electronics, and related B.Tech branches are the straightforward version of this interest."
            )
        with st.expander("Try this from Musk's story", expanded=True):
            bullets(
                [
                    "Class 9–10: get comfortable with algebra and with explaining one physics idea in plain language.",
                    "Class 11–12: if PCM is your stream, treat fundamentals as the ambition. Entrance ranks sit on top of that.",
                    "B.Tech: pick a problem that takes a whole semester. Cars, energy, and hardware reward depth.",
                ]
            )

    first, second, third = st.columns(3)
    with first:
        with st.container(border=True):
            st.markdown("**Build small**")
            st.write("A finished project teaches more than a course you only registered for.")
    with second:
        with st.container(border=True):
            st.markdown("**Learn the base subject**")
            st.write("Psychology beside code. Physics beside ambition. The second subject is not a distraction.")
    with third:
        with st.container(border=True):
            st.markdown("**Stay past the exciting week**")
            st.write("Both stories are long projects. Your version can live inside school.")

    with st.expander("Read these stories carefully"):
        st.write(
            "Zuckerberg and Musk are extreme outliers with unusual resources. Most strong careers in India "
            "still run through board exams, a Class 11 stream, and a degree. Use the stories to choose a habit "
            "for this month. Use Grade-Level Pathways when you need the actual route. "
            "If a video tells you to leave school because they did, close it and go back to the habit."
        )


def _stream_mentor_reply(model, messages):
    contents = [
        {
            "role": "user" if message["role"] == "user" else "model",
            "parts": [message["content"]],
        }
        for message in messages
    ]
    response = model.generate_content(contents, stream=True)
    for chunk in response:
        try:
            text = chunk.text
        except Exception:
            text = ""
        if text:
            yield text


def render_ai_mentor() -> None:
    st.markdown('<p class="kicker">Guidance you can question</p>', unsafe_allow_html=True)
    st.title("AI Mentor Chat")
    st.markdown(
        '<p class="lede">Ask about exams, skills, and career choices from Class 9 through B.Tech.</p>',
        unsafe_allow_html=True,
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    model = None
    if os.getenv("GEMINI_API_KEY"):
        model = genai.GenerativeModel(
            "gemini-3.5-flash-lite",
            system_instruction=MENTOR_INSTRUCTION,
        )
    else:
        st.info("Add GEMINI_API_KEY to a .env file in this folder, then restart the app.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask about JEE, NEET, skills, or a career choice.")
    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model is None:
            reply = "Set GEMINI_API_KEY in a .env file and restart Careero before asking a question."
            st.markdown(reply)
        else:
            try:
                reply = st.write_stream(_stream_mentor_reply(model, st.session_state.messages))
            except Exception as error:
                reply = f"Gemini could not answer that. {error}"
                st.markdown(reply)
            if not reply:
                reply = "Gemini returned an empty reply. Ask about an exam, a skill, or a career choice."
                st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})


def main() -> None:
    st.session_state.setdefault("nav", NAV[0])
    with st.sidebar:
        st.markdown('<p class="brand">Careero</p>', unsafe_allow_html=True)
        st.caption("Educational and career guidance for students in India, from Class 9 to B.Tech.")
        st.radio("Navigate", NAV, key="nav", label_visibility="collapsed")
        st.divider()
        st.caption("Guidance, not a verdict. Check official exam brochures and talk with a teacher before you commit.")

    page = st.session_state.nav
    {
        "Home/Landing Page": render_home,
        "Grade-Level Pathways": render_pathways,
        "Interest Assessment": render_assessment,
        "Inspiration Stories": render_stories,
        "AI Mentor Chat": render_ai_mentor,
    }[page]()


if __name__ == "__main__":
    main()
