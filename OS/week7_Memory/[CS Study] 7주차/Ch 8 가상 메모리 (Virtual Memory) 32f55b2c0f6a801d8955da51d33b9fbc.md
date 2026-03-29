# Ch 8. 가상 메모리 (Virtual Memory)

---

# 목차 (Table of Contents)

1. **Virtual Storage Concept**
2. **Address Mapping**
3. **Virtual Storage Methods**
    1. **Paging System**
    2. **Segmentation System**
    3. **Hybrid Paging/Segmentation System**

---

# 1. Virtual Storage Concept (가상 메모리 개념)

가상 메모리는 프로세스 전체가 메모리에 올라오지 않아도 실행이 가능하도록 하는 
**비연속 할당(Non-continuous allocation)** 기법입니다.

- **기본 원리**: 사용자 프로그램을 여러 개의 **Block**으로 분할합니다.
- **실행 메커니즘**:
    - **Main Memory**: 현재 실행에 필요한 Block들만 적재.
    - **Swap Device**: 나머지 Block들이 머무는 공간 (보조기억장치).
- **가상 주소(Virtual Address) vs 실제 주소(Real Address)**:
    - 프로세스는 가상의 연속된 메모리 공간을 가졌다고 착각(Virtual)하지만, 실제 물리 메모리(Real)에는 흩어져서 저장됩니다.

---

# 2. Address Mapping (주소 매핑)

- 프로세스가 사용하는 가상 주소를 실제 물리 주소로 변환하는 과정입니다.
- 사용자/프로세스는 실행 프로그램 전체가 메모리에 연속적으로 
적재되었다고 가정하고 실행 할 수 있음

## (1) 연속 할당과의 차이

- **연속 할당**: 상대 주소(0부터 시작)를 사용하며, 단순히 시작 주소를 더하는 재배치(Relocation) 과정만 거치면 됩니다.
- **비연속 할당 (가상 메모리)**: 프로그램이 조각나 있기 때문에, 각 조각이 어디에 있는지 관리하는 **Mapping Table**이 반드시 필요합니다.

## (2) Block Mapping

![image.png](Ch%208%20%EA%B0%80%EC%83%81%20%EB%A9%94%EB%AA%A8%EB%A6%AC%20(Virtual%20Memory)/image.png)

- **BMT (Block Mapping Table)**: 각 블록의 실제 시작 주소를 저장하는 표입니다.
    - **Residence Bit**: 해당 블록이 메모리에 있는지(1) 스왑 장치에 있는지(0) 표시합니다.

![image.png](Ch%208%20%EA%B0%80%EC%83%81%20%EB%A9%94%EB%AA%A8%EB%A6%AC%20(Virtual%20Memory)/image%201.png)

---

# 3. Paging System (페이징 시스템)

프로그램을 고정된 크기(Page)로 분할하는 방식입니다.

- 특징
    - **Page**: 프로그램을 고정 크기로 나눈 단위.
    - **Page Frame**: 메모리를 Page와 같은 크기로 나눈 단위.
    - No external fragmentation

## (1) Address Mapping

- v = (p, d)
- **PMT (Page Mapping Table)** 구성 요소
    - **Page Number**: 가상 페이지 번호.
    - **Secondary Storage Address**: 스왑 장치 내 위치.

![image.png](Ch%208%20%EA%B0%80%EC%83%81%20%EB%A9%94%EB%AA%A8%EB%A6%AC%20(Virtual%20Memory)/image%202.png)

1. **Direct Mapping (직접 매핑)**: PMT를 메모리에 저장.
주소 변환을 위해 메모리에 두 번 접근해야 하므로 속도가 느립니다.
**Residence bit = 0 인 경우 (page fault)**
2. **Associative Mapping (연관 매핑)**: TLB(Translation Lookaside Buffer)라는 고속 캐시 하드웨어를 사용합니다. 전체 PMT를 병렬로 검색하여 매우 빠르지만 하드웨어 비용이 비쌉니다.
3. **Hybrid Mapping (혼합 매핑) :** TLB 에 PMT 중 일부 적재 (Locality)

## (2) Memory Management

- Page와 같은 크기로 미리 분할 하여 관리/사용
    - Page frame
    - FPM 기법과 유사
- Frame table
    - Page frame당 하나의 entry
    - Allocated/available field
    - PID field
    - Link field : For free list (사용가능 한 fp들을 연결)
    - AV : Free list header (free list의 시작점)
        
        ![image.png](Ch%208%20%EA%B0%80%EC%83%81%20%EB%A9%94%EB%AA%A8%EB%A6%AC%20(Virtual%20Memory)/image%203.png)
        

## (3) Page Sharing

- 여러 프로세스가 특정 page를 공유 가능
- 공유 가능 page
    - Procedure pages(reenter code)
    
    ![image.png](Ch%208%20%EA%B0%80%EC%83%81%20%EB%A9%94%EB%AA%A8%EB%A6%AC%20(Virtual%20Memory)/image%204.png)
    
    - Data page(Read-only data, Read-write data)
        
        ![image.png](Ch%208%20%EA%B0%80%EC%83%81%20%EB%A9%94%EB%AA%A8%EB%A6%AC%20(Virtual%20Memory)/image%205.png)
        
- 여러 프로세스가 page를 공유할 때 Protection bit 사용 - 가능한 권한 부여

---

# 4. Segmentation System (세그먼테이션)

프로그램을 기계적인 크기가 아니라, **논리적 단위(Segment)**로 분할하여 메모리에 적재하는 방식입니다.

- 특징
    - **분할 단위**: Stack, Function, Library, Main Program 등 의미 있는 단위로 나눕니다.
    - **크기**: 각 세그먼트는 **크기가 서로 다릅니다(Variable Size).**
    - **메모리 할당**: 빈 공간에 가변적으로 할당하므로 외부 파편화(External Fragmentation)가 발생할 수 있습니다.
    - 메모리를 미리 분할 하지 않음

## (1) Address Mapping

- v = (s, d)를 사용합니다.
    - **s (Segment Number)**: 세그먼트 번호
    - **d (Displacement/Offset)**: 세그먼트 내에서의 변위
- **SMT(Segment Mapping Table)**
    - **segment length (Bound)**: 세그먼트의 크기
    - protection bits(R/W/X/A): 권한
        
        ![image.png](Ch%208%20%EA%B0%80%EC%83%81%20%EB%A9%94%EB%AA%A8%EB%A6%AC%20(Virtual%20Memory)/image%206.png)
        
    - 존재 비트가 0 인 경우, missing **segment fault**
    - 변위(d)가 segment 길이보다 큰 경우 (d > ls),
    **segment overflow exception** 처리 모듈을 호출
    - 허가되지 않은 연산일 경우 (protection bit field 검사),
    **segment protection exception** 처리 모듈을 호출

---

## (2) Memory management

![image.png](Ch%208%20%EA%B0%80%EC%83%81%20%EB%A9%94%EB%AA%A8%EB%A6%AC%20(Virtual%20Memory)/image%207.png)

## (3) Sharing / Protection

세그먼테이션은 페이징보다 공유와 보호 측면에서 훨씬 강력합니다.

- **공유(Sharing)**
- **보호(Protection)**: "이 세그먼트는 코드니까 읽기 전용(Read-only)", "이 세그먼트는 데이터니까 읽기/쓰기(RW)" 식의 권한 부여가 논리적으로 딱딱 맞아떨어집니다.

---

## 3. Hybrid Paging/Segmentation System

세그먼테이션의 **논리적 장점**과 페이징의 **메모리 관리 효율성**을 합친 방식입니다.

### (1) 등장 배경

- 세그먼테이션은 논리적으로 좋지만, **외부 파편화** 때문에 메모리 낭비가 심합니다.
- 페이징은 메모리 관리는 쉽지만, **공유와 보호**가 까다롭습니다.
- **해결책**: 프로그램을 먼저 세그먼트로 나누고, 그 세그먼트를 다시 페이지로 자르자!

### (2) 주소 변환 매커니즘 (3단계)

가상 주소는 $v = (s, p, d)$ 형식을 가집니다.

1. **SMT 참조**: 세그먼트 번호 $s$를 통해 해당 세그먼트의 **PMT 주소**를 알아냅니다.
2. **PMT 참조**: 알아낸 PMT에서 페이지 번호 $p$를 통해 **실제 프레임 번호($p'$)**를 찾습니다.
3. **물리 주소 계산**: $p'$와 변위 $d$를 합쳐 실제 메모리 주소에 접근합니다.

---

# 5. Hybrid Paging / Segmentation

- 프로그램 분할
    - 논리 단위의 segment로 분할 → 각 segment를 고정 크기의 page들로 분할(1) Address mapping
        
        ![image.png](Ch%208%20%EA%B0%80%EC%83%81%20%EB%A9%94%EB%AA%A8%EB%A6%AC%20(Virtual%20Memory)/image%208.png)
        

## (1) Address mapping

- v = (s, p, d)
- SMT
    
    ![image.png](Ch%208%20%EA%B0%80%EC%83%81%20%EB%A9%94%EB%AA%A8%EB%A6%AC%20(Virtual%20Memory)/image%209.png)
    
- PMT

![image.png](Ch%208%20%EA%B0%80%EC%83%81%20%EB%A9%94%EB%AA%A8%EB%A6%AC%20(Virtual%20Memory)/image%2010.png)

![image.png](Ch%208%20%EA%B0%80%EC%83%81%20%EB%A9%94%EB%AA%A8%EB%A6%AC%20(Virtual%20Memory)/image%2011.png)

---

# 가상 메모리 시스템 비교 (최종 요약)

| **구분** | **Paging** | **Segmentation** | **Hybrid** |
| --- | --- | --- | --- |
| **분할 단위** | 고정 크기 (Page) | 가변 크기 (Segment) | Segment를 Page로 재분할 |
| **외부 파편화** | 없음 | **발생 가능** | 없음 |
| **내부 파편화** | **발생 가능** | 없음 | **발생 가능** |
| **관리 overhead** | **작음** | 큼 | 작음 |
| **공유/보호** | 복잡함 | **매우 용이함** | 용이함 |
| **메모리 접근** | 2회 (Direct 기준) | 2회 (Direct 기준) | **3회** (성능 저하 위험) |