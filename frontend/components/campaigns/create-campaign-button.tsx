"use client";

import { Button } from "@/components/ui/button";

export function CreateCampaignButton() {
  function handleCreate() {
    // Kampagnen-Dialog wird später implementiert.
    console.log("Create campaign");
  }

  return (
    <Button onClick={handleCreate}>
      Neue Kampagne
    </Button>
  );
}
