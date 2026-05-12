# =====================================================================
# 대구상가맨 통합 마케팅 퍼널 콘솔 (Marketing Funnel HUB) v1.0
# ---------------------------------------------------------------------
# sangaman.com 홈페이지로의 유입을 만드는 모든 마케팅 퍼널 도구를 한 곳에.
# "최소한의 노력으로 최대한의 마케팅 성과" — 원클릭 통합 캠페인이 핵심.
#
# 탑재 도구
#   ⚡ 원클릭 통합 캠페인   : 주제(또는 권리금 케이스) 1개 → 블로그·숏폼·카드뉴스
#                            ·지식인·유튜브쇼츠·X·카카오 + 14일 배포 플랜을 한 번에
#   🔬 권리금 X-파일 엔진   : 케이스 정밀 진단(RV-19) → 옴니채널 캠페인
#   ✍️ 블로그 장문 SEO 원고 : 네이버 C-Rank/DIA 최적화 3,000자 + 해시태그 20
#   🎬 틱톡·릴스 60초 대본  : 0~3초 후크 / 타임코드 콘티 / CTA / 해시태그
#   📸 인스타 카드뉴스      : 표지~마지막 카드 + 캡션 + 해시태그 30 + 스토리 문구
#   💬 지식인·카페 답변     : 실제 질문 → 도움 위주 답변 + 홍보 수위 조절
#   🔑 키워드·소재 발굴     : 핵심/롱테일 키워드 + 소재 30 + 30일 캘린더
#   📺 유튜브 숏폼·롱폼     : 제목/썸네일/후크/콘티/설명란/태그/고정댓글
#   🗺️ 퍼널 전략 대시보드  : 4단계 흐름 + 내 상황 맞춤 90일 액션플랜
#   ⚙️ 알고리즘 가이드     : 네이버·틱톡·인스타·유튜브 랭킹 신호 + 적용 체크리스트
#
# 모든 콘텐츠 프롬프트에 2025~2026 플랫폼 알고리즘 최적화 규칙(ALGO_RULES)이 내장됨.
# 실행:  streamlit run hub.py   (접근 비밀번호: 0810)
# =====================================================================
import os
import streamlit as st

st.set_page_config(page_title="대구상가맨 마케팅 허브", page_icon="🎯", layout="wide")

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

# =====================================================================
# 코어 자산 — 브랜드 / 보이스 / 프레임워크 / 알고리즘 규칙
# =====================================================================
BRAND_CONTEXT = """
[브랜드 — 반드시 이 정체성으로]
- 화자: '대구상가맨' 오석민 대표 (15년 차 상가 양도양수·프랜차이즈 창업 전문가)
- 핵심 서비스: 무료 '전문가용 권리금 계산기'(19가지 실무 변수로 1초 만에 진짜 가치 산출),
  양수자(매수자) 수수료 0원, 17~19페이지 정밀 실사 보고서, 오석민 대표가 직접 검증한 S등급 매물 중개
- 타겟 1: 예비 창업자 — 부풀려진 권리금·권리금 사기 피해가 두려운 사람
- 타겟 2: 기존 점주·자영업자 — 후려치기 없이 빠르고 안전하게 매장을 매각(Exit)하고 싶은 사람
- 톤: 팩트 기반, 베테랑의 신뢰감, 과장 없는 단호함, 필요할 때 냉정한 경고
- 공식 사이트: www.sangaman.com / 1:1 팩트 상담 전화: 010-4570-8889 / 카카오톡 상담 가능
[작성 금지]
- 마크다운 특수기호(별표 **, 샵 #, 불릿 - 등) 사용 금지. 사람이 그대로 복사해 올릴 수 있는 평문(Plain text)으로만.
- 세금·4대보험·원가율 등 예비 창업자가 부담을 느낄 세부 차감 내역 언급 금지.
- 사용자가 입력하지 않은 매출·수익·권리금·면적 수치를 임의로 지어내지 말 것. 모르면 '추가 자료 필요'로 표기.
- 정보는 진짜로 도움이 되게 쓰되, 마지막에 자연스럽게 대구상가맨으로 연결할 것.
"""

OSM_VOICE = """
[오석민 시그니처 보이스 — 모든 콘텐츠가 이 목소리로]
- 1인칭 경험 단언: "제가 15년간 대구 현장에서 본 바로는" 식으로 권위 있게.
- 숫자·팩트 먼저, 감정 나중. '느낌'이 아니라 '수치'와 '검증 가능성'으로 말한다.
- 거품은 거품이라 말하되, 단정적 '사기' 매도는 하지 않는다. "이건 위험 신호입니다" 수준의 경고.
- 예비 창업자에겐 보호자, 기존 점주에겐 안전한 매각 조력자. 양쪽 어느 편도 적대시하지 않는다.
- 마무리는 늘 "직접 계산해 보시라"는 권유. 협박·강요 금지.
"""

# 2025~2026 플랫폼 알고리즘 최적화 규칙 (조사 기반, 모든 콘텐츠 프롬프트에 주입)
ALGO_RULES = """
[2025~2026 플랫폼 알고리즘 최적화 규칙 — 생성하는 모든 콘텐츠가 충족할 것]
공통(틱톡·릴스·쇼츠·블로그 불문):
- 콜드스타트 통과: 영상은 0~3초, 글은 첫 문장에서 시청자가 스크롤을 멈추게 만드는 후크가 반드시 있어야 한다("어? 이거 내 얘긴데" 효과).
- 시청 완주율·체류시간이 최상위 신호: 늘어지는 도입 금지. 궁금증을 먼저 띄우고 뒤에서 해소하는 구성으로 끝까지 보게 만든다.
- 공유 유발 결말: 친구·동료에게 보내고 싶게 만드는 한 문장을 끝에 둔다. (저장·DM 공유는 좋아요보다 3~5배 강한 신호 — 인스타 공식)
- 멀티모달: 핵심 키워드를 자막·내레이션·화면 텍스트로도 노출한다(추천 AI가 음성·화면까지 읽음).
- 오리지널 우선: 다른 플랫폼 워터마크 박힌 재업로드 금지, 채널 톤 일관성 유지.
네이버 검색(C-Rank · DIA · DIA+ · 스마트블록):
- C-Rank(출처 신뢰도 누적): '권리금/양도양수/대구 상가' 단일 주제에 집중하고 꾸준히 쓴다. 잡주제를 섞지 않는다.
- DIA(문서 품질): 직접 경험, 구체적 수치, 확인해야 할 서류명, 사진/자료를 본문에 담는다. 정보 없는 키워드 반복은 탈락.
- DIA+(검색 의도): 의도별로 글 형식을 분기한다 — 계산·시세형 / 사기 예방형 / 절차 안내형은 각각 다르게.
- 스마트블록: 1등 욕심보다 '의도 블록'에 들어가게 — '○○하는 법', 체크리스트, Q&A, 비교(미신 vs 팩트) 형식을 적극 활용.
유튜브: 클릭률(썸네일·제목) × 평균 시청 지속률 × 만족도(좋아요·끝까지 시청·공유). 쇼츠는 반복 재생·완주율 중심.
퍼널 관점: 모든 콘텐츠의 종착점 CTA는 'sangaman.com 무료 권리금 계산기 사용'으로 통일한다(활성화 이벤트).
"""

BRAND_CTA_SHORT = (
    "권리금, 아직도 감으로 결정하세요? RV-19 실무 변수로 1초 만에 내 매장 진짜 가치 확인 — "
    "무료 권리금 계산기 www.sangaman.com / 1:1 팩트 상담 010-4570-8889 (양수자 수수료 0원)"
)

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

GRADE_LOGIC = {
    "S등급 (초핵심)": "압도적 유동인구와 랜드마크 가치를 강조. 선점의 시급성과 고매출 팩트를 중심으로 서술.",
    "A등급 (우량)": "탄탄한 배후 수요와 안정적 수익 밸런스 강조. 리스크가 낮은 우량 자산임을 부각.",
    "B등급 (실속)": "가성비 창업과 효율적 운영 강조. 임대료 부담을 줄인 실속 있는 수익 구조를 중심으로 서술.",
    "C등급 (틈새)": "최소 비용 창업과 리스크 방어 강조. 전문가의 정밀 실사가 생존의 필수 조건임을 냉철하게 경고.",
}

# 옴니채널 캠페인의 채널별 제작 스펙
CHANNEL_SPECS = {
    "네이버 블로그 장문(SEO)": (
        "네이버 SEO 최적화 스토리텔링 포스팅. 맨 위에 [블로그 제목]을 C-Rank/DIA에 맞게 자동 창작해 먼저 출력. "
        "공백 포함 2,500자 이상, 도입부 첫 문장에 '{region} {category}'를 자연스럽게 사용(스마트블록 의도 매칭). "
        "직접 경험·구체 수치·확인 서류를 본문에 포함. 본문 끝에 해시태그 20개를 띄어쓰기로 한 줄."
    ),
    "틱톡·릴스 60초 대본": (
        "0~3초 후크([화면 자막]/[멘트]/[연출]) → 3~50초 본문(5초 단위 타임코드, 구간별 [멘트]/[자막]/[B롤 연출]) "
        "→ 50~60초 CTA + 공유 유발 결말. 추천 BGM 무드 + 편집 팁 + 해시태그(틱톡 6 / 인스타 12) 한 줄씩."
    ),
    "인스타 카드뉴스+캡션": (
        "표지~8장 카드 각각 [헤드라인]/[본문]/[디자인 노트], 마지막 카드는 저장·DM공유 유도 CTA. "
        "인스타 캡션(첫 줄 후크→본문→CTA), 해시태그 30개 한 줄, 인스타 스토리용 짧은 텍스트 2종."
    ),
    "유튜브 쇼츠 스크립트": (
        "영상 제목 3안 + 썸네일 문구 3안 + 0~15초 후크 + 본문 콘티([멘트]/[자료화면 지시]/[강조 자막]) + 마무리 CTA "
        "+ 설명란(요약·링크·해시태그 5) + 검색 태그 15개 + 고정 댓글 1개."
    ),
    "네이버 지식인 답변": (
        "이 주제와 똑같은 고민의 질문에 오석민이 답하는 형태. 권리금 적정성 판단법·확인 서류 등 실무 정보 위주, "
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
# UI 스타일 + 헤더
# ---------------------------------------------------------------------
st.markdown(
    """
    <style>
    html, body, [class*="css"], .stTextInput>div>div>input, .stSelectbox>div>div>div { font-size: 15px !important; }
    .stButton>button { font-size: 17px !important; font-weight: bold; height: 3em; width: 100%; }
    .hub-hero { background: linear-gradient(135deg,#0b132b 0%,#1c2541 45%,#3a506b 100%);
        color:#fff; padding: 22px 26px; border-radius: 14px; margin-bottom: 14px; }
    .hub-hero h1 { color:#fff; margin:0; font-size:25px; line-height:1.25; }
    .hub-hero p { color:#cfe3ff; margin:8px 0 0; font-size:14px; }
    .hub-badge { display:inline-block; background:rgba(255,255,255,.13); border:1px solid rgba(255,255,255,.3);
        padding:3px 11px; border-radius:999px; font-size:12px; margin:10px 8px 0 0; color:#eaf3ff; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# 보안 인증 (0810)
# ---------------------------------------------------------------------
if "password_correct" not in st.session_state:
    st.title("🔒 대구상가맨 마케팅 허브 — 보안 인증")
    pwd_input = st.text_input("접근 비밀번호를 입력하십시오", type="password")
    if st.button("인증 가동"):
        if pwd_input == "0810":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("비밀번호 불일치")
    st.stop()

# ---------------------------------------------------------------------
# 공통 헬퍼
# ---------------------------------------------------------------------
def show_result(result, success_msg="✅ 생성 완료. 결과창 우측 상단 복사 아이콘으로 가져가세요.", height=620, key=None):
    if isinstance(result, str) and result.startswith("❌"):
        st.error(result)
    else:
        st.success(success_msg)
        st.text_area("출력 결과", value=result, height=height, key=key)


def opt(label, value):
    value = (value or "").strip() if isinstance(value, str) else value
    if value in (None, "", []):
        return ""
    return f"- {label}: {value}\n"


def kv(label, value):
    value = (value or "").strip() if isinstance(value, str) else value
    return f"- {label}: {value if value not in (None, '', []) else '미입력'}\n"


def store(key, payload):
    st.session_state[key] = payload


# =====================================================================
# ⚡ 1. 원클릭 통합 캠페인
# =====================================================================
def page_oneclick():
    st.markdown(
        """
        <div class="hub-hero">
          <h1>⚡ 원클릭 통합 캠페인</h1>
          <p>주제(또는 권리금 케이스) 하나 → 블로그·숏폼·카드뉴스·지식인·유튜브쇼츠·X·카카오 + 14일 배포 플랜이 한 번에.</p>
          <span class="hub-badge">2025~2026 플랫폼 알고리즘 규칙 내장</span>
          <span class="hub-badge">옴니채널 일관성</span>
          <span class="hub-badge">RV-19 진단 옵션</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mode = st.radio("시작 방식", ["주제로 시작 (가장 빠름)", "권리금 케이스로 시작 (RV-19 정밀 진단 포함)"], horizontal=True)

    if mode.startswith("주제"):
        topic = st.text_input("🎯 캠페인 주제/소재 (필수)", placeholder="예: 권리금 사기 안 당하는 법 / 대구 뜨는 상권 TOP5 / '무권리'라는 말의 함정 / 폐업 vs 양도 뭐가 이득")
        col1, col2 = st.columns(2)
        with col1:
            region = st.text_input("📍 지역", value="대구")
            category = st.text_input("🏢 관련 업종/분야 (선택)", placeholder="예: 고깃집, 카페, 무인점포, 프랜차이즈")
        with col2:
            target = st.selectbox("👥 타겟", ["예비 창업자", "기존 점주·자영업자 (매각 희망)", "둘 다 (예비 창업자 + 기존 점주)"])
            tone = st.selectbox("🗣️ 톤 강도", ["신뢰·단호 (전문가 정공법)", "친근·공감 (멘토 톤)", "임팩트·경고 (충격 환기)"])
        extra = st.text_input("➕ 꼭 넣을 포인트 (선택)", placeholder="예: 양수자 수수료 0원 / 19개 변수 계산기 / 17~19페이지 정밀 실사 보고서")
        case_block = ""
        episode = st.number_input("🔢 시리즈 회차 # (선택, '권리금 X-파일'로 묶고 싶을 때)", min_value=0, max_value=999, value=0, step=1)
    else:
        col1, col2 = st.columns(2)
        with col1:
            region = st.text_input("📍 지역 (구체적으로)", value="대구 수성구")
            category = st.text_input("🏢 업종 (필수)", placeholder="예: 한우 정육식당 / 무인 아이스크림 / 헤어샵")
            asking = st.text_input("💵 매도자 호가 권리금 (선택)", placeholder="예: 권리금 1억 8,000만 원 호가")
        with col2:
            revenue = st.text_input("💰 월평균 매출 (선택)", placeholder="예: 월 8,500만 원 (POS 자료 제시 가능)")
            target = st.selectbox("👥 타겟", ["예비 창업자", "기존 점주·자영업자 (매각 희망)", "둘 다 (예비 창업자 + 기존 점주)"])
            tone = st.selectbox("🗣️ 톤 강도", ["신뢰·단호 (전문가 정공법)", "친근·공감 (멘토 톤)", "임팩트·경고 (충격 환기)"])
        loc = st.text_input("📌 입지·시설·임대차·양도사유 등 알려진 사실 (선택)", placeholder="예: 코너 1층, 전용 주차 6대, 임대차 잔여 1년 2개월, 건강 문제로 급매 주장, 직전 2년 자료 미공개")
        extra = st.text_input("➕ 꼭 넣을 포인트 (선택)", placeholder="예: 양수자 수수료 0원 강조")
        episode = st.number_input("🔢 권리금 X-파일 시리즈 회차 #", min_value=1, max_value=999, value=1, step=1)
        topic = f"{region} {category} 양도양수 케이스 진단"
        case_block = (
            kv("지역", region) + kv("업종", category) + kv("매도자 호가 권리금", asking)
            + kv("월평균 매출", revenue) + kv("입지·시설·임대차·양도사유 등", loc) + kv("그 밖의 포인트", extra)
        )

    st.write("")
    channels = st.multiselect(
        "📡 제작할 채널 (체크한 채널을 같은 주제·같은 결론으로 일제히 생성)",
        list(CHANNEL_SPECS.keys()),
        default=["네이버 블로그 장문(SEO)", "틱톡·릴스 60초 대본", "인스타 카드뉴스+캡션", "유튜브 쇼츠 스크립트", "네이버 지식인 답변"],
    )
    st.caption("⚖️ 실제 케이스를 다룰 땐 상호·정확한 위치는 비공개, 사실관계 확인된 내용만, 단정적 '사기' 단정이 아닌 '위험 신호' 수준으로. 입력 안 한 수치는 엔진이 만들지 않습니다.")

    if st.button("⚡ 원클릭 통합 캠페인 생성"):
        if mode.startswith("주제") and not (topic or "").strip():
            st.warning("캠페인 주제/소재를 입력하세요.")
            return
        if mode.startswith("권리금") and not (category or "").strip():
            st.warning("업종은 반드시 입력해야 합니다.")
            return
        if not channels:
            st.warning("제작할 채널을 1개 이상 선택하세요.")
            return

        series_tag = f"권리금 X-파일 #{int(episode)}" if episode and int(episode) > 0 else "단발 캠페인"
        specs = "\n".join(f"■ {name}\n   {CHANNEL_SPECS[name].format(region=region or '대구', category=category or '해당 업종')}" for name in channels)

        diagnostic_text = ""
        if mode.startswith("권리금"):
            with st.spinner("1/2 · RV-19 프레임워크로 케이스를 정밀 진단 중입니다..."):
                diag_prompt = f"""{BRAND_CONTEXT}
{OSM_VOICE}
{RV19_FRAMEWORK}

당신은 '대구상가맨' 오석민 대표입니다. 아래 양도양수 케이스를 RV-19 프레임워크로 정밀 진단하십시오.

[케이스 — {series_tag}]
{case_block}
[출력 — 평문. 제목 "대구상가맨 권리금 정밀 진단 리포트 — {series_tag}"]
1) 한 줄 판정: [거품 / 적정 / 저평가 / 자료 부족 / 사기 위험 신호] 중 하나 + 근거 한 문장
2) RV-19 항목별 평가: 19개 항목 각각 [상/중/하/판단불가] + 1줄 코멘트
3) 적정 권리금 밴드: 입력된 호가·매출 기준 상대 평가 밴드만 제시(없는 수치 지어내기 금지). 부족하면 필요한 자료 명시.
4) 핵심 리스크 TOP 3 + 각각의 검증/방어 방법
5) 협상 포인트 3가지
6) 즉시 액션 (요청할 자료 목록 포함)
7) 신뢰 라벨 한 줄: "본 진단은 대구상가맨 RV-19 프레임워크와 17~19페이지 정밀 실사 보고서 기준입니다. 무료 권리금 계산기 www.sangaman.com / 상담 010-4570-8889 (양수자 수수료 0원)"
"""
                diagnostic_text = get_gemini_response(diag_prompt, API_KEY)
            if isinstance(diagnostic_text, str) and diagnostic_text.startswith("❌"):
                st.error(diagnostic_text)
                return

        diag_ref = f"[참고 — 위 케이스의 정밀 진단 리포트. 콘텐츠의 뼈대로 삼되 모순되지 않게]\n{diagnostic_text}\n" if diagnostic_text else ""
        with st.spinner(("2/2 · " if mode.startswith("권리금") else "") + "옴니채널 콘텐츠 캠페인 + 14일 배포 플랜을 제작 중입니다..."):
            camp_prompt = f"""{BRAND_CONTEXT}
{OSM_VOICE}
{ALGO_RULES}

당신은 '대구상가맨' 오석민 대표의 콘텐츠 PD입니다.
아래 주제로 옴니채널 콘텐츠 캠페인을 제작하십시오. 모든 채널 콘텐츠는 같은 주제·같은 핵심 메시지·같은 결론을 공유해야 합니다.

[캠페인 정보]
- 주제/소재: {topic}
- 시리즈: {series_tag}  (시리즈명이 '단발 캠페인'이 아니면 제목·도입부에 회차를 자연스럽게 노출)
- 지역/업종: {region or '대구'} / {category or '해당 업종'}
- 타겟: {target}
- 톤 강도: {tone}
{opt('꼭 넣을 포인트', extra)}{diag_ref}
[먼저 출력]
■ 콘텐츠 코어 브리프
   - 한 줄 핵심 메시지 / 후크 후보 3개 / 근거·팩트 포인트 3개 / 통일 CTA 문구 1개("{BRAND_CTA_SHORT}" 취지)

[다음 — 아래 선택된 채널만, 각각 '■ 채널명' 헤더로 명확히 구분해 제작]
{specs}

[모든 채널 공통 규칙]
- 위 [플랫폼 알고리즘 최적화 규칙]을 빠짐없이 반영(첫 3초/첫 문장 후크, 완주 유도, 공유 유발 결말, 멀티모달 키워드, 네이버 C-Rank/DIA/스마트블록 대응).
- 신뢰 장치('RV-19 프레임워크', '양수자 수수료 0원', '17~19페이지 정밀 실사 보고서') 중 맥락에 맞는 것 1~2개 자연스럽게 삽입.
- 끝의 CTA는 "{BRAND_CTA_SHORT}" 취지를 채널 톤에 맞게 변형.
- 평문 출력, 마크다운 특수기호 금지, 차감 내역 언급 금지, 없는 수치 지어내기 금지.

[채널 블록들 뒤에 반드시 추가]
■ 14일 배포 플랜
   Day 1~14 중 어느 날 어떤 채널을 올릴지(티저 → 본편 → 후속 Q&A 구조), 각 게시물 핵심 메시지 한 줄, 채널 간 상호 링크(블로그↔숏폼↔카드뉴스) 방법, 측정 지표 3개(예: 숏폼 조회수·블로그 유입·계산기 클릭).
■ 다음 회차 소재 후보 3개
"""
            campaign_text = get_gemini_response(camp_prompt, API_KEY)
        store("oc_result", {"topic": topic, "series": series_tag, "channels": list(channels), "diagnostic": diagnostic_text, "campaign": campaign_text})

    res = st.session_state.get("oc_result")
    if res:
        err = isinstance(res["campaign"], str) and res["campaign"].startswith("❌")
        if err:
            st.error(res["campaign"])
        else:
            st.success(f"✅ '{res['series']}' 통합 캠페인 생성 완료 · {len(res['channels'])}개 채널" + (" · RV-19 진단 포함" if res["diagnostic"] else "") + " · 14일 배포 플랜")
        tabs = st.tabs((["🔬 권리금 정밀 진단"] if res["diagnostic"] else []) + ["📦 옴니채널 캠페인 + 배포 플랜"])
        idx = 0
        if res["diagnostic"]:
            with tabs[0]:
                st.text_area("진단 리포트", value=res["diagnostic"], height=600, key="oc_out_diag")
            idx = 1
        with tabs[idx]:
            if err:
                st.error(res["campaign"])
            else:
                st.text_area("옴니채널 캠페인 + 14일 배포 플랜", value=res["campaign"], height=760, key="oc_out_camp")


# =====================================================================
# 🔬 2. 권리금 X-파일 엔진 (전체 케이스 입력 → 진단 → 캠페인)
# =====================================================================
def page_xfile():
    st.title("🔬 권리금 X-파일 엔진")
    st.caption("케이스 풀입력 → RV-19 정밀 진단 → 옴니채널 콘텐츠 캠페인 + 14일 배포 플랜 + 시리즈 운영 메모.")

    DEFAULTS = {
        "xf_case_type": "가상 시뮬레이션 (교육·인지용)", "xf_episode": 1, "xf_region": "대구", "xf_category": "",
        "xf_brand": "", "xf_area": "", "xf_deposit": "", "xf_rent": "", "xf_asking": "", "xf_revenue": "",
        "xf_profit": "", "xf_composition": "", "xf_locfeat": "", "xf_reason": "", "xf_lease": "", "xf_extra": "",
        "xf_target": "둘 다 (예비 창업자 + 기존 점주)", "xf_disclosure": "익명 처리 (상호·정확한 위치 비공개)",
        "xf_tone": "신뢰·단호 (전문가 정공법)",
        "xf_channels": ["네이버 블로그 장문(SEO)", "틱톡·릴스 60초 대본", "인스타 카드뉴스+캡션", "네이버 지식인 답변"],
    }
    for k, v in DEFAULTS.items():
        st.session_state.setdefault(k, v)
    DEMO = {
        "xf_case_type": "가상 시뮬레이션 (교육·인지용)", "xf_episode": 7, "xf_region": "대구 수성구 들안길",
        "xf_category": "한우 정육식당 (점심·저녁 겸업)", "xf_brand": "", "xf_area": "1층 60평 (홀 50 / 주방 10)",
        "xf_deposit": "5,000만 원", "xf_rent": "월 380만 원", "xf_asking": "권리금 1억 8,000만 원 호가",
        "xf_revenue": "월평균 8,500만 원 (POS 자료 제시 가능)", "xf_profit": "월평균 1,600만 원 (양도자 구두 주장)",
        "xf_composition": "시설 8,000 / 영업 7,000 / 바닥 3,000 (양도자 구분)",
        "xf_locfeat": "들안길 메인, 코너 1층, 전용 주차 6대, 인근 신축 오피스텔 입주 진행 중",
        "xf_reason": "양도자 건강 문제로 급매라고 주장", "xf_lease": "임대차 잔여 1년 2개월, 갱신요구권 일부 소진",
        "xf_extra": "최근 6개월 매출 우상향 강조하나 직전 2년치 자료는 미공개", "xf_target": "예비 창업자",
        "xf_disclosure": "익명 처리 (상호·정확한 위치 비공개)", "xf_tone": "신뢰·단호 (전문가 정공법)",
        "xf_channels": ["네이버 블로그 장문(SEO)", "틱톡·릴스 60초 대본", "인스타 카드뉴스+캡션", "유튜브 쇼츠 스크립트", "네이버 지식인 답변"],
    }
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎲 데모 케이스 불러오기"):
            st.session_state.update(DEMO)
            st.rerun()
    with c2:
        if st.button("🧹 입력 초기화"):
            for k, v in DEFAULTS.items():
                st.session_state[k] = v
            st.session_state.pop("xf_result", None)
            st.rerun()

    st.subheader("1️⃣ 케이스 입력")
    cA, cB = st.columns(2)
    with cA:
        st.selectbox("케이스 유형", ["가상 시뮬레이션 (교육·인지용)", "실제 익명 케이스 (사실관계 확인됨)", "보유 매물 홍보용"], key="xf_case_type")
        st.text_input("📍 지역 (구체적으로)", key="xf_region", placeholder="예: 대구 수성구 들안길 / 동성로 / 칠곡 강변대로")
        st.text_input("🏢 업종 (필수)", key="xf_category", placeholder="예: 한우 정육식당 / 무인 아이스크림 / 헤어샵")
        st.text_input("🏷️ 브랜드명 (선택)", key="xf_brand", placeholder="예: 하남돼지집 (개인/일반이면 비워두기)")
        st.text_input("📐 면적/구성 (선택)", key="xf_area", placeholder="예: 1층 60평 (홀 50 / 주방 10)")
        st.number_input("🔢 권리금 X-파일 시리즈 회차 #", min_value=1, max_value=999, step=1, key="xf_episode")
    with cB:
        st.text_input("💵 매도자 호가 권리금 (선택)", key="xf_asking", placeholder="예: 권리금 1억 8,000만 원 호가")
        st.text_input("🏦 보증금 (선택)", key="xf_deposit", placeholder="예: 5,000만 원")
        st.text_input("🏦 월세 (선택)", key="xf_rent", placeholder="예: 월 380만 원")
        st.text_input("💰 월평균 매출 (선택)", key="xf_revenue", placeholder="예: 월 8,500만 원 (POS 자료 제시 가능 여부도)")
        st.text_input("📈 월평균 수익 (선택)", key="xf_profit", placeholder="예: 월 1,600만 원 (양도자 구두 주장)")
        st.text_input("🧩 권리금 구성 시설/영업/바닥 (선택)", key="xf_composition", placeholder="예: 시설 8,000 / 영업 7,000 / 바닥 3,000")
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
    st.multiselect("📡 제작할 채널 (옴니채널)", list(CHANNEL_SPECS.keys()), key="xf_channels")
    st.caption("⚖️ 실제 케이스는 상호·정확한 위치 비공개, 사실관계 확인된 내용만, '사기' 단정이 아닌 '위험 신호' 수준으로. 입력 안 한 수치는 엔진이 만들지 않습니다.")

    def line(label, key):
        v = st.session_state.get(key)
        v = (v or "").strip() if isinstance(v, str) else v
        return f"- {label}: {v if v not in (None, '', []) else '미입력'}\n"

    if st.button("🚀 권리금 X-파일 캠페인 생성 (진단 → 옴니채널 → 배포 플랜)"):
        s = st.session_state
        if not (s["xf_category"] or "").strip():
            st.warning("업종은 반드시 입력해야 합니다.")
            return
        if not s["xf_channels"]:
            st.warning("제작할 채널을 1개 이상 선택하세요.")
            return
        region = (s["xf_region"] or "대구").strip()
        with st.spinner("1/2 · RV-19 프레임워크로 케이스를 정밀 진단 중입니다..."):
            diag_prompt = f"""{BRAND_CONTEXT}
{OSM_VOICE}
{RV19_FRAMEWORK}

당신은 '대구상가맨' 오석민 대표입니다. 아래 양도양수 케이스를 RV-19 프레임워크로 정밀 진단하십시오.

[케이스 #{s['xf_episode']}]
- 케이스 유형: {s['xf_case_type']}
- 공개 수위: {s['xf_disclosure']}
{line('지역','xf_region')}{line('업종','xf_category')}{line('브랜드','xf_brand')}{line('면적/구성','xf_area')}{line('보증금','xf_deposit')}{line('월세','xf_rent')}{line('매도자 호가 권리금','xf_asking')}{line('월평균 매출','xf_revenue')}{line('월평균 수익','xf_profit')}{line('권리금 구성(시설/영업/바닥)','xf_composition')}{line('입지·시설 특징','xf_locfeat')}{line('양도 사유','xf_reason')}{line('임대차 잔여기간·갱신권','xf_lease')}{line('그 밖의 사실','xf_extra')}
[출력 — 평문. 제목 "대구상가맨 권리금 정밀 진단 리포트 — X-파일 #{s['xf_episode']}"]
1) 한 줄 판정: [거품 / 적정 / 저평가 / 자료 부족 / 사기 위험 신호] 중 하나 + 근거 한 문장
2) RV-19 항목별 평가: 위 19개 항목을 번호 그대로, 각 [상/중/하/판단불가] + 1줄 코멘트
3) 적정 권리금 밴드: 입력된 호가·매출 등을 기준으로 한 상대 평가 밴드만 제시. 부족하면 필요한 자료(직전 2년 POS, 카드매출 신고서, 임대차계약서, 시설 견적 등) 명시. 없는 수치 새로 만들기 금지.
4) 핵심 리스크 TOP 3 + 각각의 검증/방어 방법
5) 협상 포인트 3가지
6) 즉시 액션 (요청할 자료 목록 포함)
7) 신뢰 라벨 한 줄: "본 진단은 대구상가맨 RV-19 프레임워크와 17~19페이지 정밀 실사 보고서 기준입니다. 무료 권리금 계산기 www.sangaman.com / 상담 010-4570-8889 (양수자 수수료 0원)"
"""
            diagnostic = get_gemini_response(diag_prompt, API_KEY)
        if isinstance(diagnostic, str) and diagnostic.startswith("❌"):
            st.error(diagnostic)
            return
        chosen = s["xf_channels"]
        specs = "\n".join(f"■ {n}\n   {CHANNEL_SPECS[n].format(region=region, category=(s['xf_category'] or '해당 업종').strip())}" for n in chosen)
        with st.spinner("2/2 · 진단 결과 기반 옴니채널 캠페인 + 14일 배포 플랜을 제작 중입니다..."):
            camp_prompt = f"""{BRAND_CONTEXT}
{OSM_VOICE}
{ALGO_RULES}

당신은 '대구상가맨' 오석민 대표의 콘텐츠 PD입니다.
아래 [진단 리포트]를 원천 소스로 '권리금 X-파일 #{s['xf_episode']}' 시리즈 옴니채널 캠페인을 제작하십시오.
모든 채널 콘텐츠는 같은 케이스·같은 결론·같은 시리즈 정체성을 공유하며 진단과 모순되면 안 됩니다.

[케이스 요약]
- 시리즈: 권리금 X-파일 #{s['xf_episode']}
- 지역/업종: {region} / {(s['xf_category'] or '해당 업종').strip()}  (브랜드: {(s['xf_brand'] or '개인/일반').strip()})
- 호가 권리금: {(s['xf_asking'] or '비공개').strip()}
- 공개 수위: {s['xf_disclosure']} → 실제 케이스면 상호·정확한 위치 비공개, '사기' 단정 금지('위험 신호' 수준)
- 타겟: {s['xf_target']} / 톤: {s['xf_tone']}

[진단 리포트 — 콘텐츠의 뼈대]
{diagnostic}

[제작할 채널 — 아래 항목만, 각각 '■ 채널명'으로 시작하는 블록으로]
{specs}

[모든 채널 공통 규칙]
- 위 [플랫폼 알고리즘 최적화 규칙] 빠짐없이 반영.
- 시리즈 브랜딩: 제목·도입부에 '권리금 X-파일'과 #{s['xf_episode']} 자연스럽게 노출.
- 신뢰 장치('RV-19 프레임워크','양수자 수수료 0원','17~19페이지 정밀 실사 보고서') 중 1~2개 자연스럽게.
- CTA는 "{BRAND_CTA_SHORT}" 취지를 채널 톤에 맞게.
- 평문 출력, 마크다운 특수기호 금지, 차감 내역 언급 금지, 진단에 없는 수치 새로 만들기 금지.

[채널 블록들 뒤에 반드시 추가]
■ 14일 배포 플랜 — Day별 채널·순서(티저→본편→후속 Q&A), 게시물별 핵심 메시지 한 줄, 채널 간 상호 링크, 측정 지표 3개
■ 시리즈 운영 메모 — 다음 회차 소재 후보 3개, '권리금 X-파일'을 IP로 키우는 고정 포맷(인트로·아웃트로·썸네일/표지 규칙·시리즈 해시태그)
"""
            campaign = get_gemini_response(camp_prompt, API_KEY)
        store("xf_result", {"episode": s["xf_episode"], "channels": list(chosen), "diagnostic": diagnostic, "campaign": campaign})

    res = st.session_state.get("xf_result")
    if res:
        err = isinstance(res["campaign"], str) and res["campaign"].startswith("❌")
        if err:
            st.warning("진단은 완료됐지만 캠페인 생성에서 오류가 발생했습니다. 채널 수를 줄이거나 다시 시도하세요.")
        else:
            st.success(f"✅ 권리금 X-파일 #{res['episode']} 캠페인 생성 완료 · 진단 + {len(res['channels'])}개 채널 + 14일 배포 플랜")
        t1, t2 = st.tabs(["🔬 권리금 정밀 진단 리포트", "📦 옴니채널 콘텐츠 캠페인"])
        with t1:
            st.text_area("진단 리포트", value=res["diagnostic"], height=620, key="xf_out_diag")
        with t2:
            if err:
                st.error(res["campaign"])
            else:
                st.text_area("옴니채널 캠페인 + 14일 배포 플랜", value=res["campaign"], height=740, key="xf_out_camp")


# =====================================================================
# ✍️ 3. 블로그 장문 SEO 원고
# =====================================================================
def page_blog():
    st.title("✍️ 네이버 블로그 장문 SEO 원고 엔진")
    st.caption("C-Rank/DIA/스마트블록 대응. 제목·본문·해시태그 20개·하단 홍보 문구까지 100% 자동.")
    grade = st.radio("🏆 상권 등급", list(GRADE_LOGIC.keys()), horizontal=True)
    col1, col2 = st.columns(2)
    with col1:
        region = st.text_input("📍 구체적 지역명", value="대구")
        category = st.text_input("🏢 세부 업종 (필수)", value="유명 고기집")
    with col2:
        brand = st.text_input("🏷️ 프랜차이즈 브랜드명 (선택)", placeholder="예: 하남돼지집")
        ctype = st.selectbox("🔥 창업 유형", ["양도양수창업", "신규창업", "점포개발", "업종변경"])
    col3, col4 = st.columns(2)
    with col3:
        revenue = st.text_input("💰 월평균 매출 (선택)", placeholder="예: 5,000만 원")
    with col4:
        profit = st.text_input("📈 월평균 수익 (선택)", placeholder="예: 1,200만 원")
    extra_kw = st.text_input("🔑 반영할 추가 키워드 (선택, 쉼표 구분)", placeholder="예: 무권리, 독점상권, 리뉴얼 완료, 역세권")

    if st.button("✍️ 네이버 SEO 팩트 원고 100% 자동 생성"):
        if not category.strip():
            st.warning("세부 업종은 반드시 입력해야 합니다.")
            return
        has_fin = bool(revenue.strip() or profit.strip())
        has_brand = bool(brand.strip())
        if has_fin:
            merit = f"입력된 월평균 매출({revenue})·수익({profit}) 데이터를 최고의 무기로, 이 창업의 압도적 수익성과 투자 가치를 가장 강력하게 어필."
        elif has_brand:
            merit = f"매출 데이터는 없지만 '{brand}'의 프랜차이즈 브랜드 파워와 '{category}' 업종의 시너지를 집중 분석해 실패 없는 창업 메리트를 어필."
        else:
            merit = f"브랜드·매출 데이터 없이 '{category}' 업종 자체의 본질적 유망성·시장 트렌드와 {grade} 상권에서의 안정적 안착 가능성을 깊이 있게 서술."
        kw_logic = f"- 필수 포함 추가 키워드: {extra_kw}" if extra_kw.strip() else ""
        kw_inst = f"6. 추가 키워드 융합: [{extra_kw}]를 본문 문맥에 100% 자연스럽게 녹일 것." if extra_kw.strip() else ""
        with st.spinner("C-Rank/DIA 최적화 장문 원고 + 해시태그 20개를 연산 중입니다..."):
            prompt = f"""{BRAND_CONTEXT}
{OSM_VOICE}
{ALGO_RULES}

당신은 15년 차 프랜차이즈 전문가 '대구상가맨' 오석민 대표입니다. 네이버 검색 상위 노출(SEO)을 위한 3,000자 이상의 스토리텔링 포스팅을 작성하십시오.

[입력된 물리적 팩트]
- 지역: {region}
- 업종: {category}
- 브랜드: {brand if has_brand else "일반/개인 창업"}
- 상권 등급: {grade} ({GRADE_LOGIC[grade]})
- 창업 유형: {ctype}
{kw_logic}

[핵심 메리트 강조 지침]
{merit}

[작성 팩트 지침]
1. 자동 제목 추출: 본문 시작 전, 가장 위에 네이버 검색 로직(C-Rank/DIA/스마트블록)에 최적화된 [블로그 제목]을 알아서 창작해 먼저 출력.
2. 도입부 강제 규칙: 본문 첫 문장은 반드시 "{region} {category}" 키워드를 자연스럽게 사용해 출발.
3. 마크다운 금지: 별표(**)·샵(#) 등 특수기호 없이 평문으로만 출력.
4. 분량·깊이: C-Rank가 '전문가의 깊이 있는 칼럼'으로 인식하도록 공백 포함 3,000자 이상으로 논리적이고 길게. 직접 경험·구체 수치·확인 서류를 본문에 담아 DIA 가점.
5. 비용 수치 언급 금지: 세금·4대보험·원가율 등 차감 내역 절대 언급 금지.
{kw_inst}

[필수 하단 홍보 문구 — 토씨 그대로 출력]
부풀려진 권리금, 아직도 감으로 결정하십니까?
양도양수 시 발생하는 권리금 피해를 100% 원천 차단하고 여러분의 소중한 자본을 방어하기 위해, 15년 차 베테랑 대구상가맨이 직접 설계한 '전문가용 권리금 계산기'를 지금 무료로 개방합니다.
19가지 실무 변수를 대입하여 내 매장의 진짜 팩트 가치를 단 1초 만에 확인하십시오.

[대구상가맨 플랫폼이 예비 창업자와 기존 점주 모두에게 완벽한 이유]
예비 창업자: '양수자 수수료 0원' 혜택과 '17페이지 정밀 실사 보고서'로 권리금 사기를 차단하고 100% 자본 방어를 약속합니다.
기존 매장 점주 및 자영업자: 부당한 권리금 후려치기 없이, 투명하고 정확한 가치 평가를 통해 가장 빠르고 안전하게 매장을 매각(Exit)할 수 있도록 돕습니다.

창업의 시작부터 안전한 매각까지, 대구상가맨 플랫폼이 완벽한 성공 파트너가 되어 드립니다.
지금 바로 공식 사이트에 접속하여 무료 계산기를 두드려보시고, 오석민 대표가 직접 검증한 S등급 팩트 매물들을 직접 확인하십시오.

무료 권리금 계산기 및 안전 매물 확인: www.sangaman.com
1:1 팩트 상담 및 문의: 010-4570-8889

[해시태그 20개 자동 산출]
위 홍보 문구가 끝난 후, 맨 아랫줄에 본문·타겟 키워드·추가 키워드 기반으로 네이버 검색 노출 최적화 해시태그를 정확히 20개, 띄어쓰기로 구분해 한 줄로 나열.
(예시: #{region}창업 #{category}창업 #대구상가맨 #프랜차이즈창업 #소자본창업 ...)
"""
            show_result(get_gemini_response(prompt, API_KEY), key="bl_out")


# =====================================================================
# 🎬 4. 틱톡·릴스 60초 대본
# =====================================================================
def page_shortform():
    st.title("🎬 틱톡·릴스 60초 숏폼 대본 생성기")
    st.caption("0~3초 후크 → 타임코드 콘티 → 60초 CTA. 완주율·공유 유발에 최적화.")
    topic = st.text_input("🎯 영상 주제/소재 (필수)", placeholder="예: 권리금 1억 날린 치킨집 사장님 실화 / 장사 안 되는 상가의 공통점 3가지")
    col1, col2 = st.columns(2)
    with col1:
        ctype = st.selectbox("📺 콘텐츠 유형", ["사례·스토리텔링", "정보·꿀팁(체크리스트)", "충격·경고(사기·실패)", "미신 vs 팩트", "Q&A·반전", "비포 애프터", "트렌드·챌린지 편승"])
        target = st.selectbox("👥 타겟", ["예비 창업자", "기존 점주·자영업자(매각 희망)", "둘 다"])
        platform = st.selectbox("📱 주요 업로드 채널", ["틱톡", "인스타 릴스", "유튜브 쇼츠", "세 곳 모두"])
    with col2:
        tone = st.selectbox("🗣️ 톤앤매너", ["베테랑 전문가(신뢰·단호)", "친근한 형/누나(반말·솔직)", "자극적·후킹 우선", "차분한 내레이션"])
        hook = st.selectbox("🪝 오프닝 후크 스타일", ["충격 질문형", "결론 먼저 던지기형", "숫자·통계 제시형", "스토리 한복판에서 시작", "AI 추천"])
        n = st.slider("🔢 대본 버전 수", 1, 3, 2)
    extra = st.text_input("➕ 꼭 넣을 내용/멘트/사례 (선택)", placeholder="예: '양수자 수수료 0원' 강조 / 대구 동성로 상권")
    if st.button("🎬 60초 숏폼 대본 자동 생성"):
        if not topic.strip():
            st.warning("영상 주제/소재는 필수입니다.")
            return
        with st.spinner("후킹 멘트와 60초 콘티를 연산 중입니다..."):
            prompt = f"""{BRAND_CONTEXT}
{OSM_VOICE}
{ALGO_RULES}

당신은 조회수가 터지는 숏폼 전문 작가이자 '대구상가맨' 콘텐츠 PD입니다. 아래 조건으로 60초 이내 세로 영상 대본을 서로 다른 후크·전개로 {n}개 버전 작성하십시오.

[조건]
- 주제/소재: {topic}
- 콘텐츠 유형: {ctype} / 타겟: {target} / 업로드 채널: {platform}
- 톤앤매너: {tone} / 오프닝 후크 스타일: {hook}
{opt('반드시 반영할 내용', extra)}
[각 버전마다 — 평문, 마크다운 특수기호 없이]
■ 버전 N
1) 영상 제목 / 업로드 캡션 1줄
2) 영상 위 텍스트(썸네일용 한 줄, 10자 내외)
3) 0~3초 후크: [화면 자막] / [내레이션 멘트] / [화면 연출]
4) 3~50초 본문: 5초 안팎 타임코드로 끊어, 구간별 [멘트] / [화면 자막] / [B롤 연출]
5) 50~60초 CTA + 공유 유발 결말: [멘트] / [화면 자막] — "{BRAND_CTA_SHORT}" 취지
6) 추천 BGM 무드 + 편집 팁(자막 속도·효과음·컷 전환)
7) 해시태그: 틱톡 6 / 인스타 12 / 유튜브 8 — 각각 띄어쓰기로 한 줄씩

[규칙] 첫 3초 안에 멈추게. 멘트는 구어체로 짧게. 끝까지 보게 만드는 구성. 비용 차감 내역 언급 금지. 입력 안 한 수치 지어내기 금지.
"""
            show_result(get_gemini_response(prompt, API_KEY), key="sf_out")


# =====================================================================
# 📸 5. 인스타 카드뉴스 + 캡션
# =====================================================================
def page_cardnews():
    st.title("📸 인스타그램 카드뉴스 + 캡션 생성기")
    st.caption("저장·DM공유 유발형 카드 + 캡션 + 해시태그 30 + 스토리 문구.")
    topic = st.text_input("🎯 주제 (필수)", placeholder="예: 권리금 사기 안 당하는 법 / 대구 뜨는 상권 TOP5 / 양도양수 절차 한눈에")
    col1, col2 = st.columns(2)
    with col1:
        fmt = st.selectbox("🗂️ 카드뉴스 유형", ["정보 큐레이션(리스트)", "체크리스트(저장 유도)", "사례 분석(스토리)", "Q&A(질문-답)", "미신 vs 팩트(대비)", "단계별 가이드(프로세스)"])
        n = st.slider("🃏 카드 장수(표지 포함)", 5, 10, 8)
    with col2:
        target = st.selectbox("👥 타겟", ["예비 창업자", "기존 점주·자영업자", "둘 다"])
        tone = st.selectbox("🗣️ 톤", ["전문가·신뢰형", "친근·공감형", "임팩트·경고형"])
    extra = st.text_input("➕ 추가 키워드/포함 내용 (선택)", placeholder="예: 무권리 매물, 대구 수성구, 양수자 수수료 0원")
    if st.button("📸 카드뉴스 + 캡션 자동 생성"):
        if not topic.strip():
            st.warning("주제는 필수입니다.")
            return
        with st.spinner("카드 구성과 캡션을 연산 중입니다..."):
            prompt = f"""{BRAND_CONTEXT}
{OSM_VOICE}
{ALGO_RULES}

당신은 저장·공유율 높은 인스타 카드뉴스를 만드는 SNS 디자이너 겸 '대구상가맨' 운영자입니다. 아래 조건으로 카드뉴스 1세트와 부속 자산을 작성하십시오.

[조건] 주제: {topic} / 유형: {fmt} / 카드 {n}장 / 타겟: {target} / 톤: {tone}
{opt('추가 키워드/포함 내용', extra)}
[출력 — 평문, 마크다운 특수기호 없이]
1) 콘텐츠 컨셉 한 줄 요약
2) 표지 카드(1번): [메인 헤드라인 강력하게] / [서브 카피] / [디자인 노트 — 색상·이미지·폰트 톤]
3) 2번~{max(2, n-1)}번 카드: 각 카드 [헤드라인] / [본문 텍스트 짧고 명확] / [디자인 노트]
4) 마지막 카드({n}번): [저장·DM공유·프로필 링크 유도 CTA] / [디자인 노트] — "{BRAND_CTA_SHORT}" 취지
5) 인스타 캡션: 첫 줄 후크(더보기 누르게) → 본문 2~4문단 → CTA, 줄바꿈 깔끔하게
6) 해시태그 30개: 대구·지역 + 창업·양도양수 + 업종·상권 키워드 섞어 띄어쓰기로 한 줄
7) 인스타 스토리용 짧은 텍스트 2종(각 1~2줄)

[규칙] 카드 한 장당 텍스트는 모바일에서 한눈에 읽히게. DM공유 유발 한 문장 포함. 비용 차감 내역 언급 금지. 없는 수치 지어내기 금지.
"""
            show_result(get_gemini_response(prompt, API_KEY), key="cn_out")


# =====================================================================
# 💬 6. 네이버 지식인·카페 답변
# =====================================================================
def page_naver_qa():
    st.title("💬 네이버 지식인·카페 답변 생성기")
    st.caption("실제 질문 → 질문자에게 진짜 도움 되는 답변 + 자연스러운 안내.")
    st.warning("운영 원칙: ① 질문자에게 실제로 도움이 되는 내용 최우선 ② 같은 글 도배·복붙 금지(네이버 어뷰징 제재 대상) ③ 홍보 시 광고임을 숨기지 말고 운영자임을 자연스럽게 밝히기 권장", icon="⚠️")
    question = st.text_area("📥 질문/상황 원문 붙여넣기 (필수)", height=160, placeholder="예: 대구에서 고깃집을 양도양수로 인수하려는데 권리금 8천이 적정한지 모르겠어요...")
    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("📍 답변 위치", ["네이버 지식인", "네이버 카페 댓글/답글", "블로그 댓글", "오픈채팅·지역 커뮤니티"])
        stance = st.selectbox("🎓 답변 포지션", ["현장 전문가 분석", "비슷한 경험을 한 선배 점주", "중립적 정보 안내"])
    with col2:
        disclosure = st.selectbox("📣 홍보 수위", ["정보만 — 브랜드 직접 언급 안 함", "약하게 — 끝에 한 줄 자연스럽게", "명시적 — 운영자임을 밝히고 무료 도구 안내"])
        length = st.selectbox("📏 답변 길이", ["짧게 (3~5문장)", "보통 (1~2문단)", "자세히 (3문단 이상)"])
    extra = st.text_input("➕ 강조하고 싶은 포인트 (선택)", placeholder="예: 권리금 계산기 19개 변수 / 양수자 수수료 0원 / 17~19페이지 정밀 실사 보고서")
    if st.button("💬 답변 초안 생성"):
        if not question.strip():
            st.warning("질문/상황 원문을 입력하세요.")
            return
        with st.spinner("질문 맥락을 분석해 답변 초안을 연산 중입니다..."):
            prompt = f"""{BRAND_CONTEXT}
{OSM_VOICE}

당신은 '대구상가맨' 오석민 대표이자, 온라인에서 예비 창업자·점주의 질문에 진심으로 답해 주는 사람입니다. 아래 질문에 대한 {platform} 답변 초안을 작성하십시오.

[원문 질문/상황]
{question}

[답변 조건] 포지션: {stance} / 홍보 수위: {disclosure} / 길이: {length}
{opt('강조 포인트', extra)}
[작성 규칙 — 평문, 마크다운 특수기호 없이]
1) 질문자에게 실제로 도움이 되는 구체적·정확한 내용을 먼저 충실히. 두루뭉술한 영업 멘트 금지.
2) 권리금 적정성 판단법, 상권 체크포인트, 양도양수 절차·함정·필수 확인서류 등 실무 지식을 자연스럽게 녹일 것.
3) 홍보 수위:
   - 정보만: 대구상가맨/사이트/전화번호 전혀 언급 금지. 순수 조언만.
   - 약하게: 맨 끝에 한 문장 정도로만 "권리금 헷갈리면 무료로 계산해볼 도구도 있다"는 식으로 (사이트명 정도까지).
   - 명시적: 본인이 대구상가맨 운영자(오석민)임을 솔직히 밝히고 무료 권리금 계산기(www.sangaman.com)·1:1 상담(010-4570-8889, 양수자 수수료 0원) 안내. 광고임을 숨기지 말 것.
4) 사람이 직접 쓴 댓글처럼 자연스럽고 과하지 않은 구어체. 너무 길거나 상투적이지 않게.
5) 비용 차감 세부내역(세금·4대보험) 언급 금지. 질문에 없는 매출·권리금 수치 지어내기 금지.
6) 답변 본문 뒤 줄 바꿔 "[운영 팁]"으로 시작하는 한두 줄 — 올릴 때 주의점(맥락에 맞게 수정, 도배 금지, 홍보 시 광고 표기 권장).
"""
            show_result(get_gemini_response(prompt, API_KEY), success_msg="✅ 답변 초안 생성 완료. 그대로 붙여넣지 말고 질문 맥락에 맞게 다듬어 올리세요.", height=520, key="nq_out")


# =====================================================================
# 🔑 7. 키워드·콘텐츠 소재 발굴
# =====================================================================
def page_keyword():
    st.title("🔑 키워드 · 콘텐츠 소재 발굴기")
    st.caption("핵심/롱테일 키워드 + 소재 30개 + 30일 콘텐츠 캘린더 + 우선순위 5개.")
    col1, col2 = st.columns(2)
    with col1:
        region = st.text_input("📍 지역", value="대구")
        industries = st.text_input("🏢 관심 업종/분야 (선택, 쉼표 구분)", placeholder="예: 고깃집, 카페, 무인점포, 술집, 프랜차이즈, 미용실")
    with col2:
        target = st.selectbox("👥 주요 타겟", ["예비 창업자", "기존 점주·자영업자", "둘 다"])
        channels = st.multiselect("📡 운영 채널", ["네이버 블로그", "틱톡·릴스", "인스타그램", "유튜브", "네이버 지식인·카페"], default=["네이버 블로그", "틱톡·릴스", "인스타그램"])
    focus = st.text_input("➕ 특히 밀고 싶은 주제 (선택)", placeholder="예: 권리금 사기 예방 / 양수자 수수료 0원 / 폐업 vs 양도")
    if st.button("🔑 키워드 + 소재 + 30일 캘린더 생성"):
        with st.spinner("검색 키워드와 콘텐츠 소재를 연산 중입니다..."):
            prompt = f"""{BRAND_CONTEXT}
{ALGO_RULES}

당신은 지역 양도양수·창업 시장을 잘 아는 콘텐츠 전략가입니다. '대구상가맨'이 인지(TOFU) 단계에서 잠재 고객을 만나기 위한 키워드·소재 리스트를 작성하십시오.

[조건] 지역: {region or '대구'}
{opt('관심 업종/분야', industries)}- 타겟: {target} / 운영 채널: {', '.join(channels) if channels else '블로그·숏폼·인스타'}
{opt('특히 밀고 싶은 주제', focus)}
[출력 — 평문, 항목마다 번호]
1) 핵심 키워드 20개 — 각 옆에 (검색의도: 정보형/거래형/탐색형) + 추천 채널 1~2개 (네이버는 C-Rank/DIA/스마트블록 의도를 고려)
2) 롱테일 키워드 20개 — 사람들이 실제로 검색창에 칠 법한 구체적 문장형
3) 콘텐츠 소재 아이디어 30개 — 클릭하고 싶어지는 제목 형태, 각 옆에 [추천 채널] + [퍼널 의도: 인지/관심/전환]
4) 30일 콘텐츠 캘린더 — 1~4주차로 나눠 주차별 주제·채널 조합과 발행 빈도 구체적으로
5) 가장 먼저 만들 우선순위 콘텐츠 5개 + 각각 왜 먼저인지 한 줄 이유

[규칙] 권리금·양도양수·상권·창업 실패 예방 등 대구상가맨 강점과 이어지는 키워드 위주. 현실적 검색량 가진 키워드로. 비용 차감 내역 다루는 소재 제외.
"""
            show_result(get_gemini_response(prompt, API_KEY), key="kw_out")


# =====================================================================
# 📺 8. 유튜브 숏폼·롱폼 스크립트
# =====================================================================
def page_youtube():
    st.title("📺 유튜브 숏폼·롱폼 스크립트 생성기")
    st.caption("제목·썸네일 문구·후크·콘티·설명란·검색태그·고정댓글까지. CTR×시청지속×만족도 최적화.")
    topic = st.text_input("🎯 영상 주제 (필수)", placeholder="예: 대구 상가 양도양수 A to Z / 권리금 계산기 19개 변수 해부 / 망하는 상가 고르는 사람들의 공통점")
    col1, col2 = st.columns(2)
    with col1:
        length = st.selectbox("⏱️ 영상 길이", ["쇼츠 (~60초)", "미드폼 (3~5분)", "롱폼 (10분 이상)"])
        vtype = st.selectbox("📺 영상 유형", ["정보·노하우 강의", "실사례·인터뷰", "Q&A·고민상담", "매물·상권 소개", "시장 분석·트렌드"])
    with col2:
        target = st.selectbox("👥 타겟", ["예비 창업자", "기존 점주·자영업자", "둘 다"])
        tone = st.selectbox("🗣️ 톤", ["베테랑 전문가", "친근한 멘토", "다큐멘터리 내레이션"])
    extra = st.text_input("➕ 꼭 다룰 내용/사례 (선택)", placeholder="예: 양수자 수수료 0원 / 정밀 실사 보고서 항목 / 대구 동성로 사례")
    if st.button("📺 유튜브 스크립트 자동 생성"):
        if not topic.strip():
            st.warning("영상 주제는 필수입니다.")
            return
        with st.spinner("영상 구성을 연산 중입니다..."):
            prompt = f"""{BRAND_CONTEXT}
{OSM_VOICE}
{ALGO_RULES}

당신은 시청 지속률을 잘 잡는 유튜브 작가이자 '대구상가맨' 영상 PD입니다. 아래 조건으로 유튜브 영상 스크립트 한 편을 작성하십시오.

[조건] 주제: {topic} / 길이: {length} / 유형: {vtype} / 타겟: {target} / 톤: {tone}
{opt('꼭 다룰 내용/사례', extra)}
[출력 — 평문, 마크다운 특수기호 없이]
1) 영상 제목 3안 (클릭률 최적화, 각기 다른 각도)
2) 썸네일 문구 3안 (각 6~10자, 강렬하게) + 썸네일 이미지 컨셉 한 줄
3) 0~15초 후크: 시청 지속률 잡는 [오프닝 멘트] / [화면 연출]
4) 본문: '{length}' 분량에 맞춰 챕터(타임코드)로 나눠 각 챕터 [내레이션/대사 스크립트] / [화면 연출·자료화면 지시] / [강조 자막]
5) 마무리·CTA: 구독·알림 유도 + 권리금 계산기·무료 상담 연결 ("{BRAND_CTA_SHORT}" 취지)
6) 영상 설명란(더보기): SEO 최적화 요약 2~3문단 + 타임스탬프 챕터 목록 + 링크(www.sangaman.com / 010-4570-8889) + 해시태그 5개
7) 유튜브 검색 태그 15개 (쉼표 구분)
8) 고정 댓글 문구 1개 (참여 유도형)

[규칙] 도입 15초 안에 끝까지 보게 만들 것. 핵심 키워드를 말로도 언급(멀티모달). 비용 차감 내역 언급 금지. 입력 안 한 수치 지어내기 금지.
"""
            show_result(get_gemini_response(prompt, API_KEY), key="yt_out")


# =====================================================================
# 🗺️ 9. 퍼널 전략 대시보드
# =====================================================================
def page_dashboard():
    st.title("🗺️ 대구상가맨 마케팅 퍼널 전략 대시보드")
    st.caption("인지 → 관심 → 행동 → 전환 4단계 흐름 + 내 상황 맞춤 90일 액션플랜")
    st.markdown(
        """
| 단계 | 목표 | 이 허브가 만들어 주는 자산 | 핵심 지표(KPI) |
|---|---|---|---|
| ① 인지 (TOFU) | "대구상가맨"을 처음 만나게 | 원클릭 통합 캠페인 · 블로그 SEO · 숏폼 · 카드뉴스 · 지식인 답변 · 유튜브 | 노출수 · 조회수 · 도달 · 신규 방문자 |
| ② 관심 (MOFU) | 내 고민과 연결된 도구로 끌어들임 | 무료 권리금 계산기(19개 변수) · 17~19p 정밀 실사 보고서 · 상권 분석 | 계산기 사용수(핵심 활성화 이벤트) · 보고서 신청수 · 체류시간 |
| ③ 행동 (BOFU) | 직접 연락하게 | 1:1 팩트 상담(전화 010-4570-8889 / 카카오톡) · S등급 검증 매물 열람 | 상담 신청수 · 통화수 · 매물 문의수 |
| ④ 전환·리텐션 | 안전 거래 + 소개 | 안전 양도양수 계약(양수자 수수료 0원) · 후기·소개 요청 | 계약 건수 · 거래액 · 재의뢰·소개(플라이휠) |
"""
    )
    st.divider()
    st.subheader("🤖 내 상황 맞춤 90일 퍼널 액션플랜")
    col1, col2 = st.columns(2)
    with col1:
        cur = st.text_area("현재 상황 (선택)", height=120, placeholder="예: 블로그만 가끔, 월 문의 5건. 인스타 방치. 영상 안 해봄.")
        goal = st.text_input("3개월 목표 (선택)", placeholder="예: 월 상담 신청 30건, 매물 문의 10건")
    with col2:
        capacity = st.selectbox("콘텐츠에 쓸 수 있는 시간/인력", ["혼자 / 주 3시간 이하", "혼자 / 주 5~10시간", "1~2명 / 주 10시간 이상", "외주·편집자 활용 가능"])
        channels = st.multiselect("주력 또는 키우고 싶은 채널", ["네이버 블로그", "틱톡·릴스", "인스타그램", "유튜브", "네이버 지식인·카페", "당근·지역 커뮤니티"], default=["네이버 블로그", "틱톡·릴스", "인스타그램"])
    if st.button("🤖 맞춤 90일 액션플랜 생성"):
        with st.spinner("90일 액션플랜을 연산 중입니다..."):
            prompt = f"""{BRAND_CONTEXT}
{ALGO_RULES}

당신은 지역 양도양수·창업 중개 비즈니스를 키워본 퍼포먼스 마케팅 디렉터입니다. 아래 상황의 '대구상가맨'을 위한 90일 마케팅 퍼널 액션플랜을 작성하십시오.

[현재 상황]
{opt('현재 상황', cur)}{opt('3개월 목표', goal)}- 가용 리소스: {capacity}
- 주력/육성 채널: {', '.join(channels) if channels else '미정'}

[출력 — 평문, 마크다운 특수기호 없이]
1) 진단 한 문단: 지금 퍼널의 가장 큰 구멍 + 가장 빠르게 효과 볼 지점
2) 퍼널 4단계(인지→관심→행동→전환·리텐션)별로 무엇을 어떻게 채울지. 인지 단계는 채널별 콘텐츠 종류·발행 빈도까지 구체적으로(위 알고리즘 규칙 반영)
3) 30/60/90일 마일스톤 + 각 구간 목표 숫자
4) 가용 리소스에 맞춘 '주간 운영 루틴'(요일별 할 일 — 실제로 지킬 수 있게)
5) 이번 주에 당장 시작할 액션 5개(우선순위 순 + 한 줄 이유)
6) 모든 콘텐츠 끝에 넣을 통일 CTA 문구 2~3개 예시("{BRAND_CTA_SHORT}" 취지)

비용 차감 내역 언급 금지. 허위 수치 지어내기 금지.
"""
            show_result(get_gemini_response(prompt, API_KEY), key="db_out")


# =====================================================================
# ⚙️ 10. 알고리즘 가이드 & 적용 체크리스트
# =====================================================================
def page_algo():
    st.title("⚙️ 플랫폼 알고리즘 가이드 & 적용 체크리스트")
    st.caption("이 허브의 모든 콘텐츠 생성 프롬프트에 아래 규칙이 자동 내장됩니다. (조사 기준: 2025년 말~2026년 5월 / 정확한 가중치·산식은 어느 플랫폼도 비공개)")
    st.markdown(
        """
### 1) 네이버 검색 (한국 시장 인지 진입점)
- **C-Rank (출처 신뢰도 누적)** — 개별 글이 아니라 *채널(출처)*을 평가. 공개 축: Context(주제 집중도)·Content(콘텐츠 품질·소비 패턴)·Chain(연결: 인용·이동·소비/생산 패턴) → Creator 신뢰도. → *한 주제로 꾸준히 깊게* 쓰는 채널이 이긴다. 잡블로그 불리.
- **DIA (문서 품질 점수)** — 글 자체를 평가: 주제 적합도, 실제 경험·정보 포함, 정보 충실성. → *직접 경험·구체 수치·확인 서류·사진* 있는 글이 이긴다. 키워드 도배 탈락.
- **DIA+ (검색 의도 분석)** — 검색어의 의도(정보형/구매형/장소형 등)를 패턴 분석해 의도 맞는 글 타입을 끌어올림. → "권리금 계산"과 "권리금 사기"는 다른 의도 → 다른 형식.
- **스마트블록 (결과 구조)** — 통합검색 줄세우기가 아니라 *의도별 블록*('○○하는 법', 체크리스트, Q&A, 비교)으로 묶어 개인화·다양화. → 1등보다 *의도 블록 진입*이 목표.
- ⚠️ "블로그 지수"는 네이버 공식 용어 아님(업계 은어).

### 2) 틱톡 For You (FYP) — 공식 문서 기준
- 추천 3대 신호: ① 사용자 상호작용(완주·좋아요·댓글·공유·저장·스킵) ② 영상 정보(캡션·해시태그·사운드·자막 텍스트) ③ 계정·기기 설정(언어·국가).
- **공식 명시: 팔로워 수, 과거 영상 성과는 추천의 직접 신호 아님.** 0팔로워 첫 영상도 뜰 수 있음.
- 신규 영상은 *소규모 테스트 노출 → 반응(특히 완주율) 좋으면 확장*.
- 사실상 1순위 = **시청 완료율·평균 시청 시간**. 첫 1~3초 후크가 결정적. 가중치 체감 순서(업계 분석): 공유 > 댓글 ≈ 저장 > 좋아요.

### 3) 인스타그램 — Adam Mosseri 공식
- **단일 알고리즘 없음** — 피드/스토리/릴스/탐색 각각 다른 랭킹 시스템.
- 공통 입력: 게시물 정보 · 작성자 정보 · 내 활동 · 상호작용 이력 → 좋아요/댓글/공유/저장/프로필 방문 가능성 + *머무는 시간(dwell time)* 예측.
- **2025 릴스 핵심 3신호: ① Watch time ② Likes per reach(기존 팔로워) ③ Sends per reach(DM 공유 — 신규 도달에 가장 강력).** "좋아요 100개보다 DM 공유 10개."
- 오리지널 콘텐츠 우대 / 애그리게이터·재업로드 다운랭크 / 워터마크(틱톡 로고 등) 페널티.

### 4) 유튜브 — 공식 + Creator Insider
- **단일 알고리즘 없음** — 홈(추천)/추천(다음 동영상)/검색/쇼츠 각각 다름.
- 핵심 원리: *"알고리즘은 시청자를 따라간다"* — 클릭률(CTR) × 평균 시청 지속률(시청 시간) × **만족도**(좋아요·싫어요·"이 영상 어땠나요" 설문·공유·나중에 볼 동영상). 개인화는 시청 이력·구독·유사 시청자 패턴(협업 필터링).
- **쇼츠는 완전 별개 시스템** — 반복 재생(loop)·완주율 중심, 트렌드·현재 시청 패턴에 동적 배급.
- 2024~2025: Gemini 기반 멀티모달 콘텐츠 이해(음성·화면 텍스트·의미까지 분석).

### 5) 4개 플랫폼 관통하는 공통 원리 (= 이 허브 콘텐츠의 기본기)
1. 단일 알고리즘 신화 폐기 — 표면(피드/탐색/검색/쇼츠)별 별도 모델.
2. 콜드스타트: 초기 소수 노출의 반응(특히 시청 완주율)이 확산을 결정 → **첫 1~3초·첫 문장 후크**.
3. 시청 완주율·체류시간이 왕 → 늘어지는 도입 금지, 끝까지 보게 만드는 구성.
4. 공유(특히 DM/메신저)가 좋아요보다 3~5배 무겁다(인스타 공식) → **공유 유발 결말**.
5. 출처/창작자 신뢰도 누적(네이버 C-Rank·유튜브 채널 권위) → 한 주제 깊게·꾸준히.
6. 멀티모달·의미 이해 → 핵심 키워드를 자막·음성·화면 텍스트로도 노출.
7. 오리지널 우대, 재업로드·워터마크 페널티.

### 6) 측정 — 최고사양은 "삼각 측량"
- 어트리뷰션: Last/First-click → Linear → Time-decay → Position-based(U자) → **DDA(데이터 기반, Shapley value — GA4·Google Ads 기본값)**.
- 쿠키리스 시대: 서버사이드 태깅·Enhanced Conversions·Consent Mode + **MMM(마케팅 믹스 모델링)** 부활 + **증분성 테스트(geo holdout)** 로 교차 검증. 한 모델만 믿으면 틀린다.
- 대구상가맨 적용: GA4에서 "계산기 완료 / 상담 신청 / 매물 문의"를 핵심 전환 이벤트로. 분기마다 채널 1개씩 끄고 켜 증분성 확인.

---
**한 줄 결론:** 시기·플랫폼 불문 변하지 않는 사실 — *첫 몇 초 안에 붙잡고, 끝까지 보게 하고, 남에게 공유하게 만드는 콘텐츠가 모든 추천 알고리즘에서 이긴다.* 그리고 "○○하면 무조건 1등" 같은 보장은 존재하지 않는다.
"""
    )


# =====================================================================
# 사이드바 라우터
# =====================================================================
PAGES = {
    "⚡ 원클릭 통합 캠페인": page_oneclick,
    "🔬 권리금 X-파일 엔진": page_xfile,
    "✍️ 블로그 장문 SEO 원고": page_blog,
    "🎬 틱톡·릴스 60초 대본": page_shortform,
    "📸 인스타 카드뉴스 + 캡션": page_cardnews,
    "💬 지식인·카페 답변": page_naver_qa,
    "🔑 키워드·소재 발굴": page_keyword,
    "📺 유튜브 숏폼·롱폼 스크립트": page_youtube,
    "🗺️ 퍼널 전략 대시보드": page_dashboard,
    "⚙️ 알고리즘 가이드 & 체크리스트": page_algo,
}

st.sidebar.title("🎯 대구상가맨 마케팅 허브")
st.sidebar.caption("유입 퍼널 도구 통합 콘솔 v1.0")
if not API_KEY:
    st.sidebar.error("⚠️ GEMINI_API_KEY 미설정 — 생성 기능 비작동 (.env 또는 st.secrets)")
choice = st.sidebar.radio("도구 선택", list(PAGES.keys()))
st.sidebar.divider()
st.sidebar.markdown(
    """**퍼널 4단계**

1. 인지 — 원클릭 캠페인 · 블로그 · 숏폼 · 카드뉴스 · 지식인 · 유튜브
2. 관심 — 무료 권리금 계산기 · 정밀 실사 보고서
3. 행동 — 1:1 상담(전화·카카오) · S등급 매물 열람
4. 전환·리텐션 — 안전 양도양수 계약 · 후기·소개

모든 콘텐츠 CTA = sangaman.com 계산기"""
)
st.sidebar.divider()
st.sidebar.caption("모든 콘텐츠 프롬프트에 2025~2026 플랫폼 알고리즘 규칙 내장.")

PAGES[choice]()
