import {
  Utensils,
  Bus,
  ShoppingBag,
  Gamepad2,
  HeartPulse,
  Lightbulb,
  GraduationCap,
  CircleEllipsis,
} from "lucide-react";

const CATEGORY_META = {
  Food:          { icon: Utensils,       color: "#f97316", bg: "rgba(249,115,22,0.10)" },
  Transport:     { icon: Bus,            color: "#3b82f6", bg: "rgba(59,130,246,0.10)" },
  Shopping:      { icon: ShoppingBag,    color: "#ec4899", bg: "rgba(236,72,153,0.10)" },
  Entertainment: { icon: Gamepad2,       color: "#a855f7", bg: "rgba(168,85,247,0.10)" },
  Health:        { icon: HeartPulse,     color: "#34d399", bg: "rgba(52,211,153,0.10)" },
  Utilities:     { icon: Lightbulb,      color: "#fbbf24", bg: "rgba(251,191,36,0.10)" },
  Education:     { icon: GraduationCap,  color: "#38bdf8", bg: "rgba(56,189,248,0.10)" },
  Other:         { icon: CircleEllipsis, color: "#6b7280", bg: "rgba(107,114,128,0.10)" },
};

export function getCategoryMeta(category) {
  return CATEGORY_META[category] || CATEGORY_META.Other;
}
