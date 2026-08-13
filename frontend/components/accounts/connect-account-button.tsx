"use client";

import { Button } from "@/components/ui/button";

export function ConnectAccountButton() {
  function handleConnect() {
    // OAuth flow wird später über das Backend gestartet.
    console.log("Connect account");
  }

  return (
    <Button onClick={handleConnect}>
      Account verbinden
    </Button>
  );
}
