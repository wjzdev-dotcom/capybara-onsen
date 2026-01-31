# AI Interaction & Prompt Engineering Log

## Phase 1: Asset Generation (Visuals)
**Goal:** Create a cohesive pixel art style for the game.
**Model:** DALL-E 3 / Midjourney

> **Prompt:** "Generate a flat 2D pixel art sprite sheet containing 4 distinct items on a plain white background... Style: 32-bit retro game style, simple, clean lines, high contrast."

**Outcome:** Successfully generated Player (Capybara), Box (Yuzu), Wall (Stone), and Goal (Hot Spring).
**Refinement:** I had to crop the sprite sheet manually. AI struggled with exact spacing for automatic slicing.

---

## Phase 2: Backend Logic & Model Pivot
**Goal:** Switch from OpenAI to Google Gemini for cost efficiency and ecosystem integration.

> **Prompt:** "I need to refactor my FastAPI backend to use `google-generativeai` instead of `openai`. Please generate a function that returns a Sokoban level in strict JSON format using `response_mime_type`."

**Outcome:** The model successfully generated the code structure, but hallucinated the model version.
**Correction:** The AI suggested `gemini-1.5-flash`, which returned a 404 error. I manually corrected this to `gemini-2.0-flash-exp` (or current active version) after checking Google Cloud documentation.

---

## Phase 3: The Topology Challenge (Where AI Failed)
**Goal:** Generate playable levels with increasing difficulty.

> **Prompt:** "Generate a 10x10 Sokoban level map where 'P' is player, 'B' is box, 'X' is wall. The level must be solvable. Add a 'difficulty' parameter."

**Failure Analysis:**
Despite the prompt explicitly asking for "solvable" levels, the LLM frequently placed boxes in corners (deadlocks) or walled off the player.
* **Observation:** LLMs lack "Spatial Reasoning" and cannot simulate 10 steps ahead to verify solvability.
* **Human Intervention:** I stopped trying to fix this via Prompt Engineering. Instead, I wrote a **BFS (Breadth-First Search) verification algorithm** in Python to reject unsolvable maps before they reach the frontend.

---

## Phase 4: Dynamic NPC Dialogue (The "Soul")
**Goal:** Give the Capybara a personality using AI generation.

> **Prompt:** "Generate a one-line witty or cute quote in English for a Capybara soaking in a hot spring. The tone should be relaxing but slightly funny. Example: 'The water is hot, but my vibe is chill.'"

**Outcome:** This worked perfectly. The AI excels at creative text generation (NLU), unlike spatial logic. This became a key feature for user engagement.
