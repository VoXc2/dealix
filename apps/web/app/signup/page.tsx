import { permanentRedirect } from "next/navigation";

export default function RetiredPublicSignupPage() {
  permanentRedirect("/book");
}
