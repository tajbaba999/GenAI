# RAG Evaluation

RAG Evaluation means measuring whether a RAG system:

1. Retrieves the right information
2. Uses that information correctly
3. Gives a relevant and correct answer

---

## 1. RAG Pipeline

```text
User Query
    ↓
Retriever
    ↓
Retrieved Context
    ↓
LLM
    ↓
Final Answer
```

RAG evaluation is mainly divided into:

```text
              RAG Evaluation
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
      Retrieval            Generation
          │                   │
          ↓                   ↓
   Context Metrics       Answer Metrics
```

---

# 2. Traditional NLP Evaluation

These metrics are older and mainly compare the **generated answer with a reference/ground-truth answer**.

### BLEU

Measures **n-gram/word overlap** between generated and reference text.

Mostly used in:

* Machine Translation
* Text generation

```text
Generated Answer
       ↕
Reference Answer
       ↓
     BLEU
```

### ROUGE

Measures overlap between generated and reference text.

Mostly used in:

* Summarization
* Text generation

Common types:

```text
ROUGE-1
ROUGE-2
ROUGE-L
```

### Precision / Recall / F1

Basic classification/information retrieval metrics.

```text
Precision → How much retrieved/generated information is relevant?

Recall → How much of the relevant information was retrieved?

F1 → Balance between Precision and Recall
```

These metrics are useful, but they don't fully explain **why a RAG system is failing**.

---

# 3. Modern RAG Evaluation

Modern RAG evaluation evaluates the **retrieval + generation process**.

The main metrics to remember:

```text
Retrieval
├── Context Precision
├── Context Recall
└── Context Relevancy

Generation
├── Faithfulness
├── Answer Relevancy
└── Answer Correctness
```

---

# 4. Context Precision

### Question it answers:

> Did the retriever rank the relevant chunks highly?

Example:

```text
Query:
"What is AWS Lambda?"

Retrieved:

1. AWS Lambda is a serverless service.     ✓
2. AWS EC2 provides virtual machines.      ✗
3. Lambda executes code without servers.   ✓
4. Amazon S3 is object storage.            ✗
```

Context Precision checks the **quality/order of retrieved chunks**.

### Low Context Precision

```text
Relevant chunks are buried below
many irrelevant chunks.
```

### If low, investigate:

```text
Chunking
Embedding model
Top-K
Retriever
Reranker
```

---

# 5. Context Recall

### Question it answers:

> Did the retriever retrieve enough information to answer the question?

Example:

```text
Required information:

A
B
C

Retrieved:

A
B
```

The retriever missed `C`.

Therefore:

```text
Context Recall → Low
```

### If low, investigate:

```text
Chunk size
Chunk overlap
Embedding model
Top-K
Retriever
Query transformation
```

---

# 6. Context Relevancy

### Question it answers:

> How relevant is the retrieved context to the question?

```text
Question
   ↓
Retrieved Context
   ↓
Is this context actually useful?
```

If the retriever returns lots of unrelated information:

```text
Context Relevancy → Low
```

---

# 7. Faithfulness

### Question it answers:

> Is the answer supported by the retrieved context?

```text
Retrieved Context:
"Tesla was founded by Martin Eberhard
and Marc Tarpenning."

Answer:
"Tesla was founded by Martin Eberhard
and Marc Tarpenning."

→ High Faithfulness
```

If the model says:

```text
"Tesla was founded by Elon Musk."

→ Low Faithfulness
```

This metric is useful for detecting **hallucination/ungrounded answers**.

---

# 8. Answer Relevancy

### Question it answers:

> Does the answer actually answer the user's question?

```text
Question:
"What is AWS Lambda?"

Good:
"AWS Lambda is a serverless compute service..."

Bad:
"AWS provides EC2, S3, Lambda, DynamoDB..."
```

The second answer contains related information but doesn't directly answer the question.

```text
Answer Relevancy → Low
```

---

# 9. Answer Correctness

### Question it answers:

> Is the final answer actually correct?

This usually requires a **reference/ground-truth answer**.

```text
Question
   ↓
Generated Answer
   ↓
Compare with
   ↓
Ground Truth
```

---

# 10. Important Difference

Remember these two:

```text
Faithfulness
    ↓
Is the answer supported by the retrieved context?

Answer Correctness
    ↓
Is the answer actually correct?
```

They are not the same.

A model can produce an answer that is:

```text
Faithful to the context
        +
Actually incorrect
```

if the retrieved context itself is wrong.

---

# 11. RAG Evaluation in System Design

When designing a RAG system, don't put evaluation only at the end.

Think of it as an **evaluation layer** around the RAG pipeline.

```text
                    User Query
                         │
                         ▼
                    ┌─────────┐
                    │Retriever│
                    └────┬────┘
                         │
                         ▼
                Retrieved Context
                         │
             ┌───────────┴──────────┐
             │                      │
             ▼                      ▼
     Context Precision       Context Recall
     Context Relevancy
             │
             ▼
            LLM
             │
             ▼
       Generated Answer
             │
       ┌─────┼──────────┐
       ▼     ▼          ▼
 Faithfulness  Answer   Answer
               Relevancy Correctness
```

For production, you can additionally collect:

```text
Latency
Token Usage
Cost
User Feedback
Failure Rate
Retrieval Hit Rate
```

These are **system/production metrics**, not necessarily RAG quality metrics.

---

# 12. Where RAGAS Fits

**RAGAS** is a framework that helps calculate many RAG evaluation metrics.

Conceptually:

```text
Your RAG
   │
   ├── Question
   ├── Retrieved Context
   ├── Generated Answer
   └── Ground Truth (optional)
            │
            ▼
          RAGAS
            │
            ▼
       Evaluation Scores
```

It can evaluate things such as:

```text
Context Precision
Context Recall
Faithfulness
Answer Relevancy
Answer Correctness
```

---

# 13. Where DeepEval Fits

**DeepEval** is a broader LLM evaluation/testing framework.

```text
DeepEval
   │
   ├── RAG Evaluation
   ├── LLM Evaluation
   ├── Agent Evaluation
   ├── Hallucination Detection
   └── Custom Evaluation
```

Simple way to remember:

```text
RAGAS
→ RAG-focused evaluation

DeepEval
→ Broader LLM application evaluation
```

---

# 14. RAG Evaluation Dataset

For evaluation, create test cases:

```text
Question
Ground Truth
Retrieved Context
Generated Answer
```

Example:

```json
{
  "question": "What is AWS Lambda?",
  "ground_truth": "AWS Lambda is a serverless compute service.",
  "contexts": [
    "AWS Lambda is a serverless compute service."
  ],
  "answer": "AWS Lambda allows you to run code without managing servers."
}
```

Run your RAG system against many questions:

```text
100 Questions
      ↓
     RAG
      ↓
Evaluation
      ↓
Metrics
```

---

# 15. How to Read Evaluation Results

Example:

```text
Context Precision     0.92
Context Recall        0.61
Faithfulness          0.94
Answer Relevancy       0.91
```

Interpretation:

```text
Precision → Good
Recall    → Bad
Faithfulness → Good
Relevancy → Good
```

This suggests:

> Your retriever finds relevant chunks, but it is missing some information.

So investigate:

```text
Chunking
Embedding
Top-K
Retriever
Reranker
```

Another example:

```text
Context Precision  → 0.90
Context Recall     → 0.88
Faithfulness       → 0.55
```

Now retrieval is probably okay.

The problem is more likely:

```text
Prompt
LLM
Context handling
Hallucination
```

---

# 16. Quick Reference

| Metric             | Main Question                       | Component   |
| ------------------ | ----------------------------------- | ----------- |
| BLEU               | Does output overlap with reference? | Traditional |
| ROUGE              | Does output overlap with reference? | Traditional |
| F1                 | Precision/Recall balance?           | Traditional |
| Context Precision  | Are relevant chunks ranked well?    | Retrieval   |
| Context Recall     | Did we retrieve enough information? | Retrieval   |
| Context Relevancy  | Is retrieved context useful?        | Retrieval   |
| Faithfulness       | Is answer supported by context?     | Generation  |
| Answer Relevancy   | Does answer answer the question?    | Generation  |
| Answer Correctness | Is answer actually correct?         | Generation  |

---

# 17. The One Diagram to Remember

```text
                         RAG
                          │
              ┌───────────┴───────────┐
              │                       │
         RETRIEVAL                GENERATION
              │                       │
      ┌───────┼────────┐       ┌──────┼─────────┐
      ↓       ↓        ↓       ↓      ↓         ↓
   Context  Context  Context  Faith  Answer   Answer
   Precision Recall  Relevancy fulness Relevancy Correctness
```

### In one sentence:

> **RAG evaluation checks whether you retrieved the right information, whether the LLM used it correctly, and whether the final answer is relevant and correct.**
