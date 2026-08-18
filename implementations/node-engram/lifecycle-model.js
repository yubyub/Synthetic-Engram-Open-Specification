#!/usr/bin/env node
/** Executable non-normative identity lifecycle model. */
const fs=require('fs');
function evaluate(operation,data){
  if(operation==='export-event'){
    const kind=data.kind, previous=data.previous, candidate=data.candidate;
    if(previous===null)return {status:'valid',engram_id_retained:false,export_id_retained:false,package_id_changed:true,object_ids_retained:true};
    const retained=kind==='partial'?candidate.object_ids.every(x=>previous.object_ids.includes(x)):JSON.stringify(candidate.object_ids)===JSON.stringify(previous.object_ids);
    const sameExport=kind==='retry'||kind==='repack';
    const valid=candidate.engram_id===previous.engram_id&&((candidate.export_id===previous.export_id)===sameExport)&&candidate.package_id!==previous.package_id&&retained;
    return {status:valid?'valid':'invalid',engram_id_retained:candidate.engram_id===previous.engram_id,export_id_retained:candidate.export_id===previous.export_id,package_id_changed:candidate.package_id!==previous.package_id,object_ids_retained:retained};
  }
  if(operation==='native-map'){
    const byEngram=new Map(); for(const item of data.mappings){const key=`${item.namespace}\0${item.native_id}`;if(!byEngram.has(item.engram_id))byEngram.set(item.engram_id,new Set());byEngram.get(item.engram_id).add(key);}
    const collision=[...byEngram].find(([,values])=>values.size>1); return collision?{status:'collision',engram_id:collision[0],automatic_merge:false}:{status:'valid'};
  }
  if(operation==='reclassify')return {status:'valid',record_id:data.record_id,id_retained:true,prefix_rewritten:false};
  if(operation==='merge')return {status:'loss-report-required',survivor:data.survivor,retired:data.merged,ids_reassigned:false};
  if(operation==='split')return {status:'loss-report-required',retained:data.continuing?[data.continuing]:[],new:data.created,old_id_reused_more_than_once:false};
  throw new Error(operation);
}
const request=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));process.stdout.write(JSON.stringify(evaluate(request.operation,request.input))+'\n');
