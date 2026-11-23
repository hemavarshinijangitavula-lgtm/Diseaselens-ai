import { useMemo } from 'react'
import { Activity, CloudRain, Flame, MapPinned, Wind, Waves, Users, AlertTriangle } from 'lucide-react'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import StatCard from '../components/StatCard'
import RiskBadge from '../components/RiskBadge'
import MapView from '../components/MapView'
export default function Overview({summary, weather, risk, incidents, shelters, alerts, loading, error}) {
 const current=weather?.current||{}
 const hourly=weather?.hourly||{}
 const rainChart=useMemo(()=>hourly.time?.slice(0,24).map((t,i)=>({hour:t.slice(11,16),rain:hourly.precipitation?.[i]||0}))||[],[weather])
 const riskLevel=risk?.risk?.level||'—'; const score=risk?.risk?.score||0
 return <div className="page-content">
  {error && <div className="error-banner">{error} — API may be offline; some cards will show placeholders.</div>}
  <div className="section-title"><div><h2>Situation overview</h2><p>Current monitoring summary for your configured region</p></div><span className="demo-tag">PROTOTYPE DATA</span></div>
  <div className="stat-grid">
   <StatCard title="Tracked Incidents" value={summary?.incident_count??'—'} note={`${summary?.active_incidents??0} active records`} icon={AlertTriangle} tone="orange"/>
   <StatCard title="Risk Indicator" value={score} unit="/100" note={riskLevel+' · demo score'} icon={Activity} tone="red"/>
   <StatCard title="Shelter Locations" value={summary?.shelter_count??shelters.length} note="Demo shelter records" icon={Users} tone="green"/>
   <StatCard title="Weather Alerts" value={alerts.length} note="Informational prototype alerts" icon={CloudRain} tone="purple"/>
  </div>
  <div className="main-grid two-thirds">
   <section className="panel"><div className="panel-title"><div><h3>Rainfall forecast</h3><p>Next 24 hours · hourly precipitation</p></div><span className="panel-chip">mm</span></div>
    <div className="chart-area"><ResponsiveContainer width="100%" height={265}><AreaChart data={rainChart}><defs><linearGradient id="rainFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#3994f6" stopOpacity={.34}/><stop offset="100%" stopColor="#3994f6" stopOpacity={0}/></linearGradient></defs><CartesianGrid stroke="#233247" strokeDasharray="3 3"/><XAxis dataKey="hour" stroke="#8190a7" tick={{fontSize:11}}/><YAxis stroke="#8190a7" tick={{fontSize:11}}/><Tooltip contentStyle={{background:'#101c2b',border:'1px solid #2c3c50',borderRadius:8}}/><Area type="monotone" dataKey="rain" stroke="#459dff" strokeWidth={2} fill="url(#rainFill)"/></AreaChart></ResponsiveContainer></div>
   </section>
   <section className="panel risk-panel"><div className="panel-title"><div><h3>Weather risk indicator</h3><p>Rule-based prototype</p></div><RiskBadge level={riskLevel}/></div><div className="risk-circle" style={{'--risk':`${score*3.6}deg`}}><div><strong>{score}</strong><span>RISK SCORE</span></div></div><div className="risk-row"><span>Classification</span><RiskBadge level={riskLevel}/></div><div className="risk-row"><span>Current rainfall</span><b>{current.precipitation??'—'} mm</b></div><div className="risk-row"><span>Forecast peak hourly rain</span><b>{risk?.forecast_max_hourly_rain_mm??'—'} mm</b></div><div className="caution">Prototype only. Do not use this score for real emergency decisions.</div></section>
  </div>
  <div className="main-grid two-thirds"><section className="panel map-panel"><div className="panel-title"><div><h3>Geospatial situation map</h3><p>Incident and shelter records</p></div><span className="panel-chip">OpenStreetMap</span></div><MapView incidents={incidents} shelters={shelters} riskScore={score}/></section>
  <section className="panel"><div className="panel-title"><div><h3>Current weather</h3><p>Reference location</p></div><CloudRain size={18} className="muted-icon"/></div><div className="weather-hero"><strong>{current.temperature_2m??'—'}°</strong><span>Temperature</span></div><div className="weather-mini-grid"><div><Wind size={16}/><span>Wind</span><b>{current.wind_speed_10m??'—'} km/h</b></div><div><Waves size={16}/><span>Humidity</span><b>{current.relative_humidity_2m??'—'}%</b></div><div><CloudRain size={16}/><span>Rain</span><b>{current.precipitation??'—'} mm</b></div><div><Flame size={16}/><span>Fire detections</span><b>Not connected</b></div></div></section></div>
  <section className="panel table-panel"><div className="panel-title"><div><h3>Latest incidents</h3><p>Most recent registered reports</p></div></div><div className="table-wrap"><table><thead><tr><th>Incident</th><th>Type</th><th>Severity</th><th>Status</th><th>Location</th></tr></thead><tbody>{incidents.slice(0,5).map(i=><tr key={i.id}><td>{i.title}</td><td>{i.disaster_type}</td><td><RiskBadge level={i.severity}/></td><td>{i.status}</td><td>{i.location}</td></tr>)}{incidents.length===0&&<tr><td colSpan="5" className="empty">No incidents available.</td></tr>}</tbody></table></div></section>
 </div>
}
