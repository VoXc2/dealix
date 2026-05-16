import { ApprovalDecisionModal } from "../../components/approvals/ApprovalDecisionModal";
import { OversightQueue } from "../../components/approvals/OversightQueue";

const queueItems = [
  {
    ticketId: "apt-100",
    actionType: "whatsapp.send_message",
    requestedBy: "sales_agent",
    state: "pending"
  }
];

export default function ApprovalsPage() {
  return (
    <main className="grid">
      <h1>Approvals</h1>
      <OversightQueue items={queueItems} />
      <ApprovalDecisionModal />
    </main>
  );
}
