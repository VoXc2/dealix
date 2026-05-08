import { RegisterForm } from "@/components/shared/RegisterForm";

interface RegisterPageProps {
  params: Promise<{ locale: string }>;
}

export default async function RegisterPage({ params }: RegisterPageProps) {
  return <RegisterForm />;
}
