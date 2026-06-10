# 파일 이름 (File Names)

## 원문 규칙 번역

파일 이름은 모두 소문자여야 하며 밑줄( _ ) 또는 대시( - )를 포함할 수 있습니다. 프로젝트에서 사용하는 규칙을 따르세요. 따라야 할 일관된 로컬 패턴이 없으면 " _ "을 선호합니다.

허용되는 파일 이름의 예:

- my_useful_class.cc
- 내-유용한-class.cc
- myusefulclass.cc
- myusefulclass_test.cc // _unittest 및 _regtest는 더 이상 사용되지 않습니다.

C++ 파일은 .cc 파일 이름 확장자를 가져야 하며, 헤더 파일은 .h 확장자를 가져야 합니다. 특정 지점에 텍스트로 포함되어야 하는 파일은 .inc로 끝나야 합니다(자체 포함 헤더 섹션 참조).

db.h 와 같이 /usr/include 에 이미 존재하는 파일 이름을 사용하지 마세요.

일반적으로 파일 이름은 매우 구체적으로 지정하십시오. 예를 들어, log.h 대신 http_server_logs.h를 사용하십시오. 매우 일반적인 경우는 FooBar라는 클래스를 정의하는 foo_bar.h 및 foo_bar.cc라는 파일 쌍을 갖는 것입니다.

---

---

## 이해하기 쉽게 설명하기

이 규칙의 핵심은 허용되는 파일 이름의 예: - my_useful_class.cc - 내-유용한-class.cc - myusefulclass.cc - myusefulclass_test.cc // _unittest 및 _regtest는 더 이상 사용되지 않습니다.

실제로 코드를 볼 때는 매우 일반적인 경우는 FooBar라는 클래스를 정의하는 foo_bar.h 및 foo_bar.cc라는 파일 쌍을 갖는 것입니다.

점검할 때는 특히 다음을 확인하세요:

- db.h 와 같이 /usr/include 에 이미 존재하는 파일 이름을 사용하지 마세요.
- 예를 들어, log.h 대신 http_server_logs.h를 사용하십시오.
