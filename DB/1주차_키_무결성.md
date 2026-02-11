# 1주차 — Key(키) + 무결성(Integrity)

## 목차
1. 관계형 모델 용어 vs SQL/DBMS 용어  
2. 키(Key)의 본질: 유일성 + 최소성  
3. 키의 종류 (Super/Candidate/PK/Alternate/Unique/FK/Composite)  
4. PK 선택: 자연키 vs 대리키(AUTO_INCREMENT vs UUID)  
5. 무결성(Integrity) 개념과 종류  
6. DB 제약조건 vs 애플리케이션 검증(트레이드오프)  
7. 면접 질문 리스트(핵심 답변 프레임)

---

# 1. 관계형 모델 용어 vs SQL/DBMS 용어

## 1.1 용어 대응 (이론 ↔ 구현)

![image](./이미지/스키마예시.png)

- Relation(릴레이션) ↔ Table(테이블)
- Tuple(튜플) ↔ Row/Record(행)
- Attribute(애트리뷰트) ↔ Column(열)
- Domain(도메인) ↔ 컬럼에 들어갈 수 있는 값의 규칙(타입/범위/형식)
- Schema(스키마) ↔ 테이블/컬럼/제약조건/인덱스 등 `구조 정의`
- Instance(인스턴스) ↔ 특정 시점의 실제 데이터 (행들의 집합)

> 왼쪽은 관계형 모델(이론) 용어, 오른쪽은 SQL/DBMS(구현) 용어
> 

> 1:1 완벽 대응은 아니지만 사실상 같은 의미로 사용됨.
> 
- 스키마가 DBMS에서 유지되는 방식
    
    스키마 정보는 DBMS 내부의 **시스템 카탈로그(system catalog)** / **데이터 딕셔너리(data dictionary)** 에 **메타데이터로 저장.**
    
    - MySQL 8(InnoDB) 기준으로 테이블/컬럼 정의, 인덱스, 제약조건 같은 정보는 **DB 내부 딕셔너리(시스템 카탈로그)** 에 저장되고, `INFORMATION_SCHEMA`나 `SHOW CREATE TABLE` 같은 명령으로 확인한다.
    - FK 같은 제약은 DBMS가 내부적으로 관리하며, FK 컬럼에는 인덱스가 필요하고(없으면 생성), 관련 메타데이터도 시스템 테이블로 조회 가능하다.
- 도메인이 MySQL에서 의미하는 것
    
    **도메인 = “한 컬럼이 가질 수 있는 값들의 집합(타입/범위/형식)”**
    
    1. **타입/길이/형식(기본 공간 제한)**
    - `INT`, `BIGINT`, `DATE`, `VARCHAR(50)` …
    
    2. **NULL 허용 여부 / 기본값 / 값 제한(규칙 추가)**
    - `NOT NULL`, `DEFAULT 'active'`, `CHECK(age >= 0 AND age <= 120)` 등
    - CHECK 제약도 MySQL에서 지원/관리되며 메타데이터로 조회된다.

---

# 2. 키(Key)의 본질: 유일성 + 최소성

- `유일성`(Uniqueness)
    - 키 값으로 행을 하나로 특정할 수 있어야 함
    - 예: `{학번}` 으로 학생을 정확히 1명 지칭
- `최소성`(Minimality)
    - 유일성을 만족하는데 불필요한 컬럼이 없어야 함
    - 예: `{학번, 이름}`은 유일할 수 있지만 `{학번}`만으로 이미 충분 → 최소성 위반

---

# 3. 키의 종류

## 3.1 슈퍼키(Super Key)

> 유일성을 만족하는 컬럼 집합
> 
- 최소성은 필요 없음 → 쓸데없이 많이 묶어도 유일하면 슈퍼키
- `{학번}`도 슈퍼키
- `{학번, 이름}`도 슈퍼키

## 3.2 후보키(Candidate Key)

> `유일성`+ `최소성`을 만족하는 `슈퍼키` (PK가 될 수 있는 키)
> 
- 한 테이블에 후보키는 여러 개 있을 수 있음
- 후보키 중 하나를 `대표`로 뽑는 게 PK
- 예) 학생 테이블에서
    - 학번이 유일하고 최소면 후보키
    - 이메일도 유일하고 최소면 후보키
- “이메일 여러 개 가질 수 있지 않나?
    - 비즈니스 규칙 문제이다.
        - 학생당 이메일 1개면 이메일은 후보키 가능
        - 여러 개 가능이면 후보키 불가 → 이메일 같은 별도 테이블(1:N)로 분리

## 3.3 기본키(Primary Key)

> 후보키 중 대표 식별자로 선택한 키
> 
> 
> SQL 구현: `PRIMARY KEY` (= `UNIQUE + NOT NULL` + 의미적으로 대표)
> 

```sql
CREATE TABLE student (
  student_id BIGINT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  name  VARCHAR(50)  NOT NULL
);
```

## 3.4 대체키(Alternate Key)

> PK로 선택되지 않은 나머지 후보키
> 

## 3.5 UNIQUE 제약 (유니크키)

> PK는 아니지만 중복을 막고 싶은 컬럼(또는 컬럼 조합)에 거는 제약
> 
- PK와의 관계:
    - PK = UNIQUE + NOT NULL + “대표 식별자”
    - UNIQUE = 대표는 아니지만, 중복 방

! MySQL에서는 UNIQUE 인덱스에 NULL이 여러 개 들어갈 수 있다. (NULL은 NULL과 같다고 보지 않는 취급)

```sql
CREATE TABLE student (
  student_id BIGINT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  name  VARCHAR(50)  NOT NULL
);
```

## 3.6 외래키 (Foreign Key, FK)

> 다른 테이블의 행을 참조하는 키
> 
> 
> SQL 구현: `FOREIGN KEY (...) REFERENCES parent(...)`
> 

SQL 구현: `FOREIGN KEY (학번) REFERENCES 학생 (학번)`

- FK는 관계를 나타냄 (1:N, N:M 등)

### FK 옵션

- `RESTRICT / NO ACTION` : 부모 삭제 막기(기본) → 에세이가 있으면 멤버 삭제 X
- `CASCADE` : 부모 삭제 시 자식도 삭제 (위험할 수 있음) → 멤버 삭제 시 에세이들 다 삭제
- `SET NULL` : 부모 삭제 시 자식 FK를 NULL로 → 멤버 삭제 시 에세이들 FK(member_id) NULL로 변경

> `ON UPDATE`…로 업데이트도 동일
> 

```sql
-- 멤버 테이블
CREATE TABLE member (
  member_id BIGINT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE
);

-- 에세이(자소서) 테이블
CREATE TABLE essay (
  essay_id  BIGINT PRIMARY KEY,
  member_id BIGINT NULL,
  title     VARCHAR(200) NOT NULL,
  CONSTRAINT fk_essay_member
    FOREIGN KEY (member_id) REFERENCES member(member_id)
    ON DELETE SET NULL -- ON UPDATE도 동일
);
```

✅ “PK 아니어도 참조 가능?”

- 원칙적으로 FK는 **부모의 ‘후보키(PK 또는 UNIQUE)’** 를 참조한다고 이해하면 안전

✅ 질문: “자식(FK)에 해당하는 레코드가 부모 테이블에 2개 이상 있으면?”

- 그래서 **부모 쪽 참조 컬럼이 ‘유일’해야** 함(후보키).
- “부모에 중복이 있으면 FK가 한 행이 부모 여러 개를 가리키는 꼴”이라 의미가 깨짐.

## 3.7 복합키(Composite Key)

> 2개 이상 컬럼을 묶어서 만든 키 (PK일 수도/ UNIQUE일 수도)
> 
- 예시) 연결 테이블
    
    enrollment(학번, 과목ID)에서 (학번, 과목ID)가 PK
    
    → 한 학생이 한 과목을 중복 신청 못하게 강제 가능
    
    ```sql
    -- 수강신청 테이블
    CREATE TABLE enrollment (
      student_id BIGINT NOT NULL, -- 학생 ID
      course_id  BIGINT NOT NULL, -- 과목 ID 
      PRIMARY KEY (student_id, course_id), -- 복합키!
      FOREIGN KEY (student_id) REFERENCES student(student_id), -- 학생 테이블 FK
      FOREIGN KEY (course_id)  REFERENCES course(course_id) -- 과목 테이블 FK
    );
    ```
    
    - 장점: “학생이 같은 과목을 중복 신청” 같은 **업무 규칙을 DB가 강제**
    - 단점: 키가 길어져서 조인/인덱스/참조가 번거로워질 수 있음
- 실무 요약!
    - **엔티티 테이블:** 단일 PK(대리키) 선호
    - 연결(매핑) 테이블: 복합 PK 많이사용

---

# 4. PK 선택: 자연키 vs 대리키(AUTO_INCREMENT vs UUID)

## 4.1 자연키 (Natural Key)

> 의미 있는 값(주민번호/이메일/학번 등)을 PK로 사용
> 

**장점**

- 사람이 이해하기 쉬움
- 중복 의미가 자연스럽게 막힘

**단점**(실무에서 큼)

- 변경 가능성: 이메일 정책 변경/재발급 등 → PK 변경은 파급이 큼(FK, 인덱스, 조인 구조)
- 보안/추측 가능성: 이메일을 ID로 사용 시 추측 가능
    - 보안은 ‘ID 숨김’이 아니라 ‘`권한 검증`’으로 해결하는 게 정석!
- 외부 시스템과 결합 시 규칙이 깨질 수 있음

## 4.2 대리키(Surrogate Key)

> 의미 없는 값(자동 증가 ID, UUID 등)을 PK로 사용
> 

**장점**

- PK가 변하지 않는 안정적인 식별자
- 조인/참조가 단순

**단점**/**주의**

- 업무적으로 유일해야 하는 값(이메일/전화번호 등)은 별도 `UNIQUE + NOT NULL`로 강제해야 함.

**!질문!**

- UUID PK가 왜 인덱스에 불리할까?
    - MySQL InnoDB에서는 PK는 보통 B+Tree 기반이고, 랜덤한 키(UUID)는 삽입 시 페이지 분할과 캐시 지역성 악화로 비용이 커질 수 있음.
    - 그래서 실무에서는
        - 단일 DB/ 단일 리전 중심이면 BIGINT AUTO_INCREASEMENT를 많이 쓰고,
        - 분산 환경에서 UUID가 필요하면 시간 정렬되는 UUID(v7)/ULID 같은 전략을 고려함.

---

# 5. 무결성

## 5.1 무결성이란?

> 데이터가 스키미가 의도한 규칙을 항상 만족하도록 유지되는 성질
> 

## 5.2 무결성 종류

## 5.2.1 개체 무결성(Entity Integrity)

> 각 행은 식별 가능해야 한다. (보통 PK로 강제)
> 
- `PRIMARY KEY`가 곧 `NOT NULL + UNIQUE`

```sql
CREATE TABLE student (
  student_id BIGINT PRIMARY KEY, -- PK로 무결성 유지
  name VARCHAR(50) NOT NULL
);
```

---

## 5.2.2 참조 무결성(Referential Integrity)

> 자식(FK)이 가리키는 부모는 존재해야 한다.
> 

```sql
CREATE TABLE essay (
  essay_id  BIGINT PRIMARY KEY,
  member_id BIGINT,
  FOREIGN KEY (member_id) REFERENCES member(member_id) -- 에세이는 멤버에 속함.
);
```

---

## 5.2.3 도메인 무결성(Domain Integrity)

> 컬럼 값은 도메인(타입/범위/형식)을 만족해야 한다.
> 
- 타입 : INT, VARCHAR, DATE …
- 범위/형식: CHECK, ENUM, 정규식, 길이 제한 등

```sql
CREATE TABLE users (
  user_id BIGINT PRIMARY KEY,
  age INT NOT NULL,
  status VARCHAR(10) NOT NULL DEFAULT 'active',
  CHECK (age >= 0 AND age <= 120)
);
-- BIGINT, INT, NOT NULL, VARCHAR(10), DEFAULT, CHECK 등
```

---

## 5.2.4 사용자 정의 무결성(User-defined / Business Constraints) - `별로 안 중요!`

> 표준 분류(개체/참조/도메인)로 다 표현이 안 되는 업무 규칙
> 
- 구현 수단: `CHECK`, 트리거, 애플리케이션 검증, 배치 정합성 점검 등

**예시 1) active면 deleted_at은 NULL**

```sql
CREATE TABLE account (
  account_idBIGINTPRIMARY KEY,
  status ENUM('ACTIVE','DELETED')NOT NULL,
  deleted_at DATETIMENULL,
CHECK (
    (status='ACTIVE'AND deleted_atISNULL)OR
    (status='DELETED'AND deleted_atISNOT NULL)
  )
);
```

---

# 6. DB 제약조건 vs 애플리케이션 검증 (트레이드오프)

## 6.1 DB에서 강제(Constraints)

장점

- 데이터 품질 보장: 어떤 경로로 쓰든 규칙 유지 가능
- 데이터 품질 유지

단점

- 제약이 많아질수록 쓰기 성능/락 경합이 커질 수 있음
- 마이그레이션/스키마 변경이 까다로워짐
- 복잡한 규칙은 제약만으로 표현이 어려워 트리거 지옥이 될 수 있음

```sql
CREATE TABLE users (
  id BIGINT PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(30),
  status VARCHAR(10) NOT NULL DEFAULT 'ACTIVE',
  age INT,
  CONSTRAINT uq_users_email UNIQUE (email),
  CONSTRAINT ck_users_age CHECK (age IS NULL OR (age >= 0 AND age <= 120))
);
```

---

## 6.2 애플리케이션에서 강제

장점

- 유연하고 빠르게 변경 가능
- 복잡한 비즈니스 규칙을 표현하기 쉬움

단점

- DB에 직접 접근하는 경로가 생기면 우회 가능 (검증 X)
- 동시성 경쟁 조건(race condition)으로 깨짐
    - “중복 체크 후 INSERT”는 동시에 두 요청이 들어오면 둘 다 INSERT 통과 가능
    - 최종은 DB UNIQUE 제약이어야 함!
- Spring + JPA 예시
    
    **상황:** 회원 가입 시 이메일 중복 방지
    
    ### (A) 앱 검증만 하는 위험한 패턴
    
    ```java
    @Transactional
    public Long signUp(String email) {
        if (memberRepository.existsByEmail(email)) { // 이메일 중복 체크
            throw new IllegalArgumentException("이미 사용 중인 이메일");
        }
        Member m = new Member(email);
        memberRepository.save(m); // 동시성 상황에서 중복 저장 가능
        return m.getId();
    }
    ```
    
    ### (B) DB 제약 + 앱은 “친절한 메시지” 담당 (정석)
    
    ```java
    @Entity
    @Table(name = "member",
           uniqueConstraints = @UniqueConstraint(name="uq_member_email", columnNames="email")) // 유니크 제약 설정
    class Member {
        @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;
    
        @Column(nullable = false)
        private String email;
    }
    
    ```
    
    ```java
    @Transactional
    public Long signUp(String email) {
        try {
            Member m = new Member(email);
            memberRepository.save(m); // 멤버 저장(회원가입)
            return m.getId();
        } catch (DataIntegrityViolationException e) {
            // UNIQUE 제약 위반 -> 이미 존재
            throw new IllegalArgumentException("이미 사용 중인 이메일");
        }
    }
    
    ```
    

---

---

## 7. 면접 질문 리스트

### Q1. “FK를 왜 거나요? 앱에서만 체크하면 안 되나요?”

**핵심 의도:** “정합성 책임을 어디에 둘 거냐”

- 앱 검증은 **경로가 늘어나면 깨지기 쉬움**(배치/어드민/다른 서비스/직접 SQL)
- DB FK는 **어떤 경로로 쓰든** 참조 무결성을 강제

**한 줄 답:**

“앱 검증은 필수지만, 참조 무결성 같은 ‘불변식’은 DB가 최종 방어선으로 강제하는 게 운영 사고를 줄입니다.”

### Q2. “FK를 일부러 안 거는 경우?”

“운영에서 마음대로 만지고 싶어서”는 위험한 답이고, 더 면접친화 답은:

- 샤딩/멀티DB/마이크로서비스라 **DB 레벨 FK가 물리적으로 불가능**
- 레거시/마이그레이션 단계에서 점진 도입
- 대량 적재(ETL)에서 성능/순서 문제로 임시로 완화(대신 검증 배치/체크를 둠)

### Q3. “ON DELETE CASCADE 언제 쓰고 언제 피하나?”

- **쓰기:** “정말 종속 관계(부모 없으면 자식 의미 없음)” + 삭제량이 통제됨
- **피하기:** 주문/결제/정산/로그 같이 “삭제가 곧 사고/감사 이슈”인 데이터
- 실무에선 소프트딜리트가 흔해서 CASCADE는 더 신중

### Q4. “UNIQUE + NOT NULL이면 PK 아닌가요?”

맞지만 차이는:

- PK는 “대표 식별자” + (InnoDB에서) **데이터 정렬/저장 기준**이라 파급이 다름

---

---

# 참고 자료

기초 자료: https://wikidocs.net/book/18461