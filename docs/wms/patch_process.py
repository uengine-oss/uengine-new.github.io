#!/usr/bin/env python3
"""install_processgpt_integration.py(fc82ea2)가 넣은 프로세스를 지금의 Process GPT 엔진에 맞게 보정한다. 여러 번 돌려도 된다.

1. 게이트웨이 분기가 종료 이벤트로 바로 가면 엔진이 그 너머의 할 일을 미리 만들지 않아 PO 확정 뒤에서 흐름이 멈춘다
   (polling_service/process_definition.py 의 find_next_through_gateway). 반려 분기에 「발주 취소 확인」 활동을 끼운다.
2. 폼 정의의 html 이 비어 있어 화면이 「자유입력」 칸만 보여 준다. fields_json 으로 html 을 채운다.

    SERVICE_ROLE_KEY=... python3 patch_process.py http://127.0.0.1:54321
"""
import json, os, re, sys, urllib.parse, urllib.request, uuid

API = sys.argv[1].rstrip("/")
KEY = os.environ["SERVICE_ROLE_KEY"]
HEAD = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
P = "wms_replenishment_process"
ACT = "cancel_po_ack"
NAMES = {"request_replenishment": "재고 부족 감지", "approve_purchase": "발주 승인", "quality_inspection": "입고 품질검사",
         "scrap_disposition": "폐기 처리 확인", ACT: "발주 취소 확인"}


def call(method, path, body=None, prefer=None):
    head = dict(HEAD, **({"Prefer": prefer} if prefer else {}))
    req = urllib.request.Request(API + "/rest/v1/" + path, method=method, headers=head, data=json.dumps(body).encode() if body else None)
    text = urllib.request.urlopen(req, timeout=30).read().decode()
    return json.loads(text) if text else None


def field(f):
    key, alias = f["key"], f["text"]
    common = f"name='{key}' alias='{alias}' disabled='false' readonly='false' v-model=\"slotProps.modelValue['{key}']\""
    if f["type"] == "radio":
        return f"<radio-field is_dynamic_load='fixed' items='{json.dumps(f['items'], ensure_ascii=False)}' {common}></radio-field>"
    if f["type"] == "textarea":
        return f"<textarea-field rows='3' {common}></textarea-field>"
    if f["type"] == "checkbox":
        return f"<radio-field is_dynamic_load='fixed' items='[{{\"true\": \"완료\"}}]' {common}></radio-field>"
    return f"<text-field type='{'number' if f['type'] == 'number' else 'text'}' {common}></text-field>"


def html(row):
    cells = "\n".join(f'    <div class="row"><div class="col-sm-12">{field(f)}</div></div>' for f in row["fields_json"])
    return f"""<section>
  <row-layout name="{row['id']}" alias="{NAMES[row['activity_id']]}" is_multidata_mode="false" v-model="formValues" v-slot="slotProps">
{cells}
  </row-layout>
</section>"""


# 1. 정의(JSON·BPMN)
row = call("GET", f"proc_def?select=uuid,definition,bpmn&tenant_id=eq.localhost&id=eq.{P}")[0]
d, x = row["definition"], row["bpmn"]
form_id = f"{P}_{ACT}_form"
if not any(a["id"] == ACT for a in d["activities"]):
    base = next(a for a in d["activities"] if a["id"] == "approve_purchase")
    desc = "반려된 발주를 확인하고 취소 사유를 남긴다."
    d["activities"].append(dict(base, id=ACT, name=NAMES[ACT], tool=f"formHandler:{form_id}", description=desc, instruction=desc,
                                inputData=[f"{P}_approve_purchase_form.approval_note"], outputData=["발주 취소 확인"]))
    for s in d["sequences"]:
        if s["id"] == "seq_rejected_end":
            s["target"] = ACT
    d["sequences"].append({"id": "seq_cancel_end", "name": "", "source": ACT, "target": "end_cancelled", "condition": "", "properties": "{}"})
    x = x.replace('sourceRef="gw_approved" targetRef="end_cancelled"/>', f'sourceRef="gw_approved" targetRef="{ACT}"/><bpmn:sequenceFlow id="seq_cancel_end" sourceRef="{ACT}" targetRef="end_cancelled"/>')
    x = x.replace('<bpmn:endEvent id="end_cancelled" name="발주 취소"><bpmn:incoming>seq_rejected_end</bpmn:incoming>',
                  f'<bpmn:userTask id="{ACT}" name="{NAMES[ACT]}"><bpmn:incoming>seq_rejected_end</bpmn:incoming><bpmn:outgoing>seq_cancel_end</bpmn:outgoing></bpmn:userTask>'
                  '<bpmn:endEvent id="end_cancelled" name="발주 취소"><bpmn:incoming>seq_cancel_end</bpmn:incoming>')
    x = x.replace('<bpmn:flowNodeRef>end_cancelled</bpmn:flowNodeRef>', f'<bpmn:flowNodeRef>{ACT}</bpmn:flowNodeRef><bpmn:flowNodeRef>end_cancelled</bpmn:flowNodeRef>')
    x = x.replace('<dc:Bounds x="1130" y="50" width="36" height="36"/>', '<dc:Bounds x="1300" y="50" width="36" height="36"/>')
    x = x.replace('<bpmndi:BPMNShape id="Shape_end_cancelled"', f'<bpmndi:BPMNShape id="Shape_{ACT}" bpmnElement="{ACT}"><dc:Bounds x="1130" y="30" width="120" height="76"/></bpmndi:BPMNShape><bpmndi:BPMNShape id="Shape_end_cancelled"')
    x = re.sub(r'(<bpmndi:BPMNEdge id="Edge_seq_rejected_end" bpmnElement="seq_rejected_end">)<di:waypoint [^>]*/><di:waypoint [^>]*/>',
               r'\1<di:waypoint x="1035" y="157"/><di:waypoint x="1190" y="68"/>', x)
    x = x.replace('</bpmndi:BPMNPlane>', '<bpmndi:BPMNEdge id="Edge_seq_cancel_end" bpmnElement="seq_cancel_end"><di:waypoint x="1250" y="68"/><di:waypoint x="1318" y="68"/></bpmndi:BPMNEdge></bpmndi:BPMNPlane>')
    call("PATCH", f"proc_def?uuid=eq.{row['uuid']}", {"definition": d, "bpmn": x})
    print("process patched: reject branch goes through", ACT)

# 2. 폼
fields = [{"key": "cancel_note", "text": "취소 사유", "type": "textarea", "disabled": "false", "readonly": "false"}]
call("POST", "form_def?on_conflict=uuid", [{"uuid": str(uuid.uuid5(uuid.NAMESPACE_URL, f"process-gpt:localhost:{form_id}")), "html": "", "proc_def_id": P,
     "activity_id": ACT, "tenant_id": "localhost", "id": form_id, "fields_json": fields}], "resolution=merge-duplicates")
for r in call("GET", f"form_def?select=id,uuid,activity_id,fields_json&tenant_id=eq.localhost&proc_def_id=eq.{P}"):
    call("PATCH", "form_def?uuid=eq." + urllib.parse.quote(r["uuid"]), {"html": html(r)})
    print("form html filled:", r["id"])
