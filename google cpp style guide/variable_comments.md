# 변수 주석 (Variable Comments)

## 원문 규칙 번역

일반적으로 변수의 실제 이름은 변수의 용도를 알 수 있을 만큼 충분히 설명적이어야 합니다. 어떤 경우에는 더 많은 설명이 필요합니다.

각 클래스 데이터 멤버(인스턴스 변수 또는 멤버 변수라고도 함)의 목적은 명확해야 합니다. 유형과 이름으로 명확하게 표현되지 않은 불변사항(특수값, 구성원 간 관계, 평생 요구 사항)이 있는 경우 주석을 달아야 합니다. 그러나 유형과 이름이 충분하면( int num_events_; ) 주석이 필요하지 않습니다.

특히 nullptr, -1 등의 센티널 값이 명확하지 않은 경우 해당 값의 존재와 의미를 설명하는 주석을 추가하세요. 예를 들어:

```cpp
private:
 // Used to bounds-check table accesses. -1 means
 // that we don't yet know how many entries the table has.
 int num_total_entries_;
```

모든 전역 변수에는 그 정의, 용도, 전역 변수가 필요한 이유(불명확한 경우)를 설명하는 주석이 있어야 합니다. 예를 들어:

```cpp
// The total number of test cases that we run through in this regression test.
const int kNumTestCases = 6;
```

---

## 이해하기 쉽게 설명하기

변수 주석 규칙을 적용할 때는 원문 규칙을 문자 그대로 외우기보다, 왜 이 선택이 독자에게 더 명확한지 살펴보면 쉽습니다. 코드 리뷰에서는 이 기능이 호출 지점에서 의도를 숨기지 않는지, 더 단순한 구조로 같은 목적을 달성할 수 없는지, 기존 코드와 섞였을 때 유지보수 비용이 커지지 않는지를 확인하세요.
