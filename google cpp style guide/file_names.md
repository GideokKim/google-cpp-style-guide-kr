# 파일 이름 (File Names)

파일 이름은 모두 소문자여야 하며 밑줄( _ ) 또는 대시( - )를 포함할 수 있습니다. 프로젝트에서 사용하는 규칙을 따르세요. 따라야 할 일관된 로컬 패턴이 없으면 " _ "을 선호합니다.

허용되는 파일 이름의 예:

- my_useful_class.cc
- my-useful-class.cc
- myusefulclass.cc
- myusefulclass_test.cc // _unittest 및 _regtest는 더 이상 사용되지 않습니다.

C++ 파일은 .cc 파일 이름 확장자를 가져야 하며, 헤더 파일은 .h 확장자를 가져야 합니다. 특정 지점에 텍스트로 포함되어야 하는 파일은 .inc로 끝나야 합니다(자체 포함 헤더 섹션 참조).

db.h 와 같이 /usr/include 에 이미 존재하는 파일 이름을 사용하지 마세요.

일반적으로 파일 이름은 매우 구체적으로 지정하십시오. 예를 들어, log.h 대신 http_server_logs.h를 사용하십시오. 매우 일반적인 경우는 FooBar라는 클래스를 정의하는 foo_bar.h 및 foo_bar.cc라는 파일 쌍을 갖는 것입니다.

---

## 이해하기 쉽게 설명하기

### 핵심: 소문자 파일 이름, 구체적으로

파일 이름은 모두 소문자에 밑줄(`_`)이나 대시(`-`)를 쓸 수 있습니다. 프로젝트 관습을 따르되, 일관된 관습이 없으면 `_`를 선호하세요.

```text
my_useful_class.cc        // OK
my-useful-class.cc        // OK
myusefulclass_test.cc     // OK (_unittest, _regtest는 폐기됨)
```

### 규칙

- C++ 소스는 `.cc`, 헤더는 `.h`, 특정 지점에 텍스트로 포함되는 파일은 `.inc`.
- `/usr/include`에 이미 있는 이름(`db.h` 등)은 쓰지 마세요.
- 이름은 **구체적으로**: `log.h`보다 `http_server_logs.h`. 흔한 형태는 `FooBar` 클래스를 담는 `foo_bar.h` / `foo_bar.cc` 쌍입니다.
