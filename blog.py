import streamlit as st
import os
from dotenv import load_dotenv

# =====================================================================
# 🚨 심층 분석 패키지 로드 (무결점 코어)
# =====================================================================
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

# =====================================================================
# 🚨 하이브리드 보안 세팅 (APP_PASSWORD 의존성 제거)
# =====================================================================
load_dotenv() 
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        st.error("❌ 환경에 보안 키가 물리적으로 존재하지 않습니다.")
        st.stop()

# =====================================================================
# 🚨 무결점 AI 호출 함수 (에러 자동 우회)
# =====================================================================
def get_gemini_response(prompt, api_key):
    if not HAS_GEMINI:
        return "❌ Gemini 패키지가 설치되지 않았습니다. (pip install google-genai)"
    
    try:
        if USE_NEW_SDK:
            client = genai_new.Client(api_key=api_key)
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
            except Exception:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
            return response.text.strip()
        else:
            genai.configure(api_key=api_key)
            available_models = [m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
            preferred = ["models/gemini-2.5-flash", "models/gemini-2.0-flash", "models/gemini-1.5-flash"]
            target = next((m for m in preferred if m in available_models), available_models[0])
            model = genai.GenerativeModel(target.replace("models/", ""))
            response = model.generate_content(prompt)
            return response.text.strip()
    except Exception as e:
        return f"❌ 시스템 연산 오류 발생: {str(e)}"

# =====================================================================
# UI 폰트 15 강제 적용
# =====================================================================
st.markdown("""
    <style>
    html, body, [class*="css"], .stTextInput>div>div>input, .stSelectbox>div>div>div {
        font-size: 15px !important;
    }
    .stButton>button {
        font-size: 18px !important;
        font-weight: bold;
        height: 3em;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# 🚨 보안 인증 시스템 (0810 고정)
# =====================================================================
if "password_correct" not in st.session_state:
    st.title("🔒 대구상가맨 시스템 보안 인증")
    pwd_input = st.text_input("접근 비밀번호를 입력하십시오", type="password")
    if st.button("인증 가동"):
        if pwd_input == "0810":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("비밀번호 불일치")
    st.stop()

# =====================================================================
# 메인 엔진 화면 v15.7
# =====================================================================
st.title("🚀 대구상가맨 SEO 풀오토 엔진 v15.7")
st.info("💡 핵심 주제 입력 불필요. 추가 키워드를 융합하여 제목과 20개의 해시태그까지 100% 자동 산출합니다.")

st.subheader("1. 타겟팅 기본 설정")
grade_select = st.radio("🏆 상권 등급 선택", ["S등급 (초핵심)", "A등급 (우량)", "B등급 (실속)", "C등급 (틈새)"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    region_input = st.text_input("📍 구체적 지역명", value="대구")
    category_input = st.text_input("🏢 세부 업종 (필수 입력)", value="유명 고기집")
with col2:
    brand_input = st.text_input("🏷️ 프랜차이즈 브랜드명 (선택)", placeholder="예: 하남돼지집")
    type_select = st.selectbox("🔥 창업 유형", ["양도양수창업", "신규창업", "점포개발", "업종변경"])

st.subheader("2. 재무 팩트 데이터 (선택)")
col3, col4 = st.columns(2)
with col3:
    revenue_input = st.text_input("💰 월평균 매출", placeholder="예: 5,000만 원 (선택)")
with col4:
    profit_input = st.text_input("📈 월평균 수익", placeholder="예: 1,200만 원 (선택)")

st.subheader("3. 필수 포함 추가 키워드 (선택)")
extra_keywords = st.text_input("🔑 반영할 추가 키워드", placeholder="예: 무권리, 독점상권, 리뉴얼 완료, 역세권 (쉼표로 구분하여 입력)")

# 엔진 구동
if st.button("🚀 네이버 SEO 팩트 원고 100% 자동 생성"):
    if not category_input.strip():
        st.warning("세부 업종은 반드시 입력해야 합니다.")
    else:
        with st.spinner(f"대구상가맨 무결점 코어가 추가 키워드를 융합하여 원고 및 해시태그를 연산 중입니다..."):
            has_finance = bool(revenue_input.strip() or profit_input.strip())
            has_brand = bool(brand_input.strip())
            
            if has_finance:
                merit_logic = f"입력된 월평균 매출({revenue_input})과 수익({profit_input}) 데이터를 최고의 핵심 무기로 삼아, 이 창업의 압도적인 수익성과 투자 가치 메리트를 가장 강력하게 어필하십시오."
            elif has_brand:
                merit_logic = f"매출 데이터는 없지만 '{brand_input}'라는 강력한 프랜차이즈 브랜드 파워와 '{category_input}' 업종의 결합이 만들어내는 시너지 효과를 집중 분석하여, 브랜드 인지도를 통한 실패 없는 창업 메리트를 어필하십시오."
            else:
                merit_logic = f"브랜드명이나 특정 매출 데이터 없이 오직 '{category_input}' 업종 자체가 가진 본질적인 유망성과 시장 트렌드, 그리고 {grade_select} 상권에서 어떻게 안정적으로 자리 잡을 수 있는지에 대한 사업적 메리트를 깊이 있게 서술하십시오."
            
            grade_logic = {
                "S등급 (초핵심)": "압도적 유동인구와 랜드마크 가치를 강조. 선점의 시급성과 고매출의 팩트를 중심으로 서술.",
                "A등급 (우량)": "탄탄한 배후 수요와 안정적인 수익 밸런스 강조. 리스크가 낮은 우량 자산임을 부각.",
                "B등급 (실속)": "가성비 창업과 효율적 운영 강조. 임대료 부담을 줄인 실속 있는 수익 구조를 중심으로 서술.",
                "C등급 (틈새)": "최소 비용 창업과 리스크 방어 강조. 전문가의 정밀 실사가 생존의 필수 조건임을 냉철하게 경고."
            }
            
            keyword_logic = f"- 필수 포함 추가 키워드: {extra_keywords}" if extra_keywords.strip() else ""
            keyword_instruction = f"6. 추가 키워드 융합: 입력된 [필수 포함 추가 키워드]({extra_keywords})가 있을 경우, 해당 단어들을 본문 문맥 속에 전혀 어색하지 않게 100% 자연스럽게 녹여내십시오." if extra_keywords.strip() else ""

            prompt = f"""
            당신은 15년 차 프랜차이즈 전문가 '대구상가맨' 오석민 대표입니다. 
            네이버 검색 상위 노출(SEO)을 위한 3,000자 이상의 스토리텔링 포스팅을 작성하십시오.

            [입력된 물리적 팩트]
            - 지역: {region_input}
            - 업종: {category_input}
            - 브랜드: {brand_input if has_brand else "일반/개인 창업"}
            - 상권 등급: {grade_select} ({grade_logic[grade_select]})
            - 창업 유형: {type_select}
            {keyword_logic}

            [✨ 핵심 메리트 강조 지침 (매우 중요)]
            {merit_logic}

            [작성 팩트 지침]
            1. 자동 제목 추출: 본문 시작 전, 가장 꼭대기에 네이버 검색 로직에 최적화된 [블로그 제목]을 알아서 창작하여 먼저 출력.
            2. 도입부 강제 규칙: 본문 첫 시작은 반드시 "{region_input} {category_input}" 키워드를 문맥에 자연스럽게 사용하여 출발할 것.
            3. 마크다운 금지: 별표(**)나 샵(#) 등의 특수 기호를 절대 사용하지 말고 평문(Plain text)으로만 출력할 것.
            4. 분량 및 깊이: 네이버 C-Rank 로직이 '전문가의 깊이 있는 칼럼'으로 인식하도록 공백 포함 3,000자 이상으로 매우 논리적이고 길게 서술할 것.
            5. 비용 수치 언급 금지: 세금, 4대보험, 원가율 등 예비 창업자가 부담을 느끼는 세부 차감 내역은 절대 언급 금지.
            {keyword_instruction}
            
            [필수 하단 홍보 문구 - 100% 유입 강제화]
            원고 맨 마지막에 아래 내용을 글자 토씨 하나 틀리지 말고 그대로 출력하십시오:

            부풀려진 권리금, 아직도 감으로 결정하십니까? 
            양도양수 시 발생하는 권리금 피해를 100% 원천 차단하고 여러분의 소중한 자본을 방어하기 위해, 15년 차 베테랑 대구상가맨이 직접 설계한 '전문가용 권리금 계산기'를 지금 무료로 개방합니다. 
            19가지 실무 변수를 대입하여 내 매장의 진짜 팩트 가치를 단 1초 만에 확인하십시오.

            [대구상가맨 플랫폼이 예비 창업자와 기존 점주 모두에게 완벽한 이유]
            ▶ 예비 창업자: '양수자 수수료 0원' 혜택과 '17페이지 정밀 실사 보고서'로 권리금 사기를 차단하고 100% 자본 방어를 약속합니다.
            ▶ 기존 매장 점주 및 자영업자: 부당한 권리금 후려치기 없이, 투명하고 정확한 가치 평가를 통해 가장 빠르고 안전하게 매장을 매각(Exit)할 수 있도록 돕습니다.

            창업의 시작부터 안전한 매각까지, 대구상가맨 플랫폼이 완벽한 성공 파트너가 되어 드립니다. 
            지금 바로 공식 사이트에 접속하여 무료 계산기를 두드려보시고, 오석민 대표가 직접 검증한 S등급 팩트 매물들을 직접 확인하십시오.

            무료 권리금 계산기 및 안전 매물 확인: www.sangaman.com
            1:1 팩트 상담 및 문의: 010-4570-8889
            
            [해시태그 20개 자동 산출]
            위 홍보 문구가 끝난 후, 맨 아랫줄에 본문 내용과 타겟 키워드, 그리고 추가 키워드들을 바탕으로 네이버 검색 노출에 최적화된 해시태그를 정확히 20개 작성하십시오. 반드시 띄어쓰기로 구분하여 한 줄로 나열하십시오.
            (예시: #{region_input}창업 #{category_input}창업 #{brand_input}창업 #{type_select} #대구상가맨 #프랜차이즈창업 #소자본창업 ...)
            """
            
            ai_result = get_gemini_response(prompt, API_KEY)
            
            if ai_result.startswith("❌"):
                st.error(ai_result)
            else:
                st.success("✅ 추가 키워드가 반영된 팩트 원고 및 해시태그 20개가 완벽히 산출되었습니다.")
                st.text_area("출력 결과 (복사 아이콘 사용)", value=ai_result, height=600)