import { LayoutDashboard, Map, CloudSun, Siren, ClipboardList, Tent, ChartNoAxesCombined, ShieldAlert } from 'lucide-react'
const nav = [
  ['Overview', LayoutDashboard], ['Disaster Map', Map], ['Weather', CloudSun], ['Incidents', ClipboardList], ['Alerts', Siren], ['Shelters', Tent], ['Analytics', ChartNoAxesCombined]
]
export default function Sidebar({ page, setPage }) {
  return <aside className="sidebar">
    <div className="brand"><div className="brand-mark"><ShieldAlert size={22}/></div><div><strong>DisasterLens</strong><small>AI INTELLIGENCE</small></div></div>
    <div className="nav-caption">WORKSPACE</div>
    <nav>{nav.map(([label, Icon]) => <button key={label} className={`nav-link ${page===label?'selected':''}`} onClick={()=>setPage(label)}><Icon size={18}/><span>{label}</span></button>)}</nav>
    <div className="sidebar-foot"><div className="online-dot"/> API STATUS <b>CONNECTED</b><p>Student prototype · v1.0</p></div>
  </aside>
}
