"use client";

import { useRef } from "react";
import { Button } from "@/components/ui/button";

export function UploadVideoButton() {
  const inputRef = useRef<HTMLInputElement>(null);

  function handleClick() {
    inputRef.current?.click();
  }

  function handleChange(
    event: React.ChangeEvent<HTMLInputElement>,
  ) {
    const files = event.target.files;

    if (!files || files.length === 0) {
      return;
    }

    // Upload wird später über Supabase Storage/API implementiert.
    console.log("Selected files:", files);
  }

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        accept="video/*"
        multiple
        className="hidden"
        onChange={handleChange}
      />

      <Button onClick={handleClick}>
        Videos hochladen
      </Button>
    </>
  );
}
