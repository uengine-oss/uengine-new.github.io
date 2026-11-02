// PROCESS_AGENT 신원으로 MCP 도구를 직접 호출한다(LLM 아님). 영상과 튜토리얼에서 Agent Decisions 흐름을 보여 주는 데 쓴다.
//   node agent_tools.mjs propose          판단 기록 1건, 제안 2건을 남긴다 (WMS_CORR = 이어 붙일 인스턴스 ID)
//   node agent_tools.mjs self-confirm     자기 제안을 승인하려 해 본다 → FORBIDDEN
const MCP = process.env.WMS_MCP_URL || 'http://127.0.0.1:8199/mcp'
const T = '10000000-0000-0000-0000-00000000000a', W = '20000000-0000-0000-0000-00000000000a'
const call = async (name, args) => {
  const r = await fetch(MCP, { method: 'POST', headers: { 'content-type': 'application/json', accept: 'application/json, text/event-stream' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/call', params: { name, arguments: args } }) })
  const j = await r.json(); const res = j.result?.structuredContent ?? JSON.parse(j.result?.content?.[0]?.text ?? '{}')
  return res
}
const show = (name, r) => console.log(`${name} → ${r.result}${r.status ? ' / ' + r.status : ''}${r.document_id ? ' / ' + r.document_id.slice(0, 8) : ''}${r.error_kind ? ' / ' + r.error_kind + ': ' + String(r.message).slice(0, 170) : ''}`)
if (process.argv[2] === 'propose') {
  const corr = process.env.WMS_CORR
  const delay = await call('get_dispatch_delay_signals', { tenant_id: T, warehouse_id: W })
  console.log('get_dispatch_delay_signals →', delay.result, JSON.stringify(delay.document ?? {}).slice(0, 120))
  show('log_agent_decision', await call('log_agent_decision', { tenant_id: T, warehouse_id: W, proposal_type: 'REPLENISHMENT', correlation_id: corr,
    reasoning: '예시 기록: SKU-A-001 가용 재고 30개가 최소 기준 50개 아래이고 진행 중인 발주가 없어, 허용된 create_rfq 로 170개 구매 요청을 만들었다.',
    signals_snapshot: { available_qty: 30, reorder_min: 50 } }))
  show('propose_agent_action', await call('propose_agent_action', { tenant_id: T, warehouse_id: W, proposal_type: 'LABOR_REBALANCE',
    reasoning: '예시 제안: inbound-a 의 완료 건수가 창고 평균보다 많고 quality-a 는 적다. 오후 적치 일부를 나눌 것을 제안한다. 재배치 실행 함수가 없어 사람이 조치해야 한다.',
    proposed_action: { action: 'MOVE_PUTAWAY_WORKLOAD', from_actor_email: 'inbound-a@demo.local', to_actor_email: 'quality-a@demo.local', suggested_rpc: null } }))
  show('propose_agent_action', await call('propose_agent_action', { tenant_id: T, warehouse_id: W, proposal_type: 'EQUIPMENT_ROUTING_SUGGESTION',
    reasoning: '예시 제안: 운반차 AGV-07 이 최근 장애로 병목 후보다. 라우팅에서 임시 제외할 것을 제안한다. 설비 제외는 에이전트 권한 밖이다.',
    proposed_action: { suggested_rpc: 'wms_exclude_equipment_from_routing', equipment_code: 'AGV-07' } }))
} else if (process.argv[2] === 'self-confirm') {
  const list = await call('get_agent_decisions', { tenant_id: T, warehouse_id: W })
  const first = await call('propose_agent_action', { tenant_id: T, warehouse_id: W, proposal_type: 'LABOR_REBALANCE', reasoning: '예시 제안: 자기 승인 시도 대상.', proposed_action: { action: 'MOVE_PUTAWAY_WORKLOAD' } })
  show('propose_agent_action', first)
  show('confirm_agent_proposal', await call('confirm_agent_proposal', { decision_id: first.document_id, expected_version: first.version ?? 1 }))
}
