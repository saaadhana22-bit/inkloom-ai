"""
Inkloom AI content engine.

Combines the original rule-based rewriting behaviour with optional local
Ollama generation. Keeps the existing app.py function names and return keys.
Round 3 governance checks remain deterministic and do not require Ollama.
"""
import json
import os
import re
import urllib.error
import urllib.request


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")


def _rule_based_rewrite(
    original_content, personality=None, tone="Friendly", audience="",
    platform="", brand_name="", industry="", brand_description="",
    preferred_words="", avoid_words="", content_type="", purpose="",
    length_choice=""
):
    """Original Inkloom rule-based rewrite retained as a safe fallback."""
    rewritten = (original_content or "").strip()
    explanations = []

    rewritten = re.sub(r"([a-zA-Z])\1{2,}", r"\1\1", rewritten, flags=re.I)
    rewritten = re.sub(r"\bbuyy+\b", "buy", rewritten, flags=re.I)
    rewritten = re.sub(r"\bnoww+\b", "now", rewritten, flags=re.I)

    if isinstance(personality, str):
        personality = [personality]
    personality = personality or []

    if rewritten:
        rewritten = rewritten[0].upper() + rewritten[1:]
        if rewritten.isupper():
            rewritten = rewritten.capitalize()
        explanations.append("Improved capitalisation for readability.")

    rewritten = re.sub(r"\s+", " ", rewritten).strip()

    if re.search(r"[!?]{2,}", rewritten):
        rewritten = re.sub(r"[!?]{2,}", ".", rewritten)
        explanations.append("Reduced excessive punctuation.")

    replacements = {
        "buy now": "explore our product",
        "hurry up": "discover it today",
        "best product ever": "a product designed with you in mind",
        "don't miss out": "find out more",
        "limited time offer": "special offer",
        "amazing deal": "special opportunity",
    }
    for old, new in replacements.items():
        pattern = re.compile(re.escape(old), re.I)
        if pattern.search(rewritten):
            rewritten = pattern.sub(new, rewritten)
            explanations.append(f"Replaced '{old}' with '{new}'.")

    tone_rules = {
        "Professional": {"gonna": "going to", "wanna": "want to",
                         "awesome": "excellent", "super cool": "highly useful"},
        "Formal": {"gonna": "going to", "wanna": "wish to",
                   "hey": "hello", "cool": "excellent"},
        "Friendly": {"purchase": "get", "utilise": "use", "assistance": "help"},
        "Inspirational": {"can't": "can", "impossible": "challenging",
                          "failure": "learning experience"},
    }
    if tone in tone_rules:
        for old, new in tone_rules[tone].items():
            rewritten = re.sub(r"\b" + re.escape(old) + r"\b",
                               new, rewritten, flags=re.I)
        explanations.append(f"Adapted vocabulary for a {tone.lower()} tone.")

    personality_rules = {
        "Friendly": "friendly and approachable",
        "Professional": "professional and credible",
        "Creative": "creative and expressive",
        "Bold": "confident and direct",
        "Minimalist": "simple and concise",
        "Trustworthy": "clear and reliable",
        "Innovative": "forward-thinking",
    }
    selected = [personality_rules[p] for p in personality if p in personality_rules]
    if selected:
        explanations.append("Applied brand personality direction: " + ", ".join(selected) + ".")

    preferred = [w.strip() for w in (preferred_words or "").split(",") if w.strip()]
    if preferred:
        explanations.append("Brand vocabulary preferences were considered: " + ", ".join(preferred) + ".")

    avoided = [w.strip() for w in (avoid_words or "").split(",") if w.strip()]
    for word in avoided:
        if re.search(re.escape(word), rewritten, re.I):
            rewritten = re.sub(re.escape(word), "", rewritten, flags=re.I)
            explanations.append(f"Removed the restricted word or phrase '{word}'.")

    platform_guidance = {
        "Instagram": "Prepared for short, engaging social communication.",
        "LinkedIn": "Prepared for professional communication.",
        "Website": "Prepared for clear website communication.",
        "Email": "Prepared for direct email communication.",
        "Facebook": "Prepared for conversational social communication.",
    }
    if platform in platform_guidance:
        explanations.append(platform_guidance[platform])
    if brand_name:
        explanations.append(f"Brand: {brand_name}.")
    if industry:
        explanations.append(f"Industry context: {industry}.")
    if brand_description:
        explanations.append("Brand description considered.")
    if audience:
        explanations.append(f"Target audience: {audience}.")
    if content_type:
        explanations.append(f"Content type: {content_type}.")
    if purpose:
        explanations.append(f"Communication purpose: {purpose}.")
    if length_choice:
        explanations.append(f"Requested content length: {length_choice}.")

    return {"rewritten_content": rewritten, "explanations": explanations}


def _ollama_generate(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2, "top_p": 0.8},
    }
    request = urllib.request.Request(
        OLLAMA_URL.rstrip("/") + "/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))
        answer = (result.get("response") or "").strip()
        if not answer:
            raise RuntimeError("Ollama returned an empty response.")
        return answer
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(
            "Cannot reach Ollama. Keep Ollama running on this computer."
        ) from exc


def _parse_json(text):
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.I)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.S)
        if not match:
            raise RuntimeError("Local model returned invalid JSON.")
        return json.loads(match.group(0))


def rewrite_content(
    original_content,
    personality=None,
    tone="Friendly",
    audience="Not specified",
    platform="Other",
    brand_name="",
    industry="",
    brand_description="",
    preferred_words="",
    avoid_words="",
    content_type="",
    purpose="",
    length_choice="",
    **kwargs
):
    """
    Main rewrite function. Uses Ollama when available; falls back to the
    original rule-based engine if Ollama is unavailable or returns bad output.
    """
    original = (original_content or "").strip()
    if not original:
        return {
            "main": "", "friendly": "", "professional": "", "creative": "",
            "rewritten_content": "", "explanations": ["Please enter content to rewrite."]
        }

    fallback = _rule_based_rewrite(
        original, personality, tone, audience, platform, brand_name, industry,
        brand_description, preferred_words, avoid_words, content_type,
        purpose, length_choice
    )

    personality_text = (
        ", ".join(map(str, personality))
        if isinstance(personality, (list, tuple, set))
        else str(personality or "Not specified")
    )
    prompt = f"""
You are Inkloom AI, a careful brand copy editor. Return ONLY valid JSON.
Brand: {brand_name or "Not specified"}
Industry: {industry or "Not specified"}
Brand description: {brand_description or "Not specified"}
Brand personality: {personality_text}
Requested tone: {tone}
Audience: {audience}
Platform: {platform}
Content type: {content_type}
Purpose: {purpose}
Length preference: {length_choice}
Preferred words: {preferred_words or "None"}
Words/phrases to avoid: {avoid_words or "None"}

FACT PRESERVATION IS ESSENTIAL:
- Do not invent offers, discounts, deadlines, scarcity, popularity, reviews,
  ingredients, product benefits, results, statistics or guarantees.
- Do not add a claim that is not in the source or supplied brand description.
- Do not add urgency or a new call to action unless present in the source.
- Preserve the original meaning and language.
- Improve clarity, natural flow and requested tone without generic filler.
- If the source contains a questionable claim, retain it cautiously and flag
  it in explanations for human verification.
- Avoid the restricted words/phrases where possible.

Return exactly:
{{"main":"best version matching requested tone",
"friendly":"friendly version",
"professional":"professional version",
"creative":"creative but factually faithful version",
"explanations":["short explanation"]}}

SOURCE CONTENT:
{original}
"""
    try:
        data = _parse_json(_ollama_generate(prompt))
        main = str(data.get("main") or "").strip()
        if not main:
            raise RuntimeError("Model did not provide a main rewrite.")
        friendly = str(data.get("friendly") or main).strip()
        professional = str(data.get("professional") or main).strip()
        creative = str(data.get("creative") or main).strip()
        explanations = data.get("explanations") or []
        if not isinstance(explanations, list):
            explanations = [str(explanations)]
        explanations = [str(item) for item in explanations if str(item).strip()]
        return {
            "main": main,
            "friendly": friendly,
            "professional": professional,
            "creative": creative,
            "rewritten_content": main,
            "explanations": explanations or ["Rewritten locally using Ollama with factual-preservation instructions."],
        }
    except Exception as error:
        # Preserve app availability if the local model is unavailable.
        fallback["main"] = fallback["rewritten_content"]
        fallback["friendly"] = fallback["rewritten_content"]
        fallback["professional"] = fallback["rewritten_content"]
        fallback["creative"] = fallback["rewritten_content"]
        fallback["explanations"].append(
            f"Local AI was unavailable or returned an invalid result; the original rule-based rewrite was used instead. Details: {error}"
        )
        return fallback


# Round 3 governance helpers — intentionally local and deterministic.
CTA_PATTERN = re.compile(
    r"\b(try|explore|visit|learn|shop|contact|follow|comment|share|discover|"
    r"join|buy|book|sign\s*up|get started|download|order|register|subscribe|"
    r"apply|message|dm|click)\b", re.I
)


def detect_content_issues(original_text, avoid_words=""):
    text = original_text or ""
    issues = []
    for word in [w.strip() for w in (avoid_words or "").split(",") if w.strip()]:
        if re.search(re.escape(word), text, re.I):
            issues.append({"type": "Avoided vocabulary",
                           "description": f"Brand-restricted word detected: '{word}'."})
    if text.count("!") > 2:
        issues.append({"type": "Excessive punctuation",
                       "description": "The draft contains more than two exclamation marks."})
    for sentence in re.split(r"[.!?]+", text):
        if len(sentence.split()) > 30:
            issues.append({"type": "Long sentence",
                           "description": "A sentence contains more than 30 words."})
            break
    if not CTA_PATTERN.search(text):
        issues.append({"type": "Missing call to action",
                       "description": "No common call-to-action phrase was detected."})
    if len(text.split()) < 8:
        issues.append({"type": "Limited content",
                       "description": "The draft contains fewer than eight words."})
    return issues


def check_brand_references(content, facts):
    text = (content or "").lower()
    results = []
    for fact in facts or []:
        approved = (fact.get("fact_text") or "").strip()
        if not approved:
            continue
        matched = approved.lower() in text
        results.append({
            "fact": approved,
            "status": "Matched" if matched else "Not found",
            "message": (
                "The approved reference appears in the draft."
                if matched else
                "The approved reference was not found verbatim. This does not prove a contradiction; verify manually."
            ),
        })
    return results
