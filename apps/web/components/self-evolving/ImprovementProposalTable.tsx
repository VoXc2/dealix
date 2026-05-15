type ProposalRow = {
  proposalId: string;
  state: string;
  approvedBy: string;
};

export function ImprovementProposalTable({ proposals }: { proposals: ProposalRow[] }) {
  return (
    <div className="card">
      <h2>Improvement Proposals</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th align="left">Proposal</th>
            <th align="left">State</th>
            <th align="left">Approved By</th>
          </tr>
        </thead>
        <tbody>
          {proposals.map((proposal) => (
            <tr key={proposal.proposalId}>
              <td>{proposal.proposalId}</td>
              <td>{proposal.state}</td>
              <td>{proposal.approvedBy || "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
