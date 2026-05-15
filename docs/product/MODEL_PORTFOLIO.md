# Model Portfolio

Dealix uses different models for different tasks.

## Task Types

- classification  
- extraction  
- summarization  
- scoring  
- Arabic executive writing  
- RAG answering  
- compliance checking  
- report generation  

## Selection Criteria

- accuracy  
- Arabic quality  
- cost  
- latency  
- context length  
- data sensitivity  
- reliability  

## Rule

High-risk tasks require stronger model + validation.  
Low-risk repetitive tasks can use cheaper model.

## Model Routing Table

| Task                  | Model Tier       | Validation      |
| --------------------- | ---------------- | --------------- |
| simple classification | low-cost         | schema check    |
| outreach draft        | mid              | claims check    |
| executive report      | high             | QA review       |
| RAG answer            | high + retrieval | citation check  |
| compliance            | high + rules     | hard fail rules |
