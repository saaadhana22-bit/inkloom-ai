# Inkloom AI

### Your brand. Your voice. Every word.

Inkloom AI is a brand-focused content enhancement platform designed to help users create clearer, more consistent and platform-appropriate brand communication.

## 1. The Problem

Brands often struggle to maintain a consistent communication style across different platforms and audiences. Generic content may fail to reflect a brand's identity, personality and communication goals.

## 2. Our Solution

Inkloom AI helps users refine their content according to their brand identity, communication tone, target audience and publishing platform.

It combines a Python-based content rewriting engine with brand-oriented customisation and content quality indicators.

## 3. Key Features

- Brand personality selection
- Customisable communication tones
- Target audience and industry context
- Preferred and restricted vocabulary
- Platform-specific content guidance
- Rule-based content rewriting and enhancement
- Content quality indicators
- Brand consistency guidance
- Recent rewrite history
- Supabase database storage for generated rewrites

## 4. How It Works

1. Enter your brand details.
2. Select your brand personality and communication tone.
3. Specify your target audience and publishing platform.
4. Enter the original content.
5. Analyse and rewrite the content.
6. Review the enhanced output and content insights.
7. Save the generated rewrite to the database.

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Regular Expressions | Text processing and rewriting rules |
| Supabase | Cloud database storage |

## 6. Project Architecture

**User Interface → Python Rewriting Engine → Content Analysis → Supabase Storage**

- Streamlit handles the user interface and interactions.
- The Python engine processes content using predefined linguistic and rewriting rules.
- Content analysis provides quality-related indicators.
- Supabase stores generated rewrite records.

## 7. Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- A Supabase project

### Clone the repository

```bash
git clone https://github.com/saaadhana22-bit/inkloom-ai.git
cd inkloom-ai
```

### Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure Supabase

Create a `.env` file in the project root and configure:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_publishable_key
```

Never commit your `.env` file or expose database credentials in the repository.

Configure the corresponding environment variables in Streamlit Secrets when deploying the application.

### Run the application

```bash
streamlit run app.py
```

Open the local application at:

```text
http://localhost:8501
```

## 8. Database

Inkloom AI uses Supabase to store generated rewrites.

The `rewrite_history` table contains:

- `id`
- `original_text`
- `rewritten_text`
- `tone`
- `created_at`

The application currently supports inserting generated rewrite records. Public anonymous users are not permitted to read stored records through the table.

## 9. Current Implementation and Limitations

Inkloom AI currently uses a rule-based Python content enhancement engine.

It applies predefined phrase transformations, tone-specific vocabulary adjustments, promotional wording improvements and text-cleaning rules.

It does not currently use a generative AI model or an external paid AI API.

The visible recent-work list is maintained during the active Streamlit session. Although generated rewrites are stored in Supabase, cross-session history retrieval and user accounts are not currently implemented.

Because the rewriting engine relies on predefined rules, the quality and variety of transformations depend on the supported language patterns.

## 10. Testing

The application has been manually tested for:

- Successful application startup
- Content rewriting
- Friendly and Professional tone transformations
- Empty-input validation
- Supabase database insertion
- Repeated rewrite submissions
- Database access restrictions

## 11. Future Scope

- Advanced AI-powered content generation
- More personalised brand recommendations
- Expanded platform support
- Improved content analysis
- Enhanced language understanding
- Secure user accounts and personalised rewrite history

## 12. Project Links

- GitHub Repository: https://github.com/saaadhana22-bit/inkloom-ai
- Live Application: https://inkloom-ai-wplakcddekun8mvadi4jji.streamlit.app/

---

**Inkloom AI — Your brand. Your voice. Every word.**