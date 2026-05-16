type RoiData = {
  estimated: number;
  measured: number;
};

export function WorkflowROIReport({ roi }: { roi: RoiData }) {
  return (
    <div className="card">
      <h2>Workflow ROI Report</h2>
      <p>Estimated: {roi.estimated.toLocaleString()} SAR</p>
      <p>Measured: {roi.measured.toLocaleString()} SAR</p>
      <p>Delta: {(roi.measured - roi.estimated).toLocaleString()} SAR</p>
    </div>
  );
}
