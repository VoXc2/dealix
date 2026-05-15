# QA Checklist

- [ ] citation accuracy: sampled answers point to the correct source document
- [ ] no-source-no-answer test: questions with no supporting document return a refusal, not a guess
- [ ] hallucination test: adversarial prompts do not produce unsourced claims
- [ ] permission test: each role sees only documents it is authorised for
- [ ] confidence scores present on every answer
- [ ] audit record written for every answer (source, role, timestamp)
- [ ] evaluation report passes the agreed quality bar
- [ ] forbidden terms absent from user-facing copy (e.g. guaranteed / نضمن)
- [ ] no external sending or charging path enabled
- [ ] PII handling and access logging documented
- [ ] rollback path documented
