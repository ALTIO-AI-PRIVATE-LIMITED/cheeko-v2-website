import {chromium} from './pw.mjs';
import fs from 'node:fs';
const W=JSON.parse(fs.readFileSync('warp.json'));const old=[0,...W.old],real=[0,...W.new];
const map=x=>{let k=0;while(k<old.length-2&&x>old[k+1])k++;return real[k]+(x-old[k])/(old[k+1]-old[k])*(real[k+1]-real[k])};
const starts=[0,2,3.6,5,7,8.4,9.5,11.2,13,14,15,17,18.2,19.5,20.5,21.4,22,24.5];
const b=await(await chromium()).launch();const p=await b.newPage({viewport:{width:1080,height:1920}});let errors=[];p.on('pageerror',e=>errors.push(e.message));
await p.goto('file://'+process.cwd()+'/compose.html',{waitUntil:'networkidle'});await p.evaluate(()=>window.ready);
fs.mkdirSync('qa',{recursive:true});let report=[];
for(let i=0;i<starts.length;i++)for(const phase of [.07,.5]){
 let t=map(starts[i])+phase;await p.evaluate(t=>window.render(t),t);const issues=await p.evaluate(()=>['title','captions','eyebrow','cta'].flatMap(id=>{let el=document.getElementById(id),r=el.getBoundingClientRect();return el.offsetParent&&((r.right>1080)||(r.left<0)||(el.scrollWidth>el.clientWidth+2))?[id+' overflows']:[]}));
 const name=`qa/shot-${String(i).padStart(2,'0')}-${phase===.07?'transition':'settled'}.jpg`;await p.screenshot({path:name,type:'jpeg',quality:88});report.push({shot:i,time:t,issues,file:name});
}
await p.evaluate(t=>{window.render(t);document.getElementById('eyebrow').textContent='STORIES. QUESTIONS. PLAY.';document.getElementById('badge').textContent='A day with Cheeko 🦊';document.getElementById('captions').textContent='Little moments. More connection.';document.getElementById('footerText').textContent='cheekoai.in';document.getElementById('progress').style.width='1080px';},map(22)+.6);
await p.screenshot({path:'../thumbnail.jpg',type:'jpeg',quality:96});await b.close();fs.writeFileSync('qa/report.json',JSON.stringify({errors,report},null,2));console.log(JSON.stringify({pages:report.length,errors,layoutIssues:report.filter(x=>x.issues.length)},null,2));
