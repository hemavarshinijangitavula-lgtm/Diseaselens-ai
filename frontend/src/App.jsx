import {useCallback,useEffect,useState} from 'react'
import Sidebar from './components/Sidebar'
import Topbar from './components/Topbar'
import Overview from './pages/Overview'
import DisasterMap from './pages/DisasterMap'
import Weather from './pages/Weather'
import Incidents from './pages/Incidents'
import Alerts from './pages/Alerts'
import Shelters from './pages/Shelters'
import Analytics from './pages/Analytics'
import FireHotspots from './pages/FireHotspots'
import {fetchSummary,fetchWeather,fetchRisk,fetchIncidents,fetchShelters,fetchAlerts,fetchHealth} from './services/api'
const pages=['Overview','Disaster Map','Weather','Fire Hotspots','Incidents','Alerts','Shelters','Analytics']
export default function App(){const [page,setPage]=useState('Overview');const [summary,setSummary]=useState(null);const [weather,setWeather]=useState(null);const [risk,setRisk]=useState(null);const [incidents,setIncidents]=useState([]);const [shelters,setShelters]=useState([]);const [alerts,setAlerts]=useState([]);const [loading,setLoading]=useState(true);const [error,setError]=useState('');const [apiStatus,setApiStatus]=useState('unknown')
 const refresh=useCallback(async()=>{setLoading(true);setError('');try{const [s,w,r,i,sh,a,h]=await Promise.all([fetchSummary(),fetchWeather(),fetchRisk(),fetchIncidents(),fetchShelters(),fetchAlerts(),fetchHealth()]);setSummary(s.data);setWeather(w.data);setRisk(r.data);setIncidents(i.data);setShelters(sh.data);setAlerts(a.data);setApiStatus(h.data?.status==='ok'?'connected':'disconnected')}catch(e){setApiStatus('disconnected');setError(e?.response?.data?.detail||e.message||'Backend connection failed. Check FastAPI and refresh.')}finally{setLoading(false)}},[])
 useEffect(()=>{refresh()},[refresh]);
 let body;if(page==='Overview')body=<Overview summary={summary} weather={weather} risk={risk} incidents={incidents} shelters={shelters} alerts={alerts} loading={loading} error={error}/>;else if(page==='Disaster Map')body=<DisasterMap incidents={incidents} shelters={shelters} risk={risk}/>;else if(page==='Weather')body=<Weather weather={weather} risk={risk}/>;else if(page==='Fire Hotspots')body=<FireHotspots/>;else if(page==='Incidents')body=<Incidents incidents={incidents} refresh={refresh}/>;else if(page==='Alerts')body=<Alerts alerts={alerts} risk={risk}/>;else if(page==='Shelters')body=<Shelters shelters={shelters} incidents={incidents} risk={risk}/>;else body=<Analytics incidents={incidents} summary={summary}/>;
 return <div className="app-shell"><Sidebar page={page} setPage={setPage} apiStatus={apiStatus}/><main className="main-area"><Topbar page={page} onRefresh={refresh}/>{loading&&<div className="loading-strip">Refreshing data…</div>}{body}<footer className="footer">DisasterLens AI <span>Student prototype · Data sources and demo records must be independently verified before real-world use.</span></footer></main></div>}
