# [CS Study] 5주차

## [5주차] 프로세스 동기화 (Process Synchronization)

### 1. 배경: 비동기적 병행 프로세스의 충돌

다중 프로그래밍 시스템에서 프로세스들은 서로의 상태를 모른 채(**Asynchronous**) 동시에 존재(**Concurrent**)합니다. 이들이 공유 자원에 동시에 접근할 때 발생하는 문제를 해결하는 것이 동기화의 핵심입니다.

- **공유 데이터(Shared data):** 프로세스가 공유하는 데이터, Critical data
- **임계 영역 (Critical Section):** 공유 데이터에 접근하는 코드 영역(code segment)

![image.png](%5BCS%20Study%5D%205%EC%A3%BC%EC%B0%A8/image.png)

---

### 2. 상호 배제(Mutual Exclusion) 기본연산(primitives)

1. enterCS primitive : 들어가기 전 검사
2. exitCS primitive : 나오는 과정

![image.png](%5BCS%20Study%5D%205%EC%A3%BC%EC%B0%A8/image%201.png)

1. 해결 조건 : 임계 영역 문제를 해결하기 위한 알고리즘은 반드시 아래 3가지를 만족해야 합니다.
    - **상호 배제 (Mutual Exclusion):** CS에 한 프로세스가 진입하면 다른 프로세스는 차단.
    - **진행 (Progress):** 진입하려는 프로세스가 없고 비어있다면 즉시 진입 허용.
    - **한정 대기 (Bounded Waiting):** 무한정 기다리는 프로세스가 없어야 함 (기아 현상 방지).
2. 소프트웨어 상호 배제 시도와 한계 (v1 ~ v3)
    - **v1: Turn 변수 활용 (순번 정해주기)**
        - **원리:** `turn` 변수를 두어 이번에 들어갈 차례인 프로세스를 지정함.
        - **한계:** **진행(Progress) 조건 위배**.
            - 반드시 상대방이 한 번 들어갔다 나와서 내 차례로 바꿔줘야만 내가 들어갈 수 있음.
            - 상대방이 임계 영역에 들어갈 생각이 없더라도 내 차례가 오지 않으면 영원히 진입 불가.
    
    ![image.png](%5BCS%20Study%5D%205%EC%A3%BC%EC%B0%A8/image%202.png)
    
    - **v2: Flag 변수 활용 - 직전 확인 (깃발 들기)**
        - **원리:** 각자 `flag`를 두어 진입 의사를 표시함. 상대가 깃발을 내리고 있으면 내가 깃발을 들고 진입.
        - **한계:** **상호 배제(Mutual Exclusion) 조건 위배**.
            - 두 프로세스가 동시에 상대의 깃발이 내려간 것을 확인하고 동시에 진입할 가능성이 있음.
    
    ![image.png](%5BCS%20Study%5D%205%EC%A3%BC%EC%B0%A8/image%203.png)
    
    - **v3: Flag 변수 활용 - 미리 확인 (양보의 함정)**
        - **원리:** 일단 내 깃발을 먼저 들고 나서 상대방의 깃발을 확인함. 상대가 들고 있다면 내릴 때까지 대기.
        - **한계:** **진행(Progress) 및 한정 대기(Bounded Waiting) 위배**.
            - 두 프로세스가 동시에 각자의 깃발을 들고 서로 양보하며 무한히 기다리는 상황 발생
        
        ![image.png](%5BCS%20Study%5D%205%EC%A3%BC%EC%B0%A8/image%204.png)
        

---

### 3. 동기화 솔루션별 특성 정리

### 3.1 SoftWare solution

- **Dekker’s algorithm(Peterson’s)**
    - **원리:** `flag`와 `turn` 변수를 활용하여 소프트웨어적으로 진입 순서를 제어.
    - Two process ME를 보장하는 최초의 알고리즘

![스크린샷 2026-03-10 104108.png](%5BCS%20Study%5D%205%EC%A3%BC%EC%B0%A8/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7_2026-03-10_104108.png)

- **Dijkstra algorithm**
    - idle : 프로세스가 임계 지역 진입을 시도하고 있지 않을 때
    - want-in : 프로세스의 임계 지역 진입 시도 1단계일 때
    - in-CS : 프로세스의 임계 지역 진입 시도 2단계 및 임계 지역 내에 있을 때
    - 최초로 프로세스 n개의 상호배제 문제를 소프트웨어적으로 해결
    
    ![image.png](%5BCS%20Study%5D%205%EC%A3%BC%EC%B0%A8/image%205.png)
    
- **효과/장점:** 별도의 하드웨어 지원 없이 구현 가능.
- **단점:** 속도가 느리고 구현이 복잡하며, 기다리는 동안 CPU를 소모하는 **Busy Waiting**이 발생함.

[[5.보충1] Software Solution 동작 과정](%5BCS%20Study%5D%205%EC%A3%BC%EC%B0%A8/%5B5%20%EB%B3%B4%EC%B6%A91%5D%20Software%20Solution%20%EB%8F%99%EC%9E%91%20%EA%B3%BC%EC%A0%95%2031f55b2c0f6a8080be43e32b77815d07.md)

### 3.2 HardWare solution

- **종류:** **TAS (TestAndSet)** 명령.
- **원리:** "검사와 수정"을 하나의 기계어 명령으로 처리, TAS(lock)
- **효과/장점:** 구현이 매우 간단하고 효율적임.
- **단점:** 여전히 **Busy Waiting** 문제가 발생함.

### 3.3 OS supported SW solution

- **Spinlock**
    - **원리:** 초기화, `P(), V()` 연산으로만 접근 가능 (P :  problem, 검사 / V : Verhogen, 증가)
    - **단점:** Busy waiting

![image.png](%5BCS%20Study%5D%205%EC%A3%BC%EC%B0%A8/image%206.png)

- **세마포어 (Semaphore, Dijkstra):**
    - **원리:** 정수형 변수 `S`와 `P()`/`V()` 연산을 통해 자원 관리. 자원이 없으면 **Ready Queue**에서 대기.
    - 해결 가능한 동기화 문제들
        - **상호배제 문제(Mutual exclusion)**
        - **프로세스 동기화 문제(process synchronization problem)**
        - **생산자-소비자 문제(producer-consumer problem)**
        - **Reader-writer 문제**
        - **Dining philosopher problem**
    - **장점:** **No Busy Waiting** (대기 중인 프로세스를 Block 상태로 전환).
    - **단점:** semaphore queue에 대한 wake-up 순서는 비결정적 (Starvation problem)
    
    [[5.보충2] Semaphore 동작 과정](%5BCS%20Study%5D%205%EC%A3%BC%EC%B0%A8/%5B5%20%EB%B3%B4%EC%B6%A92%5D%20Semaphore%20%EB%8F%99%EC%9E%91%20%EA%B3%BC%EC%A0%95%2031f55b2c0f6a806a8639f07bcd42c634.md)
    
- **Eventcount/Sequencer**
    - **원리:** 번호표(Sequencer)와 알림판(Eventcount)을 이용.
    - **장점:** No busy waiting, No starvation, low-level control 가능

ㄴLow-level mechanisms : Flexible, Difficult to use → Error-prone

---

### 3.4 Language-Level solution

- **종류:** Monitor
- **원리:** 공유 데이터와 Critical section의 집합.

![image.png](%5BCS%20Study%5D%205%EC%A3%BC%EC%B0%A8/image%207.png)

- **장점: 가독성 및 안전성:** 프로그래머가 직접 락을 제어할 필요가 없어 코드가 간결하고 실수가 적음.
- **단점:** 지원하는 언어(Java 등) 환경에서만 사용 가능.
    
    [[5.보충3] Monitor 동작 과정](%5BCS%20Study%5D%205%EC%A3%BC%EC%B0%A8/%5B5%20%EB%B3%B4%EC%B6%A93%5D%20Monitor%20%EB%8F%99%EC%9E%91%20%EA%B3%BC%EC%A0%95%2031f55b2c0f6a803582afd4a2e0c3abbf.md)
    

### Q1. Race Condition(경쟁 상태)이란 무엇이며, 이를 방지하기 위한 3가지 필수 조건을 설명하세요.

---

### Q2. 세마포어(Semaphore)와 뮤텍스(Mutex)의 결정적인 차이는 무엇인가요?

---

### Q3. 세마포어가 있는데 왜 모니터(Monitor)를 사용하나요?

---

[[5.보충4]](%5BCS%20Study%5D%205%EC%A3%BC%EC%B0%A8/%5B5%20%EB%B3%B4%EC%B6%A94%5D%2032855b2c0f6a80c68dfadb11f16b0a18.md)