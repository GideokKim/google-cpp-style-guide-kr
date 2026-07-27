# sizeof

sizeof( type ) 보다 sizeof( varname ) 을 선호합니다.

특정 변수의 크기를 구할 때는 sizeof( varname )을 사용하세요. sizeof( varname )은 누군가 지금 또는 나중에 변수 유형을 변경하면 적절하게 업데이트됩니다. 적절한 C++ 유형의 변수가 편리하지 않은 외부 또는 내부 데이터 형식을 관리하는 코드와 같이 특정 변수와 관련되지 않은 코드에 sizeof( type )을 사용할 수 있습니다.

```cpp
MyStruct data;
memset(&data, 0, sizeof(data));
```

```cpp
memset(&data, 0, sizeof(MyStruct));
```

```cpp
if (raw_size < sizeof(int)) {
  LOG(ERROR) << "compressed record not big enough for count: " << raw_size;
  return false;
}
```

---

## 옮긴이 풀이

### 핵심: sizeof(type)보다 sizeof(varname)

특정 변수의 크기가 필요하면 `sizeof(type)`이 아니라 `sizeof(varname)`을 쓰세요. 나중에 변수의 타입이 바뀌어도 자동으로 따라가므로 버그를 막습니다.

```cpp
MyStruct data;
memset(&data, 0, sizeof(data));     // 좋음: data의 타입이 바뀌어도 안전
memset(&data, 0, sizeof(MyStruct)); // 덜 좋음: 타입을 직접 반복
```

### sizeof(type)이 맞는 경우

특정 변수와 무관한 코드 — 예를 들어 적절한 C++ 타입의 변수를 두기 어려운 외부·내부 데이터 포맷을 다루는 코드에서는 `sizeof(type)`을 써도 됩니다.

```cpp
if (raw_size < sizeof(int)) { ... }
```
