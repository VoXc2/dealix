import { LoginForm } from "@/components/shared/LoginForm";

interface LoginPageProps {
  params: Promise<{ locale: string }>;
}

export default async function LoginPage({ params }: LoginPageProps) {
  return <LoginForm />;
}
