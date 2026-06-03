import type { Job } from "@/types/job";

const AVATAR_GRADIENTS = [
  "from-indigo-500 to-purple-500",
  "from-sky-500 to-blue-600",
  "from-emerald-500 to-teal-600",
  "from-orange-500 to-amber-500",
  "from-pink-500 to-rose-500",
  "from-violet-500 to-fuchsia-500",
  "from-cyan-500 to-sky-600",
  "from-lime-500 to-green-600",
];

const EMPLOYMENT_TYPE_LABELS: Record<string, string> = {
  full_time: "Full-time",
  part_time: "Part-time",
  contract: "Contract",
  internship: "Internship",
  other: "Other",
};

export function getInitials(name: string): string {
  const words = name.trim().split(/\s+/).filter(Boolean);
  if (words.length === 0) return "?";
  if (words.length === 1) return words[0].slice(0, 2).toUpperCase();
  return (words[0][0] + words[words.length - 1][0]).toUpperCase();
}

export function getAvatarGradient(seed: string): string {
  let hash = 0;
  for (let i = 0; i < seed.length; i += 1) {
    hash = (hash << 5) - hash + seed.charCodeAt(i);
    hash |= 0;
  }
  const index = Math.abs(hash) % AVATAR_GRADIENTS.length;
  return AVATAR_GRADIENTS[index];
}

export function employmentTypeLabel(type: string): string {
  return EMPLOYMENT_TYPE_LABELS[type] ?? "Other";
}

export function formatPostingDate(value: string | null): string {
  if (!value) return "Date not available";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return "Date not available";
  return parsed.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export function formatRelativeDate(value: string | null): string | null {
  if (!value) return null;
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return null;

  const diffMs = Date.now() - parsed.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays <= 0) return "Today";
  if (diffDays === 1) return "Yesterday";
  if (diffDays < 30) return `${diffDays} days ago`;
  if (diffDays < 365) {
    const months = Math.floor(diffDays / 30);
    return months === 1 ? "1 month ago" : `${months} months ago`;
  }
  const years = Math.floor(diffDays / 365);
  return years === 1 ? "1 year ago" : `${years} years ago`;
}

export function formatLocation(job: Job): string {
  if (job.location.is_remote) {
    return job.location.country
      ? `Remote · ${job.location.country}`
      : "Remote";
  }

  const parts = [
    job.location.city,
    job.location.state,
    job.location.country,
  ].filter(Boolean);

  return parts.join(", ") || "Location not specified";
}

export function countryLabel(country: string): string {
  const normalized = country.trim().toLowerCase();
  if (["usa", "us", "united states"].includes(normalized)) return "USA";
  if (normalized === "canada") return "Canada";
  return country;
}
