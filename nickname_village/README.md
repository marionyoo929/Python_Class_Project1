# 디동숲

닉네임으로 DiceBear 아바타를 만들고 6개의 고정된 집에 입주시키는 학습용 Streamlit 프로젝트입니다.

## 실행
Python 3.10 이상에서 이 폴더를 터미널로 연 뒤 실행합니다.

```console
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

설치 후 Windows에서는 run.bat를 더블클릭해도 됩니다. 첫 실행 시 같은 폴더에 village.db가 자동 생성됩니다. 사진 생성은 인터넷 연결이 필요하며, 저장된 주민 조회는 외부 API를 호출하지 않습니다.

## 기능
- 2가지 스타일(픽셀/로봇)의 아바타 생성
- 빈집 입주, 6명 정원, 같은 닉네임·스타일 중복 등록 방지
- 마을 조회, 직업·성격 수정, 확인 후 퇴거
- 이미지와 주민 정보 영구 저장

## 코드 읽는 순서
1. avatar_api.py: requests.get, params, timeout, 상태 코드, SVG 텍스트 응답
2. resident_db.py: CREATE/SELECT/INSERT/UPDATE/DELETE, SQL의 ?, commit과 연결 종료
3. app.py: 입력 → API 호출 → session_state 초안 → DB 등록 → 화면 재실행

SVG는 문자열 형태의 이미지이므로 DB의 TEXT 컬럼에 그대로 저장합니다. nickname과 seed는 현재 동일하지만, 향후 닉네임과 외형을 따로 관리할 수 있도록 구분했습니다. UNIQUE(house_no)는 동시 등록에도 한 집에 두 주민이 들어가지 않도록 합니다. UNIQUE(nickname,style)는 중복 주민을 막습니다.

## 평가 준비
안내문은 AI가 작성한 코드를 그대로 제출하는 것을 허용하지 않습니다. 이 결과물은 학습용 참고 구현으로 사용하고, 각 함수를 설명하고 직접 수정할 수 있도록 이해한 뒤 본인이 작성한 코드로 과제를 진행하세요. 보고서의 실제 결과는 본인이 실행한 내용과 캡처로 기록하세요.

연습 과제: 입주민 검색, 로봇만 표시, 빈집으로 이사, 마을 이름 변경. 현재 구현에 미리 넣지 않았습니다.

## 직접 해볼 테스트
1. 빈 닉네임: 생성 거부.
2. 정상 생성 후 빈집 등록: 마을에 표시.
3. 같은 닉네임·스타일을 다른 집에 등록: 중복 거부.
4. 여섯 집을 모두 채움: 신규 입주 제한.
5. 직업·성격 수정 후 재시작: 수정 내용과 이미지 유지.
6. 퇴거 확인 후 삭제: 집이 비고 다시 입주 가능.
7. 인터넷 연결 실패: 오류 안내, 잘못된 초안 저장 방지.

## 출처
- https://www.dicebear.com/integrations/http-api/ : 인증키 없이 이용하는 HTTP API, 비상업적 이용 무료 및 호출 제한 적용
- https://www.dicebear.com/styles/pixel-art/ : CC0
- https://www.dicebear.com/styles/bottts/ : Pablo Stanley, 개인·상업 이용 무료

본 프로젝트는 특정 게임의 이미지나 캐릭터를 사용하지 않습니다. 외형은 DiceBear가 만들고 직업과 성격은 사용자가 입력합니다.
