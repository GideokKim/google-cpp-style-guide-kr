# 네임스페이스 형식 (Namespace Formatting)

## 원문 규칙 번역

네임스페이스의 내용은 들여쓰기되지 않습니다.

네임스페이스는 들여쓰기 수준을 추가하지 않습니다. 예를 들어 다음을 사용합니다.

```cpp
namespace {

void foo() {  // Correct.  No extra indentation within namespace.
  ...
}

}  // namespace
```

네임스페이스 내에서는 들여쓰기하지 마세요.

```cpp
namespace {

  // Wrong!  Indented when it should not be.
  void foo() {
    ...
  }

}  // namespace
```

---

## 이해하기 쉽게 설명하기

네임스페이스 형식 규칙을 적용할 때는 원문 규칙을 문자 그대로 외우기보다, 왜 이 선택이 독자에게 더 명확한지 살펴보면 쉽습니다. 코드 리뷰에서는 이 기능이 호출 지점에서 의도를 숨기지 않는지, 더 단순한 구조로 같은 목적을 달성할 수 없는지, 기존 코드와 섞였을 때 유지보수 비용이 커지지 않는지를 확인하세요.
