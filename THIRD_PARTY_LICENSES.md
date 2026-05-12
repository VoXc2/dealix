# Third-Party Licenses

Dealix is distributed under the [MIT License](./LICENSE) and incorporates the
following third-party open-source dependencies. Each is governed by its own
license, which is reproduced via the corresponding project upstream.

Generated from `requirements.txt`. For exhaustive transitive dependencies run
`pip-licenses --format=markdown` against a fresh install.

## Runtime dependencies

| Package | License | Upstream |
| --- | --- | --- |
| fastapi | MIT | https://github.com/fastapi/fastapi |
| uvicorn | BSD-3-Clause | https://github.com/encode/uvicorn |
| pydantic | MIT | https://github.com/pydantic/pydantic |
| pydantic-settings | MIT | https://github.com/pydantic/pydantic-settings |
| httpx | BSD-3-Clause | https://github.com/encode/httpx |
| aiohttp | Apache-2.0 | https://github.com/aio-libs/aiohttp |
| tenacity | Apache-2.0 | https://github.com/jd/tenacity |
| anthropic | MIT | https://github.com/anthropics/anthropic-sdk-python |
| openai | Apache-2.0 | https://github.com/openai/openai-python |
| google-generativeai | Apache-2.0 | https://github.com/google-gemini/generative-ai-python |
| sqlalchemy | MIT | https://github.com/sqlalchemy/sqlalchemy |
| asyncpg | Apache-2.0 | https://github.com/MagicStack/asyncpg |
| alembic | MIT | https://github.com/sqlalchemy/alembic |
| redis | MIT | https://github.com/redis/redis-py |
| motor | Apache-2.0 | https://github.com/mongodb/motor |
| typer | MIT | https://github.com/tiangolo/typer |
| rich | MIT | https://github.com/Textualize/rich |
| click | BSD-3-Clause | https://github.com/pallets/click |
| python-dotenv | BSD-3-Clause | https://github.com/theskumar/python-dotenv |
| python-multipart | Apache-2.0 | https://github.com/Kludex/python-multipart |
| email-validator | CC0-1.0 | https://github.com/JoshData/python-email-validator |
| dnspython | ISC | https://github.com/rthalley/dnspython |
| phonenumbers | Apache-2.0 | https://github.com/daviddrysdale/python-phonenumbers |
| python-dateutil | Apache-2.0 / BSD-3-Clause | https://github.com/dateutil/dateutil |
| structlog | Apache-2.0 / MIT | https://github.com/hynek/structlog |
| langfuse | MIT | https://github.com/langfuse/langfuse-python |
| hubspot-api-client | Apache-2.0 | https://github.com/HubSpot/hubspot-api-python |
| google-api-python-client | Apache-2.0 | https://github.com/googleapis/google-api-python-client |
| google-auth-httplib2 | Apache-2.0 | https://github.com/googleapis/google-auth-library-python-httplib2 |
| google-auth-oauthlib | Apache-2.0 | https://github.com/googleapis/google-auth-library-python-oauthlib |
| resend | MIT | https://github.com/resend/resend-python |
| slowapi | MIT | https://github.com/laurents/slowapi |
| opentelemetry-api / sdk / exporter / instrumentation-* | Apache-2.0 | https://github.com/open-telemetry/opentelemetry-python |
| sentry-sdk | MIT | https://github.com/getsentry/sentry-python |
| tzdata | Apache-2.0 | https://github.com/python/tzdata |
| pyyaml | MIT | https://github.com/yaml/pyyaml |
| python-jose | MIT | https://github.com/mpdavis/python-jose |
| passlib | BSD-2-Clause | https://foss.heptapod.net/python-libs/passlib |
| pyotp | MIT | https://github.com/pyauth/pyotp |
| qrcode | BSD-3-Clause | https://github.com/lincolnloop/python-qrcode |
| arq | MIT | https://github.com/python-arq/arq |
| numpy | BSD-3-Clause | https://github.com/numpy/numpy |
| ummalqura | MIT | https://github.com/tytkal/python-hijiri-ummalqura |

## Notes

- Transitive dependencies are not enumerated here — they inherit the licenses
  published by their respective projects.
- If you discover a missing or mis-attributed entry, please open a security
  advisory or contact `security@ai-company.sa`.
- This file is informational. Authoritative license text lives upstream; we
  do not re-distribute modified copies of any dependency.
