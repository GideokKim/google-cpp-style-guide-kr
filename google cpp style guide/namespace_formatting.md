# 네임스페이스 형식 (Namespace Formatting)

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

## 옮긴이 풀이

### 핵심: 네임스페이스 내용은 들여쓰지 않는다

네임스페이스는 들여쓰기 수준을 추가하지 않습니다. 내부 코드는 왼쪽 여백에 맞춰 씁니다.

```cpp
namespace {

void foo() {  // 맞음 - 네임스페이스 안에서 추가 들여쓰기 없음
  ...
}

}  // namespace
```

(네임스페이스 안의 코드를 한 단계 더 들여쓰는 것은 잘못입니다.)
