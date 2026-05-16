# Docker Runtime Baseline

هذا المسار يوثق صورة التشغيل القياسية (local + CI + staging).

## Controls

- pinned base images
- non-root runtime where possible
- deterministic startup commands
- health checks لكل خدمة
