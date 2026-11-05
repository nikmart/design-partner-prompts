# Design partner prompt pack

**Website with copy buttons:** https://nikmartelaro.com/design-partner-prompts/

These prompts make your AI agent work like a design partner. It interviews you about the app you want, sketches layouts with you, writes down what to build, and then builds it. It works the way I approach design projects with clients: understand the work first, sketch early, be honest about what's real, prove the risky parts before building on them, and leave the decisions to you.

## What's in here

| File | What it is |
|---|---|
| `designer.md` | The main prompt. Your agent follows this one. |
| `agents/user-research.md` | A subagent that turns the interview and your images into a short research report. |
| `agents/requirements.md` | A subagent that turns the research into numbered requirements and a build plan (PRD). |
| `agents/builder.md` | A subagent that builds the app with Next.js, shadcn/ui, the Vercel AI SDK and Claude, OpenAI or a local Ollama model. |
| `design-partner-all-in-one.md` | Everything above in one file, for tools that can't read separate files. |
| `build.py` | Rebuilds the all-in-one file and the website after you edit the prompts: `python3 build.py`. |
| `index.html`, `site/` | The website (GitHub Pages). `index.html` is generated from `site/template.html`. |

## How to use it

**With a coding agent that can read files and run code** (Claude Code, Codex, Cursor and similar):
1. Make an empty folder for your app and put this pack in it as `design-partner/`:
   ```bash
   git clone https://github.com/nikmart/design-partner-prompts design-partner
   ```
   Or download the ZIP from GitHub and rename the folder to `design-partner`.
2. Start your agent in that folder and say: *"Read `design-partner/designer.md` and follow it. Let's design an app."*
3. If your agent can use subagents, it will hand research, requirements and building to them. If not, it does those steps itself.

**With a chat assistant** (claude.ai, ChatGPT and similar): paste `design-partner-all-in-one.md` as the first message, or put it in a project's instructions. You'll get the interview, sketches and a finished plan (`prd.md`). Then take the plan and this pack to a coding agent to build it.

**Coming back later:** start your agent in the same folder and say the same thing. It reads `design/` and picks up where you left off.

## What to expect

- **Setup questions first:**
  - how deep to go: Quick (~10 min), Standard (~30 min) or Deep;
  - what you have already;
  - what you want by the end (a plan, a clickable prototype, or a working app).

  If the app ends up with an AI feature, it also asks which provider to use.
- **You can steer at any time.** Say *"faster"*, *"deeper"*, *"show me"*, *"just build it"*, *"go back"* or *"where are we?"*. When you skip ahead, the agent writes down its assumptions so you can check them.
- **Bring pictures.** Hand sketches, screenshots of slides, spreadsheets or the app you use today all help. The agent describes what it sees and asks what to keep.
- **Everything is saved in a `design/` folder:** the brief, interview notes, sketches, research, requirements and PRD. A new session can pick up where you left off.
- **The build starts with a feasibility check,** then grows in small milestones you can click through.
- **It's done when you can run the demo yourself and say yes.** The agent then writes `design/handoff.md`: how to start the app, and what to build next.
- **The agent asks before anything leaves your computer or costs money:** pushing code, deploying, signing up for services, big downloads or paid API use.

## Before you build

- Install Node 22 or later.
- Choose an AI provider:
  - **Anthropic:** set `ANTHROPIC_API_KEY` in the app's `.env.local` (the agent tells you where; usually `web/.env.local`).
  - **OpenAI:** set `OPENAI_API_KEY` in the same file.
  - **Ollama:** install it (ollama.com) for a free local model. Models that can read images and use tools are often 10–20 GB, and your computer needs enough memory to run them.
- Never paste keys into the chat. The agent will tell you where to put them.

The stack details in `agents/builder.md` were current in November 2026. The builder is told to check the current docs, because these libraries change quickly.
