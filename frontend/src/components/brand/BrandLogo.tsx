import Image from "next/image";
import { cn } from "@/lib/utils";

export function BrandLogo({ variant = "full", className, priority }: { variant?: "full" | "mark"; className?: string; priority?: boolean }) {
  const src = variant === "mark" ? "/brand/logo-mark.svg" : "/brand/logo.svg";
  return <Image src={src} alt="Dealix" width={variant === "mark" ? 40 : 160} height={variant === "mark" ? 40 : 48} className={cn(className)} priority={priority} />;
}
