# 부동소수점 타입 (Floating-Point Types)

내장된 C++ 부동 소수점 유형 중에서 사용되는 유일한 유형은 float 및 double 입니다. 이러한 유형은 각각 IEEE-754 바이너리32 및 바이너리64를 나타낸다고 가정할 수 있습니다.

이식 불가능한 결과를 제공하므로 long double 을 사용하지 마세요.

---

## 이해하기 쉽게 설명하기

### 핵심: float와 double만, long double은 금지

내장 부동소수점 타입 중 **`float`와 `double`만** 쓰세요. 각각 IEEE-754 binary32, binary64를 나타낸다고 가정해도 됩니다. `long double`은 플랫폼마다 결과가 달라(이식 불가) 쓰지 마세요.
