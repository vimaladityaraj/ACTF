// Independent code path: ECMAScript scalar distances on exchanged JSON records.
import fs from 'node:fs';
const records=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const keys=['S','So','Sa','B','P','A'];
// Inputs are schema-validated by Python; this is not a schema validator.
// Object keys are unordered, but array order (e.g. time windows) is meaningful.
function equalJSON(a, b) {
 if (a === b) return true;
 if (a === null || b === null || typeof a !== 'object' || typeof b !== 'object') return false;
 if (Array.isArray(a) || Array.isArray(b)) {
  return Array.isArray(a) && Array.isArray(b) && a.length === b.length && a.every((v,i) => equalJSON(v,b[i]));
 }
 const keys = Object.keys(a);
 return keys.length === Object.keys(b).length && keys.every(k => Object.hasOwn(b,k) && equalJSON(a[k],b[k]));
}
const rows=[];
for(let i=0;i<records.length;i++)for(let j=i+1;j<records.length;j++){
 const a=records[i],b=records[j];
 if(a.data_kind!==b.data_kind || !equalJSON(a.protocol,b.protocol))throw Error('Incompatible');
 if(a.data_kind!=='synthetic' && (a.protocol.window_s===null || b.protocol.window_s===null))throw Error('Incompatible: unknown window');
 let total=0;
 for(const k of keys){const x=a.coordinates[k],y=b.coordinates[k];if(typeof x!=='number'||typeof y!=='number'||!Number.isFinite(x)||!Number.isFinite(y)||x<0||x>1||y<0||y>1)throw Error('Invalid complete coordinate');total+=(x-y)**2;}
 rows.push({a:a.sample.id,b:b.sample.id,Dn:Math.sqrt(total/6)});
}
console.log(JSON.stringify(rows));
