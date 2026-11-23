import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
const center=[13.5503,78.5029]
export default function MapView({ incidents=[], shelters=[], riskScore=0 }) {
 return <MapContainer center={center} zoom={7} className="map-view">
   <TileLayer attribution='&copy; OpenStreetMap contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
   <Circle center={center} radius={Math.max(1500,riskScore*250)} pathOptions={{color:riskScore>=75?'#ef4444':riskScore>=50?'#f97316':'#3b82f6',fillOpacity:.12}}/>
   <Marker position={center}><Popup><b>Monitoring reference location</b><br/>Madanapalle area · prototype risk overlay</Popup></Marker>
   {incidents.map(i=><Marker key={`i-${i.id}`} position={[i.latitude,i.longitude]}><Popup><b>{i.title}</b><br/>{i.disaster_type} · {i.severity}<br/>{i.status}</Popup></Marker>)}
   {shelters.map(s=><Marker key={s.id} position={[s.latitude,s.longitude]}><Popup><b>{s.name}</b><br/>Shelter · Available capacity: {s.available}</Popup></Marker>)}
 </MapContainer>
}
