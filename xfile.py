# =====================================================================
# 대구상가맨 권리금 X-파일 캠페인 엔진 (Omnichannel Campaign Engine) v1.0
# ---------------------------------------------------------------------
# "케이스 하나 → 정밀 진단 → 옴니채널 콘텐츠 캠페인 → 14일 배포 플랜" 을
# 한 번에 산출하는 플래그십 도구.
#   - 코어: 대구상가맨 RV-19 권리금 평가 프레임워크 (자체 진단 루브릭)
#   - 보이스 락: 오석민 시그니처 톤 (모든 채널 콘텐츠가 같은 목소리)
#   - 시리즈화: '권리금 X-파일 #N' 콘텐츠 IP 포맷으로 누적
# 단발 도구(틱톡/카드뉴스 등 개별 생성)는 funnel.py, 장문 블로그는 blog.py.
# 실행:  streamlit run xfile.py   (접근 비밀번호: 0810)
# =====================================================================
import os
import streamlit as st

st.set_page_config(page_title="권리금 X-파일 캠페인 엔진", page_icon="🔬", layout="wide")

from dotenv import load_dotenv

# ---------------------------------------------------------------------
# Gemini SDK 로드 (신/구 SDK 자동 폴백)
# ---------------------------------------------------------------------
genai = None
try:
    from google import genai as genai_new
    HAS_GEMINI = True
    USE_NEW_SDK = True
except ImportError:
    genai_new = None
    try:
        import google.generativeai as genai
        HAS_GEMINI = True
        USE_NEW_SDK = False
    except ImportError:
        HAS_GEMINI = False
        USE_NEW_SDK = False

# ---------------------------------------------------------------------
# 보안 키 로드 (.env → st.secrets)
# ---------------------------------------------------------------------
load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None

# ---------------------------------------------------------------------
# AI 호출 (모델 자동 폴백)
# ---------------------------------------------------------------------
def get_gemini_response(prompt, api_key):
    if not HAS_GEMINI:
        return "❌ Gemini 패키지가 설치되지 않았습니다. (pip install google-genai)"
    if not api_key:
        return "❌ GEMINI_API_KEY가 설정되지 않았습니다. (.env 또는 st.secrets 확인)"
    try:
        if USE_NEW_SDK:
            client = genai_new.Client(api_key=api_key)
            for model_name in ("gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"):
                try:
                    response = client.models.generate_content(model=model_name, contents=prompt)
                    return response.text.strip()
                except Exception:
                    continue
            return "❌ 사용 가능한 Gemini 모델을 찾지 못했습니다."
        genai.configure(api_key=api_key)
        available = [m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
        preferred = ["models/gemini-2.5-flash", "models/gemini-2.0-flash", "models/gemini-1.5-flash"]
        target = next((m for m in preferred if m in available), available[0])
        model = genai.GenerativeModel(target.replace("models/", ""))
        return model.generate_content(prompt).text.strip()
    except Exception as e:
        return f"❌ 시스템 연산 오류: {str(e)}"

# ---------------------------------------------------------------------
# 코어 자산 — 자체 프레임워크 / 브랜드 보이스 / 컨텍스트
# ---------------------------------------------------------------------
RV19_FRAMEWORK = """
[대구상가맨 RV-19 권리금 평가 프레임워크 — 진단은 반드시 이 19개 항목으로만]
1. 입지 등급 (유동인구·가시성·접근성)
2. 상권 안정성 (배후 수요·공실률 추세)
3. 입지-업종 적합도
4. 매출 검증 가능성 (POS·카드매출 자료 유무)
5. 수익 구조 건전성
6. 시설 권리금 (감가 후 잔존가치)
7. 영업 권리금 (단골·매출 지속성)
8. 바닥 권리금 (자리값 시세)
9. 임대차 안정성 (잔여기간·갱신요구권·임대인 성향)
10. 임대료 적정성 (매출 대비 임대료 비중)
11. 경쟁 강도 (반경 내 동종업종 밀도)
12. 업종 트렌드 리스크 (수명주기상 위치)
13. 양도 사유 신뢰도
14. 권리금 회수 가능성 (재양도 시 시장성)
15. 인테리어·설비 노후도
16. 인허가 승계 리스크
17. 직원·노무 승계 이슈
18. 계절·요일 매출 변동성
19. 종합 협상 레버리지 (매수자 우위 정도)
"""

OSM_VOICE = """
[오석민 시그니처 보이스 — 모든 진단·콘텐츠가 이 목소리로]
- 1인칭 경험 단언: "제가 15년간 대구 현장에서 본 바로는" 식으로 권위 있게.
- 숫자·팩트 먼저, 감정 나중. '느낌'이 아니라 '수치'와 '검증 가능성'으로 말한다.
- 거품은 거품이라 말하되, 단정적 '사기' 매도는 하지 않는다. "이건 위험 신호입니다" 수준의 경고.
- 예비 창업자에겐 보호자, 기존 점주에겐 안전한 매각 조력자. 양쪽 어느 편도 적대시하지 않는다.
- 마무리는 늘 "직접 계산해 보시라"는 권유. 협박·강요 금지.
"""

BRAND_CONTEXT = """
[브랜드 — 반드시 이 정체성으로]
- 화자: '대구상가맨' 오석민 대표 (15년 차 상가 양도양수·프랜차이즈 창업 전문가)
- 핵심: 무료 '전문가용 권리금 계산기'(19가지 실무 변수), 양수자 수수료 0원, 17~19페이지 정밀 실사 보고서, 직접 검증한 S등급 매물 중개
- 사이트 www.sangaman.com / 상담 010-4570-8889 / 카카오톡 상담 가능
[작성 금지]
- 마크다운 특수기호(별표 **, 샵 #, 불릿 - 등) 금지. 그대로 복사해 올릴 수 있는 평문으로만.
- 세금·4대보험·원가율 등 차감 내역 언급 금지.
- 입력되지 않은 매출·수익·권리금·면적 수치를 임의로 지어내지 말 것. 모르면 '추가 자료 필요'로 표기.
"""

BRAND_CTA_SHORT = (
    "권리금, 아직도 감으로 결정하세요? RV-19 실무 변수로 1초 만에 내 매장 진짜 가치 확인 — "
    "무료 권리금 계산기 www.sangaman.com / 1:1 팩트 상담 010-4570-8889 (양수자 수수료 0원)"
)

# 채널별 제작 스펙 (선택된 것만 프롬프트에 주입)
CHANNEL_SPECS = {
    "네이버 블로그 장문(SEO)": (
        "네이버 SEO 최적화 스토리텔링 포스팅. 맨 위에 [블로그 제목] 자동 창작 후 출력. "
        "공백 포함 2,500자 이상, 도입부 첫 문장에 '{region} {category}' 자연스럽게 사용. 본문 끝에 해시태그 20개 한 줄."
    ),
    "틱톡·릴스 60초 대본": (
        "0~3초 후크([화면 자막]/[멘트]/[연출]) → 3~50초 본문(5초 단위 타임코드, 구간별 [멘트]/[자막]/[B롤 연출]) "
        "→ 50~60초 CTA. 추천 BGM 무드 + 편집 팁 + 해시태그(틱톡 6 / 인스타 12) 한 줄씩."
    ),
    "인스타 카드뉴스+캡션": (
        "표지~8장 카드 각각 [헤드라인]/[본문]/[디자인 노트], 마지막 카드는 CTA. 인스타 캡션(첫 줄 후크→본문→CTA), "
        "해시태그 30개 한 줄, 스토리용 짧은 텍스트 2종."
    ),
    "유튜브 쇼츠 스크립트": (
        "영상 제목 3안 + 썸네일 문구 3안 + 0~15초 후크 + 본문 콘티([멘트]/[자료화면 지시]/[강조 자막]) + 마무리 CTA "
        "+ 설명란(요약·링크·해시태그 5) + 검색 태그 15개 + 고정 댓글 1개."
    ),
    "네이버 지식인 답변": (
        "이 케이스와 똑같은 고민의 질문에 오석민이 답하는 형태. 권리금 적정성 판단법·확인 서류 등 실무 정보 위주, "
        "끝에 한두 문장으로만 무료 도구를 부담 없이 안내. 마지막에 '[운영 팁]' 한 줄(도배 금지·맥락 맞춰 수정·광고 표기)."
    ),
    "X(트위터)·스레드 단문": (
        "강한 후크형 단문 3개 버전(각 280자 내외). 첫 줄에서 멈추게, 마지막 줄에 CTA 또는 시리즈 안내."
    ),
    "카카오톡 채널 메시지": (
        "구독자 발송용 1건. [메시지 제목] + [본문 100자 내외 핵심] + [버튼 문구 1개]. 군더더기 없이 클릭하게."
    ),
    "지역 언론 제보용 보도자료": (
        "지역 언론 제보 톤의 보도자료 1건. [제목] / [리드 문단] / [본문 3문단] / [문의처]. 과장 없는 사실 위주, "
        "공익적 정보(권리금 거품·사기 예방 캠페인) 프레임으로."
    ),
}

# ---------------------------------------------------------------------
# UI 스타일 (히어로 배너 포함)
# ---------------------------------------------------------------------
st.markdown(
    """
    <style>
    html, body, [class*="css"], .stTextInput>div>div>input, .stSelectbox>div>div>div { font-size: 15px !important; }
    .stButton>button { font-size: 18px !important; font-weight: bold; height: 3em; width: 100%; }
    .xf-hero { background: linear-gradient(135deg,#0f2027 0%,#203a43 55%,#2c5364 100%);
        color:#fff; padding: 22px 26px; border-radius: 14px; margin-bottom: 14px; }
    .xf-hero h1 { color:#fff; margin:0; font-size:26px; line-height:1.25; }
    .xf-hero p { color:#cfe8ff; margin:8px 0 0; font-size:14px; }
    .xf-badge { display:inline-block; background:rgba(255,255,255,.14); border:1px solid rgba(255,255,255,.32);
        padding:3px 11px; border-radius:999px; font-size:12px; margin:10px 8px 0 0; color:#eaf6ff; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# 보안 인증 (0810)
# ---------------------------------------------------------------------
if "password_correct" not in st.session_state:
    st.title("🔒 권리금 X-파일 캠페인 엔진 — 보안 인증")
    pwd_input = st.text_input("접근 비밀번호를 입력하십시오", type="password")
    if st.button("인증 가동"):
        if pwd_input == "0810":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("비밀번호 불일치")
    st.stop()

# ---------------------------------------------------------------------
# 헤더
# ---------------------------------------------------------------------
st.markdown(
    """
    <div class="xf-hero">
      <h1>🔬 대구상가맨 권리금 X-파일 캠페인 엔진</h1>
      <p>케이스 하나 → 정밀 진단 → 옴니채널 콘텐츠 캠페인 → 14일 배포 플랜까지, 단 한 번에.</p>
      <span class="xf-badge">RV-19 권리금 평가 프레임워크 탑재</span>
      <span class="xf-badge">오석민 시그니처 보이스 락</span>
      <span class="xf-badge">시리즈 IP: 권리금 X-파일</span>
      <span class="xf-badge">v1.0</span>
    </div>
    """,
    unsafe_allow_html=True,
)
if not API_KEY:
    st.error("⚠️ GEMINI_API_KEY 미설정 — 생성 기능이 작동하지 않습니다. (.env 또는 st.secrets)")

# ---------------------------------------------------------------------
# 입력 폼 (세션 키 기반 — 데모 케이스 자동 채우기 지원)
# ---------------------------------------------------------------------
DEFAULTS = {
    "xf_case_type": "가상 시뮬레이션 (교육·인지용)",
    "xf_episode": 1,
    "xf_region": "대구",
    "xf_category": "",
    "xf_brand": "",
    "xf_area": "",
    "xf_deposit": "",
    "xf_rent": "",
    "xf_asking": "",
    "xf_revenue": "",
    "xf_profit": "",
    "xf_composition": "",
    "xf_locfeat": "",
    "xf_reason": "",
    "xf_lease": "",
    "xf_extra": "",
    "xf_target": "둘 다 (예비 창업자 + 기존 점주)",
    "xf_disclosure": "익명 처리 (상호·정확한 위치 비공개)",
    "xf_tone": "신뢰·단호 (전문가 정공법)",
    "xf_channels": ["네이버 블로그 장문(SEO)", "틱톡·릴스 60초 대본", "인스타 카드뉴스+캡션", "네이버 지식인 답변"],
}
for _k, _v in DEFAULTS.items():
    st.session_state.setdefault(_k, _v)

DEMO_CASE = {
    "xf_case_type": "가상 시뮬레이션 (교육·인지용)",
    "xf_episode": 7,
    "xf_region": "대구 수성구 들안길",
    "xf_category": "한우 정육식당 (점심·저녁 겸업)",
    "xf_brand": "",
    "xf_area": "1층 60평 (홀 50 / 주방 10)",
    "xf_deposit": "5,000만 원",
    "xf_rent": "월 380만 원",
    "xf_asking": "권리금 1억 8,000만 원 호가",
    "xf_revenue": "월평균 8,500만 원 (POS 자료 제시 가능)",
    "xf_profit": "월평균 1,600만 원 (양도자 구두 주장)",
    "xf_composition": "시설 8,000 / 영업 7,000 / 바닥 3,000 (양도자 구분)",
    "xf_locfeat": "들안길 메인, 코너 1층, 전용 주차 6대, 인근 신축 오피스텔 입주 진행 중",
    "xf_reason": "양도자 건강 문제로 급매라고 주장",
    "xf_lease": "임대차 잔여 1년 2개월, 갱신요구권 일부 소진",
    "xf_extra": "최근 6개월 매출 우상향이라 강조하나 직전 2년치 자료는 미공개",
    "xf_target": "예비 창업자",
    "xf_disclosure": "익명 처리 (상호·정확한 위치 비공개)",
    "xf_tone": "신뢰·단호 (전문가 정공법)",
    "xf_channels": ["네이버 블로그 장문(SEO)", "틱톡·릴스 60초 대본", "인스타 카드뉴스+캡션", "유튜브 쇼츠 스크립트", "네이버 지식인 답변"],
}

c_demo, c_reset = st.columns([1, 1])
with c_demo:
    if st.button("🎲 데모 케이스 불러오기"):
        st.session_state.update(DEMO_CASE)
        st.rerun()
with c_reset:
    if st.button("🧹 입력 초기화"):
        for _k, _v in DEFAULTS.items():
            st.session_state[_k] = _v
        st.session_state.pop("xf_result", None)
        st.rerun()

st.subheader("1️⃣ 케이스 입력")
cA, cB = st.columns(2)
with cA:
    st.selectbox("케이스 유형", ["가상 시뮬레이션 (교육·인지용)", "실제 익명 케이스 (사실관계 확인됨)", "보유 매물 홍보용"], key="xf_case_type")
    st.text_input("📍 지역 (구체적으로)", key="xf_region", placeholder="예: 대구 수성구 들안길 / 동성로 / 칠곡 강변대로")
    st.text_input("🏢 업종 (필수)", key="xf_category", placeholder="예: 한우 정육식당 / 무인 아이스크림 / 헤어샵 / 프랜차이즈 치킨")
    st.text_input("🏷️ 브랜드명 (선택)", key="xf_brand", placeholder="예: 하남돼지집 (개인/일반이면 비워두기)")
    st.text_input("📐 면적/구성 (선택)", key="xf_area", placeholder="예: 1층 60평 (홀 50 / 주방 10)")
    st.number_input("🔢 권리금 X-파일 시리즈 회차 #", min_value=1, max_value=999, step=1, key="xf_episode")
with cB:
    st.text_input("💵 매도자 호가 권리금 (선택)", key="xf_asking", placeholder="예: 권리금 1억 8,000만 원 호가")
    st.text_input("🏦 보증금 / 월세 (선택)", key="xf_deposit", placeholder="보증금 예: 5,000만 원")
    st.text_input("　", key="xf_rent", placeholder="월세 예: 월 380만 원", label_visibility="collapsed")
    st.text_input("💰 월평균 매출 (선택)", key="xf_revenue", placeholder="예: 월 8,500만 원 (POS 자료 제시 가능 여부도 적기)")
    st.text_input("📈 월평균 수익 (선택)", key="xf_profit", placeholder="예: 월 1,600만 원 (양도자 구두 주장)")
    st.text_input("🧩 권리금 구성: 시설/영업/바닥 (선택)", key="xf_composition", placeholder="예: 시설 8,000 / 영업 7,000 / 바닥 3,000")

st.text_input("📌 입지·시설 특징 (선택)", key="xf_locfeat", placeholder="예: 코너 1층, 전용 주차 6대, 인근 신축 오피스텔 입주 진행 중")
cC, cD = st.columns(2)
with cC:
    st.text_input("🚪 양도 사유 (선택)", key="xf_reason", placeholder="예: 양도자 건강 문제로 급매 주장")
with cD:
    st.text_input("📄 임대차 잔여기간·갱신권 (선택)", key="xf_lease", placeholder="예: 잔여 1년 2개월, 갱신요구권 일부 소진")
st.text_input("➕ 그 밖에 알려진 사실 (선택)", key="xf_extra", placeholder="예: 최근 6개월 매출 우상향 강조하나 직전 2년치 자료 미공개")

st.subheader("2️⃣ 캠페인 설정")
cE, cF, cG = st.columns(3)
with cE:
    st.selectbox("타겟", ["예비 창업자", "기존 점주·자영업자 (매각 희망)", "둘 다 (예비 창업자 + 기존 점주)"], key="xf_target")
with cF:
    st.selectbox("공개 수위", ["익명 처리 (상호·정확한 위치 비공개)", "지역·업종까지만 공개", "완전 가상 사례로 각색"], key="xf_disclosure")
with cG:
    st.selectbox("톤 강도", ["신뢰·단호 (전문가 정공법)", "친근·공감 (멘토 톤)", "임팩트·경고 (충격 환기)"], key="xf_tone")
st.multiselect("📡 제작할 채널 (옴니채널 — 같은 케이스에서 일제히 파생)", list(CHANNEL_SPECS.keys()), key="xf_channels")

st.caption("⚖️ 실제 케이스를 다룰 땐 상호·정확한 위치를 비공개하고, 사실관계가 확인된 내용만, 단정적 '사기' 매도가 아닌 '위험 신호' 수준으로 다루세요. 입력하지 않은 수치는 엔진이 임의로 만들지 않습니다.")

# ---------------------------------------------------------------------
# 헬퍼
# ---------------------------------------------------------------------
def line(label, key):
    v = (st.session_state.get(key) or "").strip() if isinstance(st.session_state.get(key), str) else st.session_state.get(key)
    if v in (None, "", []):
        return f"- {label}: 미입력\n"
    return f"- {label}: {v}\n"

def build_diag_prompt():
    s = st.session_state
    region = (s["xf_region"] or "대구").strip()
    return f"""{BRAND_CONTEXT}
{OSM_VOICE}
{RV19_FRAMEWORK}

당신은 '대구상가맨' 오석민 대표입니다. 아래 양도양수 케이스를 RV-19 프레임워크로 정밀 진단하십시오.

[케이스 #{s['xf_episode']}]
- 케이스 유형: {s['xf_case_type']}
- 공개 수위: {s['xf_disclosure']}
{line('지역', 'xf_region')}{line('업종', 'xf_category')}{line('브랜드', 'xf_brand')}{line('면적/구성', 'xf_area')}{line('보증금', 'xf_deposit')}{line('월세', 'xf_rent')}{line('매도자 호가 권리금', 'xf_asking')}{line('월평균 매출', 'xf_revenue')}{line('월평균 수익', 'xf_profit')}{line('권리금 구성(시설/영업/바닥)', 'xf_composition')}{line('입지·시설 특징', 'xf_locfeat')}{line('양도 사유', 'xf_reason')}{line('임대차 잔여기간·갱신권', 'xf_lease')}{line('그 밖의 사실', 'xf_extra')}

[출력 — 평문. 제목은 "대구상가맨 권리금 정밀 진단 리포트 — X-파일 #{s['xf_episode']}"]
1) 한 줄 판정: [거품 / 적정 / 저평가 / 자료 부족 / 사기 위험 신호] 중 하나 + 근거 한 문장.
2) RV-19 항목별 평가: 위 19개 항목을 번호 그대로, 각 항목 [상 / 중 / 하 / 판단불가] + 1줄 코멘트.
3) 적정 권리금 밴드: 입력된 호가·매출 등을 기준으로 한 '상대 평가 밴드'만 제시(예: 호가 대비 약 N~N% 수준이 합리적, 또는 매출 대비 권리금 배수 관점). 입력이 부족하면 어떤 자료(직전 2년 POS, 카드매출 신고서, 임대차계약서, 시설 견적 등)가 더 필요한지 명시. 입력에 없는 구체 수치를 새로 지어내지 말 것.
4) 핵심 리스크 TOP 3: 이 거래에서 가장 위험한 것 3가지 + 각각의 검증/방어 방법.
5) 협상 포인트 3가지: 매수자가 권리금을 깎거나 안전장치를 걸 수 있는 지점.
6) 즉시 액션: 양수 검토자가 지금 당장 해야 할 일(요청할 자료 목록 포함).
7) 신뢰 라벨 한 줄: "본 진단은 대구상가맨 RV-19 프레임워크와 17~19페이지 정밀 실사 보고서 기준으로 작성되었습니다. 무료 권리금 계산기: www.sangaman.com / 상담 010-4570-8889 (양수자 수수료 0원)"
"""

def build_campaign_prompt(diagnostic_text):
    s = st.session_state
    region = (s["xf_region"] or "대구").strip()
    category = (s["xf_category"] or "해당 업종").strip()
    chosen = s["xf_channels"] or list(CHANNEL_SPECS.keys())[:1]
    specs = "\n".join(
        f"■ {name}\n   {CHANNEL_SPECS[name].format(region=region, category=category)}" for name in chosen
    )
    return f"""{BRAND_CONTEXT}
{OSM_VOICE}

당신은 '대구상가맨' 오석민 대표의 콘텐츠 PD입니다.
아래 [진단 리포트]를 원천 소스로 삼아, '권리금 X-파일 #{s['xf_episode']}' 시리즈 콘텐츠 캠페인을 옴니채널로 제작하십시오.
모든 채널 콘텐츠는 같은 케이스·같은 결론·같은 시리즈 정체성을 공유해야 하며, 진단 리포트의 판정·리스크·협상 포인트와 모순되면 안 됩니다.

[케이스 요약]
- 시리즈 회차: 권리금 X-파일 #{s['xf_episode']}
- 지역/업종: {region} / {category}  (브랜드: {(s['xf_brand'] or '개인/일반').strip()})
- 매도자 호가 권리금: {(s['xf_asking'] or '비공개').strip()}
- 공개 수위: {s['xf_disclosure']}  → 실제 케이스라면 상호·정확한 위치는 반드시 비공개, 단정적 '사기' 단정 금지(‘위험 신호’ 수준).
- 타겟: {s['xf_target']}
- 톤 강도: {s['xf_tone']}

[진단 리포트 — 이 내용을 콘텐츠의 뼈대로]
{diagnostic_text}

[제작할 채널 — 아래 항목만, 각각 '■ 채널명'으로 시작하는 블록으로 명확히 구분]
{specs}

[모든 채널 공통 규칙]
- 시리즈 브랜딩: 제목 또는 도입부에 '권리금 X-파일'과 회차 #{s['xf_episode']}를 자연스럽게 노출. 시리즈 인지를 만들 것.
- 신뢰 장치: '대구상가맨 RV-19 프레임워크', '양수자 수수료 0원', '17~19페이지 정밀 실사 보고서' 중 맥락에 맞는 것을 1~2개 자연스럽게 삽입.
- 일관된 CTA: 끝에 "{BRAND_CTA_SHORT}" 취지를 각 채널 톤에 맞게 변형해서 배치.
- 평문 출력, 마크다운 특수기호 금지, 차감 내역 언급 금지, 진단에 없는 수치 새로 만들지 말 것.
- 정보가 진짜로 도움이 되게 쓰되 마지막에 대구상가맨으로 연결.

[채널 블록들 뒤에 반드시 추가 출력]
■ 14일 배포 플랜
   Day 1~14 중 어느 날 어떤 채널을 올릴지(티저 → 본편 → 후속 Q&A·반응 콘텐츠 구조), 각 게시물의 핵심 메시지 한 줄, 채널 간 상호 링크(블로그↔숏폼↔카드뉴스) 연결 방법, 그리고 이 캠페인의 측정 지표 3개(예: 숏폼 조회수, 블로그 유입, 계산기 클릭).
■ 시리즈 운영 메모
   이 #{s['xf_episode']} 다음 회차 소재 후보 3개, '권리금 X-파일'을 콘텐츠 IP로 키우기 위한 고정 포맷 제안(인트로 멘트 1줄·아웃트로 1줄·썸네일/표지 규칙·시리즈 해시태그).
"""

# ---------------------------------------------------------------------
# 실행
# ---------------------------------------------------------------------
st.divider()
if st.button("🚀 권리금 X-파일 캠페인 생성 (진단 → 옴니채널 → 배포 플랜)"):
    if not (st.session_state["xf_category"] or "").strip():
        st.warning("업종은 반드시 입력해야 합니다.")
    elif not st.session_state["xf_channels"]:
        st.warning("제작할 채널을 1개 이상 선택하세요.")
    else:
        with st.spinner("1/2 · RV-19 프레임워크로 케이스를 정밀 진단 중입니다..."):
            diagnostic = get_gemini_response(build_diag_prompt(), API_KEY)
        if isinstance(diagnostic, str) and diagnostic.startswith("❌"):
            st.error(diagnostic)
            st.session_state.pop("xf_result", None)
        else:
            with st.spinner("2/2 · 진단 결과를 바탕으로 옴니채널 캠페인 + 14일 배포 플랜을 제작 중입니다..."):
                campaign = get_gemini_response(build_campaign_prompt(diagnostic), API_KEY)
            st.session_state["xf_result"] = {
                "episode": st.session_state["xf_episode"],
                "channels": list(st.session_state["xf_channels"]),
                "diagnostic": diagnostic,
                "campaign": campaign,
            }

# ---------------------------------------------------------------------
# 결과 표시 (탭)
# ---------------------------------------------------------------------
res = st.session_state.get("xf_result")
if res:
    err = isinstance(res["campaign"], str) and res["campaign"].startswith("❌")
    if err:
        st.warning("진단은 완료됐지만 캠페인 생성 단계에서 오류가 발생했습니다. 채널 수를 줄이거나 다시 시도해 보세요.")
    else:
        st.success(f"✅ 권리금 X-파일 #{res['episode']} 캠페인 생성 완료 · 진단 + {len(res['channels'])}개 채널 + 14일 배포 플랜")

    tab1, tab2, tab3 = st.tabs(["🔬 권리금 정밀 진단 리포트", "📦 옴니채널 콘텐츠 캠페인", "ℹ️ 이 캠페인 구성"])
    with tab1:
        st.text_area("진단 리포트 (복사 아이콘 사용)", value=res["diagnostic"], height=620, key="xf_out_diag")
    with tab2:
        if err:
            st.error(res["campaign"])
        else:
            st.text_area("옴니채널 캠페인 + 14일 배포 플랜 (복사 아이콘 사용)", value=res["campaign"], height=720, key="xf_out_camp")
    with tab3:
        st.markdown(
            f"""
- 시리즈 회차: 권리금 X-파일 #{res['episode']}
- 포함 채널 ({len(res['channels'])}개): {', '.join(res['channels'])}
- 코어 프레임워크: 대구상가맨 RV-19 (19개 평가 항목)
- 보이스: 오석민 시그니처 톤 락
- 사용법: ① 진단 리포트로 케이스의 팩트와 결론을 잡고 → ② 옴니채널 캠페인의 각 채널 블록을 그대로 가져가 발행하며 → ③ 14일 배포 플랜 순서대로 운영하고 측정 지표를 기록하세요.
- 다음 회차: 입력 폼 상단의 'X-파일 시리즈 회차 #'를 올리고 새 케이스를 넣으면 시리즈가 누적됩니다.
"""
        )
