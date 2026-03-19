# [5.보충3] Monitor 동작 과정

## 1. 모니터의 구조적 특징

![image.png](%5B5%20%EB%B3%B4%EC%B6%A93%5D%20Monitor%20%EB%8F%99%EC%9E%91%20%EA%B3%BC%EC%A0%95/image.png)

1. **상호 배제 (Mutual Exclusion) 보장:** 모니터 내부에 정의된 함수(Procedure)는 **한 번에 하나의 프로세스만 실행**할 수 있도록 설계되어 있습니다. 이는 언어/컴파일러 차원에서 자동으로 보장되므로, 개발자가 직접 `lock`을 걸고 푸는 코드를 작성할 필요가 없습니다.
2. **진입 큐 (Entry Queue):** 현재 다른 프로세스가 모니터 내부 함수를 실행 중일 때, 진입을 시도하는 프로세스들이 줄을 서서 대기하는 큐입니다.
3. **조건 변수 (Condition Variable):** 프로세스가 모니터 내부에는 들어왔으나, 특정 조건(예: 자원 부족)이 맞지 않아 더 이상 진행할 수 없을 때 사용하는 '신호' 장치입니다

---

## 2. 자원 할당 시나리오

![image.png](%5B5%20%EB%B3%B4%EC%B6%A93%5D%20Monitor%20%EB%8F%99%EC%9E%91%20%EA%B3%BC%EC%A0%95/image%201.png)

![image.png](%5B5%20%EB%B3%B4%EC%B6%A93%5D%20Monitor%20%EB%8F%99%EC%9E%91%20%EA%B3%BC%EC%A0%95/image%202.png)

![image.png](%5B5%20%EB%B3%B4%EC%B6%A93%5D%20Monitor%20%EB%8F%99%EC%9E%91%20%EA%B3%BC%EC%A0%95/image%203.png)

![image.png](%5B5%20%EB%B3%B4%EC%B6%A93%5D%20Monitor%20%EB%8F%99%EC%9E%91%20%EA%B3%BC%EC%A0%95/image%204.png)

![image.png](%5B5%20%EB%B3%B4%EC%B6%A93%5D%20Monitor%20%EB%8F%99%EC%9E%91%20%EA%B3%BC%EC%A0%95/image%205.png)

---

## 3. 동기화 문제 상황별 동작 과정

### 3.1 생산자-소비자 문제 (Producer-Consumer)

![image.png](%5B5%20%EB%B3%B4%EC%B6%A93%5D%20Monitor%20%EB%8F%99%EC%9E%91%20%EA%B3%BC%EC%A0%95/image%206.png)

![image.png](%5B5%20%EB%B3%B4%EC%B6%A93%5D%20Monitor%20%EB%8F%99%EC%9E%91%20%EA%B3%BC%EC%A0%95/image%207.png)

- **Producer:** 버퍼가 가득 차 있으면 `notFull.wait()`를 호출하여 자물쇠를 반납하고 잠듭니다. 소비자가 물건을 빼가며 `notFull.signal()`을 보내면 깨어나 데이터를 채웁니다.
- **Consumer:** 버퍼가 비어 있으면 `notEmpty.wait()`를 호출하고 잠듭니다. 생산자가 물건을 넣으며 `notEmpty.signal()`을 보내면 깨어나 데이터를 가져갑니다.

### 3.2 Reader-Writer 문제

![image.png](%5B5%20%EB%B3%B4%EC%B6%A93%5D%20Monitor%20%EB%8F%99%EC%9E%91%20%EA%B3%BC%EC%A0%95/image%208.png)

- **동작 제어:** 현재 실행 중인 Reader의 수와 Writer의 유무를 변수로 관리합니다.
- **Writer:** 다른 Writer가 있거나 Reader가 한 명이라면 `canWrite.wait()`를 호출합니다.
- **Reader:** Writer가 활동 중이면 `canRead.wait()`를 호출합니다.

### 3.3 식사하는 철학자 문제 (Dining Philosophers)

![image.png](%5B5%20%EB%B3%B4%EC%B6%A93%5D%20Monitor%20%EB%8F%99%EC%9E%91%20%EA%B3%BC%EC%A0%95/image%209.png)

![image.png](%5B5%20%EB%B3%B4%EC%B6%A93%5D%20Monitor%20%EB%8F%99%EC%9E%91%20%EA%B3%BC%EC%A0%95/image%2010.png)

![image.png](%5B5%20%EB%B3%B4%EC%B6%A93%5D%20Monitor%20%EB%8F%99%EC%9E%91%20%EA%B3%BC%EC%A0%95/image%2011.png)

- 철학자들은 생각하는 일, 스파게티 먹는 일만 반복함
- 공유 자원 : 스파게티, 포크
- 스파게티를 먹기 위해서는 좌우 포크 2개 모두 들어야 함