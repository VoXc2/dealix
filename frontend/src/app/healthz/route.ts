export const dynamic = 'force-dynamic';

function resolveGitSha(): string {
  const candidates = [
    process.env.NEXT_PUBLIC_GIT_SHA,
    process.env.VERCEL_GIT_COMMIT_SHA,
    process.env.GIT_SHA,
  ];
  for (const candidate of candidates) {
    const sha = candidate?.trim();
    if (sha) return sha;
  }
  return 'unknown';
}

export function GET() {
  return Response.json(
    {
      status: 'ok',
      service: 'dealix-frontend',
      git_sha: resolveGitSha(),
    },
    {
      headers: { 'cache-control': 'no-store' },
    },
  );
}
