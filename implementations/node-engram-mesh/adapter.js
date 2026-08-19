#!/usr/bin/env node
const fs = require('fs'); const path = require('path');
const request = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const mesh = path.join(request.fixture, 'engram-mesh.json'); const value = JSON.parse(fs.readFileSync(mesh, 'utf8'));
if (value.format !== 'engram-mesh' || value.version !== '0.3') throw new Error('unsupported Engram Mesh document');
for (const key of ['sources', 'nodes', 'bindings', 'relationships']) if (!Array.isArray(value[key])) throw new Error(`missing ${key}`);
const nodeIds = new Set(value.nodes.map(node => node.id)), sourceIds = new Set(value.sources.map(source => source.id));
for (const binding of value.bindings) if (!nodeIds.has(binding.node) || !sourceIds.has(binding.source)) throw new Error('unresolved source binding');
for (const relationship of value.relationships) if (!nodeIds.has(relationship.from) || !nodeIds.has(relationship.to)) throw new Error('unresolved relationship');
let artifacts = [];
if (['produce', 'round-trip'].includes(process.argv[2])) { fs.copyFileSync(mesh, path.join(request.artifact_directory, 'engram-mesh.json')); artifacts = [{path: 'engram-mesh.json', media_type: 'application/json'}]; }
process.stdout.write(JSON.stringify({protocol_version:'1.0', case_id:request.case_id, outcome:'completed', observed:{status:'success',mesh_id:value.mesh_id}, diagnostics:[], artifacts})+'\n');
