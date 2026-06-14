# 함수 이름 (Function Names)

일반적으로 함수는 PascalCase를 따릅니다. 즉, 대문자로 시작하고 각 새 단어에 대문자가 있습니다.

```cpp
AddTableEntry()
DeleteUrl()
OpenFileOrDie()
```

API의 일부로 노출되고 함수처럼 보이도록 의도된 클래스 및 네임스페이스 범위 상수에도 동일한 명명 규칙이 적용됩니다. 왜냐하면 함수가 아닌 개체라는 사실은 중요하지 않은 구현 세부 사항이기 때문입니다.

접근자와 변경자(get 및 set 함수)는 snake_case 에서 변수처럼 이름이 지정될 수 있습니다. 이는 실제 멤버 변수에 해당하는 경우가 많지만 필수는 아닙니다. 예를 들어 int count() 및 void set_count(int count) 입니다.

---

## 이해하기 쉽게 설명하기

### 핵심: 함수는 PascalCase

함수는 대문자로 시작하고 새 단어마다 대문자를 씁니다.

```cpp
AddTableEntry();
DeleteUrl();
OpenFileOrDie();
```

### 두 가지 보충

- **함수처럼 보이도록 의도된 상수**(API로 노출되는 클래스·네임스페이스 범위 상수)도 같은 PascalCase를 씁니다. 실제로는 함수가 아니라는 건 중요치 않은 구현 세부사항이기 때문입니다.
- **접근자·설정자**(get/set)는 변수처럼 `snake_case`로 둘 수 있습니다: `int count()`, `void set_count(int count)`.
