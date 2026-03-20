Notionlink

https://www.notion.so/spspd/6-AOP-3285bd6cf75e801bb754edae5a28d734?source=copy_link

---
created: 2026-03-19 16:55
type: study-summary
source: codex
source_task: [[40 작업/작업/260319_02_토비의스프링_6장_AOP_학습대화]]
tags:
  - spring
  - aop
  - transaction
  - study-summary
---

# 260319_02_토비의스프링_6장_AOP_정리

> 토비의 스프링 3.1 Vol.1 6장을 지금까지 학습한 범위 기준으로 다시 정리한 요약본  
> 용도: 복습, 발표 준비, 빠른 재참고

## 1. 장 전체 한 줄 요약

- 6장은 `트랜잭션 같은 공통 부가기능을 비즈니스 로직에서 분리하고, 프록시와 AOP로 공통 적용하는 방법`을 설명하는 장이다.

## 2. 왜 AOP가 필요한가

- OOP는 객체별 책임 분리에는 강하다.
- 하지만 `트랜잭션`, `로깅`, `보안`, `성능 측정`처럼 여러 객체를 가로지르는 기능은 OOP만으로 깔끔하게 분리하기 어렵다.
- 이런 공통 기능을 `횡단 관심사`라고 한다.
- AOP는 이 횡단 관심사를 핵심 비즈니스 로직 밖으로 빼서, 필요한 지점에 공통으로 적용하게 해준다.

### 핵심 문장

- `OOP = 객체별 책임 분리`
- `AOP = 횡단 관심사 분리`
- `AOP는 OOP를 대체하는 게 아니라 보완한다`

## 3. 왜 선언적 트랜잭션이 대표 사례인가

- 트랜잭션은 거의 모든 서비스 계층에서 반복된다.
- begin / commit / rollback 코드는 중요하지만 비즈니스 본질은 아니다.
- 서비스 메서드마다 직접 넣으면 핵심 로직과 기술 코드가 섞인다.
- 그래서 `선언적 트랜잭션`이 AOP의 대표 사례가 된다.

### 예시

```java
public void transfer() {
    transactionManager.begin();
    try {
        withdraw();
        deposit();
        transactionManager.commit();
    } catch (Exception e) {
        transactionManager.rollback();
        throw e;
    }
}
```

- 위 코드는 동작은 맞지만 비즈니스 로직과 트랜잭션 코드가 섞여 있다.
- AOP를 적용하면 트랜잭션은 밖으로 빠지고, 서비스 메서드는 업무 로직에만 집중할 수 있다.

```java
@Transactional
public void transfer() {
    withdraw();
    deposit();
}
```

## 4. 장 5와 장 6의 차이

- 장 5는 `무슨 기술을 쓸지`를 추상화했다.
- 장 6은 `그 기술 제어 코드를 누가 책임질지`를 분리한다.
- 즉:
- 장 5 = 기술 추상화와 DI
- 장 6 = 횡단 관심사 분리와 AOP

## 5. 장의 전개 흐름

1. 서비스 코드 안에 직접 들어간 트랜잭션 경계설정 코드를 문제로 본다.
2. `UserServiceTx` 같은 수동 프록시를 도입해 트랜잭션을 서비스 밖으로 분리한다.
3. 수동 프록시의 중복 문제를 해결하기 위해 JDK 동적 프록시를 사용한다.
4. 이를 스프링 빈으로 다루기 위해 `FactoryBean`, `ProxyFactoryBean`을 쓴다.
5. 부가기능과 적용 대상을 분리하기 위해 `Advice`, `Pointcut`, `Advisor` 개념을 도입한다.
6. `BeanPostProcessor` 기반 자동 프록시 생성기로 프록시 적용을 자동화한다.
7. 이후 트랜잭션 속성, `@Transactional`, 트랜잭션 테스트 지원으로 이어진다.

## 6. 핵심 개념 정리

- `Target`: 실제 핵심 로직을 수행하는 객체
- `Proxy`: 타깃 앞에서 호출을 대신 받고 부가기능을 붙이거나 접근을 제어하는 객체
- `Decorator`: 기능 추가 목적의 프록시 패턴
- `AOP`: 핵심 로직과 공통 부가기능을 분리하는 방식
- `횡단 관심사`: 여러 객체에 걸쳐 반복되는 공통 기능
- `Advice`: 무엇을 할까, 즉 부가기능 자체
- `Pointcut`: 어디에 할까, 즉 적용 대상 선정 기준
- `Advisor`: Advice와 Pointcut을 묶은 적용 단위
- `Aspect`: 부가기능 관점 전체를 가리키는 개념
- `Join Point`: 부가기능이 들어갈 수 있는 실행 지점
- `Weaving`: 부가기능을 실제 실행 구조에 결합하는 과정
- `JDK Dynamic Proxy`: 인터페이스 기반 프록시를 런타임에 자동 생성하는 자바 기능
- `InvocationHandler`: 동적 프록시로 들어온 호출을 한곳에서 처리하는 객체
- `FactoryBean`: 복잡한 객체 생성 로직을 감싸 최종 객체를 빈처럼 제공하는 특수 빈
- `ProxyFactoryBean`: 스프링에서 프록시 객체 생성을 담당하는 팩토리 빈
- `BeanPostProcessor`: 빈 생성 후 가공하거나 교체에 개입하는 확장 지점
- `Auto Proxy Creator`: 대상 빈이면 자동으로 프록시로 바꿔주는 빈 후처리기

### 외우기 쉬운 압축

- `Advice = 무엇`
- `Pointcut = 어디`
- `Advisor = 무엇 + 어디`

## 7. 프록시와 데코레이터

- 클라이언트가 타깃을 직접 호출하면 부가기능을 끼워 넣기 어렵다.
- 그래서 타깃과 같은 인터페이스를 구현한 프록시가 먼저 호출을 받는다.
- 프록시는:
- 호출 전 부가기능 수행
- 실제 타깃 호출
- 호출 후 후처리
- 를 담당한다.

### 구조

- `클라이언트 -> 프록시 -> 타깃`

### 자바 IO 예시

```java
InputStream is = new BufferedInputStream(new FileInputStream("a.txt"));
```

- `FileInputStream`은 타깃
- `BufferedInputStream`은 버퍼링 기능을 추가하는 데코레이터
- `UserServiceTx`도 같은 관점으로 이해할 수 있다.

## 8. 수동 프록시의 한계

- 인터페이스를 다시 구현해야 한다.
- 위임 코드가 반복된다.
- 서비스마다 비슷한 프록시 클래스가 계속 생긴다.
- 부가기능 코드가 여러 프록시에 중복된다.

## 9. 동적 프록시와 리플렉션

- JDK 동적 프록시는 프록시 객체를 런타임에 자동 생성한다.
- 프록시로 들어온 메서드 호출은 `InvocationHandler`가 처리한다.
- 실제 타깃 메서드 호출은 `Method.invoke(target, args)`로 수행된다.
- 여기서 `Method`는 메서드를 만드는 객체가 아니라 메서드 정보를 담은 객체다.

### 역할 구분

- `JDK`가 프록시를 만든다.
- `InvocationHandler`가 호출을 가로채 처리한다.
- `target`은 실제 일을 한다.

### 주의점

- target이 호출된 Method의 선언 타입과 맞지 않으면 런타임 예외가 난다.
- reflection으로 타깃 메서드를 실행했을 때 내부 예외는 `InvocationTargetException`으로 감싸져 전달된다.

## 10. 스프링으로 가져오기

- 순수 자바 동적 프록시는 원리 이해에는 좋지만 스프링 DI와 바로 연결되지는 않는다.
- 스프링은 런타임 생성 객체를 빈처럼 다루기 위해 `FactoryBean`, `ProxyFactoryBean`을 제공한다.

### ProxyFactoryBean 장점

- 프록시 생성 위임
- 부가기능 재사용성 향상
- 스프링 DI와 자연스러운 통합

### 한계

- 여러 타깃에 공통 적용하려면 설정이 반복될 수 있다.
- 그래서 `Advice`, `Pointcut`, `Advisor`로 더 일반화한다.

## 11. 6.4 핵심: Advice / Pointcut / Advisor

- `Advice`: 무슨 부가기능을 할까
- `Pointcut`: 어디에 적용할까
- `Advisor`: 그 둘을 묶은 규칙 단위

### 중요한 뜻

- Advice는 특정 타깃을 직접 들고 있는 객체라기보다, `순수 부가기능`에 집중한 재사용 가능한 로직이다.
- 어떤 타깃에 붙일지, 어떤 메서드에 적용할지는 스프링이 관리한다.

## 12. 6.5 핵심: 자동 프록시 생성

- 스프링은 `BeanPostProcessor` 기반 자동 프록시 생성기를 통해 빈을 검사한다.
- Pointcut에 맞는 빈이면 원본 대신 프록시를 반환한다.
- 따라서 개발자가 프록시를 일일이 수동 등록하지 않아도 된다.

### 핵심 문장

- `6.5는 프록시 적용의 자동화다`

## 13. 6.6 ~ 6.8 정리

### 6.6 트랜잭션 속성

- 트랜잭션은 단순히 적용할지 말지만 정하는 것이 아니다.
- `propagation`, `readOnly`, `rollback rule` 같은 세부 동작 정책까지 정해야 한다.
- 즉 6.6은 `트랜잭션을 어떻게 동작시킬까`를 다룬다.

### 6.7 애노테이션 기반 트랜잭션

- 위 정책을 XML 대신 `@Transactional`로 코드에 선언한다.
- 스프링 AOP 프록시가 이를 읽어 실제 트랜잭션을 처리한다.
- 즉 6.7은 `트랜잭션 정책을 어떻게 선언할까`를 다룬다.

### 6.8 트랜잭션 지원 테스트

- 테스트도 트랜잭션 안에서 실행하고 끝나면 롤백할 수 있다.
- 그래서 DB를 쉽게 원상복구하고 반복 가능한 테스트를 만들 수 있다.
- 즉 6.8은 `트랜잭션을 테스트에 어떻게 활용할까`를 다룬다.

## 14. 트랜잭션과 `@Transactional`

- `트랜잭션`은 여러 작업을 하나의 안전한 실행 단위로 묶는 개념이다.
- 전부 성공하면 반영하고, 하나라도 실패하면 전체를 되돌린다.
- `@Transactional`은 그 트랜잭션 정책을 스프링에 선언하는 어노테이션이다.

### 중요한 오해 방지

- `@Transactional`이 직접 commit/rollback 하는 것이 아니다.
- 실제 처리는 스프링 AOP 프록시가 담당한다.
- 즉:
- `트랜잭션` = 개념
- `@Transactional` = 선언
- `스프링 AOP 프록시` = 실제 적용 메커니즘

## 15. 테스트 관점 정리

- 좋은 테스트는 대상을 가능한 작게 고립시키는 단위 테스트다.
- DI를 이용해 외부 의존성을 스텁, 목 객체로 대체하면 테스트가 쉬워진다.
- Mockito 같은 목 프레임워크는 상호작용 검증을 쉽게 만든다.
- 트랜잭션 경계설정을 비즈니스 로직에서 분리하면 테스트도 더 분리하기 쉬워진다.

## 16. 자주 헷갈리는 포인트

- `AOP는 OOP를 대체하지 않는다`
- `Spring AOP는 프록시 기반이다`
- `AspectJ는 위빙/바이트코드 조작 기반이다`
- `readOnly`는 우선 힌트이지 만능 최적화 스위치가 아니다
- `LazyInitializationException`은 단순히 "트랜잭션이 없어서"라고만 말하면 부정확하다
- `@Transactional`을 붙였다고 무조건 모든 내부 호출까지 다 잡히는 것은 아니다

## 17. 발표용 초압축 버전

- `6장은 트랜잭션 같은 공통 기능을 비즈니스 로직에서 분리하고, 프록시와 AOP로 공통 적용하는 방법을 설명하는 장이다.`
- `핵심은 핵심 로직과 횡단 관심사를 분리하는 것이고, 대표 예가 선언적 트랜잭션이다.`
- `장 흐름은 수동 프록시 -> 동적 프록시 -> ProxyFactoryBean -> Advice/Pointcut/Advisor -> 자동 프록시 -> @Transactional -> 테스트 지원으로 이어진다.`

## 18. 2분 발표용 골자

- `6.6은 트랜잭션의 동작 정책`
- `6.7은 그 정책을 @Transactional로 선언하는 방법`
- `6.8은 그 트랜잭션을 테스트에 활용하는 방법`

## 19. 참고

- [학습 대화 원본](C:\SSAFY\workspace\obsidian\Main\obsidian_2026\40 작업\작업\260319_02_토비의스프링_6장_AOP_학습대화.md)
- [작업 메모](C:\SSAFY\workspace\obsidian\Main\obsidian_2026\40 작업\작업 메모\260319_02_토비의스프링_6장_AOP_학습대화 작업 메모.md)
- [Spring AOP Proxying](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html)
- [Spring Declarative Transaction Management](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative.html)

<!-- AI_NOTE: 이 문서는 대화 원본 로그를 풀어 다시 정리한 학습용 요약본이다. 이후 6.6~6.8 상세 설명을 더 보강할 때 이 문서를 우선 업데이트한다. -->
