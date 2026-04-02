# Automotive RAG System
## Multimodal Retrieval-Augmented Generation for Tata Harrier BS6 Service Manual Intelligence

---

## Problem Statement

### Domain Identification

This project operates within the **automotive and mechanical engineering** domain,
specifically targeting the workflows of service engineers, workshop technicians,
and vehicle owners working with Tata Motors vehicles — particularly the
**Tata Harrier BS6** SUV. These professionals and owners rely on the official
Tata Harrier BS6 Owner's Manual to perform diagnostics, scheduled maintenance,
fault identification, and component-level repairs.

### Problem Description

The Tata Harrier BS6 Owner's Manual is a comprehensive, multimodal document
containing dense procedural text, specification tables, warning diagrams,
component layouts, and maintenance schedules. A service technician or an
informed vehicle owner attempting to resolve a fault or perform maintenance
must manually navigate this document — often across multiple unrelated sections
— to locate the precise information needed.

The core problem is **retrieval inefficiency in a safety-critical environment**.
Consider a technician needing to verify the tyre inflation pressure for the
Harrier BS6 under full load, or a vehicle owner trying to understand what a
specific dashboard warning light means. The answer may exist in a specifications
table in one chapter and cross-referenced by a warning indicator diagram in
another. A keyword search returns too many hits. The table of contents offers
only coarse navigation. Neither approach surfaces the precise, contextually
correct answer quickly.

This problem is compounded by the multimodal nature of the manual. Critical
information is frequently split across modalities — a maintenance procedure
described in text references a component layout diagram for physical location,
and a specification table for tolerance values. Traditional search tools treat
these modalities as disconnected, failing to retrieve the complete answer the
technician or owner actually needs.

### Why This Problem Is Unique

Unlike a generic document Q&A system, the Tata Harrier BS6 Owner's Manual
presents specific challenges that make retrieval non-trivial:

- **Specialized terminology:** Terms like TPMS (Tyre Pressure Monitoring
  System), ESP (Electronic Stability Programme), HVAC controls, BS6 emission
  norms, and Kryotec diesel engine specifications are Harrier-specific and
  context-dependent. A generic search engine has no awareness of these.
- **Precision requirements:** Answers are safety-critical. An incorrect tyre
  pressure value, wrong engine oil grade (e.g. 15W-40 vs 0W-30), or missed
  service interval for the Harrier's Kryotec 2.0L diesel engine can cause
  vehicle damage or void the warranty.
- **Cross-modal dependency:** Questions about dashboard warning indicators
  require image summaries. Fluid specification questions require table
  extraction. Step-by-step tyre change or jack usage procedures require
  sequential text retrieval. No single modality contains the complete answer.
- **Owner accessibility:** Unlike dealership technicians, vehicle owners are
  not trained to navigate dense technical manuals. A natural language interface
  dramatically lowers the barrier to accessing safety-critical information.

### Why RAG Is the Right Approach

Fine-tuning a language model on the Tata Harrier BS6 manual is impractical —
it would require retraining for every new manual edition or variant, cannot
cite the source page, and risks hallucinating safety-critical values such as
torque limits or fluid capacities. Manual keyword search does not scale and
cannot reason across text, tables, and diagrams simultaneously.

Retrieval-Augmented Generation addresses these limitations directly. By
embedding document chunks — text paragraphs, specification tables, and
VLM-generated descriptions of warning diagrams and component layouts — into
a local vector index, the system retrieves only the most relevant chunks for
a given query. The LLM then generates a grounded answer using exclusively
retrieved context, with full source attribution (filename, page number, chunk
type). This ensures every answer is traceable and verifiable against the
official Tata Harrier BS6 Owner's Manual.

### Expected Outcomes

A successful system will enable the following query types against the
Tata Harrier BS6 Owner's Manual:

- **Text retrieval:** "What is the procedure to use the scissor jack safely
  on the Harrier?" → returns step-by-step procedure with page reference.
- **Table retrieval:** "What engine oil grade and capacity is recommended
  for the Kryotec 2.0L diesel engine?" → returns specification table with
  grade, viscosity, and volume data.
- **Image retrieval:** "What does the orange TPMS warning light on the
  dashboard mean?" → returns a VLM-generated description of the warning
  indicator diagram and associated action.

The system reduces manual lookup time from 10–20 minutes to under 30 seconds,
empowers vehicle owners to safely self-diagnose common issues, and provides
a scalable foundation that can be extended to other Tata Motors vehicle manuals.
