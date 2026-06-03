// Single place to configure where site enquiries go. The marketing forms build a
// mailto: link to this address (nothing is sent server-side / automatically).
// TODO(founder): replace with the real inbox before launch.
export const CONTACT_EMAIL = 'hello@dealix.sa'

export function buildMailto(subject: string, body: string): string {
  return `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`
}
