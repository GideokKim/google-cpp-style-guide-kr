# 아키텍처 이식성 (Architecture Portability)

아키텍처 이식 가능한 코드를 작성합니다. 단일 프로세서에 특정한 CPU 기능에 의존하지 마세요.

- 값을 인쇄할 때 printf 함수 계열 대신 absl::StrCat , absl::Substitute , absl::StrFormat 또는 std::ostream 과 같은 유형이 안전한 숫자 형식 지정 라이브러리를 사용하십시오.
- 구조화된 데이터를 프로세스 내부 또는 외부로 이동할 때 메모리 내 표현을 복사하는 대신 프로토콜 버퍼와 같은 직렬화 라이브러리를 사용하여 인코딩하십시오.
- 메모리 주소를 정수로 작업해야 하는 경우 uint32_t s 또는 uint64_t s가 아닌 uintptr_t s에 저장하세요.
- 64비트 상수를 생성하려면 필요에 따라 중괄호 초기화를 사용하세요. 예: int64_t my_value{0x123456789}; uint64_t my_mask{uint64_t{3} << 48};
- 이식 가능한 부동소수점 타입을 사용하세요. `long double`을 피하세요.
- 이식 가능한 정수 타입을 사용하세요. `short`, `long`, `long long`을 피하세요.

---

## 옮긴이 풀이

### 핵심: 특정 CPU에 의존하지 않는 코드

단일 프로세서에만 있는 CPU 기능에 의존하지 말고, 아키텍처 이식 가능한 코드를 쓰세요. 실무 지침:

- **숫자 출력**: `printf` 계열 대신 타입 안전한 `absl::StrCat`, `absl::StrFormat`, `std::ostream` 등을 사용.
- **데이터 이동**: 메모리 표현을 그대로 복사하지 말고 프로토콜 버퍼 같은 직렬화 라이브러리로 인코딩.
- **주소를 정수로**: `uint32_t`/`uint64_t`가 아니라 `uintptr_t`에 저장.
- **64비트 상수**: 중괄호 초기화 사용. 예: `int64_t my_value{0x123456789};`, `uint64_t my_mask{uint64_t{3} << 48};`
- **이식 가능한 타입**: `long double`을 피하고, `short`/`long`/`long long` 대신 정확한 너비 타입을 사용.
