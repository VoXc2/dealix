"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { fetchAgents } from "@/lib/api/agentMesh";

type AgentRow = {
  agent_id?: string;
  name?: string;
  owner?: string;
  autonomy_level?: number;
  status?: string;
  trust_tier?: string;
};

export function AgentRegistryTable() {
  const [agents, setAgents] = useState<AgentRow[]>([]);

  useEffect(() => {
    fetchAgents()
      .then((payload) => setAgents(Array.isArray(payload?.agents) ? payload.agents : []))
      .catch(() => setAgents([]));
  }, []);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Agent Registry</CardTitle>
      </CardHeader>
      <CardContent>
        {!agents.length ? (
          <p className="text-sm text-muted-foreground">No registered agents found.</p>
        ) : (
          <div className="space-y-2">
            {agents.map((agent, idx) => (
              <div key={`${agent.agent_id || "agent"}-${idx}`} className="rounded border p-3 text-sm">
                <div><strong>agent_id:</strong> {agent.agent_id || "-"}</div>
                <div><strong>name:</strong> {agent.name || "-"}</div>
                <div><strong>owner:</strong> {agent.owner || "-"}</div>
                <div><strong>trust_tier:</strong> {agent.trust_tier || "-"}</div>
                <div><strong>autonomy_level:</strong> {agent.autonomy_level ?? "-"}</div>
                <div><strong>status:</strong> {agent.status || "-"}</div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
