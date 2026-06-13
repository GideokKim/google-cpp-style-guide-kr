# 포함 순서와 이름 (Names and Order of Includes)

헤더를 다음 순서로 포함하세요: 관련 헤더, C 시스템 헤더, C++ 표준 라이브러리 헤더, 다른 라이브러리의 헤더, 프로젝트의 헤더.

프로젝트의 모든 헤더 파일은 프로젝트의 소스 디렉토리의 하위 항목으로 나열되어야 하며, UNIX 디렉토리 별칭인 `.`(현재 디렉토리) 또는 `..`(상위 디렉토리)를 사용하지 않아야 합니다. 예를 들어, `google-awesome-project/src/base/logging.h`는 다음과 같이 포함되어야 합니다:

```cpp
#include "base/logging.h"
```

라이브러리가 요구하는 경우에만 각괄호로 둘러싼 경로를 사용하여 헤더를 포함해야 합니다. 특히 다음 헤더는 각괄호가 필요합니다:

- C 및 C++ 표준 라이브러리 헤더 (예: `<stdlib.h>` 및 `<string>`).
- POSIX, Linux, Windows 시스템 헤더 (예: `<unistd.h>` 및 `<windows.h>`).
- 드문 경우로, 서드파티 라이브러리 (예: `<Python.h>`).

`dir/foo.cc` 또는 `dir/foo_test.cc`에서, 주요 목적이 `dir2/foo2.h`의 내용을 구현하거나 테스트하는 경우, 포함 순서는 다음과 같습니다:

1. `dir2/foo2.h`.
2. 빈 줄
3. C 시스템 헤더 및 `.h` 확장자를 가진 각괄호로 둘러싼 다른 헤더, 예: `<unistd.h>`, `<stdlib.h>`, `<Python.h>`.
4. 빈 줄
5. C++ 표준 라이브러리 헤더 (파일 확장자 없음), 예: `<algorithm>`, `<cstddef>`.
6. 빈 줄
7. 다른 라이브러리의 `.h` 파일.
8. 빈 줄
9. 프로젝트의 `.h` 파일.

각 비어 있지 않은 그룹은 하나의 빈 줄로 구분합니다.

선호하는 순서를 사용하면, 관련 헤더 `dir2/foo2.h`가 필요한 포함을 생략한 경우, `dir/foo.cc` 또는 `dir/foo_test.cc`의 빌드가 깨집니다. 따라서 이 규칙은 빌드 오류가 다른 패키지의 무고한 사람들이 아닌, 이러한 파일을 작업하는 사람들에게 먼저 나타나도록 보장합니다.

`dir/foo.cc`와 `dir2/foo2.h`는 보통 같은 디렉토리에 있지만(예: `base/basictypes_test.cc`와 `base/basictypes.h`), 때때로 다른 디렉토리에 있을 수도 있습니다.

`stddef.h`와 같은 C 헤더는 본질적으로 C++ 대응물(`cstddef`)과 상호 교환 가능합니다. 어느 스타일이든 허용되지만, 기존 코드와의 일관성을 선호하세요.

각 섹션 내에서 포함은 알파벳 순서로 정렬되어야 합니다. 오래된 코드는 이 규칙을 따르지 않을 수 있으며, 편리할 때 수정해야 합니다.

예를 들어, `google-awesome-project/src/foo/internal/fooserver.cc`의 포함은 다음과 같을 수 있습니다:

```cpp
#include "foo/server/fooserver.h"

#include <sys/types.h>
#include <unistd.h>

#include <string>
#include <vector>

#include "base/basictypes.h"
#include "foo/server/bar.h"
#include "third_party/absl/flags/flag.h"
```

**예외:**

때때로 시스템별 코드는 조건부 포함이 필요합니다. 이러한 코드는 다른 포함 뒤에 조건부 포함을 둘 수 있습니다. 물론, 시스템별 코드를 작고 지역화된 상태로 유지하세요. 예:

```cpp
#include "foo/public/fooserver.h"

#ifdef _WIN32
#include <windows.h>
#endif  // _WIN32
```

---

## 이해하기 쉽게 설명하기

### 포함 순서가 중요한 이유

헤더 파일을 포함하는 순서는 코드의 가독성과 유지보수성에 중요한 영향을 미칩니다. 일관된 순서를 사용하면:

- 코드를 읽기 쉬워집니다
- 빌드 오류를 빠르게 발견할 수 있습니다
- 의존성을 명확히 파악할 수 있습니다

### 포함 순서 규칙

#### 1. 기본 순서

헤더는 다음 순서로 포함해야 합니다:

1. **관련 헤더** (해당 `.cc` 파일과 연관된 `.h` 파일)
2. 빈 줄
3. **C 시스템 헤더** (예: `<unistd.h>`, `<stdlib.h>`)
4. 빈 줄
5. **C++ 표준 라이브러리 헤더** (예: `<string>`, `<vector>`)
6. 빈 줄
7. **다른 라이브러리의 헤더** (예: `"third_party/absl/flags/flag.h"`)
8. 빈 줄
9. **프로젝트의 헤더**

#### 2. 관련 헤더를 먼저 포함하는 이유

관련 헤더를 가장 먼저 포함하면, 해당 헤더가 필요한 다른 헤더를 포함하지 않았을 때 빌드 오류가 즉시 발생합니다. 이렇게 하면:

- 헤더 파일을 작성하는 사람이 문제를 먼저 발견합니다
- 다른 패키지의 무고한 사람들이 영향을 받지 않습니다
- 헤더 파일의 자체 포함(self-contained) 여부를 쉽게 확인할 수 있습니다

#### 예시: 좋은 순서

```cpp
// foo/internal/fooserver.cc
// 이 파일은 foo/server/fooserver.h를 구현함

#include "foo/server/fooserver.h"  // 1. 관련 헤더 (가장 먼저)

#include <sys/types.h>  // 2. C 시스템 헤더
#include <unistd.h>

#include <string>  // 3. C++ 표준 라이브러리 헤더
#include <vector>

#include "base/basictypes.h"  // 4. 프로젝트 헤더
#include "foo/server/bar.h"
#include "third_party/absl/flags/flag.h"
```

#### 예시: 나쁜 순서

```cpp
// 나쁜 예: 순서가 뒤섞임
#include <vector>
#include "foo/server/fooserver.h"  // 관련 헤더가 먼저 와야 함
#include <unistd.h>
#include "base/basictypes.h"
```

### 헤더 이름 규칙

#### 1. 프로젝트 헤더: 따옴표 사용

프로젝트 내의 헤더는 **따옴표(`"`)**를 사용합니다:

```cpp
#include "base/logging.h"
#include "foo/server/fooserver.h"
```

#### 2. 절대 경로 사용 금지

UNIX 디렉토리 별칭인 `.`(현재 디렉토리) 또는 `..`(상위 디렉토리)를 사용하지 마세요:

```cpp
// 나쁜 예
#include "../base/logging.h"
#include "./local_header.h"

// 좋은 예
#include "base/logging.h"
#include "foo/local_header.h"
```

프로젝트의 소스 디렉토리 기준으로 상대 경로를 사용하세요.

#### 3. 시스템/표준 라이브러리: 각괄호 사용

다음 헤더는 **각괄호(`<>`)**를 사용합니다:

- C 및 C++ 표준 라이브러리 헤더
- POSIX, Linux, Windows 시스템 헤더
- 서드파티 라이브러리 (드문 경우)

```cpp
// C 표준 라이브러리
#include <stdlib.h>
#include <stdio.h>

// C++ 표준 라이브러리
#include <string>
#include <vector>
#include <algorithm>

// 시스템 헤더
#include <unistd.h>  // POSIX
#include <windows.h>  // Windows

// 서드파티 라이브러리 (드문 경우)
#include <Python.h>
```

### 각 섹션 내 알파벳 순서

각 섹션 내에서 헤더는 **알파벳 순서**로 정렬해야 합니다:

```cpp
#include "foo/server/fooserver.h"

#include <sys/types.h>  // 알파벳 순서: sys/types.h < unistd.h
#include <unistd.h>

#include <algorithm>  // 알파벳 순서: algorithm < string < vector
#include <string>
#include <vector>

#include "base/basictypes.h"  // 알파벳 순서: base < foo < third_party
#include "foo/server/bar.h"
#include "third_party/absl/flags/flag.h"
```

### C 헤더 vs C++ 헤더

C 헤더(예: `stddef.h`)와 C++ 헤더(예: `cstddef`)는 본질적으로 상호 교환 가능합니다:

```cpp
// 둘 다 허용됨
#include <stddef.h>  // C 스타일
#include <cstddef>   // C++ 스타일
```

하지만 기존 코드와의 **일관성**을 유지하는 것이 중요합니다. 프로젝트에서 C++ 스타일을 사용한다면 그것을 따르세요.

### 예외: 조건부 포함

시스템별 코드가 필요한 경우, 조건부 포함을 다른 포함 뒤에 둘 수 있습니다:

```cpp
#include "foo/public/fooserver.h"

#include <string>
#include <vector>

// 시스템별 코드는 마지막에
#ifdef _WIN32
#include <windows.h>
#endif  // _WIN32

#ifdef __linux__
#include <linux/limits.h>
#endif  // __linux__
```

시스템별 코드는 **작고 지역화된 상태**로 유지하세요.

### 실제 예시

#### 예시 1: 일반적인 .cc 파일

```cpp
// base/logging.cc
// 이 파일은 base/logging.h를 구현함

#include "base/logging.h"  // 관련 헤더

#include <sys/types.h>  // C 시스템 헤더
#include <unistd.h>

#include <string>  // C++ 표준 라이브러리
#include <vector>

#include "base/basictypes.h"  // 프로젝트 헤더
#include "base/strings/string_util.h"
```

#### 예시 2: 테스트 파일

```cpp
// base/logging_test.cc
// 이 파일은 base/logging.h를 테스트함

#include "base/logging.h"  // 관련 헤더

#include <string>  // C++ 표준 라이브러리

#include "base/test/gtest.h"  // 프로젝트 헤더 (테스트 프레임워크)
```

#### 예시 3: 다른 디렉토리의 헤더 사용

```cpp
// foo/internal/bar.cc
// 이 파일은 foo/public/bar.h를 구현함
// (다른 디렉토리에 있지만 관련 헤더는 먼저)

#include "foo/public/bar.h"  // 관련 헤더 (다른 디렉토리여도 먼저)

#include <algorithm>
#include <string>

#include "base/basictypes.h"
```

### 정리

- **포함 순서**:
  1. 관련 헤더
  2. 빈 줄
  3. C 시스템 헤더
  4. 빈 줄
  5. C++ 표준 라이브러리 헤더
  6. 빈 줄
  7. 다른 라이브러리 헤더
  8. 빈 줄
  9. 프로젝트 헤더

- **헤더 이름 규칙**:
  - 프로젝트 헤더: 따옴표(`"`) 사용
  - 시스템/표준 라이브러리: 각괄호(`<>`) 사용
  - 절대 경로 사용 금지 (`.`, `..` 사용하지 않음)

- **각 섹션 내**: 알파벳 순서로 정렬

- **효과**:
  - 코드 가독성 향상
  - 빌드 오류 조기 발견
  - 의존성 명확화
  - 일관된 코딩 스타일

