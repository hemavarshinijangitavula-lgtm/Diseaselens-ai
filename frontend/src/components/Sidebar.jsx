import { LayoutDashboard, Map, CloudSun, Siren, ClipboardList, Tent, ChartNoAxesCombined, ShieldAlert, Flame } from 'lucide-react'
const nav = [
  ['Overview', LayoutDashboard], ['Disaster Map', Map], ['Weather', CloudSun], ['Fire Hotspots', Flame], ['Incidents', ClipboardList], ['Alerts', Siren], ['Shelters', Tent], ['Analytics', ChartNoAxesCombined]
]
export default function Sidebar({ page, setPage, apiStatus = 'unknown' }) {
  return <aside className="sidebar">
    <div className="brand"><div className="brand-mark"><ShieldAlert size={22}/></div><div><strong>DisasterLens</strong><small>AI INTELLIGENCE</small></div></div>
    <div className="nav-caption">WORKSPACE</div>
    <nav>{nav.map(([label, Icon]) => <button key={label} className={`nav-link ${page===label?'selected':''}`} onClick={()=>setPage(label)}><Icon size={18}/><span>{label}</span></button>)}</nav>
    <div className="sidebar-foot"><div className={`online-dot ${apiStatus==='disconnected'?'offline-dot':''}`}/> API STATUS <b className={apiStatus==='disconnected'?'api-offline':''}>{apiStatus.toUpperCase()}</b><p>Student prototype · v1.1</p></div>
  </aside>
}
