
import re


def rewrite_content(
    original_content,
    personality,
    tone,
    audience,
    platform,
    brand_name="",
    industry="",
    brand_description="",
    preferred_words="",
    avoid_words="",
    content_type="",
    purpose="",
    length_choice=""
):
    text = re.sub(r"\s+", " ", (original_content or "")).strip()
    explanations = []

    if not text:
        return {
            "rewritten_content": "",
            "explanations": ["No content was provided."]
        }

    # 1. Normalize input
    text = re.sub(r"([a-zA-Z])\1{2,}", r"\1\1", text)
    text = re.sub(r"[!?]{2,}", ".", text)

    if isinstance(personality, str):
        personality = [personality]

    personality = personality or []

    # 2. Product launch rewriting
    launch_pattern = (
        r"\b(?:we have|we've) launched "
        r"(?:our )?(?:new )?collection\b"
    )

    launch_styles = {
        "Friendly": "Great news — our new collection is here",
        "Professional": "Introducing our latest collection",
        "Formal": "We are pleased to present our latest collection",
        "Bold": "It's here — discover our new collection",
        "Inspirational": "A fresh new collection has arrived",
        "Creative": "A new chapter in style begins today",
        "Minimalist": "Our new collection has arrived"
    }

    if re.search(launch_pattern, text, re.IGNORECASE):
        selected_style = launch_styles.get(tone)

        if not selected_style:
            selected_style = (
                launch_styles["Creative"]
                if "Creative" in personality
                else launch_styles["Friendly"]
            )

        text = re.sub(
            launch_pattern,
            selected_style,
            text,
            count=1,
            flags=re.IGNORECASE
        )

        explanations.append(
            "Reworked the product-launch opening."
        )

    # 3. Promotional phrase improvements
    phrase_rules = {
        r"\bhey everyone[!,.]?\s*": "",
        r"\bcome and explore\b": "discover",
        r"\bcheck it out\b": "take a closer look",

        r"\bcome and explore\b": "discover",
        r"\bcheck it out\b": "take a closer look",
        r"\bbuy now\b": "explore the collection",
        r"\bhurry up\b": "discover it today",
        r"\bdon't miss out on\b": "explore",
        r"\bdon't miss out\b": "find out more",
        r"\bbest product ever\b": "a product designed with you in mind",
        r"\blimited time offer\b": "special offer",
        r"\bamazing deal\b": "special opportunity",
        r"\bshop now\b": "explore our collection"
    }

    for pattern, replacement in phrase_rules.items():
        updated = re.sub(
            pattern,
            replacement,
            text,
            flags=re.IGNORECASE
        )

        if updated != text:
            text = updated
            explanations.append("Improved promotional wording.")

    # 4. Tone-specific vocabulary
    tone_rules = {
        "Friendly": {
            "purchase": "get",
            "utilise": "use",
            "assistance": "help",
            "discover": "come explore"
        },
        "Professional": {
            "gonna": "going to",
            "wanna": "want to",
            "awesome": "excellent",
            "discover": "explore"
        },
        "Formal": {
            "gonna": "going to",
            "wanna": "wish to",
            "hey": "hello",
            "cool": "excellent",
            "discover": "explore"
        },
        "Bold": {
            "discover": "experience",
            "maybe": "now is the time to",
            "try": "experience"
        },
        "Inspirational": {
            "impossible": "challenging",
            "failure": "learning experience",
            "discover": "find inspiration in"
        },
        "Creative": {
            "discover": "step into"
        },
        "Minimalist": {
            "purchase": "buy",
            "in order to": "to"
        }
    }

    rules = tone_rules.get(tone, {})

    for old, new in rules.items():
        text = re.sub(
            r"\b" + re.escape(old) + r"\b",
            new,
            text,
            flags=re.IGNORECASE
        )

    if rules:
        explanations.append(
            f"Applied {tone.lower()} tone adjustments."
        )

    # 5. Personality direction
    personality_notes = {
        "Friendly": "approachable and conversational",
        "Professional": "credible and polished",
        "Creative": "expressive and imaginative",
        "Bold": "confident and direct",
        "Minimalist": "simple and concise",
        "Trustworthy": "clear and reassuring",
        "Innovative": "modern and forward-thinking"
    }

    active_personalities = [
        personality_notes[p]
        for p in personality
        if p in personality_notes
    ]

    if active_personalities:
        explanations.append(
            "Applied brand personality: "
            + ", ".join(active_personalities) + "."
        )

    # 6. Platform-specific finishing
    if platform == "Instagram":
        explanations.append(
            "Prepared the wording for Instagram."
        )

    elif platform == "LinkedIn":
        explanations.append(
            "Prepared polished professional communication for LinkedIn."
        )

    elif platform == "Email":
        explanations.append(
            "Prepared concise wording suitable for email."
        )

    elif platform == "Website":
        explanations.append(
            "Prepared clear website-friendly communication."
        )

    elif platform == "Facebook":
        explanations.append(
            "Prepared conversational social media communication."
        )

    # 7. Preferred vocabulary
    preferred = [
        word.strip()
        for word in (preferred_words or "").split(",")
        if word.strip()
    ]

    if preferred:
        explanations.append(
            "Brand vocabulary preferences supplied: "
            + ", ".join(preferred) + "."
        )

    # 8. Restricted vocabulary
    avoided = [
        word.strip()
        for word in (avoid_words or "").split(",")
        if word.strip()
    ]

    for word in avoided:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        text = pattern.sub("", text)

    # 9. Clean spacing and punctuation
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.!?])", r"\1", text)
    text = re.sub(r"([,.!?])([A-Za-z])", r"\1 \2", text)
    text = text.strip()

    # 10. Capitalisation
    if text:
        text = text[0].upper() + text[1:]

        text = re.sub(
            r"([.!?]\s+)([a-z])",
            lambda match: match.group(1) + match.group(2).upper(),
            text
        )

    # 11. Context explanations
    if brand_name:
        explanations.append(f"Brand: {brand_name}.")

    if industry:
        explanations.append(f"Industry: {industry}.")

    if audience:
        explanations.append(f"Target audience: {audience}.")

    if content_type:
        explanations.append(f"Content type: {content_type}.")

    if purpose:
        explanations.append(f"Communication purpose: {purpose}.")

    if length_choice:
        explanations.append(f"Requested length: {length_choice}.")

    if brand_description:
        explanations.append("Brand description supplied.")

    return {
        "rewritten_content": text,
        "explanations": explanations
    }
