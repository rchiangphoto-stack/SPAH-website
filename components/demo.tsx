import MorphingArrowButton from "@/components/ui/morphing-arrow-button";

export default function Demo() {
  return (
    <div className="h-screen w-screen flex items-center justify-center gap-10 p-4">
      <MorphingArrowButton direction="left" />
      <MorphingArrowButton direction="right" />
    </div>
  );
}
