# 변수 주석 (Variable Comments)

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

### 핵심: 이름으로 부족할 때만 변수에 주석

보통 변수 이름이 용도를 충분히 설명해야 합니다. 타입·이름으로 드러나지 않는 **불변식**(특수값, 멤버 간 관계, 수명 요구)이 있을 때만 주석을 답니다. `int num_events_;`처럼 자명하면 주석은 불필요.

### 센티널 값·전역 변수

- `nullptr`, `-1` 같은 **센티널 값**의 의미가 불분명하면 설명하세요.
- **모든 전역 변수**는 정의·용도·(불분명하면) 왜 전역이어야 하는지를 주석으로.

```cpp
// 테이블 접근 범위 검사용. -1은 아직 항목 수를 모른다는 뜻.
int num_total_entries_;
```
