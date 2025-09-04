from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
import json, re, os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "employees.json"

app = FastAPI(title="HR Resource Chatbot - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    DB = json.load(f)["employees"]

class ChatRequest(BaseModel):
    query: str
    top_k: int = 5

def parse_hints(q: str) -> Dict[str, Any]:
    ql = q.lower()
    hints = {"skills": set(), "min_exp": None, "domain": None, "availability": None}
    # experience like 3+ years or 4 years
    m = re.search(r"(\d+)\+?\s*(years|yrs|year)", ql)
    if m:
        hints["min_exp"] = int(m.group(1))
    # skills heuristic: split words and match against skills in DB
    tokens = re.findall(r"[a-zA-Z+#]+", ql)
    # collect known skills from DB
    known_skills = set()
    for e in DB:
        for s in e.get('skills', []):
            known_skills.add(s.lower())
    for t in tokens:
        if t in known_skills:
            hints["skills"].add(t)
    # domain keywords
    domains = ['healthcare','fintech','e-commerce','edtech','retail','logistics','ai','cv','nlp','ml']
    for d in domains:
        if d in ql:
            hints['domain'] = d
            break
    if 'available' in ql:
        hints['availability'] = 'available'
    if 'busy' in ql:
        hints['availability'] = 'busy'
    if 'notice' in ql:
        hints['availability'] = 'notice'
    return hints

def score_employee(e: dict, hints: dict, query: str) -> float:
    score = 0.0
    ql = query.lower()
    # skill overlap
    skills = {s.lower() for s in e.get('skills', [])}
    overlap = len(skills.intersection(hints.get('skills', set())))
    score += overlap * 1.0
    # project/domain match
    if hints.get('domain'):
        for p in e.get('projects', []):
            if hints['domain'] in p.lower():
                score += 1.2
    # experience
    if hints.get('min_exp') is not None and e.get('experience_years', 0) >= hints['min_exp']:
        score += 0.8
    # availability
    if hints.get('availability') and e.get('availability','').lower()==hints['availability']:
        score += 0.5
    # fuzzy match on query words
    for field in ['name'] + e.get('skills',[]) + e.get('projects',[]):
        if isinstance(field,str) and field.lower() in ql:
            score += 0.1
    return score

@app.get('/health')
def health():
    return {'status':'ok'}

@app.get('/employees/search')
def search_employees(skill: Optional[List[str]] = Query(default=None), min_experience: Optional[int] = Query(default=None), availability: Optional[str] = Query(default=None)):
    results = DB
    if skill:
        skill_lower = {s.lower() for s in skill}
        results = [e for e in results if skill_lower.issubset({sk.lower() for sk in e.get('skills',[])})]
    if min_experience is not None:
        results = [e for e in results if e.get('experience_years',0) >= min_experience]
    if availability:
        results = [e for e in results if e.get('availability','').lower() == availability.lower()]
    return results

@app.post('/chat')
def chat(req: ChatRequest):
    hints = parse_hints(req.query)
    scored = []
    for e in DB:
        s = score_employee(e, hints, req.query)
        if s>0:
            scored.append((s,e))
    # if no scored by heuristics, fallback to keyword presence
    if not scored:
        for e in DB:
            s = 0
            ql = req.query.lower()
            # simple keyword count
            for word in set(re.findall(r"[a-zA-Z+#]+", ql)):
                if any(word in str(v).lower() for v in e.get('skills',[]) + e.get('projects',[]) + [e.get('name','')]):
                    s += 0.5
            if s>0:
                scored.append((s,e))
    scored.sort(key=lambda x: -x[0])
    top = [dict(item[1], match_score=round(float(item[0]),3)) for item in scored[:req.top_k]]
    # Construct a friendly answer
    if not top:
        answer = f"I couldn't find a strong match for: '{req.query}'. Try adding specific skills or min experience."
    else:
        lines = [f"Based on your query: '{req.query}', here are the top {len(top)} candidates:"]
        for i,c in enumerate(top, start=1):
            lines.append(f"{i}. {c['name']} · {c['experience_years']} yrs · {c['availability']}\n   Skills: {', '.join(c.get('skills',[]))} \n   Projects: {', '.join(c.get('projects',[]))} \n   Match score: {c['match_score']}")
        lines.append("\nWould you like me to check availability or schedule introductions?")
        answer = "\n".join(lines)
    return {'query': req.query, 'candidates': top, 'answer': answer}
