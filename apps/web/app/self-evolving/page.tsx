import { ImprovementProposalTable } from "../../components/self-evolving/ImprovementProposalTable";

const proposals = [
  { proposalId: "prop-001", state: "pending_approval", approvedBy: "" },
  { proposalId: "prop-002", state: "approved", approvedBy: "sami" }
];

export default function SelfEvolvingPage() {
  return (
    <main className="grid">
      <h1>Self-Evolving OS</h1>
      <ImprovementProposalTable proposals={proposals} />
    </main>
  );
}
