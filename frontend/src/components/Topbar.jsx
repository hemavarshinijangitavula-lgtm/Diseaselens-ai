import { Bell, Search, RefreshCw } from 'lucide-react'
export default function Topbar({ page, onRefresh }) {
 return <header className="topbar"><div><div className="eyebrow">DISASTER MANAGEMENT / {page.toUpperCase()}</div><h1>{page==='Overview'?'Disaster Intelligence Center':page}</h1><p className="top-sub">Environmental monitoring, risk analysis and response coordination</p></div><div className="top-actions"><div className="live-pill"><span className="online-dot"/> LIVE SYSTEM</div><button className="icon-btn" title="Alerts"><Bell size={18}/></button><button className="refresh-btn" onClick={onRefresh}><RefreshCw size={16}/> Refresh</button></div></header>
}
