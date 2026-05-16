# Orchestration Layer Architecture

Orchestration coordinates:
- workflow sequencing,
- agent invocation order,
- approval pauses/resumes,
- retry and compensation behavior.

This layer binds `workflow_engine`, `governance`, and `execution_engine` at runtime.
