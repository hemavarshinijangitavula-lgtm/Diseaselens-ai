export default function RiskBadge({level='Low'}) { return <span className={`risk-badge ${String(level).toLowerCase()}`}>{level}</span> }
