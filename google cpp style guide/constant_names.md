# 상수 이름 (Constant Names)

## 원문 규칙 번역

constexpr 또는 const 로 선언되고 해당 값이 프로그램 기간 동안 고정되는 변수의 이름은 앞에 "k" 뒤에 대소문자가 혼합되어 지정됩니다. 밑줄은 대문자를 구분에 사용할 수 없는 드문 경우에 구분 기호로 사용할 수 있습니다. 예를 들어:

```cpp
const int kDaysInAWeek = 7;
const int kAndroid8_0_0 = 24;  // Android 8.0.0
```

정적 저장 기간이 있는 모든 변수(예: 정적 변수 및 전역 변수, 자세한 내용은 저장 기간 참조)는 정적 상수 클래스 데이터 멤버인 변수와 템플릿의 다양한 인스턴스화가 다른 값을 가질 수 있는 템플릿의 변수를 포함하여 이 방식으로 이름을 지정해야 합니다. 이 규칙은 자동 변수와 같은 다른 저장소 클래스의 변수에 대해서는 선택 사항입니다. 그렇지 않으면 일반적인 변수 명명 규칙이 적용됩니다. 예를 들어:

```cpp
void ComputeFoo(absl::string_view suffix) {
  // Either of these is acceptable.
  const absl::string_view kPrefix = "prefix";
  const absl::string_view prefix = "prefix";
  ...
}
```

```cpp
void ComputeFoo(absl::string_view suffix) {
  // Bad - different invocations of ComputeFoo give kCombined different values.
  const std::string kCombined = absl::StrCat(kPrefix, suffix);
  ...
}
```

---

## 이해하기 쉽게 설명하기

상수 이름 규칙을 적용할 때는 원문 규칙을 문자 그대로 외우기보다, 왜 이 선택이 독자에게 더 명확한지 살펴보면 쉽습니다. 코드 리뷰에서는 이 기능이 호출 지점에서 의도를 숨기지 않는지, 더 단순한 구조로 같은 목적을 달성할 수 없는지, 기존 코드와 섞였을 때 유지보수 비용이 커지지 않는지를 확인하세요.
