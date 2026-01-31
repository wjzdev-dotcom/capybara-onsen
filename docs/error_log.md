# Engineering Error Log & Reflection

## 1. Environment Configuration Error
**Error:** `-bash: uvicorn: command not found`
**Cause:** The executable was installed in a user-local directory not included in the system `$PATH`.
**Solution:** Used `python3 -m uvicorn` to invoke the module directly.
**Reflection:** This highlighted the importance of understanding Python's execution environment versus relying on global shell aliases in cloud shells.

## 2. API Model Versioning (Temporal Hallucination)
**Error:** `404 models/gemini-1.5-flash is not found`
**Analysis:** The AI assistant provided code using a specific model version assuming it was the current standard. However, LLM training data is static and does not know real-time API depreciation schedules.
**Fix:** Manually investigated the Google Cloud documentation and updated the model version strings.
**Lesson:** Human oversight is essential for maintaining software dependencies that change frequently.

## 3. Quota Limits & Resilience
**Error:** `429 You exceeded your current quota`
**Impact:** Relying solely on the live API would have halted development/demo.
**Solution:** Implemented a **Fallback Mechanism**. The system now wraps API calls in a `try-except` block and serves a locally cached 'Emergency Level' when the AI provider is unavailable.
**Design Choice:** Real-world AI systems must degrade gracefully rather than crashing.

## 4. Deployment Platform Migration
**Challenge:** Google Cloud Platform billing setup latency and credit card requirements.
**Action:** Pivoted deployment from GCP Cloud Run to **Render**.
**Result:** This proved the **portability** of the Dockerized architecture. The system is cloud-agnostic and was successfully deployed to a PaaS provider without code changes, fulfilling the Continuous Delivery (CD) requirement.

## 5. Topological Validity (The "Deadlock" Bug)
**Issue:** AI generated unplayable levels (approx. 40% failure rate).
**Solution:** Implemented a **Formal Verification Layer**.
* **AI:** Handles Creativity (Layout variation, Dialogue).
* **Algorithm:** Handles Correctness (BFS Solver).
**Conclusion:** A hybrid approach (AI + Algorithm) is superior to a pure AI approach for constraint-satisfaction problems like Sokoban.
