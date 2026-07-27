# #define 가드

모든 헤더 파일은 다중 포함을 방지하기 위해 `#define` 가드를 가져야 합니다. 심볼 이름의 형식은 `<PROJECT>_<PATH>_<FILE>_H_`이어야 합니다.

고유성을 보장하기 위해 프로젝트의 소스 트리에서 전체 경로를 기반으로 해야 합니다. 예를 들어, 프로젝트 `foo`의 `foo/src/bar/baz.h` 파일은 다음과 같은 가드를 가져야 합니다:

```cpp
#ifndef FOO_BAR_BAZ_H_
#define FOO_BAR_BAZ_H_

...

#endif  // FOO_BAR_BAZ_H_
```

---

## 옮긴이 풀이

### #define 가드란?

`#define` 가드(또는 헤더 가드, header guard)는 헤더 파일이 여러 번 포함되는 것을 방지하는 메커니즘입니다. 같은 헤더 파일이 여러 번 `#include`되면 중복 정의 오류가 발생할 수 있는데, 가드를 사용하면 이를 방지할 수 있습니다.

### 왜 필요한가?

헤더 파일이 여러 번 포함될 수 있는 상황:

- 여러 소스 파일에서 같은 헤더를 포함하는 경우
- 헤더 파일이 다른 헤더 파일을 포함하고, 그 헤더가 또 다른 헤더를 포함하는 경우
- 복잡한 의존 관계로 인해 간접적으로 같은 헤더가 여러 번 포함되는 경우

가드가 없으면 다음과 같은 오류가 발생할 수 있습니다:

```cpp
// widget.h
class Widget { ... };  // 첫 번째 포함 시 정의됨
// ... 나중에 다시 포함되면
class Widget { ... };  // 중복 정의 오류!
```

### 가드 이름 규칙

가드 심볼 이름은 다음 형식을 따라야 합니다:

```text
<PROJECT>_<PATH>_<FILE>_H_
```

- `<PROJECT>`: 프로젝트 이름 (대문자)
- `<PATH>`: 소스 트리 내 경로 (슬래시 `/`를 언더스코어 `_`로 변환)
- `<FILE>`: 파일 이름 (확장자 제외, 대문자)
- 끝에 `_H_` 추가

여기서 `<PATH>`는 **`#include`에 사용하는 경로와 같은 경로**, 즉 프로젝트 소스 트리의 루트를 기준으로 한 상대 경로입니다. 따라서 핵심은 "특정 디렉토리 이름을 제외한다"가 아니라, **포함 경로를 그대로 대문자로 바꾸고 슬래시를 `_`로 치환한 뒤 `_H_`를 붙인다**는 것입니다.

예를 들어 프로젝트 `foo`의 파일 `foo/src/bar/baz.h`는 가드가 `FOO_BAR_BAZ_H_`가 됩니다. `src`가 이 프로젝트의 소스 루트이므로 트리 내 경로는 `bar/baz.h`이고(이 파일은 `#include "bar/baz.h"`로 포함됩니다), 여기에 프로젝트 이름 `foo`를 앞에 붙인 것입니다. 이는 "포함 순서와 이름" 규칙에서 `google-awesome-project/src/base/logging.h`를 `#include "base/logging.h"`로 포함하는 것과 같은 원리입니다.

즉, 소스 루트가 `src`든 `include`든 그 아래의 경로만 가드에 반영되며, 경로가 다르면 가드도 달라져 고유성이 보장됩니다.

### 예시

프로젝트 구조와 가드 이름 예시:

```text
프로젝트: MyProject
파일 경로: myproject/src/ui/widget.h
가드 이름: MYPROJECT_UI_WIDGET_H_
```

```cpp
// myproject/src/ui/widget.h
#ifndef MYPROJECT_UI_WIDGET_H_
#define MYPROJECT_UI_WIDGET_H_

class Widget {
  // ...
};

#endif  // MYPROJECT_UI_WIDGET_H_
```

다른 예시:

```text
프로젝트: MyProject
파일 경로: myproject/include/utils/string_utils.h
가드 이름: MYPROJECT_UTILS_STRING_UTILS_H_
```

```cpp
// myproject/include/utils/string_utils.h
#ifndef MYPROJECT_UTILS_STRING_UTILS_H_
#define MYPROJECT_UTILS_STRING_UTILS_H_

// ...

#endif  // MYPROJECT_UTILS_STRING_UTILS_H_
```

### 가드 작성 방법

1. **파일 시작 부분**: `#ifndef`와 `#define`을 파일의 맨 위에 작성
2. **파일 끝 부분**: `#endif`를 파일의 맨 끝에 작성하고 주석으로 가드 이름 표시

```cpp
#ifndef PROJECT_PATH_FILE_H_
#define PROJECT_PATH_FILE_H_

// 헤더 파일 내용

#endif  // PROJECT_PATH_FILE_H_
```

### 주의사항

- 가드 이름은 **반드시 고유**해야 합니다. 프로젝트 전체에서 중복되지 않아야 합니다.
- 전체 경로를 기반으로 하면 파일이 이동되어도 고유성이 보장됩니다.
- 가드 이름 끝의 주석(`// PROJECT_PATH_FILE_H_`)은 가독성을 위해 권장됩니다.
