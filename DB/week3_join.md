# 지난 번 주제 회고 (정규화 + 이상)

### 1. 이상(삽입/삭제/수정)이란

### 2. 정규화 목적: 중복 제거 + 무결성 강화 + 이상 방지

### 3. 대신 조회가 불편해짐 → 조인이 등장

---

# 조인이란?

분해한 정보를 조회 시점에 다시 조립!

- 정규화로 분해한 데이터(테이블)를 **필요한 형태**로 합쳐 조회
- `데이터 설계의 대가`를 치르는 도구

# JOIN 종류

![image.png](./images/image.png)

![image.png](./images/image%20(1).png)

### 1. INNER JOIN

- 매칭되는 행만 남는다 (교집합)

```sql
SELECT 
	e.emp_id, 
	e.name, 
	s.pay_month, 
	s.amount
FROM employees e
INNER JOIN salaries s
  ON e.emp_id = s.emp_id;
```

- **결과**

| emp_id | name | pay_month | amount |
| --- | --- | --- | --- |
| 1 | 현승 | 2026-01 | 500 |
| 1 | 현승 | 2026-02 | 520 |
| 2 | 민지 | 2026-01 | 480 |

### 2. LEFT JOIN

- 왼쪽은 무조건 유지, 오른쪽은 매칭 실패 시 NULL

```sql
SELECT e.emp_id, e.name, s.pay_month, s.amount
FROM employees e
LEFT JOIN salaries s
  ON e.emp_id = s.emp_id;
```

- **결과**

| emp_id | name | pay_month | amount |
| --- | --- | --- | --- |
| 1 | 현승 | 2026-01 | 500 |
| 1 | 현승 | 2026-02 | 520 |
| 2 | 민지 | 2026-01 | 480 |
| 3 | 철수 | NULL | NULL |

### 3. RIGHT JOIN

- LEFT JOIN의 반대 버전
- 실무에서는 보통 LEFT JOIN으로 통일

```sql
SELECT e.emp_id, e.name, s.pay_month, s.amount
FROM employees e
RIGHT JOIN salaries s
  ON e.emp_id = s.emp_id;
```

```sql
SELECT e.emp_id, e.name, s.pay_month, s.amount
FROM salaries s
LEFT JOIN employees e
  ON e.emp_id = s.emp_id;
```

### 4. CROSS JOIN

- 두 테이블의 모든 행 조합(데카르트 곱)을 만드는 조인

```sql
SELECT
  e.emp_id   AS e_emp_id,
  e.name,
  e.dept,
  s.emp_id   AS s_emp_id,
  s.pay_month,
  s.amount
FROM employees e
CROSS JOIN salaries s;
```

```sql
SELECT ...
FROM employees e, salaries s;
```

```sql
SELECT d.date, s.store_id
FROM stores s
CROSS JOIN dates d;
-- 결과: 특정 기간의 모든 날짜와 모든 매장의 조합
```

### 결과 (총 3 x 3 = 9행)

| e_emp_id | name | dept | s_emp_id | pay_month | amount |
| --- | --- | --- | --- | --- | --- |
| 1 | 현승 | DEV | 1 | 2026-01 | 500 |
| 1 | 현승 | DEV | 1 | 2026-02 | 520 |
| 1 | 현승 | DEV | 2 | 2026-01 | 480 |
| 2 | 민지 | DEV | 1 | 2026-01 | 500 |
| 2 | 민지 | DEV | 1 | 2026-02 | 520 |
| 2 | 민지 | DEV | 2 | 2026-01 | 480 |
| 3 | 철수 | HR | 1 | 2026-01 | 500 |
| 3 | 철수 | HR | 1 | 2026-02 | 520 |
| 3 | 철수 | HR | 2 | 2026-01 | 480 |

다른 조인 참고

![image.png](./images/image%20(2).png)

---

# 조인 동작 원리

### 논리적 의미

- `A ⋈(조건) B = σ(조건)(A × B)`
- 조건이 없으면 `A × B` 그대로이므로 결과 행 수가 `|A| × |B|` 로 폭발 (=CROSS JOIN)

### 물리적 실행 (실제 DB 동작)

BUT! `A × B` 의 비용이 천문학적이기에

대신 **`옵티마이저`**가 쿼리 실행 계획을 결정

> 
> 
> 
> ### 옵티마이저(Optimizer)란?
> 
> - SQL을 실행하기 전에, **가장 싸게 끝날 실행 계획(Execution Plan)** 을 고르는 컴포넌트
> - MySQL은 **CBO(Cost-Based Optimizer)**:
>     
>     테이블/인덱스 통계(행 수 추정, 선택도, 분포)로 비용을 추정해서
>     
>     1. 어떤 테이블부터 읽을지(조인 순서)
>     2. `인덱스`를 쓸지/`풀스캔`할지(접근 방식)
>     3. 어떤 조인 방식(`NLJ`/`Hash` 등)을 쓸지
>         
>         를 결정한다.
>         

![image.png](./images/image%20(9).png)

1. 조건을 가능한 빨리 적용하고(**`Predicate pushdown`**)
    
    ```sql
    SELECT *
    FROM A
    JOIN B ON A.id = B.aid
    WHERE A.status = 'ACTIVE'   -- A만으로 판단 가능
      AND B.type = 'X';         -- B만으로 판단 가능
    ```
    
2. 조인 순서를 재배치하고(**`Reordering`**)
    - 비용에 따라 조인 순서 재배치
    - `비용(Cost) ≈ outer_rows × inner_lookup_cost`
3. 상황에 맞는 알고리즘(**`해시 조인`**/~~머지 조인~~/**`네스티드 루프 조인`**)을 선택해
    - `Nested Loop 조인`(기본)
        - 한쪽을 읽고, 다른쪽에서 매칭 찾기(인덱스 있으면 유리)
        - `이중 for문`이라 생각하면 편함
        
		![image.png](./images/image%20(3).png)
        
    - `Hash Join`
        - MySQL도 해시 조인이 있다(가능 조건/언제 선택될 수 있는지 키워드 수준)
        - 8.0.20부터는 인덱스가 없을 경우 hash join이 기본이 됨.
        
        ![image.png](./images/image%20(4).png)
        

---

# 성능 최적화를 위한 전략

### 1. 조인 키/필터 컬럼에 인덱스 설계

### 2. 조건을 인덱스 친화적으로 작성(sargable)

- 컬럼에 함수 적용하면 인덱스 못 탐:

```sql
-- ❌ 인덱스 잘 못 탐
WHERE DATE(created_at) = '2026-02-26'
-- ✅ 범위로 쓰면 인덱스 잘 탐
WHERE created_at >= '2026-02-26' AND created_at < '2026-02-27'
```

## 3. NLJ 최적화

### **Multi Range Read (MRR)**

![image.png](./images/image%20(5).png)

![image.png](./images/image%20(6).png)

### **Batched Key Access (BKA)**

![image.png](./images/image%20(7).png)

![image.png](./images/image%20(8).png)

---

# 질문

- FK도 다른 테이블 간의 관계인데 조인과 뭐가 다른가요?
    - **FK는 스키마 레벨 제약조건**이라서, 자식 값이 부모(보통 PK/UNIQUE)에 존재해야 한다는 **참조 무결성**을 강제합니다.
    - **JOIN은 조회 시점에** 두 테이블의 행을 **조건으로 결합**해서 결과를 만드는 연산입니다.
    - JOIN 조건은 **FK가 아니어도** 가능하고, FK는 JOIN을 **자동으로 수행하지도** 않습니다.
- 정규화와 조인의 상관관계에 대해서 설명해보거라.
    - 정규화는 **중복을 줄이고 무결성을 강화**해서 삽입/삭제/수정 이상을 줄입니다.
    - 대신 데이터가 여러 테이블로 분리되므로 조회 시 **JOIN이 필요해지는 경우가 많습니다.**
    - 다만 성능은 “정규화=느림”이 아니라, **인덱스/조인 조건/접근 패턴**에 따라 달라서, 실무에선 일부는 반정규화로 타협하기도 합니다.
- INNER JOIN vs LEFT JOIN 결과 집합 차이
    - **INNER JOIN**은 조인 조건을 만족하는 행만 남아서, 매칭이 없으면 제거됩니다.
        
        특히 1:N이면 왼쪽 1행이 오른쪽 N행과 매칭되어 결과가 **N행으로 늘어날 수** 있습니다.
        
    - **LEFT JOIN**은 왼쪽 테이블의 모든 행을 유지하고, 매칭 실패한 오른쪽 컬럼들은 **NULL로 채웁니다.**
        
        즉 결과는 “INNER 결과 + 매칭 실패한 왼쪽 행(NULL 포함)”입니다.
        
- LEFT JOIN인데 결과가 줄었다. 왜?
    - LEFT JOIN은 먼저 결과를 만들 때 **매칭 실패한 오른쪽을 NULL로 채워** 왼쪽을 살립니다.
    - 그런데 `WHERE`에서 오른쪽 컬럼 조건(예: `s.pay_month='2026-01'`)을 걸면, NULL인 행은 조건을 만족 못 해서(UNKNOWN) **최종 결과에서 제거**되어 LEFT JOIN이 사실상 INNER JOIN처럼 됩니다.
    - 해결은 보통 오른쪽 필터를 **ON으로 옮기거나**, `OR s.col IS NULL`을 명시합니다.
- JOIN이 느려지는 원인
    1. 조인키 인덱스 부재
        - NLJ에서 inner가 반복 스캔되어 비용이 급증(outer_rows × inner_scan)
    2. 필터/조건이 인덱스를 못 타는 경우(함수/형변환 등)
        - range/ref가 아닌 ALL로 떨어져 읽는 row가 폭증
    3. 잘못된 조인 순서
- 조인 순서가 성능에 영향을 미치는 이유가 무엇일까?
