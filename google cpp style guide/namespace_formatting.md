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

---

## 이해하기 쉽게 설명하기

이 규칙의 핵심은 네임스페이스는 들여쓰기 수준을 추가하지 않습니다.

실제로 코드를 볼 때는 네임스페이스는 들여쓰기 수준을 추가하지 않습니다.

점검할 때는 특히 다음을 확인하세요:

- 이 선택이 독자에게 숨은 전제나 비용을 만들지 않는지 확인하세요.
