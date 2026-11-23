export default function StatCard({ title, value, unit='', note='', icon: Icon, tone='blue' }) {
 return <div className="stat-card"><div className="stat-head"><span>{title}</span><div className={`stat-icon ${tone}`}>{Icon && <Icon size={18}/>}</div></div><div className="stat-value">{value}<small>{unit}</small></div><div className="stat-note">{note}</div></div>
}
