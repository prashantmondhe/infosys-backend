  import { Button } from "@/components/ui/button";
  import { LucideIcon } from "lucide-react";

  interface Props {
    title: string;
    description: string;
    buttonText?: string;
    buttonIcon?: LucideIcon;
    onButtonClick?: () => void;
  }

  export default function PageHeader({
    title,
    description,
    buttonText,
    buttonIcon: Icon,
    onButtonClick,
  }: Props) {
    return (
      <div className="flex items-center justify-between">

        <div>

          <h1 className="text-3xl font-bold">
            {title}
          </h1>

          <p className="mt-2 text-slate-500">
            {description}
          </p>

        </div>

        {buttonText && (
          <Button
            onClick={onButtonClick}
            className="rounded-xl bg-violet-600 hover:bg-violet-700"
          >
            {Icon && <Icon className="mr-2 h-4 w-4" />}
            {buttonText}
          </Button>
        )}

      </div>
    );
  }